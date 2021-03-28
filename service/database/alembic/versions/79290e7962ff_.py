"""

Revision ID: 79290e7962ff
Revises: 9e306dabae18
Create Date: 2021-03-27 14:12:48.814147

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '79290e7962ff'
down_revision = '9e306dabae18'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'news',
        sa.Column('news_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('news_id'),
    )
    op.create_index(op.f('ix_news_news_id'), 'news', ['news_id'], unique=False)
    op.create_table(
        'trips',
        sa.Column('trip_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('trip_id'),
    )
    op.create_index(op.f('ix_trips_trip_id'), 'trips', ['trip_id'], unique=False)

    with open('/opt/app/scripts/create_regions.sql') as f:
        create_regions = f.readlines()
    with open('/opt/app/scripts/create_locations.sql') as f:
        create_locations = f.readlines()
    with open('/opt/app/scripts/create_categories.sql') as f:
        create_categories = f.readlines()

    conn = op.get_bind()
    conn.execute(create_regions)
    conn.execute(create_locations)
    conn.execute(create_categories)


def downgrade():
    op.drop_index(op.f('ix_trips_trip_id'), table_name='trips')
    op.drop_table('trips')
    op.drop_index(op.f('ix_news_news_id'), table_name='news')
    op.drop_table('news')

    raise RuntimeError('Not downgradable')
