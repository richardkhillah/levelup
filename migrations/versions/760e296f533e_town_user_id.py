"""town user_id

Revision ID: 760e296f533e
Revises: 2e13b6198ff8
Create Date: 2020-06-12 14:15:47.699888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '760e296f533e'
down_revision = '2e13b6198ff8'
branch_labels = None
depends_on = None





def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()




#--------------------------------
# Default
def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


#--------------------------------
# Township
def upgrade_township_data():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_township_data():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


#--------------------------------
# User
def upgrade_user_data():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('town', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'town', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade_user_data():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'town', type_='foreignkey')
    op.drop_column('town', 'user_id')
    # ### end Alembic commands ###
