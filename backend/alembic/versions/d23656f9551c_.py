"""empty message

Revision ID: d23656f9551c
Revises: c60bb5a8eaea
Create Date: 2022-08-07 10:30:29.372078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd23656f9551c'
down_revision = 'c60bb5a8eaea'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('group_id', sa.Integer(), nullable=True))
    op.add_column('group', sa.Column('social_media_type', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group', 'social_media_type')
    op.drop_column('group', 'group_id')
    # ### end Alembic commands ###