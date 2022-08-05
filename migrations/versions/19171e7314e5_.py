"""empty message

Revision ID: 19171e7314e5
Revises: c1a1267e92f7
Create Date: 2022-07-07 00:19:51.747589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19171e7314e5'
down_revision = 'c1a1267e92f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('title2', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('test2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=60), nullable=True),
    sa.Column('title2', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test2')
    op.drop_table('test')
    # ### end Alembic commands ###