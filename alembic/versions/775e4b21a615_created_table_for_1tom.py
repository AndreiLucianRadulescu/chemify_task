"""Created table for 1tom

Revision ID: 775e4b21a615
Revises: 787ff5b56ab1
Create Date: 2023-11-19 03:50:33.878021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "775e4b21a615"
down_revision = "787ff5b56ab1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_task_table",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["task.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "task_id"),
    )
    op.drop_constraint("task_user_id_fkey", "task", type_="foreignkey")
    op.drop_column("task", "user_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "task", sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False)
    )
    op.create_foreign_key("task_user_id_fkey", "task", "user", ["user_id"], ["id"])
    op.drop_table("user_task_table")
    # ### end Alembic commands ###
