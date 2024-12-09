import sqlalchemy as sa


class BaseModel:
    created_at = sa.Column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )
    created_by = sa.Column(sa.String, nullable=False)
    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
    updated_by = sa.Column(sa.String, nullable=False)
    is_deleted = sa.Column(sa.Boolean, nullable=False, default=False)
    deleted_by = sa.Column(sa.String, nullable=True)
    deleted_at = sa.Column(sa.DateTime(timezone=True), nullable=True)
