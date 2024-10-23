"""empty message

Revision ID: 8aa6828a9c4d
Revises: 3303f6593f54
Create Date: 2024-10-18 12:00:31.197981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8aa6828a9c4d'
down_revision = '3303f6593f54'
branch_labels = None
depends_on = None


def upgrade():
    # Add column with default value for flights
    with op.batch_alter_table('flights', schema=None) as batch_op:
        batch_op.add_column(sa.Column('person', sa.Integer(), nullable=False, server_default='1'))

    # Add column with default value for hotels
    with op.batch_alter_table('hotels', schema=None) as batch_op:
        batch_op.add_column(sa.Column('person', sa.Integer(), nullable=False, server_default='1'))


def downgrade():
    # Remove the added columns
    with op.batch_alter_table('hotels', schema=None) as batch_op:
        batch_op.drop_column('person')

    with op.batch_alter_table('flights', schema=None) as batch_op:
        batch_op.drop_column('person')
