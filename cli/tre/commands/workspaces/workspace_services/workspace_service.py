import logging
import click
from tre.api_client import ApiClient
from tre.output import output, output_option, query_option

from .contexts import WorkspaceWorkspaceServiceContext, pass_workspace_workspace_service_context


@click.group(name="workspace-service", invoke_without_command=True, help="Perform actions on an workspace-service")
@click.argument('service_id', required=True)
@click.pass_context
def workspace_workspace_service(ctx: click.Context, service_id) -> None:
    ctx.obj = WorkspaceWorkspaceServiceContext.add_service_id_to_context_obj(ctx, service_id)


# TODO - table output
@click.command(name="show", help="Workspace service")
@output_option()
@query_option()
@pass_workspace_workspace_service_context
def workspace_workspace_service_show(workspace_workspace_service_context: WorkspaceWorkspaceServiceContext, output_format, query) -> None:
    log = logging.getLogger(__name__)

    workspace_id = workspace_workspace_service_context.workspace_id
    if workspace_id is None:
        raise click.UsageError('Missing workspace ID')
    service_id = workspace_workspace_service_context.service_id
    if service_id is None:
        raise click.UsageError('Missing service ID')

    client = ApiClient.get_api_client_from_config()
    workspace_scope = client.get_workspace_scope(log, workspace_id)

    response = client.call_api(
        log,
        'GET',
        f'/api/workspaces/{workspace_id}/workspace-services/{service_id}',
        scope_id=workspace_scope,
    )

    output(response.text, output_format=output_format, query=query)


workspace_workspace_service.add_command(workspace_workspace_service_show)


# TODO - operations endpoints
