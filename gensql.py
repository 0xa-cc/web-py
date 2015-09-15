#coding=utf8

def GenerateCoinSQL(strSku, fPrice, nAmount):
    sqlChannel = "delete from tb_w_skus_of_channel where Sku=\"%s\";" % (strSku)
    print(sqlChannel)

    sqlChannel = "insert into tb_w_skus_of_channel (Channel, Sku) values (\"default\", \"%s\");" % (strSku)
    print(sqlChannel)

    sqlChannel = "delete from tb_w_skus where Sku=\"%s\";" % (strSku)
    print(sqlChannel)

    strPrice = "¥%.2f" % (fPrice)
    strAmount = str(nAmount)
    strName = "%d个万能豆" % (nAmount)
    nPresent = nAmount*0.2
    strFirstAddition = "首充将加送您%d个万能豆" % (nPresent)
    nFirstAmount = nAmount + nPresent
    sqlSku = "insert into tb_w_skus (Sku,DispOrder,Icon,Image,PriceInfo,Price,Title,Type,Name,Addition,Addition2,Descript,AmountInfo,Amount,FirstName,FirstAddition,FirstAmount,Enable,Visible) values (\"%s\", 1, \"\",\"\", \"%s\", %.2f, \"\", \"coin\", \"%s\", \"\", \"\", \"\", \"%s\", %d, \"\", \"%s\", %d, 1, 0);" % (strSku, strPrice, fPrice, strName, strAmount, nAmount, strFirstAddition, nFirstAmount)
    print(sqlSku)
    
    sqlChannel = "delete from tb_w_score_of_sku where Sku=\"%s\";" % (strSku)
    # print(sqlChannel)

    ayScore = ((2, 10, 3), (11, 50, 5), (51, 100, 10), (101, 200, 30), (201, 500, 100), (501, 1000, 300))
    for s in ayScore:
        if fPrice >= s[0] and fPrice <= s[1]:
            sqlScore = "insert into tb_w_score_of_sku (Sku, Score) values (\"%s\", %d);" % (strSku, s[2])
            # print(sqlScore)
            break

    sqlChannel = "delete from tb_w_skus_for_vip where Sku=\"%s\";" % (strSku)
    # print(sqlChannel)
    for i in range(4):
        if i == 0:
            fRate = 0.02
        elif i == 1:
            fRate = 0.03
        elif i == 2:
            fRate = 0.04
        elif i == 3:
            fRate = 0.05
        nPresent = nAmount*fRate
        nVipAmount = nAmount + nPresent
        strAddition = "购买将加送您%d个万能豆" % (nPresent)
        sqlVip = "insert into tb_w_skus_for_vip (Sku,VipLevel,VipName,VipAddition,VipAmount,VipTime,VipAddition2) values (\"%s\", %d, \"\", \"%s\", %d, 0, \"\");" % (strSku, i+1, strAddition, nVipAmount)
        # print(sqlVip)

    print("\n")

def GenerateVipSQL(strSku, fPrice, nAmount):
    sqlChannel = "delete from tb_w_skus_of_channel where Sku=\"%s\";" % (strSku)
    print(sqlChannel)

    sqlChannel = "insert into tb_w_skus_of_channel (Channel, Sku) values (\"default\", \"%s\");" % (strSku)
    print(sqlChannel)

    sqlChannel = "delete from tb_w_skus where Sku=\"%s\";" % (strSku)
    print(sqlChannel)

    strPrice = "¥%.2f" % (fPrice)
    strAmount = str(nAmount)
    nScore = 0
    if nAmount == 30:
        strAddition = "购买赠送月度会员尊贵标志"
        nScore = 10
    elif nAmount == 90:
        strAddition = "购买赠送季度会员尊贵标志"
        nScore = 20
    elif nAmount == 180:
        strAddition = "购买赠送半年度会员尊贵标志"
        nScore = 35
    elif nAmount == 360:
        strAddition = "购买赠送年度会员尊贵标志"
        nScore = 100

    strFirstAddition = strAddition
    nFirstAmount = nAmount
    sqlSku = "insert into tb_w_skus (Sku,DispOrder,Icon,Image,PriceInfo,Price,Title,Type,Name,Addition,Addition2,Descript,AmountInfo,Amount,FirstName,FirstAddition,FirstAmount,Enable,Visible) values (\"%s\", 1, \"\",\"\", \"%s\", %.2f, \"\", \"vip\", \"%s\", \"%s\", \"\", \"\", \"%s\", %d, \"\", \"%s\", %d, 1, 1);" % (strSku, strPrice, fPrice, "", strAddition, strAmount, nAmount, strFirstAddition, nFirstAmount)
    print(sqlSku)

    sqlChannel = "delete from tb_w_score_of_sku where Sku=\"%s\";" % (strSku)
    print(sqlChannel)
    sqlScore = "insert into tb_w_score_of_sku (Sku, Score) values (\"%s\", %d);" % (strSku, nScore)
    print(sqlScore)

    sqlChannel = "delete from tb_w_skus_for_vip where Sku=\"%s\";" % (strSku)
    print(sqlChannel)
    for i in range(4):
        nVipAmount = nAmount
        sqlVip = "insert into tb_w_skus_for_vip (Sku,VipLevel,VipName,VipAddition,VipAmount,VipTime,VipAddition2) values (\"%s\", %d, \"\", \"%s\", %d, 0, \"\");" % (strSku, i+1, strAddition, nVipAmount)
        print(sqlVip)

    print("\n")

