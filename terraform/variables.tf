variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "Name of the project, used as prefix for all resources"
  type        = string
  default     = "openhands-todo"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "container_port" {
  description = "Port exposed by the container"
  type        = number
  default     = 54439  # Port used in the FastAPI application
}

variable "container_image" {
  description = "Docker image for the application"
  type        = string
  default     = "your-account.dkr.ecr.us-west-2.amazonaws.com/openhands-todo"
}

variable "container_tag" {
  description = "Tag of the Docker image"
  type        = string
  default     = "latest"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Name of the database"
  type        = string
  default     = "openhands_todo"
}

variable "db_username" {
  description = "Username for the database"
  type        = string
  default     = "openhands"
}

variable "db_password" {
  description = "Password for the database"
  type        = string
  sensitive   = true
}

variable "task_cpu" {
  description = "CPU units for the ECS task"
  type        = string
  default     = "256"
}

variable "task_memory" {
  description = "Memory for the ECS task"
  type        = string
  default     = "512"
}

variable "service_desired_count" {
  description = "Desired number of tasks running in the service"
  type        = number
  default     = 2
}

variable "common_tags" {
  description = "Common tags to be applied to all resources"
  type        = map(string)
  default = {
    Project     = "openhands-todo"
    Environment = "production"
    Terraform   = "true"
  }
}
