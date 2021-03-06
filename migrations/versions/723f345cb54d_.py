"""empty message

Revision ID: 723f345cb54d
Revises: 
Create Date: 2019-06-19 16:40:01.362549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '723f345cb54d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Application',
    sa.Column('id', sa.String(length=2048), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('position_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['position_id'], ['Position.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'position_id', 'company_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('CV',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('photo', sa.String(length=256), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('telephone', sa.String(length=16), nullable=True),
    sa.Column('birthday', sa.String(length=256), nullable=True),
    sa.Column('location', sa.String(length=256), nullable=True),
    sa.Column('about', sa.String(length=512), nullable=True),
    sa.Column('education', sa.String(length=2048), nullable=True),
    sa.Column('projects', sa.String(length=2048), nullable=True),
    sa.Column('skills', sa.String(length=512), nullable=True),
    sa.Column('languages', sa.String(length=512), nullable=True),
    sa.Column('hobbies', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=32768), nullable=True),
    sa.Column('logo', sa.String(length=256), nullable=True),
    sa.Column('website', sa.String(length=256), nullable=True),
    sa.Column('contacts', sa.String(length=32768), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('School',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Mapper',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=128), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['Company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Position',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=32768), nullable=True),
    sa.Column('location', sa.String(length=32768), nullable=True),
    sa.Column('date', sa.String(length=32768), nullable=True),
    sa.Column('available', sa.Boolean(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('hours_per_day', sa.String(length=128), nullable=True),
    sa.Column('age_required', sa.String(length=128), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('views', sa.Integer(), default=0),
    sa.ForeignKeyConstraint(['company_id'], ['Company.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['Tag.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('cv_id', sa.Integer(), nullable=True),
    sa.Column('verification_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['Company.id'], ),
    sa.ForeignKeyConstraint(['school_id'], ['School.id'], ),
    sa.ForeignKeyConstraint(['cv_id'], ['CV.id'], ),
    sa.ForeignKeyConstraint(['verification_id'], ['Verify.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_User_email'), 'User', ['email'], unique=True)
    op.create_table('Verify',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('code', sa.String(length=6), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Verify')
    op.drop_index(op.f('ix_User_email'), table_name='User')
    op.drop_table('User')
    op.drop_table('Tag')
    op.drop_table('Position')
    op.drop_table('Mapper')
    op.drop_table('Company')
    op.drop_table('CV')
    op.drop_table('Application')
    # ### end Alembic commands ###
