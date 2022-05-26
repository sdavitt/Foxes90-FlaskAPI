"""empty message

Revision ID: f50420dea65e
Revises: eab41b4c76f8
Create Date: 2022-05-26 11:03:55.706832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f50420dea65e'
down_revision = 'eab41b4c76f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('api_token', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'api_token')
    # ### end Alembic commands ###
