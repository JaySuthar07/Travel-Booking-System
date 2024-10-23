"""Set default status to Pending

Revision ID: <new_revision_id>
Revises: 8aa6828a9c4d
Create Date: <current_date_and_time>

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '<new_revision_id>'
down_revision = '8aa6828a9c4d'
branch_labels = None
depends_on = None


def upgrade():
    # Update existing records to have a default status
    op.execute("UPDATE flights SET status = 'Pending' WHERE status IS NULL")
    op.execute("UPDATE hotels SET status = 'Pending' WHERE status IS NULL")


def downgrade():
    # Optionally, you can define how to revert this change if necessary
    pass
