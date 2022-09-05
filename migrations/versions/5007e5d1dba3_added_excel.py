"""added excel

Revision ID: 5007e5d1dba3
Revises: c7e1f7327a42
Create Date: 2022-09-05 09:54:58.164533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5007e5d1dba3'
down_revision = 'c7e1f7327a42'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trains', sa.Column('excel', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trains', 'excel')
    # ### end Alembic commands ###
