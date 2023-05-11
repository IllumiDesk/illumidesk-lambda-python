variable "api_user_name" {
  description = "Value (name) of the api user name"
  type        = string
  default     = "api-illumidesk"
}

variable "environment" {
  description = "The environment to deploy to"
  type        = string
  default     = "dev"
}

variable "ecr_repository_name" {
  description = "The name of the ECR repository to create"
  type        = string
  default     = "lambda-container-image"
}