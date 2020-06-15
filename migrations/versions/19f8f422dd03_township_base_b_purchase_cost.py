"""township base_b purchase_cost

Revision ID: 19f8f422dd03
Revises: 760e296f533e
Create Date: 2020-06-13 14:56:33.107671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19f8f422dd03'
down_revision = '760e296f533e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('source', sa.Column('purchase_cost', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('source', 'purchase_cost')
    # ### end Alembic commands ###
