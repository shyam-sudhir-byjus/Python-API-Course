"""Add content column to posts table

Revision ID: fa22800e0508
Revises: 93ca87e1389b
Create Date: 2023-01-14 16:50:28.894528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa22800e0508'
down_revision = '93ca87e1389b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
