# TRE CLI

**WARNING - this CLI is currently experimental**

## Installation

Currently, installation has only been tested within the dev container. In this context, `make install-cli` should work

## Shell completion

The `tre` cli supports shell completion. To enable, run `source <(_TRE_COMPLETE=bash_source tre)` (or add to your profile).

Other shells are supported, see [the click docs](https://click.palletsprojects.com/en/8.1.x/shell-completion/#enabling-completion).

## Login

The CLI allows you to log in using either a device code flow or client credentials flow.

### Device code flow (interactive)

To log in using device code flow, run:

```bash
tre login device-code \
  --base-url https://mytre.westeurope.cloudapp.azure.com/ \
  --client-id <API_CLIENT_ID> \
  --aad-tenant-id <AAD_TENANT_ID> \
  --api-scope <ROOT_API_SCOPE>
```

This will prompt you to copy a device code and nagivate to <https://microsoft.com/devicelogin> to complete the login flow interactively.

You can specify `--no-verify` to disable SSL cert verification.

NOTE: the api scope is usually of the form  `api://<API_CLIENT_ID>/user_impersonation`

NOTE 2: When using device code flow, you need to ensure that the app registrations for the root API and any workspaces you access have device code flow enabled. (Automating this is tracked in [#2709](https://github.com/microsoft/AzureTRE/issues/2709) )

#### Workspace authentication

Since the api scope for each workspace is different, the token returned when authenticating against the root API isn't valid against a workspace.
When running interactively, the CLI will prompt you when it needs to reauthenticate for a workspace API.

You can pre-emptively get an authentication token for a workspace using the `--workspace` option. This can be specified multiple times to authenticate against multiple workspaces at once. You can also using `--all-workspaces` to get a token for all workspaces in one command.

### Client credentials (service)

To log in using client credentials flow (for a service principal), run:

```bash
tre login client-credentials \
  --base-url https://mytre.westeurope.cloudapp.azure.com/ \
  --client-id <SERVICE_PRINICPAL_CLIENT_ID> \
  --client-secret <SERVICE_PRINCIPAL_CLIENT_SECRET> \
  --aad-tenant-id <AAD_TENANT_ID> \
  --api-scope <ROOT_API_SCOPE>
```

You can specify `--no-verify` to disable SSL cert verification.

NOTE: the api scope is usually of the form  `api://<API_CLIENT_ID>/user_impersonation`


### Login misc

A number of the parameters on login could be removed by adding a `/.metadata` endpoint or similar to the API that returns the tenant id, api-scope and client id. This would likely also be useful for the UI.

## General command structure

The general command structure for the CLI is:

```bash
tre plural_noun cmd
# or 
tre singular_noun id cmd
```

For example:

```bash
# list workspaces
tre workspaces list

## show an individual workspace
tre workspace 567f17d6-1abb-450f-991a-19398f89b3c2 show
```

This pattern is nested for sub-resources, e.g. operations for a workspace:

```bash

## list operations for a workspace
tre workspace 567f17d6-1abb-450f-991a-19398f89b3c2 operations list

## show an individual operation for a workspace
tre workspace 567f17d6-1abb-450f-991a-19398f89b3c2 operation 0f66839f-8727-43db-b2d6-6c7197712e36 show
```

### Alternative structures considered

Initially, the command structure was more similar to the `az` CLI:

```bash
## NOTE this is an alternate syntax for illustration (i.e. not how the CLI works)
# list workspaces
tre workspace list

## show an individual workspace
tre workspace show --workspace-id 567f17d6-1abb-450f-991a-19398f89b3c2
```

The consistency of command grouping in this structure is nice.

However, as nested commands are added it requires editing multiple locations in the command text. So the flow when drilling down into an operation is:


```bash
## NOTE this is an alternate syntax for illustration (i.e. not how the CLI works)
# Find the workspace
tre workspace list

# Show operations for the workspace
tre workspace operation list --workspace-id 567f17d6-1abb-450f-991a-19398f89b3c2

# Show the operation
tre workspace operation show --workspace-id 567f17d6-1abb-450f-991a-19398f89b3c2 --operation-id 0f66839f-8727-43db-b2d6-6c7197712e36
```

This compares to: the current structure where the changes between successive commands are all at the end of the command text:

```bash
tre workspaces list
tre workspace 567f17d6-1abb-450f-991a-19398f89b3c2 operations list
tre workspace 567f17d6-1abb-450f-991a-19398f89b3c2 operation 0f66839f-8727-43db-b2d6-6c7197712e36 show
```

## Asynchronous operations

Many operations in TRE are asynchronous, and the corresponding API endpoints return a `202 Accepted` response with a `Location` header pointing to an operation endpoint.

The commands corresponding to these asynchronous operations will poll this resulting operation and wait until it has completed. If you don't want this behaviour, you can pass the `--no-wait` option.

## Command output

### Output formats

Most commands support formatting output as `json` (default), `table`, or `none` via the `--output` option. This can also be controlled using the `TRECLI_OUTPUT` environment variable, i.e. set `TRECLI_OUTPUT` to `table` to default to the table output format.

### Querying output

Most commands support [JMESPath](https://jmespath.org/) queries for the output via the `--query` option.

For example, to get a list of workspace IDs run `tre workspaces list --query workspaces[].id`.

This can be combined with `--output table`, e.g. `tre workspaces list -o table --query "workspaces[].{id:id, name: properties.display_name}"`. Note that the query result must be an object with named properties (or an array of such objects)

### Capturing results

Some of the commands in the CLI output progress information (e.g. `tre workspace new ...`).

When the CLI outputs progress information, it outputs it to stderr. The final result of the command is output to stdout.

This gives a good experience when chaining commands together, e.g.:

```bash
# Set the workspace to use
WORKSPACE_ID=567f17d6-1abb-450f-991a-19398f89b3c2
# Get the workspace etag
ETAG=$(tre workspace $WORKSPACE_ID show --query workspace._etag --output json)
# Disable the workspace (this is an asynchronous operation)
OPERATION=$(tre workspace $WORKSPACE_ID set-enabled --etag $ETAG --enable --output json)
# ^ this last command will output progress information while waiting for the operation to complete.
# And OPERATION contains the JSON describing the completed operation
# allowing you to query the status property etc
echo $OPERATION
```

## Passing definitions

When creating new resources (e.g. workspaces), you need to pass in a definition. This can be passed in various ways: as an inline value, from a file, or from stdin.


To pass a definition inline, use the `--definition` option and include the JSON content, e.g. `tre workspace new --definition '{"templateName":...}'`

To load a definition from a file, use the `--definition-file` option, e.g. `tre workspace new --definition-file my-worspace.json`

To pass a definition via stdin, use `--definition-file -` (note the `-` to signal reading from stdin).

Reading from stdin allows you to take some interesting approaches to specifying the definition.

For example, you can use HEREDOC syntax to describe the JSON payload over multiple lines:

```bash
cat << EOF | tre workspaces new --definition-file -
{
  "templateName": "my-workspace",
  "properties": {
    "display_name": $DISPLAY_NAME,
    ...
  }
}
EOF
```

Or you can load the content from a file that contains embedded environment variables and use `envsubst` to substitute them:

`cat my-workspace.json | envsubst | tre workspace new --definition file -`

## Overriding the API URL

When you run `tre login` you specify the base URL for the API, but when you are developing AzureTRE you may want to make calls against the locally running API.

To support this, you can set the `TRECLI_BASE_URL` environment variable and that will override the API endpoint used by the CLI.
