"""combination fix

Revision ID: 3ef13975399f
Revises: 
Create Date: 2018-06-21 19:29:13.450399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ef13975399f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('race_com_fis_points',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('race_competitor_id', sa.Integer(), nullable=True),
    sa.Column('discipline_id', sa.Integer(), nullable=True),
    sa.Column('fispoint', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['discipline_id'], ['discipline.id'], ),
    sa.ForeignKeyConstraint(['race_competitor_id'], ['race_competitor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('discipline', sa.Column('is_combination', sa.Boolean(), nullable=True))
    op.add_column('run_info', sa.Column('discipline_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'run_info', 'discipline', ['discipline_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'run_info', type_='foreignkey')
    op.drop_column('run_info', 'discipline_id')
    op.drop_column('discipline', 'is_combination')
    op.drop_table('race_com_fis_points')
    # ### end Alembic commands ###
