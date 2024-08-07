"""add fullname hash_password phone about_me created updated column to users table

Revision ID: 30e0faa978ce
Revises: 1523ccfabc33
Create Date: 2024-08-07 10:14:10.622493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.libs.sql_alchemy_lib import Base
from sqlalchemy.dialects import mysql
# revision identifiers, used by Alembic.
revision: str = '30e0faa978ce'
down_revision: Union[str, None] = '1523ccfabc33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('fullname', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('hash_password', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('phone', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('about_me', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.create_index(op.f('ix_users_fullname'), 'users', ['fullname'], unique=True)
    op.create_index(op.f('ix_users_phone'), 'users', ['phone'], unique=True)
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', mysql.VARCHAR(length=100), nullable=True))
    op.drop_index(op.f('ix_users_phone'), table_name='users')
    op.drop_index(op.f('ix_users_fullname'), table_name='users')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'about_me')
    op.drop_column('users', 'phone')
    op.drop_column('users', 'hash_password')
    op.drop_column('users', 'fullname')
    # ### end Alembic commands ###