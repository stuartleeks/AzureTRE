import logging
import click
from tre.commands.operation import operation_show
from tre.output import output_option, query_option

from .contexts import pass_workspace_operation_context, WorkspaceOperationContext


@click.group(name="operation", invoke_without_command=True, help="Perform actions on an operation")
@click.argument('operation_id', required=True)
@click.pass_context
def workspace_operation(ctx: click.Context, operation_id) -> None:
    ctx.obj = WorkspaceOperationContext.add_operation_id_to_context_obj(ctx, operation_id)


@click.command(name="show", help="Workspace operation")
@click.option('--wait-for-completion',
              help="If an operation is in progress, wait for it to complete (when operation_id is specified)",
              flag_value=True,
              default=False)
@output_option()
@query_option()
@pass_workspace_operation_context
def workspace_operation_show(workspace_operation_context: WorkspaceOperationContext, wait_for_completion, output_format, query, suppress_output: bool = False) -> None:
    log = logging.getLogger(__name__)

    workspace_id = workspace_operation_context.workspace_id
    if workspace_id is None:
        raise click.UsageError('Missing workspace ID')
    operation_id = workspace_operation_context.operation_id
    if operation_id is None:
        raise click.UsageError('Missing operation ID')

    operation_url = f'/api/workspaces/{workspace_id}/operations/{operation_id}'
    operation_show(log, operation_url, wait_for_completion, output_format, query, suppress_output)


workspace_operation.add_command(workspace_operation_show)
