from flask import Blueprint, current_app
from flask.cli import AppGroup
from sqlalchemy.exc import IntegrityError
import click

from uffd.role.models import Role
from uffd.database import db

from .models import User

bp = Blueprint('user_cli', __name__)
user_cli = AppGroup('user', help='Manage users')

@bp.record
def add_cli_commands(state):
	state.app.cli.add_command(user_cli)

# pylint: disable=too-many-arguments

def update_attrs(user, mail=None, displayname=None, password=None,
                 prompt_password=False, clear_roles=False,
                 add_role=tuple(), remove_role=tuple()):
	if password is None and prompt_password:
		password = click.prompt('Password', hide_input=True, confirmation_prompt='Confirm password')
	if mail is not None and not user.set_mail(mail):
		raise click.ClickException('Invalid mail address')
	if displayname is not None and not user.set_displayname(displayname):
		raise click.ClickException('Invalid displayname')
	if password is not None and not user.set_password(password):
		raise click.ClickException('Invalid password')
	if clear_roles:
		user.roles.clear()
	for role_name in add_role:
		role = Role.query.filter_by(name=role_name).one_or_none()
		if role is None:
			raise click.ClickException(f'Role {role_name} not found')
		role.members.append(user)
	for role_name in remove_role:
		role = Role.query.filter_by(name=role_name).one_or_none()
		if role is None:
			raise click.ClickException(f'Role {role_name} not found')
		role.members.remove(user)
	user.update_groups()

@user_cli.command(help='List login names of all users')
def list():
	with current_app.test_request_context():
		for user in User.query:
			click.echo(user.loginname)

@user_cli.command(help='Show details of user')
@click.argument('loginname')
def show(loginname):
	with current_app.test_request_context():
		user = User.query.filter_by(loginname=loginname).one_or_none()
		if user is None:
			raise click.ClickException(f'User {loginname} not found')
		click.echo(f'Loginname: {user.loginname}')
		click.echo(f'Displayname: {user.displayname}')
		click.echo(f'Mail: {user.mail}')
		click.echo(f'Service User: {user.is_service_user}')
		click.echo(f'Roles: {", ".join([role.name for role in user.roles])}')
		click.echo(f'Groups: {", ".join([group.name for group in user.groups])}')

@user_cli.command(help='Create new user')
@click.argument('loginname')
@click.option('--mail', required=True, metavar='EMAIL_ADDRESS', help='E-Mail address')
@click.option('--displayname', help='Set display name. Defaults to login name.')
@click.option('--service/--no-service', default=False, help='Create service or regular (default) user. '+\
                                                            'Regular users automatically have roles marked as default. '+\
                                                            'Service users do not.')
@click.option('--password', help='Password for SSO login. Login disabled if unset.')
@click.option('--prompt-password', is_flag=True, flag_value=True, default=False, help='Read password interactively from terminal.')
@click.option('--add-role', multiple=True, help='Add role to user. Repeat to add multiple roles.', metavar='ROLE_NAME')
def create(loginname, mail, displayname, service, password, prompt_password, add_role):
	with current_app.test_request_context():
		if displayname is None:
			displayname = loginname
		user = User(is_service_user=service)
		if not user.set_loginname(loginname, ignore_blocklist=True):
			raise click.ClickException('Invalid loginname')
		try:
			db.session.add(user)
			update_attrs(user, mail, displayname, password, prompt_password, add_role=add_role)
			db.session.commit()
		except IntegrityError as ex:
			raise click.ClickException(f'User creation failed: {ex}')

@user_cli.command(help='Update user attributes and roles')
@click.argument('loginname')
@click.option('--mail', metavar='EMAIL_ADDRESS', help='Set e-mail address.')
@click.option('--displayname', help='Set display name.')
@click.option('--password', help='Set password for SSO login.')
@click.option('--prompt-password', is_flag=True, flag_value=True, default=False, help='Set password by reading it interactivly from terminal.')
@click.option('--clear-roles', is_flag=True, flag_value=True, default=False, help='Remove all roles from user. Executed before --add-role.')
@click.option('--add-role', multiple=True, help='Add role to user. Repeat to add multiple roles.')
@click.option('--remove-role', multiple=True, help='Remove role from user. Repeat to remove multiple roles.')
def update(loginname, mail, displayname, password, prompt_password, clear_roles, add_role, remove_role):
	with current_app.test_request_context():
		user = User.query.filter_by(loginname=loginname).one_or_none()
		if user is None:
			raise click.ClickException(f'User {loginname} not found')
		update_attrs(user, mail, displayname, password, prompt_password, clear_roles, add_role, remove_role)
		db.session.commit()

@user_cli.command(help='Delete user')
@click.argument('loginname')
def delete(loginname):
	with current_app.test_request_context():
		user = User.query.filter_by(loginname=loginname).one_or_none()
		if user is None:
			raise click.ClickException(f'User {loginname} not found')
		db.session.delete(user)
		db.session.commit()
