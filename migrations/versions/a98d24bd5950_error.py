"""error

Revision ID: a98d24bd5950
Revises: 11533c5f4ead
Create Date: 2016-10-21 11:21:53.144010

"""

# revision identifiers, used by Alembic.
revision = 'a98d24bd5950'
down_revision = '11533c5f4ead'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sms_record', sa.Column('error', sa.String(length=256), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sms_record', 'error')
    ### end Alembic commands ###
