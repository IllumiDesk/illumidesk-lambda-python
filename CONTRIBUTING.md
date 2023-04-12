# Contributing to illumidesk-lambda-function

## Requirements

1. [install pre-commit](https://pre-commit.com/)
2. configure pre-commit: `pre-commit install`
3. install required tools
    - [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
    - [docker](https://docs.docker.com/get-docker/).
    - [sam cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).
    - [tflint](https://github.com/terraform-linters/tflint)
    - [tfsec](https://aquasecurity.github.io/tfsec/v1.0.11/)
    - [terraform-docs](https://github.com/terraform-docs/terraform-docs)
    - [golang](https://go.dev/doc/install) (for macos you can use `brew`)
    - [coreutils](https://www.gnu.org/software/coreutils/)

Write code according to [I&A module standards](https://aws-ia.github.io/standards-terraform/)

## Module Documentation

**Do not manually update README.md**. `terraform-docs` is used to generate README files. For any instructions an content, please update [.header.md](./.header.md) then simply run `terraform-docs ./` or allow the `pre-commit` to do so.

## Updating the Lambda Function

This implementation of AWS Lambda uses [docker containers](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html) to run the code. The lambda function consists of a **function name** and is associated to a **container image**. The container image is stored in [AWS ECR](https://aws.amazon.com/ecr/).

There are two files to update the lambda function:

1. The `Dockerfile` contains the instructions to build the container image.
2. The `requirements.txt` file contains the list of Python packages that are installed in the container image.

All other files are used to test the Lambda function locally and are not required for cloud deployments with AWS.

### Updating the Lambda Function Code

The Lambda function code is located in the `app.py` file. The `lambda_handler` function is the entry point for the Lambda function.

### Building the Docker Image used by the Lambda Function

From the root directory, run the following command to build the Docker image:

```bash
docker build -t 860100747351.dkr.ecr.us-east-1.amazonaws.com/python:3.9 . --platform=linux/amd64 --no-cache
```

> **Note:** The `--platform=linux/amd64` flag is required to build the Docker image for the `python:3.9` image when using environments with other architecture types, such as MacOSX with M1 (ARM) processors. The `--no-cache` flag is used to force a rebuild of the image.

## Testing AWS Lambda Function Locally

This section explains how to test your AWS Lambda function locally using the AWS Serverless Application Model (SAM) CLI and Docker.

### Building and Invoking the Lambda Function Locally

From the `tests/lambda_function` directory, run the following commands to build and invoke the Lambda function locally:

```bash
sam build --use-container
sam local invoke ExecuteCodeFunction -e event.json
```

The `sam local invoke ...` command will run your Lambda function in a Docker container and use the `event.json` file as the input event.

If the function ran successfully, you should see the following output:

```bash
{"statusCode": 200, "body": "{\"result\": {\"a\": 5, \"b\": 20}}"}
```

### Test the Lambda Function with Boto3

From the root directory, run the following command to test the Lambda function with Boto3. Ensure that the `ARN` value is exported with the `LAMBDA_FUNCTION_ARN` environment variable before executing the test:

```bash
# example for development environment lambda function
export LAMBDA_FUNCTION_ARN=arn:aws:lambda:us-east-1:860100747351:function:app-dev-docker-lambda_handler
python test_lambda_with_arn.py
```

This should output a result similar to the following:

```bash
{'statusCode': 200, 'body': '{"result": {"a": 5, "b": 20}}'}
```

## Terratest

Please include tests to validate your examples/<> root modules, at a minimum. This can be accomplished with usually only slight modifications to the [boilerplate test provided in this template](./test/examples\_basic\_test.go)

### Configure and run Terratest

1. Install

    [golang](https://go.dev/doc/install) (for macos you can use `brew`)

2. Change directory into the test folder.

    `cd tests`

3. Initialize your test

    go mod init github.com/[github_org]/[repo_name]

    For example:

    `go mod init github.com/illumidesk/illumidesk-cloud`

4. Run tidy

    `git mod tidy`

5. Install Terratest

    `go get github.com/gruntwork-io/terratest/modules/terraform`

6. Run test (You can have multiple test files).
    - Run all tests

        `go test`

    - Run a specific test with a timeout

        `go test -run TestExamplesBasic -timeout 45m`

## Continuous Integration

The IllumiDesk team uses GitHub Actions to perform continuous integration (CI) within the organization. Our CI uses the a repo's `.pre-commit-config.yaml` file as well as some other checks.

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0.7 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 4.0.0, < 5.0.0 |
| <a name="requirement_awscc"></a> [awscc](#requirement\_awscc) | >= 0.24.0 |