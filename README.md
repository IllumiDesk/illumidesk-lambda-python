<!-- BEGIN_TF_DOCS -->
# Terraform AWS Lambda Function

This is an opinionated setup that uses Terraform to manage an AWS Lambda function.

## What will this setup do?

This is a Terraform configuration that manages the an AWS EKS stack. It will create the following resources:

- AWS Lambda Function
- AWS ECR Repository
- Docker Image Build and Push to AWS ECR repository

This setup the Terraform CLI to manage the IllumiDesk stack using Terraform Workspaces.

## Requirements

Ensure you have the following installed on your local machine:

    - [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
    - [docker](https://docs.docker.com/get-docker/).
    - [sam cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).
    - [terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

You must have an AWS account and provide your AWS Access Key ID and AWS Secret Access Key.

The values for `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` should be saved as environment variables on your workspace or they can be provided as variables in the `*.tfvars` file.

## Quick Start

Copy the `example.tfvars` file to `<environment>.tfvars` and update the values with your AWS credentials.

```bash
cp example.tfvars dev.tfvars
```

Create and/or select a Terraform workspace.

```bash
terraform workspace new dev
```

Initialize the Terraform configuration.

```bash
terraform init
```

Plan the Terraform configuration.

```bash
terraform plan -var-file=dev.tfvars
```

Apply the Terraform configuration.

```bash
terraform apply -var-file=dev.tfvars
```

### Assert the Lambda Function with Boto3

From the `tests/lambda_function` directory, run the following command to test the Lambda function with Boto3. Ensure that the `ARN` value is exported with the `LAMBDA_FUNCTION_ARN` environment variable before executing the test:

```bash
# example for development environment lambda function
export LAMBDA_FUNCTION_ARN=arn:aws:lambda:us-east-1:860100747351:function:app-dev-docker-lambda_handler
python test_lambda_with_arn.py
```

This should output a result similar to the following:

```bash
{'statusCode': 200, 'body': '{"result": {"a": 5, "b": 20}}'}
```

## Terraform Reference

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 0.13.1 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 3.19 |
| <a name="requirement_docker"></a> [docker](#requirement\_docker) | >= 2.12 |
| <a name="requirement_random"></a> [random](#requirement\_random) | >= 2.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | >= 3.19 |
| <a name="provider_random"></a> [random](#provider\_random) | >= 2.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_docker_image"></a> [docker\_image](#module\_docker\_image) | ./docker-build | n/a |
| <a name="module_lambda_function_from_container_image"></a> [lambda\_function\_from\_container\_image](#module\_lambda\_function\_from\_container\_image) | terraform-aws-modules/lambda/aws | ~> 4.13 |

## Resources

| Name | Type |
|------|------|
| [random_pet.this](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/pet) | resource |
| [aws_caller_identity.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_ecr_authorization_token.token](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/ecr_authorization_token) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

No inputs.

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_docker_image_uri"></a> [docker\_image\_uri](#output\_docker\_image\_uri) | The ECR Docker image URI used to deploy Lambda Function |
| <a name="output_lambda_cloudwatch_log_group_arn"></a> [lambda\_cloudwatch\_log\_group\_arn](#output\_lambda\_cloudwatch\_log\_group\_arn) | The ARN of the Cloudwatch Log Group |
| <a name="output_lambda_function_arn"></a> [lambda\_function\_arn](#output\_lambda\_function\_arn) | The ARN of the Lambda Function |
| <a name="output_lambda_function_arn_static"></a> [lambda\_function\_arn\_static](#output\_lambda\_function\_arn\_static) | The static ARN of the Lambda Function. Use this to avoid cycle errors between resources (e.g., Step Functions) |
| <a name="output_lambda_function_invoke_arn"></a> [lambda\_function\_invoke\_arn](#output\_lambda\_function\_invoke\_arn) | The Invoke ARN of the Lambda Function |
| <a name="output_lambda_function_kms_key_arn"></a> [lambda\_function\_kms\_key\_arn](#output\_lambda\_function\_kms\_key\_arn) | The ARN for the KMS encryption key of Lambda Function |
| <a name="output_lambda_function_last_modified"></a> [lambda\_function\_last\_modified](#output\_lambda\_function\_last\_modified) | The date Lambda Function resource was last modified |
| <a name="output_lambda_function_name"></a> [lambda\_function\_name](#output\_lambda\_function\_name) | The name of the Lambda Function |
| <a name="output_lambda_function_qualified_arn"></a> [lambda\_function\_qualified\_arn](#output\_lambda\_function\_qualified\_arn) | The ARN identifying your Lambda Function Version |
| <a name="output_lambda_function_region"></a> [lambda\_function\_region](#output\_lambda\_function\_region) | The region of the Lambda Function |
| <a name="output_lambda_function_source_code_hash"></a> [lambda\_function\_source\_code\_hash](#output\_lambda\_function\_source\_code\_hash) | Base64-encoded representation of raw SHA-256 sum of the zip file |
| <a name="output_lambda_function_source_code_size"></a> [lambda\_function\_source\_code\_size](#output\_lambda\_function\_source\_code\_size) | The size in bytes of the function .zip file |
| <a name="output_lambda_function_version"></a> [lambda\_function\_version](#output\_lambda\_function\_version) | Latest published version of Lambda Function |
| <a name="output_lambda_layer_arn"></a> [lambda\_layer\_arn](#output\_lambda\_layer\_arn) | The ARN of the Lambda Layer with version |
| <a name="output_lambda_layer_created_date"></a> [lambda\_layer\_created\_date](#output\_lambda\_layer\_created\_date) | The date Lambda Layer resource was created |
| <a name="output_lambda_layer_layer_arn"></a> [lambda\_layer\_layer\_arn](#output\_lambda\_layer\_layer\_arn) | The ARN of the Lambda Layer without version |
| <a name="output_lambda_layer_source_code_size"></a> [lambda\_layer\_source\_code\_size](#output\_lambda\_layer\_source\_code\_size) | The size in bytes of the Lambda Layer .zip file |
| <a name="output_lambda_layer_version"></a> [lambda\_layer\_version](#output\_lambda\_layer\_version) | The Lambda Layer version |
| <a name="output_lambda_role_arn"></a> [lambda\_role\_arn](#output\_lambda\_role\_arn) | The ARN of the IAM role created for the Lambda Function |
| <a name="output_lambda_role_name"></a> [lambda\_role\_name](#output\_lambda\_role\_name) | The name of the IAM role created for the Lambda Function |
<!-- END_TF_DOCS -->