#先删除原有数据
# print("delete from tb_w_skus_of_channel;")
# print("delete from tb_w_skus;")
# print("delete from tb_w_skus_for_vip;")
# print("delete from tb_w_score_of_sku;")
# print("\n")

#1-30元商品
# for i in range(30):
#     nIndex = i+1
#指定几个
ayId = (2, 8, 18, 30)
for nIndex in ayId:
    strSku = "LZDZPK.%02d" % (nIndex)
    # strSku = "iPhone.LZDZPK.%02d" % (nIndex)
    GenerateCoinSQL(strSku, nIndex, 5000*nIndex)

#31-35
# GenerateCoinSQL("LZDZPK.31", 58, 30*10000)
# GenerateCoinSQL("LZDZPK.32", 128, 135*10000)
# GenerateCoinSQL("LZDZPK.34", 288, 318*10000)
# GenerateCoinSQL("LZDZPK.35", 588, 668*10000)
# GenerateCoinSQL("LZDZPK.36", 998, 1180*10000)

# GenerateCoinSQL("iPad.LZDZPK.288", 288, 318*10000)
# GenerateCoinSQL("iPad.LZDZPK.588", 588, 668*10000)

#VIP
# GenerateVipSQL("LZDZPKHY.01", 15, 30)
# GenerateVipSQL("LZDZPKHY.02", 35, 90)
# GenerateVipSQL("LZDZPKHY.03", 78, 180)
# GenerateVipSQL("LZDZPKHY.04", 108, 360)

#更新要在商城中显示的商品，指定本地图像
aySkus = (("LZDZPK.02", "shop_icon_jszplb.png"), 
    ("LZDZPK.08", "shop_icon_sxcylb.png"), 
    ("LZDZPK.18","shop_icon_jwjlb.png"), 
    ("LZDZPK.30", "shop_icon_cxmjlb.png"), 
    ("LZDZPK.31", "shop_icon_zjlb.png"), 
    ("LZDZPK.32","shop_icon_whyxlb.png"), 
    ("LZDZPK.34","shop_icon_gwjxlb.png"), 
    ("LZDZPK.35","shop_icon_wzlb.png"), 
    ("LZDZPK.36","shop_icon_cjzzlb.png"))
for p in aySkus:
    strSku = p[0]
    strImage = p[1]
    strSql = "update tb_w_skus set Visible=1, Image=\"%s\" where Sku=\"%s\";" % (strImage, strSku)
    print(strSql)

#VIP需要更新的信息
ayVip = (("LZDZPKHY.01", "shop_month_vip_icon.png"), ("LZDZPKHY.02", "shop_quarter_vip_icon.png"), ("LZDZPKHY.03", "shop_half_year_vip_icon.png"), ("LZDZPKHY.04", "shop_year_vip_icon.png"))
for v in ayVip:
    strSku = v[0]
    strImage = v[1]
    strSql = "update tb_w_skus set Visible=1, Image=\"%s\" where sku=\"%s\";" % (strImage, strSku)
    print(strSql)
print("\n")

#以下都是生成的测试数据
#测试商品
# GenerateCoinSQL("LZDZPK.TEST.01", 0.1, 10000)
# print("update tb_w_skus set Visible=1, Image=\"shop_icon_jszplb.png\" where sku=\"LZDZPK.TEST.01\";")
# print("\n")
# GenerateVipSQL("LZDZPKHY.TEST.01", 0.1, 30)
# print("update tb_w_skus set Visible=1, Image=\"shop_month_vip_icon.png\" where sku=\"LZDZPKHY.TEST.01\";")
# print("\n")

#由于移动中心配置的商品不够全，禁止一些商品以适应其配置
# for i in range(36):
#     if i < 11 or i == 15 or i == 20 or i == 30:
#         strSql = "update tb_w_skus set Visible=0 where sku=\"LZDZPK.%02d\";" % (i)
#         print(strSql)
#         continue
    # strSql = "update tb_w_skus set Enable=0 where sku=\"LZDZPK.%02d\";" % (i)
    # print(strSql)

