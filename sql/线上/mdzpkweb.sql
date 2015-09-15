/*
SQLyog Ultimate v9.60 
MySQL - 5.6.22-log : Database - mdzpkweb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`mdzpkweb` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;

USE `mdzpkweb`;

/*Table structure for table `tb_w_purchase` */

CREATE TABLE `tb_w_purchase` (
  `trade_no` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '定单号',
  `UserID` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '用户ID',
  `sku` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品ID',
  `skutype` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品类型',
  `amount` bigint(20) NOT NULL COMMENT '数量',
  `original_data` varchar(1024) COLLATE utf8_bin DEFAULT NULL COMMENT '原始数据',
  `result` int(2) DEFAULT '0' COMMENT '定单结果，1：处理完成，0：正在处理',
  `recdate` datetime NOT NULL COMMENT '记录时间',
  PRIMARY KEY (`trade_no`),
  KEY `Index_purchase_1` (`UserID`),
  KEY `sku` (`sku`,`recdate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `tb_w_purchase_bak` */

CREATE TABLE `tb_w_purchase_bak` (
  `trade_no` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '定单号',
  `UserID` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '用户ID',
  `sku` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品ID',
  `skutype` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品类型',
  `amount` bigint(20) NOT NULL COMMENT '数量',
  `original_data` varchar(1024) COLLATE utf8_bin DEFAULT NULL COMMENT '原始数据',
  `result` int(2) DEFAULT '0' COMMENT '定单结果，1：处理完成，0：正在处理',
  `recdate` datetime NOT NULL COMMENT '记录时间',
  PRIMARY KEY (`trade_no`),
  KEY `Index_purchase_1` (`UserID`),
  KEY `sku` (`sku`,`recdate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `tb_w_purchaselog` */

CREATE TABLE `tb_w_purchaselog` (
  `TimeStamp` datetime NOT NULL COMMENT '时间',
  `UserID` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '用户ID',
  `ActionType` int(4) NOT NULL COMMENT '1:购买',
  `AmountBefore` bigint(20) NOT NULL COMMENT '操作前数量',
  `AmountChange` bigint(20) NOT NULL COMMENT '操作变化量',
  `AmountAfter` bigint(20) NOT NULL COMMENT '操作后数量',
  `Remark` varchar(128) COLLATE utf8_bin DEFAULT NULL COMMENT '支付序列号、牌桌ID等',
  KEY `Index_PurchaseLog_1` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `tb_w_score_of_sku` */

CREATE TABLE `tb_w_score_of_sku` (
  `Sku` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品ID',
  `Score` int(11) DEFAULT NULL COMMENT '积分',
  PRIMARY KEY (`Sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `tb_w_score_of_sku_bak` */

CREATE TABLE `tb_w_score_of_sku_bak` (
  `Sku` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品ID',
  `Score` int(11) DEFAULT NULL COMMENT '积分',
  PRIMARY KEY (`Sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `tb_w_skus` */

CREATE TABLE `tb_w_skus` (
  `Sku` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品ID',
  `DispOrder` int(2) DEFAULT NULL COMMENT '显示顺序，暂时没有使用',
  `Icon` varchar(255) COLLATE utf8_bin DEFAULT NULL COMMENT '图标url',
  `Image` varchar(255) COLLATE utf8_bin DEFAULT NULL COMMENT '图像url',
  `PriceInfo` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '价格信息',
  `Price` decimal(10,2) NOT NULL COMMENT '价格数值',
  `Title` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '标题',
  `Name` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '名称',
  `Type` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '类型：coin,vip',
  `Addition` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '附加信息',
  `Descript` varchar(240) COLLATE utf8_bin DEFAULT NULL COMMENT '描述',
  `AmountInfo` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '数量信息',
  `Amount` bigint(20) NOT NULL COMMENT '数量',
  `FirstName` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '首充显示名称',
  `FirstAddition` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '首充附加信息',
  `FirstAmount` bigint(20) NOT NULL COMMENT '首充数量',
  `Addition2` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '附加信息',
  `Enable` int(1) NOT NULL COMMENT '启用标志，1：启用，0：不启用',
  `Visible` int(1) NOT NULL COMMENT '可见标志，1：商城可见，0：隐藏，不显示在商城',
  `UpdateDate` datetime DEFAULT NULL,
  `Hot` int(1) NOT NULL DEFAULT '0' COMMENT '热卖标志',
  PRIMARY KEY (`Sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `tb_w_skus_bak` */

CREATE TABLE `tb_w_skus_bak` (
  `Sku` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品ID',
  `DispOrder` int(2) DEFAULT NULL COMMENT '显示顺序，暂时没有使用',
  `Icon` varchar(255) COLLATE utf8_bin DEFAULT NULL COMMENT '图标url',
  `Image` varchar(255) COLLATE utf8_bin DEFAULT NULL COMMENT '图像url',
  `PriceInfo` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '价格信息',
  `Price` decimal(10,2) NOT NULL COMMENT '价格数值',
  `Title` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '标题',
  `Name` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '名称',
  `Type` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '类型：coin,vip',
  `Addition` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '附加信息',
  `Descript` varchar(240) COLLATE utf8_bin DEFAULT NULL COMMENT '描述',
  `AmountInfo` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '数量信息',
  `Amount` bigint(20) NOT NULL COMMENT '数量',
  `FirstName` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '首充显示名称',
  `FirstAddition` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '首充附加信息',
  `FirstAmount` bigint(20) NOT NULL COMMENT '首充数量',
  `Addition2` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT '附加信息',
  `Enable` int(1) NOT NULL COMMENT '启用标志，1：启用，0：不启用',
  `Visible` int(1) NOT NULL COMMENT '可见标志，1：商城可见，0：隐藏，不显示在商城',
  `updatedate` datetime DEFAULT NULL,
  PRIMARY KEY (`Sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `tb_w_skus_for_vip` */

CREATE TABLE `tb_w_skus_for_vip` (
  `Sku` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品ID',
  `VipLevel` int(2) NOT NULL COMMENT 'VIP级别',
  `VipName` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT 'VIP名称',
  `VipAddition` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT 'VIP附加信息',
  `VipAmount` bigint(20) NOT NULL COMMENT 'VIP数量',
  `VipTime` int(11) NOT NULL COMMENT '增加VIP时长，暂时不使用',
  `VipAddition2` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT 'VIP附加信息',
  PRIMARY KEY (`Sku`,`VipLevel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `tb_w_skus_for_vip_bak` */

CREATE TABLE `tb_w_skus_for_vip_bak` (
  `Sku` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品ID',
  `VipLevel` int(2) NOT NULL COMMENT 'VIP级别',
  `VipName` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT 'VIP名称',
  `VipAddition` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT 'VIP附加信息',
  `VipAmount` bigint(20) NOT NULL COMMENT 'VIP数量',
  `VipTime` int(11) NOT NULL COMMENT '增加VIP时长，暂时不使用',
  `VipAddition2` varchar(90) COLLATE utf8_bin DEFAULT NULL COMMENT 'VIP附加信息',
  PRIMARY KEY (`Sku`,`VipLevel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `tb_w_skus_limit_perday` */

CREATE TABLE `tb_w_skus_limit_perday` (
  `Sku` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品ID',
  `LimitNum` int(11) NOT NULL DEFAULT '0' COMMENT '每天最多购买数量',
  `TodayNum` int(11) NOT NULL DEFAULT '0' COMMENT '当天已购买数量',
  `recdate` datetime DEFAULT NULL COMMENT '更新当天次数时间',
  `resetdate` datetime DEFAULT NULL COMMENT '重置时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='商品每天购买数量限制表';

/*Table structure for table `tb_w_skus_of_channel` */

CREATE TABLE `tb_w_skus_of_channel` (
  `Channel` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '渠道',
  `Sku` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品ID',
  PRIMARY KEY (`Channel`,`Sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `tb_w_skus_of_channel_bak` */

CREATE TABLE `tb_w_skus_of_channel_bak` (
  `Channel` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '渠道',
  `Sku` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '商品ID',
  PRIMARY KEY (`Channel`,`Sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Table structure for table `tb_w_skus_opertionLog` */

CREATE TABLE `tb_w_skus_opertionLog` (
  `Sku` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '产品ID',
  `OperType` varchar(20) COLLATE utf8_bin DEFAULT NULL COMMENT '操作类型 添加 删除 上架修改  下架修改',
  `PackageName` varchar(20) COLLATE utf8_bin DEFAULT NULL COMMENT '礼包名称',
  `Price` int(20) DEFAULT NULL COMMENT '价格',
  `SheBei` varchar(20) COLLATE utf8_bin DEFAULT NULL COMMENT '设备',
  `SellNum` int(11) DEFAULT NULL COMMENT '出售数量',
  `Amount` bigint(20) DEFAULT NULL COMMENT '万能豆数量',
  `Stat` varchar(20) COLLATE utf8_bin DEFAULT NULL COMMENT '状态',
  `UpdateDate` datetime DEFAULT NULL COMMENT '修改时间',
  `OperUserName` varchar(20) COLLATE utf8_bin DEFAULT NULL COMMENT '修改人员'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/* Procedure structure for procedure `pd_w_purchase` */

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`172.28.11.44` PROCEDURE `pd_w_purchase`(out pResult int, out pMsg varchar(64), in pTradeNo varchar(64), in pUserID varchar(64), in pSku varchar(64), in pOriginalData varchar(1024), in pVipLevel int, out pAmountPurchased bigint, out pAmountCur bigint, out pSkuType varchar(64))
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
end */$$
DELIMITER ;

/* Procedure structure for procedure `pd_w_purchase_bak` */

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`172.28.11.44` PROCEDURE `pd_w_purchase_bak`(out pResult int, out pMsg varchar(64), in pTradeNo varchar(64), in pUserID varchar(64), in pSku varchar(64), in pOriginalData varchar(1024), in pVipLevel int, out pAmountPurchased bigint, out pAmountCur bigint, out pSkuType varchar(64))
begin
    declare t_error int default 0; 
    declare v_llAmount bigint default 0;
    declare v_llFirstAmount bigint default 0;
    declare v_llAmountBefore bigint default 0;
    declare v_nCharged int default 0;
    declare v_nTime int default 0;
    declare v_timeExpire datetime;
    declare v_nLevel int default 0;
    DECLARE continue HANDLER FOR SQLEXCEPTION SET t_error = -1;
    START TRANSACTION;
    
    select Amount into v_llAmount from tb_w_purchase where trade_no=pTradeNo;
    if v_llAmount != 0 then
        set pResult = 2;
        set pMsg = "same trade no";
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
    if t_error = 0 then
        commit;
    else
        set pResult = t_error;
        set pMsg = "sqlexception";
        rollback;
    end if;
end */$$
DELIMITER ;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
