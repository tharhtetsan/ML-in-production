variable  "aws_region" {
  type        = string
  default     = "ap-southeast-2"
  description = "AWS Region to create resources"
}

variable "project_id" {
  type        = string
  default     = "mlops-zoomcamp"
  description = "Project ID"
}

variable "output_stream_name" {
  description = ""
}

variable "source_stream_name" {
  description = ""
}

variable "model_bucket"{
  description = ""
}

variable "ecr_repo_name" {
  description = ""
}

variable "lambda_function_local_path" {
  description = ""
}

variable "docker_image_local_path" {
  description = ""
}

variable "lambda_function_name" {
  description = ""
}