import click
import json
import logging

from tre.api_client import ApiClient
from tre.commands.operation import default_operation_table_query, operation_show
from tre.output import output, output_option, query_option


@click.group(help="List/add workspaces")
def workspaces() -> None:
    pass


@click.command(name="list", help="List workspaces")
@output_option()
@query_option()
def workspaces_list(output_format, query):
    log = logging.getLogger(__name__)

    client = ApiClient.get_api_client_from_config()
    response = client.call_api(log, 'GET', '/api/workspaces')
    output(
        response.text,
        output_format=output_format,
        query=query,
        default_table_query=r"workspaces[].{id:id, display_name:properties.display_name, deployment_status:deploymentStatus, workspace_url:workspaceURL}")
    return response.text


@click.command(name="new", help="Create a new workspace")
@click.option('--definition', help='JSON definition for the workspace', required=False)
@click.option('--definition-file', help='File containing JSON definition for the workspace', required=False, type=click.File("r"))
@click.option('--wait-for-completion',
              flag_value=True,
              default=False)
@output_option()
@query_option()
@click.pass_context
def workspaces_create(ctx, definition, definition_file, wait_for_completion, output_format, query):
    log = logging.getLogger(__name__)

    if definition is None:
        if definition_file is None:
            raise click.UsageError('Please specify either a definition or a definition file')
        definition = definition_file.read()

    definition_dict = json.loads(definition)

    client = ApiClient.get_api_client_from_config()
    click.echo("Creating workspace...", err=True)
    response = client.call_api(log, 'POST', '/api/workspaces', json_data=definition_dict)

    if wait_for_completion:
        operation_url = response.headers['location']
        operation_show(log, operation_url, wait_for_completion=True, output_format=output_format, query=query)
    else:
        output(response.text, output_format=output_format, query=query, default_table_query=default_operation_table_query())
        return response.text


workspaces.add_command(workspaces_list)
workspaces.add_command(workspaces_create)
