"""create users table

Revision ID: 1b40d5775cd1
Revises: 
Create Date: 2021-05-26 14:28:35.729792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b40d5775cd1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_full_name"), "user", ["full_name"], unique=False)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)



def downgrade():
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_full_name"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
