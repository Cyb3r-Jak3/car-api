"""Add DB relationship between trip and range

Revision ID: a6a27dfb9df1
Revises: 1be17cd7777b
Create Date: 2022-05-22 17:54:42.189924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6a27dfb9df1'
down_revision = '1be17cd7777b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('range_table', sa.Column('trip_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'range_table', 'trip_table', ['trip_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'range_table', type_='foreignkey')
    op.drop_column('range_table', 'trip_id')
    # ### end Alembic commands ###
