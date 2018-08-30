"""new col

Revision ID: 7872f807b1fd
Revises: 69960197d1e8
Create Date: 2018-08-20 14:58:57.250016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7872f807b1fd'
down_revision = '69960197d1e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email_hash', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'email_hash')
    # ### end Alembic commands ###