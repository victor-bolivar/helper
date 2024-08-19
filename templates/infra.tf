terraform {
  required_providers {
    openstack = {
      source = "terraform-provider-openstack/openstack"
      version = "1.54.1"
    }
  }
}

variable "OS_AUTH_URL" { type = string }
variable "OS_PROJECT_NAME" { type = string }
variable "OS_USERNAME" { type = string }
variable "OS_PASSWORD" { type = string }
variable "OS_REGION_NAME" { type = string }

provider "openstack" {
  user_name   = var.OS_USERNAME
  password    = var.OS_PASSWORD
  tenant_name = var.OS_PROJECT_NAME
  auth_url    = var.OS_AUTH_URL
  region      = var.OS_REGION_NAME
}

