terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Data source to get the latest Amazon Linux 2023 AMI
data "aws_ami" "alpine_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Security Group for the EC2 instance
resource "aws_security_group" "goatbot_sg" {
  name        = "${var.project_name}-sg"
  description = "Security group for GoatBot application"

  # HTTP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP"
  }

  # HTTPS
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS"
  }

  # SSH (restrict to your IP if possible)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ssh_allowed_cidrs
    description = "SSH"
  }

  # Backend API (optional - can be restricted to internal only)
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Backend API"
  }

  # Streamlit (optional - can be restricted to internal only)
  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Streamlit"
  }

  # All outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound"
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

# IAM role for EC2 instance
resource "aws_iam_role" "goatbot_role" {
  name = "${var.project_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-role"
  }
}

# IAM instance profile
resource "aws_iam_instance_profile" "goatbot_profile" {
  name = "${var.project_name}-profile"
  role = aws_iam_role.goatbot_role.name
}

# EC2 Instance
resource "aws_instance" "goatbot" {
  ami                    = data.aws_ami.alpine_linux.id
  instance_type          = var.instance_type
  key_name               = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.goatbot_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.goatbot_profile.name

  user_data = templatefile("${path.module}/user-data.sh", {
    project_name = var.project_name
    domain_name  = var.domain_name
  })

  root_block_device {
    volume_type = "gp3"
    volume_size = var.volume_size
    encrypted   = true
  }

  tags = {
    Name = var.project_name
  }
}

# Elastic IP (optional but recommended for static IP)
resource "aws_eip" "goatbot_eip" {
  count    = var.allocate_elastic_ip ? 1 : 0
  instance = aws_instance.goatbot.id
  domain   = "vpc"

  tags = {
    Name = "${var.project_name}-eip"
  }
}

# Route 53 Hosted Zone (only if domain_name is provided and create_dns_records is true)
resource "aws_route53_zone" "goatbot_zone" {
  count = var.domain_name != "" && var.create_dns_records ? 1 : 0
  name  = var.domain_name

  tags = {
    Name = "${var.project_name}-zone"
  }
}

# Route 53 A record pointing to Elastic IP
resource "aws_route53_record" "goatbot_a_record" {
  count   = var.domain_name != "" && var.create_dns_records && var.allocate_elastic_ip ? 1 : 0
  zone_id = aws_route53_zone.goatbot_zone[0].zone_id
  name    = var.domain_name
  type    = "A"
  ttl     = 300
  records = [aws_eip.goatbot_eip[0].public_ip]
}

# Route 53 A record for www subdomain (optional)
resource "aws_route53_record" "goatbot_www_record" {
  count   = var.domain_name != "" && var.create_dns_records && var.allocate_elastic_ip && var.create_www_record ? 1 : 0
  zone_id = aws_route53_zone.goatbot_zone[0].zone_id
  name    = "www.${var.domain_name}"
  type    = "A"
  ttl     = 300
  records = [aws_eip.goatbot_eip[0].public_ip]
}
