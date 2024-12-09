"""email_model_add_column

Revision ID: 60f2b3603728
Revises: e1051c2e4db3
Create Date: 2024-12-09 12:44:26.845440

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "60f2b3603728"
down_revision = "e1051c2e4db3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("email_messages", sa.Column("type", sa.String(), nullable=False))
    op.add_column(
        "email_messages",
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("email_messages", "tags")
    op.drop_column("email_messages", "type")
    # ### end Alembic commands ###
