"""Squash migrations

Revision ID: 0282ff58cb00
Revises: 
Create Date: 2023-12-02 14:29:22.284715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0282ff58cb00'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('current_price', sa.Float(), nullable=True),
    sa.Column('market_cap', sa.BigInteger(), nullable=True),
    sa.Column('market_cap_rank', sa.Integer(), nullable=True),
    sa.Column('fully_diluted_valuation', sa.BigInteger(), nullable=True),
    sa.Column('total_volume', sa.BigInteger(), nullable=True),
    sa.Column('high_24h', sa.Float(), nullable=True),
    sa.Column('low_24h', sa.Float(), nullable=True),
    sa.Column('price_change_24h', sa.Float(), nullable=True),
    sa.Column('price_change_percentage_24h', sa.Float(), nullable=True),
    sa.Column('market_cap_change_24h', sa.BigInteger(), nullable=True),
    sa.Column('market_cap_change_percentage_24h', sa.Float(), nullable=True),
    sa.Column('circulating_supply', sa.Float(), nullable=True),
    sa.Column('total_supply', sa.Float(), nullable=True),
    sa.Column('max_supply', sa.Float(), nullable=True),
    sa.Column('ath', sa.Float(), nullable=True),
    sa.Column('ath_change_percentage', sa.Float(), nullable=True),
    sa.Column('ath_date', sa.String(length=30), nullable=True),
    sa.Column('atl', sa.Float(), nullable=True),
    sa.Column('atl_change_percentage', sa.Float(), nullable=True),
    sa.Column('atl_date', sa.String(length=30), nullable=True),
    sa.Column('roi', sa.JSON(), nullable=True),
    sa.Column('last_updated', sa.String(length=30), nullable=True),
    sa.Column('sparkline_in_7d', sa.JSON(), nullable=True),
    sa.Column('price_change_percentage_1h_in_currency', sa.Float(), nullable=True),
    sa.Column('price_change_percentage_24h_in_currency', sa.Float(), nullable=True),
    sa.Column('price_change_percentage_7d_in_currency', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('archived_tokens_refs', sa.JSON(), nullable=True),
    sa.Column('monitored_tokens_refs', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user_token',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('token_id', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['token_id'], ['token.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.UniqueConstraint('user_id', 'token_id', name='uq_user_token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_token')
    op.drop_table('user')
    op.drop_table('token')
    # ### end Alembic commands ###
