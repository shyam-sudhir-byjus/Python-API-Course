"""add last few columns to posts table

Revision ID: 40869fb55d41
Revises: 8cd996201ce8
Create Date: 2023-01-14 17:05:48.236296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40869fb55d41'
down_revision = '8cd996201ce8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))    
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
