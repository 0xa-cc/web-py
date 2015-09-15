/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50626
 Source Host           : localhost
 Source Database       : test112

 Target Server Type    : MySQL
 Target Server Version : 50626
 File Encoding         : utf-8

 Date: 08/28/2015 15:47:32 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `tb_w_channel`
-- ----------------------------
DROP TABLE IF EXISTS `tb_w_channel`;
CREATE TABLE `tb_w_channel` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `Channel` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '渠道唯一标识',
  `ChannelName` varchar(200) COLLATE utf8_bin NOT NULL COMMENT '渠道名称',
  `Image` varchar(400) COLLATE utf8_bin NOT NULL COMMENT '渠道图片',
  `Descript` varchar(400) COLLATE utf8_bin DEFAULT NULL COMMENT '渠道描述',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='支付渠道配置表';

-- ----------------------------
--  Table structure for `tb_w_payload`
-- ----------------------------
DROP TABLE IF EXISTS `tb_w_payload`;
CREATE TABLE `tb_w_payload` (
  `PayloadID` varchar(64) NOT NULL COMMENT '定单ID',
  `Sku` varchar(64) NOT NULL COMMENT '商品ID',
  `User` varchar(128) NOT NULL COMMENT '用户名',
  `Role` varchar(128) DEFAULT NULL COMMENT '角色名',
  `UserData` varchar(128) DEFAULT NULL COMMENT '用户自定义数据',
  `Channel` varchar(64) NOT NULL COMMENT '渠道号',
  `recdate` datetime NOT NULL COMMENT '生成记录时间',
  `Status` int(1) NOT NULL DEFAULT '0' COMMENT '完成状态，未完成：0，已完成：1',
  PRIMARY KEY (`PayloadID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品定单表';

-- ----------------------------
--  Table structure for `tb_w_purchase`
-- ----------------------------
DROP TABLE IF EXISTS `tb_w_purchase`;
CREATE TABLE `tb_w_purchase` (
  `trade_no` varchar(64) NOT NULL COMMENT '定单号',
  `UserID` varchar(32) NOT NULL COMMENT '用户ID',
  `sku` varchar(64) NOT NULL COMMENT '商品ID',
  `skutype` varchar(64) NOT NULL COMMENT '商品类型',
  `amount` bigint(20) NOT NULL COMMENT '数量',
  `original_data` varchar(1024) DEFAULT NULL COMMENT '原始数据',
  `result` int(2) DEFAULT '0' COMMENT '定单结果，1：处理完成，0：正在处理',
  `recdate` datetime NOT NULL COMMENT '记录时间',
  PRIMARY KEY (`trade_no`),
  KEY `Index_purchase_1` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tb_w_purchaselog`
-- ----------------------------
DROP TABLE IF EXISTS `tb_w_purchaselog`;
CREATE TABLE `tb_w_purchaselog` (
  `TimeStamp` datetime NOT NULL COMMENT '时间',
  `UserID` varchar(32) NOT NULL COMMENT '用户ID',
  `ActionType` int(4) NOT NULL COMMENT '1:购买',
  `AmountBefore` bigint(20) NOT NULL COMMENT '操作前数量',
  `AmountChange` bigint(20) NOT NULL COMMENT '操作变化量',
  `AmountAfter` bigint(20) NOT NULL COMMENT '操作后数量',
  `Remark` varchar(128) DEFAULT NULL COMMENT '支付序列号、牌桌ID等',
  KEY `Index_PurchaseLog_1` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tb_w_score_of_sku`
-- ----------------------------
DROP TABLE IF EXISTS `tb_w_score_of_sku`;
CREATE TABLE `tb_w_score_of_sku` (
  `Sku` varchar(64) NOT NULL COMMENT '商品ID',
  `Score` int(11) DEFAULT NULL COMMENT '积分',
  PRIMARY KEY (`Sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tb_w_skus`
-- ----------------------------
DROP TABLE IF EXISTS `tb_w_skus`;
CREATE TABLE `tb_w_skus` (
  `Sku` varchar(64) NOT NULL COMMENT '商品ID',
  `DispOrder` int(2) DEFAULT NULL COMMENT '显示顺序，暂时没有使用',
  `Icon` varchar(255) DEFAULT NULL COMMENT '图标url',
  `Image` varchar(255) DEFAULT NULL COMMENT '图像url',
  `PriceInfo` varchar(90) DEFAULT NULL COMMENT '价格信息',
  `Price` decimal(10,2) NOT NULL COMMENT '价格数值',
  `Title` varchar(90) DEFAULT NULL COMMENT '标题',
  `Name` varchar(90) DEFAULT NULL COMMENT '名称',
  `Type` varchar(64) NOT NULL COMMENT '类型：coin,vip',
  `Addition` varchar(90) DEFAULT NULL COMMENT '附加信息',
  `Descript` varchar(240) DEFAULT NULL COMMENT '描述',
  `AmountInfo` varchar(90) DEFAULT NULL COMMENT '数量信息',
  `Amount` bigint(20) NOT NULL COMMENT '数量',
  `FirstName` varchar(90) DEFAULT NULL COMMENT '首充显示名称',
  `FirstAddition` varchar(90) DEFAULT NULL COMMENT '首充附加信息',
  `FirstAmount` bigint(20) NOT NULL COMMENT '首充数量',
  `Addition2` varchar(90) DEFAULT NULL COMMENT '附加信息',
  `ENABLE` int(1) NOT NULL COMMENT '礼包状态，1：已上架，0：已下架，2：已删除',
  `Visible` int(1) NOT NULL COMMENT '可见标志，1：商城可见，0：隐藏，不显示在商城',
  `HOT` int(1) NOT NULL DEFAULT '0' COMMENT '标签：0无，1热卖，2新品',
  `EndTime` datetime DEFAULT NULL COMMENT '下架时间',
  `AddNum` bigint(20) NOT NULL DEFAULT '0' COMMENT '加送万能豆数量',
  PRIMARY KEY (`Sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tb_w_skus_for_vip`
-- ----------------------------
DROP TABLE IF EXISTS `tb_w_skus_for_vip`;
CREATE TABLE `tb_w_skus_for_vip` (
  `Sku` varchar(64) NOT NULL COMMENT '商品ID',
  `VipLevel` int(2) NOT NULL COMMENT 'VIP级别',
  `VipName` varchar(90) DEFAULT NULL COMMENT 'VIP名称',
  `VipAddition` varchar(90) DEFAULT NULL COMMENT 'VIP附加信息',
  `VipAmount` bigint(20) NOT NULL COMMENT 'VIP数量',
  `VipTime` int(11) NOT NULL COMMENT '增加VIP时长，暂时不使用',
  `VipAddition2` varchar(90) DEFAULT NULL COMMENT 'VIP附加信息',
  PRIMARY KEY (`Sku`,`VipLevel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tb_w_skus_limit_perday`
-- ----------------------------
DROP TABLE IF EXISTS `tb_w_skus_limit_perday`;
CREATE TABLE `tb_w_skus_limit_perday` (
  `Sku` varchar(64) NOT NULL COMMENT '商品ID',
  `LimitNum` int(11) NOT NULL DEFAULT '0' COMMENT '每天最多购买数量',
  `TodayNum` int(11) NOT NULL DEFAULT '0' COMMENT '当天已购买数量',
  `recdate` datetime DEFAULT NULL COMMENT '更新当天次数时间',
  `resetdate` datetime DEFAULT NULL COMMENT '重置时间',
  PRIMARY KEY (`Sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品每天购买数量限制表';

-- ----------------------------
--  Table structure for `tb_w_skus_of_channel`
-- ----------------------------
DROP TABLE IF EXISTS `tb_w_skus_of_channel`;
CREATE TABLE `tb_w_skus_of_channel` (
  `Channel` varchar(64) NOT NULL COMMENT '渠道',
  `Sku` varchar(64) NOT NULL COMMENT '商品ID',
  PRIMARY KEY (`Channel`,`Sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
