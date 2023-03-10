"""init_sqlite_location_table

Revision ID: c74d6b2647f6
Revises: bc993cc2bb84
Create Date: 2022-12-28 22:35:02.975789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c74d6b2647f6'
down_revision = 'bc993cc2bb84'  # change it to None?
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('kitespot', sa.Boolean(), nullable=False),
    sa.Column('surfspot', sa.Boolean(), nullable=False),
    sa.Column('best_wind', sa.String(), nullable=True),
    sa.Column('best_tide', sa.String(), nullable=True),
    sa.Column('wave_info', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('locations')
    # ### end Alembic commands ###
