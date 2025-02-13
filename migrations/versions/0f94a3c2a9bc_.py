"""empty message

Revision ID: 0f94a3c2a9bc
Revises: <new_revision_id>
Create Date: 2024-10-21 12:58:11.147919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f94a3c2a9bc'
down_revision = '<new_revision_id>'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.drop_column('person_count')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('person_count', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
