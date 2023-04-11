# IllumiDesk Lambda Function for Executing Python Code

This repository contains the source code for the IllumiDesk Lambda function that executes Python code.

### Prerequisites

- Install the AWS CLI by following the [official documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html).
- Install Docker by following the [official documentation](https://docs.docker.com/get-docker/).
- (For Testing) Install AWS SAM CLI by following the official [installation instructions](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).

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

### Pushing the Docker Image to AWS ECR

From the root directory, run the following command to push the Docker image to AWS ECR:

```bash
docker push 860100747351.dkr.ecr.us-east-1.amazonaws.com/python:3.9
```

### (Optional) Test the Lambda Function with Boto3

From the root directory, run the following command to test the Lambda function with Boto3. Ensure that the `ARN` value in the `test_lambda_with_arn.py` file is updated with the ARN of the Lambda function you want to test:

```bash
python test_lambda_with_arn.py
```

This should output a result similar to the following:

```bash
{'statusCode': 200, 'body': '{"result": {"a": 5, "b": 20}}'}
```

## Testing AWS Lambda Function Locally

This section explains how to test your AWS Lambda function locally using the AWS Serverless Application Model (SAM) CLI and Docker.

### Building and Invoking the Lambda Function Locally

From the root directory, run the following commands to build and invoke the Lambda function locally:

```bash
sam build --use-container
sam local invoke ExecuteCodeFunction -e event.json
```

The `sam local invoke ...` command will run your Lambda function in a Docker container and use the `event.json` file as the input event.

If the function ran successfully, you should see the following output:

```bash
{"statusCode": 200, "body": "{\"result\": {\"a\": 5, \"b\": 20}}"}
```
