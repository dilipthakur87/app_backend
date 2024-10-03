"""empty message

Revision ID: 89cd31d71e4e
Revises: 9c86a3e8d329
Create Date: 2024-10-03 09:11:35.501340

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '89cd31d71e4e'
down_revision = '9c86a3e8d329'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('note', schema=None) as batch_op:
        batch_op.add_column(sa.Column('celery_task_id', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('note', schema=None) as batch_op:
        batch_op.drop_column('celery_task_id')

    # ### end Alembic commands ###
