from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "account" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(255) NOT NULL  DEFAULT '',
    "last_name" VARCHAR(255) NOT NULL  DEFAULT '',
    "deactivated" BOOL NOT NULL  DEFAULT False,
    "about" TEXT
);
CREATE TABLE IF NOT EXISTS "group" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "group_id" INT NOT NULL  DEFAULT 0,
    "name" VARCHAR(255) NOT NULL,
    "screen_name" VARCHAR(512) NOT NULL,
    "is_closed" BOOL NOT NULL  DEFAULT False,
    "description" TEXT NOT NULL,
    "contact_id" INT NOT NULL,
    "social_media_type" VARCHAR(255) NOT NULL
);
COMMENT ON COLUMN "group"."social_media_type" IS 'тип соц. сети';
CREATE TABLE IF NOT EXISTS "post" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "post_id" INT NOT NULL,
    "date" TIMESTAMPTZ NOT NULL,
    "marked_as_ads" BOOL NOT NULL  DEFAULT False,
    "post_type" VARCHAR(255) NOT NULL,
    "text" TEXT NOT NULL,
    "group_id" INT NOT NULL REFERENCES "group" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_post_post_id_51fb27" ON "post" ("post_id");
CREATE INDEX IF NOT EXISTS "idx_post_date_fab403" ON "post" ("date");
CREATE TABLE IF NOT EXISTS "comment" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "author_id" INT NOT NULL REFERENCES "account" ("id") ON DELETE CASCADE,
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "poststats" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "likes_count" INT NOT NULL,
    "repost_count" INT NOT NULL,
    "views_count" INT NOT NULL,
    "comment_count" INT NOT NULL,
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "postword" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "word" VARCHAR(255) NOT NULL,
    "date" TIMESTAMPTZ NOT NULL,
    "count" SMALLINT NOT NULL,
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "email" VARCHAR(512) NOT NULL  DEFAULT '',
    "password" VARCHAR(2048),
    "first_name" VARCHAR(255) NOT NULL  DEFAULT '',
    "last_name" VARCHAR(255) NOT NULL  DEFAULT ''
);
CREATE INDEX IF NOT EXISTS "idx_user_usernam_9987ab" ON "user" ("username");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
