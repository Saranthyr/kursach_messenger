"""Data migration ver 0.2.0

Revision ID: cd0c600a3876
Revises: 71e29218ea73
Create Date: 2023-04-27 16:04:30.410404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd0c600a3876'
down_revision = '71e29218ea73'
branch_labels = None
depends_on = None


def upgrade() -> None:
    chat_types = sa.sql.table("chat_types",
                              sa.sql.column('id', sa.INTEGER()),
                              sa.sql.column('name', sa.VARCHAR(32)))

    op.bulk_insert(chat_types,
                   [
                       {'id': 1, 'name': 'Private'},
                       {'id': 2, 'name': 'Group'},
                       {'id': 3, 'name': 'Supergroup'},
                   ])


def downgrade() -> None:
    op.execute('delete from chat_types where id in (1,2,3)')
