"""Improved file storage

Revision ID: d64a8087c1fc
Revises: 4a07ac822a75
Create Date: 2018-10-26 19:43:33.290000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import delete
import ScoringEngine.core.db.customTypes

# revision identifiers, used by Alembic.
revision = 'd64a8087c1fc'
down_revision = '4a07ac822a75'
branch_labels = None
depends_on = None


def upgrade():

    op.execute(delete('teaminjectsubmissionattachments'))

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attachments',
    sa.Column('id', ScoringEngine.core.db.customTypes.GUID(), autoincrement=False, nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('ignore_virus', sa.Boolean(), nullable=False),
    sa.Column('data', sa.LargeBinary(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attachments_id'), 'attachments', ['id'], unique=True)
    op.add_column(u'teaminjectsubmissionattachments', sa.Column('attachment_id', ScoringEngine.core.db.customTypes.GUID(), nullable=True))
    op.create_foreign_key(None, 'teaminjectsubmissionattachments', 'attachments', ['attachment_id'], ['id'])
    op.drop_column(u'teaminjectsubmissionattachments', 'size')
    op.drop_column(u'teaminjectsubmissionattachments', 'data')
    op.drop_column(u'teaminjectsubmissionattachments', 'filename')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'teaminjectsubmissionattachments', sa.Column('filename', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column(u'teaminjectsubmissionattachments', sa.Column('data', sa.LargeBinary(), autoincrement=False, nullable=False))
    op.add_column(u'teaminjectsubmissionattachments', sa.Column('size', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'teaminjectsubmissionattachments', type_='foreignkey')
    op.drop_column(u'teaminjectsubmissionattachments', 'attachment_id')
    op.drop_index(op.f('ix_attachments_id'), table_name='attachments')
    op.drop_table('attachments')
    # ### end Alembic commands ###
