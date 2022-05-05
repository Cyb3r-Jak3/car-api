"""Change column names

Revision ID: 234633eb1485
Revises: 58627ce4a028
Create Date: 2022-05-05 16:52:31.578288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '234633eb1485'
down_revision = '58627ce4a028'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('charging_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('charge_time', sa.Interval(), nullable=True),
    sa.Column('charge_amount', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('charging_table')
    # ### end Alembic commands ###