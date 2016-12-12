"""empty message

Revision ID: 55d4fe1d571d
Revises: 
Create Date: 2016-12-11 10:41:22.635845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55d4fe1d571d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ideas', sa.Column('createdDate', sa.DateTime(timezone=True), nullable=True))
    op.add_column('ideas', sa.Column('isActive', sa.Boolean(), nullable=True))
    op.add_column('ideas', sa.Column('updatedDate', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ideas', 'updatedDate')
    op.drop_column('ideas', 'isActive')
    op.drop_column('ideas', 'createdDate')
    # ### end Alembic commands ###