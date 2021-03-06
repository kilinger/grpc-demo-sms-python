"""empty message

Revision ID: 3bf410c3a395
Revises: None
Create Date: 2016-10-21 09:52:14.669939

"""

# revision identifiers, used by Alembic.
revision = '3bf410c3a395'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('provider',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('host', sa.String(length=256), nullable=False),
    sa.Column('user', sa.String(length=120), nullable=False),
    sa.Column('pwd', sa.String(length=120), nullable=False),
    sa.Column('charge_type', sa.String(length=15), nullable=False),
    sa.Column('surplus_count', sa.Integer(), nullable=True),
    sa.Column('method_send', sa.String(length=10), nullable=False),
    sa.Column('param_user', sa.String(length=10), nullable=False),
    sa.Column('param_pwd', sa.String(length=10), nullable=False),
    sa.Column('param_tel', sa.String(length=10), nullable=False),
    sa.Column('param_msg', sa.String(length=10), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=256), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('msg', sa.Text(), nullable=False),
    sa.Column('tel', sa.Text(), nullable=False),
    sa.Column('sender', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sms_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=256), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('sms_id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.String(length=120), nullable=True),
    sa.Column('is_receipt', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.id'], ),
    sa.ForeignKeyConstraint(['sms_id'], ['sms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sms_record')
    op.drop_table('sms')
    op.drop_table('provider')
    ### end Alembic commands ###
