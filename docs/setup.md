## Setup

You must first set the AWS keys for accessing the account keys: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY. Once you have done this, you can invoke with the following command:

`make run workflow=<workflow id> scenario=<scenario name>`

Scenario ID must match a valid json input scenario from tests/inputs/<workflow_id>/

## Example

`make run workflow=definition_workflow_01PLT6C492IVT09dl7dcdzSgu8NgQBuOu1Z scenario=dont_send_to_snow`

# TODO

1) resolve all TODOs
2) Resolve all NotImplementedErrors