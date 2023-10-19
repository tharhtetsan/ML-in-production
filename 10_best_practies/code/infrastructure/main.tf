# Make sure to create state bucket beforehand

terraform {
  required_version = ">= 1.6.2"
  backend "s3" {
    bucket  = "tf-state-mlops-zoomcamp"
    key     = "mlops-zoomcamp-stg.tfstate"
    region  = "ap-southeast-2"
    encrypt = true
  }
}

provider "aws" {
    region = var.aws_region
}

data aws_caller_identity = "current_identity" {}

locals {
  account_id = data.aws_caller_identity.current_identity.account_id
}
