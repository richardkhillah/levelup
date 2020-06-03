"""rename premissions to permissions

Revision ID: af28b282adc7
Revises: 727d53ab11f0
Create Date: 2020-05-28 15:36:31.370061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af28b282adc7'
down_revision = '727d53ab11f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('permissions', sa.Integer(), nullable=True))
    # op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    op.drop_column('roles', 'premissions')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('premissions', sa.INTEGER(), nullable=True))
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_column('roles', 'permissions')
    # ### end Alembic commands ###
