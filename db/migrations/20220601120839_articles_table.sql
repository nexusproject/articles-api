-- migrate:up

SET NAMES UTF8;

CREATE TABLE IF NOT EXISTS articles (
    article_id  BIGINT UNSIGNED AUTO_INCREMENT NOT NULL COMMENT 'Unique article id',
    topic       VARCHAR(255) NOT NULL COMMENT 'Article topic',
    text        TEXT COLUMN_FORMAT COMPRESSED COMMENT 'Article text',
    created     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation datetime',
    updated     DATETIME DEFAULT NULL COMMENT 'Date and time of last update',

    PRIMARY KEY (article_id, created),
    KEY (topic),
    KEY (created),
    KEY (updated)
)
    ENGINE=InnoDB
    DEFAULT CHARSET=utf8
    COMMENT='Articles'

    PARTITION BY RANGE(YEAR(created)) (
        PARTITION articles_current VALUES LESS THAN(2023),
        PARTITION articles_2023 VALUES LESS THAN(2024),
        PARTITION articles_2024 VALUES LESS THAN(2025),
        PARTITION articles_2025 VALUES LESS THAN(2026)
    );


-- migrate:down

