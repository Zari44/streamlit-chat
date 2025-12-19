# GoatBot Infrastructure as Code

This directory contains Terraform configuration files to deploy GoatBot on AWS EC2.

## Prerequisites

1. **AWS Account**: You need an AWS account with appropriate permissions
2. **AWS CLI**: Install and configure AWS CLI with your credentials
   ```bash
   aws configure
   ```
3. **Terraform**: Install Terraform (>= 1.0)
   - Download from https://www.terraform.io/downloads
   - Or use a package manager: `brew install terraform` (macOS) or `sudo apt install terraform` (Ubuntu)
4. **AWS Key Pair**: Create an EC2 key pair in your AWS region
   - Go to EC2 → Key Pairs → Create key pair
   - Save the private key file (`.pem`) securely

## Quick Start

1. **Configure variables**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values, especially key_pair_name
   ```

2. **Initialize Terraform**:
   ```bash
   terraform init
   ```

3. **Review the plan**:
   ```bash
   terraform plan
   ```

4. **Apply the configuration**:
   ```bash
   terraform apply
   ```

5. **After deployment, copy your application files**:
   ```bash
   # Get the instance IP from terraform output
   INSTANCE_IP=$(terraform output -raw instance_public_ip)

   # Copy application files
   scp -i ~/.ssh/your-key.pem -r ../backend ../streamlit-chat ../shared ../Caddyfile ../docker-compose.yml ../pyproject.toml ../uv.lock ec2-user@$INSTANCE_IP:/opt/goatbot/

   # SSH into the instance
   ssh -i ~/.ssh/your-key.pem ec2-user@$INSTANCE_IP

   # On the instance, navigate to the app directory and start services
   cd /opt/goatbot
   docker-compose up -d
   ```

## Configuration Variables

Edit `terraform.tfvars` to customize:

- `aws_region`: AWS region (default: us-east-1)
- `project_name`: Project name for resource naming (default: goatbot)
- `instance_type`: EC2 instance type (default: t3.medium)
- `key_pair_name`: **REQUIRED** - Your AWS key pair name
- `volume_size`: Root volume size in GB (default: 20)
- `ssh_allowed_cidrs`: CIDR blocks for SSH access (default: 0.0.0.0/0 - restrict this!)
- `allocate_elastic_ip`: Allocate static IP (default: true)
- `domain_name`: Domain name for Caddy and DNS (e.g., "goatbot.com.pl")
- `create_dns_records`: Create Route 53 DNS records (default: false)
- `create_www_record`: Create www subdomain record (default: true)

## Security Recommendations

1. **Restrict SSH access**: Update `ssh_allowed_cidrs` in `terraform.tfvars` to your IP address:
   ```hcl
   ssh_allowed_cidrs = ["YOUR_IP/32"]
   ```

2. **Use a domain name**: Set up a domain and configure DNS to point to your Elastic IP, then update the Caddyfile

3. **Enable HTTPS**: Caddy will automatically provision SSL certificates if you use a domain name

4. **Regular updates**: Keep your EC2 instance and Docker images updated

## Deployment Workflow

### Option 1: Manual Deployment (Current Setup)

1. Deploy infrastructure with Terraform
2. Manually copy application files via SCP
3. SSH into instance and run `docker-compose up -d`

### Option 2: Git-based Deployment (Recommended)

1. Push your code to a Git repository (GitHub, GitLab, etc.)
2. Update `user-data.sh` to clone from your repository:
   ```bash
   git clone https://github.com/yourusername/goatbot.git /opt/goatbot
   ```
3. The instance will automatically pull and deploy on startup

### Option 3: AWS CodeDeploy (Advanced)

Set up AWS CodeDeploy for automated deployments. This requires additional Terraform configuration.

## Managing the Infrastructure

- **View outputs**: `terraform output`
- **Destroy infrastructure**: `terraform destroy`
- **Update configuration**: Edit `.tf` files and run `terraform apply`

## Troubleshooting

### SSH Connection Issues
- Verify your key pair name matches the one in AWS
- Check security group allows SSH from your IP
- Ensure the private key has correct permissions: `chmod 400 ~/.ssh/your-key.pem`

### Application Not Starting
- SSH into the instance and check Docker: `docker ps`
- View logs: `docker-compose logs`
- Check user-data script logs: `cat /var/log/user-data.log`

### Port Access Issues
- Verify security groups allow traffic on ports 80, 443, 8000, 8501
- Check EC2 instance status in AWS Console

## Cost Estimation

Approximate monthly costs (us-east-1):
- t3.medium instance: ~$30/month
- Elastic IP (if not attached): $0/month (free when attached)
- Data transfer: Varies based on usage
- Storage (20GB gp3): ~$2/month

**Total estimated**: ~$32-35/month for basic setup

## DNS Configuration with Route 53

To set up DNS for your domain (e.g., `goatbot.com.pl`):

### Option 1: Using Terraform (Recommended)

1. **Update `terraform.tfvars`**:
   ```hcl
   domain_name = "goatbot.com.pl"
   create_dns_records = true
   create_www_record = true
   ```

2. **Apply Terraform configuration**:
   ```bash
   terraform apply
   ```

3. **Get the name servers**:
   ```bash
   terraform output route53_name_servers
   ```

4. **Update your domain registrar**:
   - Go to your domain registrar (where you purchased `goatbot.com.pl`)
   - Update the domain's name servers to the ones shown in the Terraform output
   - This typically takes 24-48 hours to propagate globally

### Option 2: Manual DNS Configuration

If you prefer to manage DNS at your domain registrar:

1. **Get your Elastic IP**:
   ```bash
   terraform output elastic_ip
   ```

2. **Create DNS records at your registrar**:
   - Create an **A record** for `goatbot.com.pl` pointing to the Elastic IP
   - Optionally create a **CNAME record** for `www.goatbot.com.pl` pointing to `goatbot.com.pl`

3. **Set `create_dns_records = false`** in `terraform.tfvars` to prevent Terraform from managing DNS

### After DNS Setup

Once DNS is configured and propagated:
- Caddy will automatically obtain SSL certificates via Let's Encrypt
- Your application will be accessible at `https://goatbot.com.pl`
- The `Caddyfile.prod` is already configured for the domain

## Next Steps

1. ✅ Set up a domain name and configure DNS (see above)
2. ✅ Configure Caddy with your domain in the Caddyfile (already done)
3. Set up automated backups for the database
4. Consider using AWS RDS for the database instead of SQLite
5. Set up CloudWatch monitoring and alarms
6. Configure auto-scaling if needed

## Additional Resources

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [EC2 User Guide](https://docs.aws.amazon.com/ec2/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
