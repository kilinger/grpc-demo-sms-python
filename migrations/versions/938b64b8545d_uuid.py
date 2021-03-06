"""uuid

Revision ID: 938b64b8545d
Revises: 5734f9a60a02
Create Date: 2016-10-21 17:44:30.228211

"""

# revision identifiers, used by Alembic.
revision = '938b64b8545d'
down_revision = '5734f9a60a02'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('provider', sa.Column('type', sa.String(length=10), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('provider', 'type')
    ### end Alembic commands ###
