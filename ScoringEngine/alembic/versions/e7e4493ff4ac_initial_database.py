"""Initial Database

Revision ID: e7e4493ff4ac
Revises: 
Create Date: 2018-09-25 22:48:32.812000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7e4493ff4ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('current', sa.Boolean(), nullable=True),
    sa.Column('start', sa.DateTime(), nullable=True),
    sa.Column('end', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_current'), 'events', ['current'], unique=False)
    op.create_index(op.f('ix_events_end'), 'events', ['end'], unique=False)
    op.create_index(op.f('ix_events_id'), 'events', ['id'], unique=True)
    op.create_index(op.f('ix_events_start'), 'events', ['start'], unique=False)
    op.create_table('injectcategories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('parentid', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_injectcategories_id'), 'injectcategories', ['id'], unique=True)
    op.create_index(op.f('ix_injectcategories_parentid'), 'injectcategories', ['parentid'], unique=False)
    op.create_table('log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('severity', sa.Integer(), nullable=False),
    sa.Column('module', sa.String(length=60), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_log_id'), 'log', ['id'], unique=True)
    op.create_table('passdb',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.Column('domain', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_passdb_id'), 'passdb', ['id'], unique=True)
    op.create_index(op.f('ix_passdb_name'), 'passdb', ['name'], unique=True)
    op.create_table('servers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('ip_3', sa.String(length=3), nullable=True),
    sa.Column('ip_4', sa.String(length=3), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_servers_id'), 'servers', ['id'], unique=True)
    op.create_table('servicetypes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.Column('tester', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_servicetypes_id'), 'servicetypes', ['id'], unique=True)
    op.create_table('teams',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.Column('network', sa.String(length=15), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teams_id'), 'teams', ['id'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=45), nullable=True),
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('team', sa.Integer(), nullable=False),
    sa.Column('group', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('injects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('categoryid', sa.Integer(), nullable=True),
    sa.Column('subject', sa.String(length=255), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['categoryid'], ['injectcategories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_injects_id'), 'injects', ['id'], unique=True)
    op.create_table('passdbentry',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('passdbid', sa.Integer(), nullable=True),
    sa.Column('user', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['passdbid'], ['passdb.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_passdbentry_id'), 'passdbentry', ['id'], unique=True)
    op.create_index(op.f('ix_passdbentry_passdbid'), 'passdbentry', ['passdbid'], unique=False)
    op.create_table('services',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('serverid', sa.Integer(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.Column('typeid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['serverid'], ['servers.id'], ),
    sa.ForeignKeyConstraint(['typeid'], ['servicetypes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_services_id'), 'services', ['id'], unique=True)
    op.create_table('teamservers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('teamid', sa.Integer(), nullable=True),
    sa.Column('serverid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['serverid'], ['servers.id'], ),
    sa.ForeignKeyConstraint(['teamid'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teamservers_id'), 'teamservers', ['id'], unique=True)
    op.create_table('assignedinjects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('eventid', sa.Integer(), nullable=True),
    sa.Column('injectid', sa.Integer(), nullable=True),
    sa.Column('subject', sa.String(length=255), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('when', sa.DateTime(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('allowlate', sa.Boolean(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['eventid'], ['events.id'], ),
    sa.ForeignKeyConstraint(['injectid'], ['injects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assignedinjects_id'), 'assignedinjects', ['id'], unique=True)
    op.create_table('incedentresponses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('eventid', sa.Integer(), nullable=True),
    sa.Column('teamserverid', sa.Integer(), nullable=True),
    sa.Column('addedby', sa.Integer(), nullable=True),
    sa.Column('added', sa.DateTime(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('comments', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['addedby'], ['users.id'], ),
    sa.ForeignKeyConstraint(['eventid'], ['events.id'], ),
    sa.ForeignKeyConstraint(['teamserverid'], ['teamservers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_incedentresponses_eventid'), 'incedentresponses', ['eventid'], unique=False)
    op.create_index(op.f('ix_incedentresponses_id'), 'incedentresponses', ['id'], unique=True)
    op.create_index(op.f('ix_incedentresponses_teamserverid'), 'incedentresponses', ['teamserverid'], unique=False)
    op.create_table('scoreevents',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('eventid', sa.Integer(), nullable=True),
    sa.Column('teamserverid', sa.Integer(), nullable=True),
    sa.Column('serviceid', sa.Integer(), nullable=True),
    sa.Column('scoretime', sa.DateTime(), nullable=False),
    sa.Column('up', sa.Boolean(), nullable=False),
    sa.Column('info', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['eventid'], ['events.id'], ),
    sa.ForeignKeyConstraint(['serviceid'], ['services.id'], ),
    sa.ForeignKeyConstraint(['teamserverid'], ['teamservers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scoreevents_eventid'), 'scoreevents', ['eventid'], unique=False)
    op.create_index(op.f('ix_scoreevents_id'), 'scoreevents', ['id'], unique=True)
    op.create_index(op.f('ix_scoreevents_scoretime'), 'scoreevents', ['scoretime'], unique=False)
    op.create_index(op.f('ix_scoreevents_serviceid'), 'scoreevents', ['serviceid'], unique=False)
    op.create_index(op.f('ix_scoreevents_teamserverid'), 'scoreevents', ['teamserverid'], unique=False)
    op.create_table('serviceargs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('serverid', sa.Integer(), nullable=True),
    sa.Column('serviceid', sa.Integer(), nullable=True),
    sa.Column('key', sa.String(length=50), nullable=False),
    sa.Column('value', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['serverid'], ['teamservers.id'], ),
    sa.ForeignKeyConstraint(['serviceid'], ['services.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_serviceargs_id'), 'serviceargs', ['id'], unique=True)
    op.create_table('incedentresponseattachments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('irid', sa.Integer(), nullable=True),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('data', sa.LargeBinary(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('added_by', sa.Integer(), nullable=True),
    sa.Column('added', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['added_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['irid'], ['incedentresponses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_incedentresponseattachments_id'), 'incedentresponseattachments', ['id'], unique=True)
    op.create_table('teaminjectsubmissions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('assignedinjectid', sa.Integer(), nullable=True),
    sa.Column('teamid', sa.Integer(), nullable=True),
    sa.Column('when', sa.DateTime(), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['assignedinjectid'], ['assignedinjects.id'], ),
    sa.ForeignKeyConstraint(['teamid'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teaminjectsubmissions_id'), 'teaminjectsubmissions', ['id'], unique=True)
    op.create_table('teaminjectsubmissionattachments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('teaminjectid', sa.Integer(), nullable=True),
    sa.Column('filename', sa.String(length=255), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['teaminjectid'], ['teaminjectsubmissions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teaminjectsubmissionattachments_id'), 'teaminjectsubmissionattachments', ['id'], unique=True)
    op.create_table('teaminjectsubmissionnotes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('teaminjectid', sa.Integer(), nullable=True),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['teaminjectid'], ['teaminjectsubmissions.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teaminjectsubmissionnotes_id'), 'teaminjectsubmissionnotes', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_teaminjectsubmissionnotes_id'), table_name='teaminjectsubmissionnotes')
    op.drop_table('teaminjectsubmissionnotes')
    op.drop_index(op.f('ix_teaminjectsubmissionattachments_id'), table_name='teaminjectsubmissionattachments')
    op.drop_table('teaminjectsubmissionattachments')
    op.drop_index(op.f('ix_teaminjectsubmissions_id'), table_name='teaminjectsubmissions')
    op.drop_table('teaminjectsubmissions')
    op.drop_index(op.f('ix_incedentresponseattachments_id'), table_name='incedentresponseattachments')
    op.drop_table('incedentresponseattachments')
    op.drop_index(op.f('ix_serviceargs_id'), table_name='serviceargs')
    op.drop_table('serviceargs')
    op.drop_index(op.f('ix_scoreevents_teamserverid'), table_name='scoreevents')
    op.drop_index(op.f('ix_scoreevents_serviceid'), table_name='scoreevents')
    op.drop_index(op.f('ix_scoreevents_scoretime'), table_name='scoreevents')
    op.drop_index(op.f('ix_scoreevents_id'), table_name='scoreevents')
    op.drop_index(op.f('ix_scoreevents_eventid'), table_name='scoreevents')
    op.drop_table('scoreevents')
    op.drop_index(op.f('ix_incedentresponses_teamserverid'), table_name='incedentresponses')
    op.drop_index(op.f('ix_incedentresponses_id'), table_name='incedentresponses')
    op.drop_index(op.f('ix_incedentresponses_eventid'), table_name='incedentresponses')
    op.drop_table('incedentresponses')
    op.drop_index(op.f('ix_assignedinjects_id'), table_name='assignedinjects')
    op.drop_table('assignedinjects')
    op.drop_index(op.f('ix_teamservers_id'), table_name='teamservers')
    op.drop_table('teamservers')
    op.drop_index(op.f('ix_services_id'), table_name='services')
    op.drop_table('services')
    op.drop_index(op.f('ix_passdbentry_passdbid'), table_name='passdbentry')
    op.drop_index(op.f('ix_passdbentry_id'), table_name='passdbentry')
    op.drop_table('passdbentry')
    op.drop_index(op.f('ix_injects_id'), table_name='injects')
    op.drop_table('injects')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_teams_id'), table_name='teams')
    op.drop_table('teams')
    op.drop_index(op.f('ix_servicetypes_id'), table_name='servicetypes')
    op.drop_table('servicetypes')
    op.drop_index(op.f('ix_servers_id'), table_name='servers')
    op.drop_table('servers')
    op.drop_index(op.f('ix_passdb_name'), table_name='passdb')
    op.drop_index(op.f('ix_passdb_id'), table_name='passdb')
    op.drop_table('passdb')
    op.drop_index(op.f('ix_log_id'), table_name='log')
    op.drop_table('log')
    op.drop_index(op.f('ix_injectcategories_parentid'), table_name='injectcategories')
    op.drop_index(op.f('ix_injectcategories_id'), table_name='injectcategories')
    op.drop_table('injectcategories')
    op.drop_index(op.f('ix_events_start'), table_name='events')
    op.drop_index(op.f('ix_events_id'), table_name='events')
    op.drop_index(op.f('ix_events_end'), table_name='events')
    op.drop_index(op.f('ix_events_current'), table_name='events')
    op.drop_table('events')
    # ### end Alembic commands ###
