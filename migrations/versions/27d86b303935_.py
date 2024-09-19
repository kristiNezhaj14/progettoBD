"""empty message

Revision ID: 27d86b303935
Revises: 3da2eeeebddb
Create Date: 2024-09-19 16:51:58.555147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27d86b303935'
down_revision = '3da2eeeebddb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_item', schema=None) as batch_op:
        batch_op.drop_constraint('order_item_product_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'product', ['product_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_item', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('order_item_product_id_fkey', 'product', ['product_id'], ['id'])

    # ### end Alembic commands ###