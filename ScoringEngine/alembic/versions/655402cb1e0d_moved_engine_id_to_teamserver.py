"""Moved engine_id to TeamServer

Revision ID: 655402cb1e0d
Revises: 85921a98562e
Create Date: 2019-02-26 21:50:12.689000

"""
from alembic import op
import sqlalchemy as sa
import ScoringEngine.core.db.customTypes

from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# revision identifiers, used by Alembic.
revision = '655402cb1e0d'
down_revision = '85921a98562e'
branch_labels = None
depends_on = None


class TeamServer(Base):
    __tablename__ = 'teamservers'

    id = sa.Column(sa.Integer, primary_key=True)
    engine_id = sa.Column(sa.Integer, sa.ForeignKey("engines.id"))


class Engine(Base):
    __tablename__ = 'engines'

    id = sa.Column(sa.Integer, primary_key=True)


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    # ### commands auto generated by Alembic - please adjust! ###
    if 'sqlite' not in op.get_context().connection.engine.url.drivername:
        op.drop_constraint(u'servers_engine_id_fkey', 'servers', type_='foreignkey')
        op.drop_column('servers', 'engine_id')
    op.add_column('teamservers', sa.Column('engine_id', sa.Integer(), nullable=True))
    if 'sqlite' not in op.get_context().connection.engine.url.drivername:
        op.create_foreign_key(None, 'teamservers', 'engines', ['engine_id'], ['id'])
    # ### end Alembic commands ###

    for server in session.query(TeamServer):
        server.engine_id = 0

    session.commit()

    if 'sqlite' not in op.get_context().connection.engine.url.drivername:
        op.alter_column('teamservers', 'engine_id', nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'teamservers', type_='foreignkey')
    op.drop_column('teamservers', 'engine_id')
    op.add_column('servers', sa.Column('engine_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'servers_engine_id_fkey', 'servers', 'engines', ['engine_id'], ['id'])
    # ### end Alembic commands ###