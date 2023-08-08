from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "postword" ALTER COLUMN "date" TYPE DATE USING "date"::DATE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "postword" ALTER COLUMN "date" TYPE TIMESTAMPTZ USING "date"::TIMESTAMPTZ;"""
