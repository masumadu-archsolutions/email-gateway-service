"""initial_migration_script

Revision ID: e1051c2e4db3
Revises:
Create Date: 2024-12-09 11:38:42.707399

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e1051c2e4db3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "email_accounts",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("mail_address", sa.String(), nullable=False),
        sa.Column("sender_name", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_by", sa.String(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_by", sa.String(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_email_accounts_mail_address"),
        "email_accounts",
        ["mail_address"],
        unique=True,
    )
    op.create_index(
        op.f("ix_email_accounts_user_id"), "email_accounts", ["user_id"], unique=False
    )
    op.create_table(
        "email_message_types",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("priority", sa.String(), server_default="high", nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_by", sa.String(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_by", sa.String(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("type"),
    )
    op.create_index(
        op.f("ix_email_message_types_user_id"),
        "email_message_types",
        ["user_id"],
        unique=False,
    )
    op.create_table(
        "email_messages",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("sender_address", sa.String(), nullable=False),
        sa.Column("sender_name", sa.String(), nullable=True),
        sa.Column("subject", sa.String(), nullable=True),
        sa.Column("html_body", sa.String(), nullable=True),
        sa.Column("text_body", sa.String(), nullable=True),
        sa.Column("is_scheduled", sa.Boolean(), nullable=False),
        sa.Column("scheduled_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("total_recipients", sa.Integer(), nullable=False),
        sa.Column(
            "require_callback", sa.Boolean(), server_default="False", nullable=False
        ),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_by", sa.String(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_by", sa.String(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_email_messages_sender_address"),
        "email_messages",
        ["sender_address"],
        unique=False,
    )
    op.create_index(
        op.f("ix_email_messages_sender_name"),
        "email_messages",
        ["sender_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_email_messages_user_id"), "email_messages", ["user_id"], unique=False
    )
    op.create_table(
        "email_message_batches",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("email_id", sa.UUID(), nullable=False),
        sa.Column("total_recipients", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_by", sa.String(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_by", sa.String(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["email_id"],
            ["email_messages.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_email_message_batches_email_id"),
        "email_message_batches",
        ["email_id"],
        unique=False,
    )
    op.create_table(
        "email_message_recipients",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("batch_id", sa.UUID(), nullable=True),
        sa.Column("mail_address", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_by", sa.String(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_by", sa.String(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["batch_id"],
            ["email_message_batches.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_email_message_recipients_batch_id"),
        "email_message_recipients",
        ["batch_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_email_message_recipients_batch_id"),
        table_name="email_message_recipients",
    )
    op.drop_table("email_message_recipients")
    op.drop_index(
        op.f("ix_email_message_batches_email_id"), table_name="email_message_batches"
    )
    op.drop_table("email_message_batches")
    op.drop_index(op.f("ix_email_messages_user_id"), table_name="email_messages")
    op.drop_index(op.f("ix_email_messages_sender_name"), table_name="email_messages")
    op.drop_index(op.f("ix_email_messages_sender_address"), table_name="email_messages")
    op.drop_table("email_messages")
    op.drop_index(
        op.f("ix_email_message_types_user_id"), table_name="email_message_types"
    )
    op.drop_table("email_message_types")
    op.drop_index(op.f("ix_email_accounts_user_id"), table_name="email_accounts")
    op.drop_index(op.f("ix_email_accounts_mail_address"), table_name="email_accounts")
    op.drop_table("email_accounts")
    # ### end Alembic commands ###
