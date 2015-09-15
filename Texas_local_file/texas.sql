drop table if exists tb_w_skus;

create table tb_w_skus
(
   Sku                  varchar(64) not null comment '商品ID',
   DispOrder            int(2) comment '显示顺序，暂时没有使用',
   Icon                 varchar(255) comment '图标url',
   Image                varchar(255) comment '图像url',
   PriceInfo            varchar(90) comment '价格信息',
   Price                float not null comment '价格数值',
   Title                varchar(90) comment '标题',
   Name                 varchar(90) comment '名称',
   Type                 varchar(64) not null comment '类型：coin,vip',
   Addition             varchar(90) comment '附加信息',
   Descript             varchar(240) comment '描述',
   AmountInfo           varchar(90)  comment '数量信息',
   Amount               bigint not null comment '数量',
   FirstName            varchar(90) comment '首充显示名称',
   FirstAddition        varchar(90) comment '首充附加信息',
   FirstAmount          bigint not null comment '首充数量',
   Addition2             varchar(90) comment '附加信息',
   Enable               int(1)  not null comment '启用标志，1：启用，0：不启用',
   Visible                int(1)  not null comment '可见标志，1：商城可见，0：隐藏，不显示在商城',
   primary key (Sku)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

alter table tb_w_skus add
(
   Hot                   int(1) default 0 comment '热卖标志'
);

drop table tb_w_skus_for_vip;

create table tb_w_skus_for_vip
(
   Sku     varchar(64) not null comment '商品ID',
   VipLevel int(2) not null comment 'VIP级别',
   VipName                 varchar(90) comment 'VIP名称',
   VipAddition             varchar(90) comment 'VIP附加信息',
   VipAmount               bigint not null comment 'VIP数量',
   VipTime   int not null comment '增加VIP时长，暂时不使用',
   VipAddition2           varchar(90) comment 'VIP附加信息',
   primary key (Sku, VipLevel)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table if exists tb_w_purchase;

create table tb_w_purchase
(
	trade_no            varchar(64) not null comment '定单号',
	UserID              varchar(32) not null comment '用户ID',
	sku                 varchar(64) not null comment '商品ID',
          skutype          varchar(64) not null comment '商品类型',
	amount              bigint not null comment '数量',
	original_data       varchar(1024) comment '原始数据',
         result                int(2) default 0 comment '定单结果，1：处理完成，0：正在处理',
	recdate             datetime not null comment '记录时间',
	primary key (trade_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index Index_purchase_1 on tb_w_purchase
(
   UserID
);

drop index Index_ChipsLog_1 on tb_w_purchaselog;

drop table if exists tb_w_purchaselog;

create table tb_w_purchaselog
(
   TimeStamp            datetime not null comment '时间',
   UserID               varchar(32) not null comment '用户ID',
   ActionType           int(4) not null comment '1:购买',
   AmountBefore         bigint not null comment '操作前数量',
   AmountChange         bigint not null comment '操作变化量',
   AmountAfter          bigint not null comment '操作后数量',
   Remark               varchar(128) comment '支付序列号、牌桌ID等'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index Index_PurchaseLog_1 on tb_w_purchaselog
(
   UserID
);

drop table tb_w_skus_of_channel;
create table tb_w_skus_of_channel
(
  Channel varchar(64) not null comment '渠道',
  Sku     varchar(64) not null comment '商品ID', 
  primary key(Channel, Sku)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table tb_w_score_of_sku;

create table tb_w_score_of_sku
(
   Sku     varchar(64) not null comment '商品ID',
   Score  int comment '积分',
   primary key (Sku)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table tb_w_skus_limit_perday;
create table tb_w_skus_limit_perday
(
   Sku                  varchar(64) not null comment '商品ID',
   LimitNum         int not null default 0 comment '每天最多购买数量',
   TodayNum       int not null default 0 comment '当天已购买数量',
   recdate datetime comment '更新当天次数时间',
   resetdate datetime comment '重置时间',
   primary key (Sku)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '商品每天购买数量限制表';


drop table tb_w_payload;
create table tb_w_payload
(
   PayloadID        varchar(64) not null comment '定单ID',
   Sku                  varchar(64) not null comment '商品ID',
   User                 varchar(128) not null comment '用户名',
   Role                 varchar(128) comment '角色名',
   UserData         varchar(128) comment '用户自定义数据',
   Channel           varchar(16) not null comment '渠道号',
   recdate            datetime not null comment '生成记录时间',
   Status               int(1) not null default 0 comment '完成状态，未完成：0，已完成：1',
   primary key (PayloadID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '商品定单表';

drop table tb_w_channel;
create table tb_w_channel (
   ID                 BIGINT(20) NOT NULL AUTO_INCREMENT,
   Channel            VARCHAR(64)  NOT NULL COMMENT '渠道唯一标识',
   ChannelName        VARCHAR(200)  NOT NULL COMMENT '渠道名称',
   Image              VARCHAR(400)  NOT NULL COMMENT '渠道图片',
   Descript           VARCHAR(400)  DEFAULT NULL COMMENT '渠道描述',
   PRIMARY KEY (`ID`)
) ENGINE=INNODB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='支付渠道配置表';

ALTER TABLE tb_w_skus ADD StartTime DATETIME DEFAULT NULL COMMENT '上架时间';
ALTER TABLE tb_w_skus ADD EndTime DATETIME DEFAULT NULL COMMENT '下架时间';
ALTER TABLE tb_w_skus ADD AddNum BIGINT(20) NOT NULL DEFAULT '0' COMMENT '加送万能豆数量';
ALTER TABLE tb_w_skus MODIFY COLUMN Price decimal(10,2) NOT NULL COMMENT '价格数值';
ALTER TABLE tb_w_skus MODIFY COLUMN ENABLE INT(1) NOT NULL COMMENT '礼包状态，1：已上架，0：已下架，2：已删除';
ALTER TABLE tb_w_skus MODIFY COLUMN HOT INT(1)  NOT NULL DEFAULT '0' COMMENT '标签：0无，1热卖，2新品';
ALTER TABLE tb_w_payload MODIFY COLUMN Channel VARCHAR(64) NOT NULL COMMENT '渠道号';


