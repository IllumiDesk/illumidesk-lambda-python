resource "random_pet" "this" {
  length = 2
}

module "lambda_function_from_container_image" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 4.13"

  function_name = "${var.environment}-${random_pet.this.id}-lambda-from-container-image"
  description   = "IllumiDesk's lambda function to run python from container image"

  create_package = false

  ##################
  # Container Image
  ##################
  image_uri     = module.docker_image.image_uri
  package_type  = "Image"
  architectures = ["x86_64"]
}

module "docker_image" {
  source = "./docker-build"

  create_ecr_repo = true
  ecr_repo        = "${var.environment}-${var.ecr_repository_name}"
  ecr_repo_lifecycle_policy = jsonencode({
    "rules" : [
      {
        "rulePriority" : 1,
        "description" : "Keep only the last 2 images",
        "selection" : {
          "tagStatus" : "any",
          "countType" : "imageCountMoreThan",
          "countNumber" : 2
        },
        "action" : {
          "type" : "expire"
        }
      }
    ]
  })

  image_tag   = "2.0"
  source_path = "context"
  platform    = "linux/amd64"
}

module "kms" {
  source  = "terraform-aws-modules/kms/aws"
  version = "~> 1.0"

  description = "S3 encryption key"

  grants = {
    lambda = {
      grantee_principal = module.lambda_function_from_container_image.lambda_role_arn
      operations = [
        "GenerateDataKey",
      ]
    }
  }
}

module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 3.10"

  bucket_prefix = "${var.environment}-${random_pet.this.id}-"
  force_destroy = true

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  versioning = {
    enabled = true
  }

  attach_policy = true
  policy        = data.aws_iam_policy_document.bucket.json

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        kms_master_key_id = module.kms.key_id
        sse_algorithm     = "aws:kms"
      }
    }
  }
}

# Add new IAM policy for api-illumidesk user
resource "aws_iam_policy" "lambda_invoke" {
  name        = "lambda_invoke"
  description = "Allow user to invoke Lambda function"
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "lambda:InvokeFunction"
      ],
      "Effect": "Allow",
      "Resource": "${module.lambda_function_from_container_image.lambda_function_arn}"
    }
  ]
}
EOF
}

# Attach the new policy to the api-illumidesk user
resource "aws_iam_user_policy_attachment" "user_lambda_invoke" {
  user       = var.api_user_name
  policy_arn = aws_iam_policy.lambda_invoke.arn
}
