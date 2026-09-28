-- 社員管理テーブルの作成
CREATE TABLE IF NOT EXISTS `employees` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '社員ID',
    `employee_code` VARCHAR(20) NOT NULL UNIQUE COMMENT '社員番号（例: EMP001）',
    `name` VARCHAR(100) NOT NULL COMMENT '氏名',
    `email` VARCHAR(150) NOT NULL UNIQUE COMMENT 'メールアドレス',
    `department` VARCHAR(50) NOT NULL COMMENT '所属部署（開発部, 営業部, 人事部, 総務部）',
    `position` VARCHAR(50) NOT NULL COMMENT '役職（一般, リーダー, マネージャー, 部長）',
    `joined_date` DATE NOT NULL COMMENT '入社日',
    `status` VARCHAR(20) NOT NULL DEFAULT '在籍' COMMENT '在籍ステータス（在籍, 休職, 退職）',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='社員マスタテーブル';

-- 初期サンプルデータの投入
INSERT INTO `employees` (`employee_code`, `name`, `email`, `department`, `position`, `joined_date`, `status`) VALUES
('EMP001', '山田 太郎', 'yamada.taro@example.com', '開発部', 'リーダー', '2021-04-01', '在籍'),
('EMP002', '佐藤 花子', 'sato.hanako@example.com', '開発部', '一般', '2023-04-01', '在籍'),
('EMP003', '鈴木 一郎', 'suzuki.ichiro@example.com', '営業部', 'マネージャー', '2019-10-01', '在籍'),
('EMP004', '高橋 健太', 'takahashi.kenta@example.com', '人事部', '一般', '2022-04-01', '休職'),
('EMP005', '田中 美咲', 'tanaka.misaki@example.com', '総務部', '一般', '2024-04-01', '在籍')
ON DUPLICATE KEY UPDATE `id`=`id`;
