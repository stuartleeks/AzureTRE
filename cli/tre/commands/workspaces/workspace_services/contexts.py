import click


class WorkspaceWorkspaceServiceContext(object):
    def __init__(self, workspace_id: str, service_id: str):
        self.workspace_id = workspace_id
        self.service_id = service_id

    @staticmethod
    def add_service_id_to_context_obj(ctx: click.Context, service_id: str) -> "WorkspaceWorkspaceServiceContext":
        workspace_context = ctx.find_object(WorkspaceContext)
        return WorkspaceWorkspaceServiceContext(workspace_context.workspace_id, service_id)


pass_workspace_workspace_service_context = click.make_pass_decorator(WorkspaceWorkspaceServiceContext)
