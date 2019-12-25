"""empty message

Revision ID: 9fde25628739
Revises: 7a2aa3fd8ab1
Create Date: 2019-12-23 14:54:46.575820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fde25628739'
down_revision = '7a2aa3fd8ab1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('evals',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('year', sa.INTEGER(), nullable=True),
    sa.Column('quarter', sa.CHAR(length=6), nullable=True),
    sa.Column('course_id', sa.INTEGER(), nullable=True),
    sa.Column('instructor_name', sa.VARCHAR(), nullable=True),
    sa.Column('subject', sa.CHAR(length=4), nullable=True),
    sa.Column('subject_number', sa.CHAR(length=5), nullable=True),
    sa.Column('response_rate', sa.FLOAT(), nullable=True),
    sa.Column('num_enrolled', sa.INTEGER(), nullable=True),
    sa.Column('num_responses', sa.INTEGER(), nullable=True),
    sa.Column('class_name', sa.VARCHAR(), nullable=True),
    sa.Column('overall_avg', sa.FLOAT(), nullable=True),
    sa.Column('overall_std_dev', sa.FLOAT(), nullable=True),
    sa.Column('difficulty_avg', sa.FLOAT(), nullable=True),
    sa.Column('difficulty_med', sa.FLOAT(), nullable=True),
    sa.Column('difficulty_std_dev', sa.FLOAT(), nullable=True),
    sa.Column('avg_weekly_workload', sa.FLOAT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('evals')
    # ### end Alembic commands ###