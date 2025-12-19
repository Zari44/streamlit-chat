output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.goatbot.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.goatbot.public_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.goatbot.public_dns
}

output "elastic_ip" {
  description = "Elastic IP address (if allocated)"
  value       = var.allocate_elastic_ip ? aws_eip.goatbot_eip[0].public_ip : null
}

output "ssh_command" {
  description = "Command to SSH into the instance"
  value       = "ssh -i ~/.ssh/${var.key_pair_name}.pem ec2-user@${var.allocate_elastic_ip ? aws_eip.goatbot_eip[0].public_ip : aws_instance.goatbot.public_ip}"
}

output "application_url" {
  description = "URL to access the application"
  value       = var.domain_name != "" ? "https://${var.domain_name}" : "http://${var.allocate_elastic_ip ? aws_eip.goatbot_eip[0].public_ip : aws_instance.goatbot.public_ip}"
}

output "route53_zone_id" {
  description = "Route 53 hosted zone ID (if DNS records were created)"
  value       = var.domain_name != "" && var.create_dns_records ? aws_route53_zone.goatbot_zone[0].zone_id : null
}

output "route53_name_servers" {
  description = "Route 53 name servers for the hosted zone (update your domain registrar with these)"
  value       = var.domain_name != "" && var.create_dns_records ? aws_route53_zone.goatbot_zone[0].name_servers : null
}
