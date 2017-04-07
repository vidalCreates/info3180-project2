"""empty message

Revision ID: 414777a4181e
Revises: 067146298c06
Create Date: 2017-04-06 16:45:53.655000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '414777a4181e'
down_revision = '067146298c06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('password', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profile', 'password')
    # ### end Alembic commands ###
