"""first

Revision ID: d9eefdd54c6a
Revises: 
Create Date: 2022-09-23 17:52:14.886793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9eefdd54c6a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('excel_file', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('smgs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('railway_code', sa.String(), nullable=True),
    sa.Column('sender', sa.String(), nullable=True),
    sa.Column('departure_station', sa.String(), nullable=True),
    sa.Column('sender_statement', sa.String(), nullable=True),
    sa.Column('recipient', sa.String(), nullable=True),
    sa.Column('destination_station', sa.String(), nullable=True),
    sa.Column('border_crossing_stations', sa.String(), nullable=True),
    sa.Column('railway_carriage', sa.String(), nullable=True),
    sa.Column('shipping_name', sa.String(), nullable=True),
    sa.Column('container_owner', sa.String(), nullable=True),
    sa.Column('container', sa.String(), nullable=True),
    sa.Column('container_type', sa.String(), nullable=True),
    sa.Column('container_type_code', sa.String(), nullable=True),
    sa.Column('type_of_packaging', sa.String(), nullable=True),
    sa.Column('number_of_seats', sa.String(), nullable=True),
    sa.Column('net', sa.String(), nullable=True),
    sa.Column('tara', sa.String(), nullable=True),
    sa.Column('gross', sa.String(), nullable=True),
    sa.Column('seals', sa.String(), nullable=True),
    sa.Column('seal_quantity', sa.String(), nullable=True),
    sa.Column('submerged', sa.String(), nullable=True),
    sa.Column('method_of_determining_mass', sa.String(), nullable=True),
    sa.Column('payment_of_legal_fees', sa.String(), nullable=True),
    sa.Column('carriers', sa.String(), nullable=True),
    sa.Column('documents_by_sender', sa.String(), nullable=True),
    sa.Column('additional_information', sa.String(), nullable=True),
    sa.Column('custom_seal', sa.String(), nullable=True),
    sa.Column('inspector_name', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('file_draft', sa.String(), nullable=True),
    sa.Column('file_original', sa.String(), nullable=True),
    sa.Column('train_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['train_id'], ['trains.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('smgs')
    op.drop_table('trains')
    # ### end Alembic commands ###