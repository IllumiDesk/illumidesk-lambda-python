module "lambda_function_from_container_image" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 4.13"

  function_name = "${random_pet.this.id}-lambda-from-container-image"
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
  ecr_repo        = random_pet.this.id
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

resource "random_pet" "this" {
  length = 2
}
