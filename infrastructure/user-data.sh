#!/bin/bash
# set -e

# # Update system
# sudo yum update -y

# # Install Docker
# sudo yum install -y docker
# sudo systemctl start docker
# sudo systemctl enable docker
# sudo usermod -aG docker ec2-user

# # Install Docker Compose
# sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# sudo chmod +x /usr/local/bin/docker-compose

# # Install Git
# sudo yum install -y git

# # Create application directory
# sudo mkdir -p /opt/${project_name}
# sudo chown ec2-user:ec2-user /opt/${project_name}

# # Clone or copy application files
# # Note: You'll need to either:
# # 1. Push your code to a Git repository and clone it here
# # 2. Use AWS CodeDeploy or similar service
# # 3. Manually copy files via SCP after instance is created

# # For now, we'll create a placeholder script that you can customize
# cat > /opt/${project_name}/deploy.sh << 'DEPLOY_SCRIPT'
# #!/bin/bash
# cd /opt/${project_name}

# # Pull latest code (if using Git)
# # git pull origin main

# # Build and start containers
# docker-compose down
# docker-compose build
# docker-compose up -d

# # Show logs
# docker-compose logs -f
# DEPLOY_SCRIPT

# chmod +x /opt/${project_name}/deploy.sh

# # Create a systemd service for auto-start (optional)
# cat > /tmp/goatbot.service << 'SERVICE_FILE'
# [Unit]
# Description=GoatBot Application
# After=docker.service
# Requires=docker.service

# [Service]
# Type=oneshot
# RemainAfterExit=yes
# WorkingDirectory=/opt/goatbot
# ExecStart=/usr/local/bin/docker-compose up -d
# ExecStop=/usr/local/bin/docker-compose down
# User=ec2-user
# Group=ec2-user

# [Install]
# WantedBy=multi-user.target
# SERVICE_FILE

# # Note: The service file is created but not enabled by default
# # To enable it, run: sudo systemctl enable goatbot.service

# # Log completion
# echo "User data script completed at $(date)" >> /var/log/user-data.log
