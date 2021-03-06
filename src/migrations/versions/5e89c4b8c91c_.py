"""empty message

Revision ID: 5e89c4b8c91c
Revises: 212ea5e66da6
Create Date: 2017-12-11 17:13:25.473844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e89c4b8c91c'
down_revision = '212ea5e66da6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_user_first_name'), 'user', ['first_name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_first_name'), table_name='user')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###
