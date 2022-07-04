"""empty message

Revision ID: 8cf1ab81d214
Revises: 5aca326e6310
Create Date: 2022-06-30 15:05:40.656812

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8cf1ab81d214'
down_revision = '5aca326e6310'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admin', 'role')
    op.drop_column('user', 'role')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', mysql.VARCHAR(length=10), nullable=False))
    op.add_column('admin', sa.Column('role', mysql.VARCHAR(length=10), nullable=False))
    # ### end Alembic commands ###
