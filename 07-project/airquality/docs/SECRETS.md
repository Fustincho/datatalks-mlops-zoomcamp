
# AWS Secrets Manager CLI: basics

## Introduction

In this tutorial, we will cover how to create secrets, retrieve them, update values, and delete secrets using the AWS CLI. This document serves to help you understand how secrets are retrieved and updated during the CI/CD workflows.

## Prerequisites

- AWS CLI installed and configured with appropriate permissions.
- Basic knowledge of the command line interface.

## Creating a Secret

Let's begin by creating a simple secret with this key-value pair: `my_awesome_key = my_awesome_value`. To create a secret in AWS Secrets Manager, use the following command:

```bash
aws secretsmanager create-secret --name my_awesome_secret --secret-string '{"my_awesome_key":"my_awesome_value"}'
```

- `--secret-string '{"my_awesome_key":"my_awesome_value"}'`: This is the secret data in JSON format.

## Retrieving a Secret

To retrieve the value of your secret, use the following command:

```bash
aws secretsmanager get-secret-value --secret-id my_awesome_secret
```

### Sample Output:

```json
{
    "ARN": "arn:aws:secretsmanager:us-east-1:<YOUR_AWS_ACCOUNT_ID>:secret:my_awesome_secret-TF5XZr",
    "Name": "my_awesome_secret",
    "VersionId": "2a52eaf0-7c28-4b9c-a015-a7bfe260fb6c",
    "SecretString": "{\"my_awesome_key\": \"my_awesome_value\"}",
    "VersionStages": [
        "AWSCURRENT"
    ],
    "CreatedDate": "2024-08-23T10:15:06.257000-05:00"
}
```

### Retrieve Just the Secret String

If you want to retrieve just the secret string, use the `--query` parameter:

```bash
aws secretsmanager get-secret-value --secret-id my_awesome_secret --query SecretString
```

```bash
# Output
"{\"my_awesome_key\":\"my_awesome_value\"}"
```

You can also retrieve the secret string as plain text:

```bash
aws secretsmanager get-secret-value --secret-id my_awesome_secret --query SecretString --output text
```

```bash
# Output
{"my_awesome_key":"my_awesome_value"}
```

## Updating a Secret

To update the value of an existing secret, use `put-secret-value`. The new JSON will replace the key-value pairs that you previously had, so if you want to preserve some of the keys you need to re-include them in your statement:

```bash
aws secretsmanager put-secret-value --secret-id my_awesome_secret --secret-string '{"one": "eins", "two": "zwei", "three": "drei", "four": "vier", "five": "5"}'
```

## Working with JSON Data

You can store the secret value in a variable and manipulate it using `jq`, a lightweight and flexible command-line JSON processor.

### Store Secret in a Variable

```bash
awesome_secrets=$(aws secretsmanager get-secret-value --secret-id my_awesome_secret --query SecretString --output text)
```

### Modify a JSON Key

To modify a key's value using `jq`:

```bash
echo $awesome_secrets | jq '.five = "fünf"'
```

### Using Variables in `jq`

You can pass a value to the `jq` program as a predefined variable:

```bash
echo $awesome_secrets | jq --arg new_value fünf '.five = $new_value'
```

### Create New JSON Key-Value Pairs

You can also create new key-value pairs in your JSON:

```bash
echo $awesome_secrets | jq --arg new_value fünf '.five = $new_value | .all = .one + " " + .two + " " + .three + " " + .four + " " + .five'
```

## Deleting a Secret

Secrets in AWS Secrets Manager are not deleted immediately to prevent accidental loss. By default, a secret is scheduled for deletion after a recovery period. Also, you won't be able to create another secret with the same name until it is fully deleted.

To delete a secret without the recovery option, use the following command:

```bash
aws secretsmanager delete-secret --secret-id my_awesome_secret --force-delete-without-recovery
```

For more detailed information, visit the official [AWS Documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_delete-secret.html).
