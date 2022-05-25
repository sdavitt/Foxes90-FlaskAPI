"""empty message

Revision ID: 939e6cee09bf
Revises: 
Create Date: 2022-05-25 11:40:43.455176

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '939e6cee09bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('animal', sa.Column('species', sa.String(length=50), nullable=False))
    op.add_column('animal', sa.Column('latin_name', sa.String(length=255), nullable=True))
    op.add_column('animal', sa.Column('size_cm', sa.Integer(), nullable=True))
    op.add_column('animal', sa.Column('diet', sa.String(length=255), nullable=True))
    op.add_column('animal', sa.Column('lifespan', sa.String(length=255), nullable=True))
    op.add_column('animal', sa.Column('description', sa.String(length=255), nullable=False))
    op.add_column('animal', sa.Column('image', sa.String(length=100), nullable=True))
    op.add_column('animal', sa.Column('price', sa.Float(precision=2), nullable=False))
    op.add_column('animal', sa.Column('created_on', sa.DateTime(), nullable=True))
    op.drop_column('animal', 'latin')
    op.drop_column('animal', 'created')
    op.drop_column('animal', 'cool')
    op.drop_column('animal', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('animal', sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.add_column('animal', sa.Column('cool', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('animal', sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('animal', sa.Column('latin', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('animal', 'created_on')
    op.drop_column('animal', 'price')
    op.drop_column('animal', 'image')
    op.drop_column('animal', 'description')
    op.drop_column('animal', 'lifespan')
    op.drop_column('animal', 'diet')
    op.drop_column('animal', 'size_cm')
    op.drop_column('animal', 'latin_name')
    op.drop_column('animal', 'species')
    # ### end Alembic commands ###
