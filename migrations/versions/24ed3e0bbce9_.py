"""empty message

Revision ID: 24ed3e0bbce9
Revises: 57a658eaccea
Create Date: 2019-08-25 20:24:30.588510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24ed3e0bbce9'
down_revision = '57a658eaccea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Tag')
    op.drop_table('Application')
    op.drop_table('CV')
    op.drop_table('Position')
    op.drop_index('ix_User_email', table_name='User')
    op.drop_table('User')
    op.drop_table('Company')
    op.drop_table('Verify')
    op.drop_table('School')
    op.drop_table('Mapper')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Mapper',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('company_name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('company_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['Company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('School',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('admin', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Verify',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('code', sa.VARCHAR(length=6), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Company',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('uid', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('description', sa.VARCHAR(length=32768), nullable=True),
    sa.Column('logo', sa.VARCHAR(length=256), nullable=True),
    sa.Column('website', sa.VARCHAR(length=256), nullable=True),
    sa.Column('contacts', sa.VARCHAR(length=32768), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('User',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.Column('cv_id', sa.INTEGER(), nullable=True),
    sa.Column('verification_id', sa.INTEGER(), nullable=True),
    sa.Column('company_id', sa.INTEGER(), nullable=True),
    sa.Column('school_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['Company.id'], ),
    sa.ForeignKeyConstraint(['cv_id'], ['CV.id'], ),
    sa.ForeignKeyConstraint(['school_id'], ['School.id'], ),
    sa.ForeignKeyConstraint(['verification_id'], ['Verify.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_User_email', 'User', ['email'], unique=1)
    op.create_table('Position',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('company_id', sa.INTEGER(), nullable=True),
    sa.Column('description', sa.VARCHAR(length=32768), nullable=True),
    sa.Column('location', sa.VARCHAR(length=32768), nullable=True),
    sa.Column('date', sa.VARCHAR(length=32768), nullable=True),
    sa.Column('available', sa.BOOLEAN(), nullable=True),
    sa.Column('duration', sa.INTEGER(), nullable=True),
    sa.Column('email', sa.VARCHAR(length=128), nullable=True),
    sa.Column('hours_per_day', sa.VARCHAR(length=128), nullable=True),
    sa.Column('age_required', sa.VARCHAR(length=128), nullable=True),
    sa.Column('tag_id', sa.INTEGER(), nullable=True),
    sa.Column('views', sa.INTEGER(), nullable=True),
    sa.CheckConstraint('available IN (0, 1)'),
    sa.ForeignKeyConstraint(['company_id'], ['Company.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['Tag.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('CV',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('photo', sa.VARCHAR(length=256), nullable=True),
    sa.Column('name', sa.VARCHAR(length=256), nullable=True),
    sa.Column('email', sa.VARCHAR(length=256), nullable=True),
    sa.Column('telephone', sa.VARCHAR(length=16), nullable=True),
    sa.Column('birthday', sa.VARCHAR(length=256), nullable=True),
    sa.Column('location', sa.VARCHAR(length=256), nullable=True),
    sa.Column('about', sa.VARCHAR(length=512), nullable=True),
    sa.Column('education', sa.VARCHAR(length=2048), nullable=True),
    sa.Column('projects', sa.VARCHAR(length=2048), nullable=True),
    sa.Column('skills', sa.VARCHAR(length=512), nullable=True),
    sa.Column('languages', sa.VARCHAR(length=512), nullable=True),
    sa.Column('hobbies', sa.VARCHAR(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Application',
    sa.Column('id', sa.VARCHAR(length=2048), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('position_id', sa.INTEGER(), nullable=False),
    sa.Column('company_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['position_id'], ['Position.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'position_id', 'company_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('Tag',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###