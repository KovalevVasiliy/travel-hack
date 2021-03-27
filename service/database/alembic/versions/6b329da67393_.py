"""

Revision ID: 6b329da67393
Revises: 79290e7962ff
Create Date: 2021-03-27 15:32:26.357670

"""
import sqlalchemy as sa
from alembic import op

revision = '6b329da67393'
down_revision = '79290e7962ff'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_to_locations',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('location_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['gotorussia_travels_locations.id'],),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'],),
    )
    op.create_table(
        'user_to_news',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('news_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['news_id'], ['news.news_id'],),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'],),
    )
    op.create_table(
        'user_to_trips',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('trip_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['trip_id'], ['trips.trip_id'],),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'],),
    )


def downgrade():
    op.drop_table('user_to_trips')
    op.drop_table('user_to_news')
    op.drop_table('user_to_locations')
