"""empty message

Revision ID: 4646921a52ac
Revises: 
Create Date: 2022-05-24 11:42:48.094355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4646921a52ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('animal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('latin', sa.String(length=255), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('cool', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('animal')
    # ### end Alembic commands ###
