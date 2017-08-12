CREATE TABLE `users` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
    `username` varchar(64) NOT NULL DEFAULT '' COMMENT '用户名',
    `email` varchar(128) NOT NULL DEFAULT '' COMMENT '注册邮箱',
    `role_id` int(11) NOT NULL DEFAULT 0 COMMENT '角色ID',
    `password_hash` varchar(128) NOT NULL DEFAULT '' COMMENT '秘钥串',
    `confirmed` tinyint(1) NOT NULL DEFAULT 0 COMMENT '确认状态',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`),
    UNIQUE KEY `uk_email` (`email`),
    KEY `ix_created_at` (`created_at`),
    KEY `ix_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户';

CREATE TABLE `roles` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
    `name` varchar(64) NOT NULL DEFAULT '' COMMENT '角色名称',
    `default` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否默认角色',
    `permissions` int(11) NOT NULL DEFAULT 0 COMMENT '权限',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_name` (`name`),
    KEY `ix_created_at` (`created_at`),
    KEY `ix_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色';

CREATE TABLE `user_profile` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
    `user_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '用户ID',
    `name` varchar(64) NOT NULL DEFAULT '' COMMENT '真实姓名',
    `location` varchar(64) NOT NULL DEFAULT '' COMMENT '地点',
    `about_me` TEXT COMMENT '自我介绍',
    `last_seen` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上次登录时间',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_id` (`user_id`),
    KEY `ix_created_at` (`created_at`),
    KEY `ix_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户个人资料';
