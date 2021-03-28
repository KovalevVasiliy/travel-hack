"""

Revision ID: 9e306dabae18
Revises: 
Create Date: 2021-03-27 13:59:54.424181

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '9e306dabae18'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('fio', sa.String(length=100), nullable=False),
        sa.Column('avatar', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('user_id'),
    )
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_table('users')
