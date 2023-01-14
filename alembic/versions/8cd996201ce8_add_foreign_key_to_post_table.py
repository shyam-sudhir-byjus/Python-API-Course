"""Add foreign key to post table

Revision ID: 8cd996201ce8
Revises: 41a335eaf0b1
Create Date: 2023-01-14 17:01:14.523496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cd996201ce8'
down_revision = '41a335eaf0b1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table='posts', referent_table='users', 
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
