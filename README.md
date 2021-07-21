# Running

SEE DOCS HERE: TODO

## Setup

You must first set the `SXO_LOCAL_SECRET_KEY` environment variable to the decryption secret key. Once you have done this, you can invoke with the following command:

`make run-workflow workflow=<workflow id> scenario=<scenario name>`

Scenario ID must match a valid json input scenario from tests/inputs/<workflow_id>/

## Example

`make run-workflow workflow=definition_workflow_01PLT6C492IVT09dl7dcdzSgu8NgQBuOu1Z scenario=dont_send_to_snow`

# TODO

1) resolve all TODOs
2) Resolve all NotImplementedErrors
4) Ability to customize workflow/atomic action/account_keys directory