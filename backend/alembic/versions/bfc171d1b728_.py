"""empty message

Revision ID: bfc171d1b728
Revises: d23656f9551c
Create Date: 2022-08-08 15:23:14.651405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfc171d1b728'
down_revision = 'd23656f9551c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_post_date'), 'post', ['date'], unique=False)
    op.create_index(op.f('ix_postword_date'), 'postword', ['date'], unique=False)
    op.create_index(op.f('ix_postword_post_id'), 'postword', ['post_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_postword_post_id'), table_name='postword')
    op.drop_index(op.f('ix_postword_date'), table_name='postword')
    op.drop_index(op.f('ix_post_date'), table_name='post')
    # ### end Alembic commands ###
