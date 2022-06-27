import click

from tre.commands.login import login
from tre.commands.api_call import call_api
from tre.commands.workspaces.workspace import workspace
from tre.commands.workspaces.workspaces import workspaces
from tre.commands.shared_services.shared_service import shared_service
from tre.commands.shared_services.shared_services import shared_services


@click.group()
def cli():
    pass


cli.add_command(login)
cli.add_command(call_api)
cli.add_command(workspaces)
cli.add_command(workspace)
cli.add_command(shared_services)
cli.add_command(shared_service)

# TODO - costs endpoints
# TODO - workspace service endpoints
# TODO - shared service templates
# TODO - migrations?

# TODO - allow output format from env var

if __name__ == "__main__":
    cli()
