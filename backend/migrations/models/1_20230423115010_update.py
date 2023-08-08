from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "account" ADD "activities" TEXT;
        ALTER TABLE "account" ADD "bdate" TIMESTAMPTZ;
        ALTER TABLE "account" ADD "last_seen" TIMESTAMPTZ;
        """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "account" DROP COLUMN "activities";
        ALTER TABLE "account" DROP COLUMN "bdate";
        ALTER TABLE "account" DROP COLUMN "last_seen";"""
