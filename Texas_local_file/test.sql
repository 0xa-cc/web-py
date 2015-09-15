#测试
call pd_w_purchase(@a, @b, '201411280534', 'abc', 'iPad.LZDZPK.288', '', 0, @c, @d, @e);
select @a, @b, @c, @d, @e;


insert into tb_w_skus_limit_perday (Sku, LimitNum, recdate) values ('iPad.LZDZPK.288', 1, now());
update tb_w_skus_limit_perday set TodayNum=0;
select * from tb_w_skus_limit_perday;


#增加支付渠道对应商品
delete from tb_w_skus_of_channel where Sku='gg.lzdzpk.01';
delete from tb_w_skus where Sku='gg.lzdzpk.01';
insert into tb_w_skus_of_channel (Channel, Sku) values ('googleplay', 'gg.lzdzpk.01');
insert into tb_w_skus (Sku,DispOrder,Icon,Image,PriceInfo,Price,Title,Type,Name,Addition,Addition2,Descript,AmountInfo,Amount,FirstName,FirstAddition,FirstAmount,Enable,Visible) values ("gg.lzdzpk.01", 1, "","", "$0.99", 0.99, "", "coin", "36000 coins", "", "", "", "36000", 36000, "", "", 36000, 1, 0);


delete from tb_w_skus_of_channel where Sku='mol.lzdzpk.01';
delete from tb_w_skus where Sku='mol.lzdzpk.01';
insert into tb_w_skus_of_channel (Channel, Sku) values ('mol', 'mol.lzdzpk.01');
insert into tb_w_skus (Sku,DispOrder,Icon,Image,PriceInfo,Price,Title,Type,Name,Addition,Addition2,Descript,AmountInfo,Amount,FirstName,FirstAddition,FirstAmount,Enable,Visible) values ("mol.lzdzpk.01", 1, "","", "$1", 1, "", "coin", "10000 coins", "", "", "", "10000", 10000, "", "", 10000, 1, 0);

delete from tb_w_skus_of_channel where Sku='mol.lzdzpk.02';
delete from tb_w_skus where Sku='mol.lzdzpk.02';
insert into tb_w_skus_of_channel (Channel, Sku) values ('mol', 'mol.lzdzpk.02');
insert into tb_w_skus (Sku,DispOrder,Icon,Image,PriceInfo,Price,Title,Type,Name,Addition,Addition2,Descript,AmountInfo,Amount,FirstName,FirstAddition,FirstAmount,Enable,Visible) values ("mol.lzdzpk.02", 1, "","", "$10", 10, "", "coin", "100000 coins", "", "", "", "100000", 100000, "", "", 100000, 1, 0);

delete from tb_w_skus_of_channel where Sku='mol.lzdzpk.03';
delete from tb_w_skus where Sku='mol.lzdzpk.03';
insert into tb_w_skus_of_channel (Channel, Sku) values ('mol', 'mol.lzdzpk.03');
insert into tb_w_skus (Sku,DispOrder,Icon,Image,PriceInfo,Price,Title,Type,Name,Addition,Addition2,Descript,AmountInfo,Amount,FirstName,FirstAddition,FirstAmount,Enable,Visible) values ("mol.lzdzpk.03", 1, "","", "$100", 100, "", "coin", "1000000 coins", "", "", "", "1000000", 1000000, "", "", 1000000, 1, 0);



测试web接口
http://172.28.160.103:8080/googleplay/purchase?user=test&data={%22orderId%22:%2212999763169054705758.1336765116266576%22,%22packageName%22:%22com.pokerxo.com%22,%22productId%22:%22gg.lzdzpk.01%22,%22purchaseTime%22:1364802898000,%22purchaseState%22:0,%22developerPayload%22:%22abcdefghijk%22,%22purchaseToken%22:%22bsqmyqimmkkjmaukozbmzdld.AO-J1OwvL8XlSH8UQbC6lSiVfBzvtrGJlHw9YF_p1O3vyQVFnaLWdrjmgG1ucMhpIAy4zKJ6-aymwNBJTAydoQ3N_dHS-R99rpDOr1dasbOLOh3oWtUI7ZH76OIXMGP-SIVUkjazpZAg%22}

http://172.28.160.103:8080/mol/notify?applicationCode=3f2504e04f8911d39a0c0305e82c3301&referenceId=TRX1708901&paymentId=MPO000000000001&version=v1&amount=1000&currencyCode=MYR&paymentStatusCode=00&paymentStatusDate=2012-12-31T14%3A59%3A59Z&customerId=BFEE7E00E41E6D6F&signature=5e2a170eabcb54db0b2937874c39549b

http://172.28.160.103:8080/purchase/payload?shop=ourgame&userid=chaim0415&sku=LZDZPK.02&role=chaim0415


http://202.108.0.244:8080/
映射到
http://172.28.14.170:8080/
