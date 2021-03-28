"""

Revision ID: 340aeabf873a
Revises: 6b329da67393
Create Date: 2021-03-27 17:52:39.492053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '340aeabf873a'
down_revision = '6b329da67393'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('user_to_locations', 'location_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('user_to_locations', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('user_to_news', 'news_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('user_to_news', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('user_to_trips', 'trip_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('user_to_trips', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with open('/opt/app/scripts/create_tours.sql') as f:
        create_tours = f.readlines()

    conn = op.get_bind()
    conn.execute(create_tours)


def downgrade():
    op.alter_column('user_to_trips', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('user_to_trips', 'trip_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('user_to_news', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('user_to_news', 'news_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('user_to_locations', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('user_to_locations', 'location_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    raise RuntimeError('Not downgradable')
