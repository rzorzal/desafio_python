"""add_uuid_extension

Revision ID: 3f2faf536fc0
Revises: 
Create Date: 2024-12-01 16:02:50.950827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f2faf536fc0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """)



def downgrade() -> None:
    op.execute("""
        DELETE EXTENSION IF EXISTS "uuid-ossp";
    """)
