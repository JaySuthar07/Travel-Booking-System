"""Initial migration.

Revision ID: d55774462078
Revises: 
Create Date: 2024-10-15 22:40:13.674414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd55774462078'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flights', schema=None) as batch_op:
        batch_op.alter_column('Departure',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.Date(),
               existing_nullable=False)
        batch_op.alter_column('Return',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.Date(),
               existing_nullable=True)
        batch_op.alter_column('price',
               existing_type=sa.FLOAT(),
               type_=sa.Numeric(precision=10, scale=2),
               existing_nullable=False)

    with op.batch_alter_table('hotels', schema=None) as batch_op:
        batch_op.alter_column('Check_In',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.Date(),
               existing_nullable=False)
        batch_op.alter_column('Check_Out',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.Date(),
               existing_nullable=False)
        batch_op.alter_column('price',
               existing_type=sa.FLOAT(),
               type_=sa.Numeric(precision=10, scale=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hotels', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Numeric(precision=10, scale=2),
               type_=sa.FLOAT(),
               existing_nullable=False)
        batch_op.alter_column('Check_Out',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)
        batch_op.alter_column('Check_In',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)

    with op.batch_alter_table('flights', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Numeric(precision=10, scale=2),
               type_=sa.FLOAT(),
               existing_nullable=False)
        batch_op.alter_column('Return',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(length=80),
               existing_nullable=True)
        batch_op.alter_column('Departure',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###
