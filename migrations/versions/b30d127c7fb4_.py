"""empty message

Revision ID: b30d127c7fb4
Revises: de4280a78122
Create Date: 2022-06-30 14:58:05.525566

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b30d127c7fb4'
down_revision = 'de4280a78122'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('admin', 'role',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)
    op.alter_column('user', 'role',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'role',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)
    op.alter_column('admin', 'role',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)
    # ### end Alembic commands ###
