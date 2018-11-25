"""added cohort

Revision ID: 14d3c89a0856
Revises: 2897ff863a4f
Create Date: 2018-11-25 01:24:18.781579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14d3c89a0856'
down_revision = '2897ff863a4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cohort',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company', sa.String(length=100), nullable=True),
    sa.Column('founder', sa.String(length=280), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('industry', sa.String(length=280), nullable=True),
    sa.Column('skills', sa.String(length=280), nullable=True),
    sa.Column('help_req', sa.String(length=280), nullable=True),
    sa.Column('mentor1', sa.String(length=128), nullable=True),
    sa.Column('mentor2', sa.String(length=128), nullable=True),
    sa.Column('mentor3', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cohort_email'), 'cohort', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cohort_email'), table_name='cohort')
    op.drop_table('cohort')
    # ### end Alembic commands ###
