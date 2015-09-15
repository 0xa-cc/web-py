drop procedure pd_w_purchase;
delimiter $$
create procedure pd_w_purchase(out pResult int, out pMsg varchar(64), in pTradeNo varchar(64), in pUserID varchar(64), in pSku varchar(64), in pOriginalData varchar(1024), in pVipLevel int, out pAmountPurchased bigint, out pAmountCur bigint, out pSkuType varchar(64))
begin
    declare t_error int default 0; 
    declare v_llAmount bigint default 0;
    declare v_llFirstAmount bigint default 0;
    declare v_llAmountBefore bigint default 0;
    declare v_nCharged int default 0;
    declare v_nTime int default 0;
    declare v_timeExpire datetime;
    declare v_nLevel int default 0;
    declare v_nLimitNum int default -1;
    declare v_nTodayNum int default -1;

    DECLARE continue HANDLER FOR SQLEXCEPTION SET t_error = -1;
    START TRANSACTION;
    
    #先查找购买数量是否超过限制
    -- select LimitNum, TodayNum into v_nLimitNum, v_nTodayNum from tb_w_skus_limit_perday where Sku=pSku;
    -- if v_nLimitNum > 0 and v_nTodayNum >= v_nLimitNum then
    --     set pResult = 1;
    --     set pMsg = "exceed limit";
    -- else
        select Amount into v_llAmount from tb_w_purchase where trade_no=pTradeNo;
        if v_llAmount != 0 then
            set pResult = 2;
            set pMsg = "same trade no";
            set pAmountPurchased = v_llAmount;
            set pAmountCur = v_llAmountBefore+v_llAmount;
        else
            select count(*) into v_nCharged from tb_w_purchase where UserID=pUserID and skutype='coin';#是否购买过万能豆
            select Amount,FirstAmount,Type into v_llAmount,v_llFirstAmount,pSkuType from tb_w_skus where Sku=pSku;
            if v_nCharged = 0 then#首充
                set v_llAmount = v_llFirstAmount;
            end if;
            if v_llAmount is not NULL and v_llAmount > 0 then
                if pVipLevel > 0 then
                    if v_nCharged > 0 then#是首充就用首充的数量，不是首充则用VIP数量
                        select VipAmount into v_llAmount from tb_w_skus_for_vip where Sku=pSku and VipLevel=pVipLevel;#是VIP则用VIP的充值数量
                    end if;
                end if;

                update tb_w_skus_limit_perday set TodayNum=TodayNum+1 where Sku=pSku;#更新当天已购买数量，此处必须在表中先配置数据，只更新不插入，不配置就不做数量限制

                insert into tb_w_purchase (trade_no, UserID, Sku, skutype, Amount, original_data, recdate) values (pTradeNo, pUserID, pSku, pSkuType, v_llAmount, pOriginalData, now());
                insert into tb_w_purchaselog (TimeStamp, UserID, ActionType, AmountBefore, AmountChange, AmountAfter, Remark) values (now(), pUserID, 1, v_llAmountBefore, v_llAmount, v_llAmountBefore+v_llAmount, concat('trade_no:',pTradeNo,',vip:',pVipLevel,',charged:',v_nCharged));                    
                set pAmountCur = v_llAmountBefore+v_llAmount;
                set pAmountPurchased = v_llAmount;
                set pResult = 0;
                set pMsg = "success";
            else
                set pResult = 4;
                set pMsg = "can not find Amount of sku";
            end if;
        end if;
    -- end if;

    if t_error = 0 then
        commit;
    else
        set pResult = t_error;
        set pMsg = "sqlexception";
        rollback;
    end if;
end $$
delimiter ;
