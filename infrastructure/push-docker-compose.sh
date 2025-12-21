#!/bin/bash
# Script to push docker-compose.prod.yml configuration file to the remote instance

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if terraform command is available
if ! command -v terraform &> /dev/null; then
    echo -e "${RED}Error: terraform command not found${NC}"
    exit 1
fi

# Get instance IP from Terraform output
# INSTANCE_IP=$(terraform output -raw instance_public_ip 2>/dev/null || echo "")
# if [ -z "$INSTANCE_IP" ]; then
#     echo -e "${RED}Error: Could not get instance IP from Terraform output${NC}"
#     echo "Make sure you've run 'terraform apply' first"
#     exit 1
# fi

INSTANCE_IP="51.21.48.62"
echo -e "${GREEN}Using instance IP: $INSTANCE_IP${NC}"

# Get key pair name from terraform
KEY_NAME=$(terraform output -raw key_pair_name 2>/dev/null || grep -E '^key_pair_name\s*=' terraform.tfvars | sed 's/.*=\s*"\(.*\)".*/\1/' | head -1)
if [ -z "$KEY_NAME" ]; then
    echo -e "${YELLOW}Warning: Could not determine key pair name${NC}"
    read -p "Enter your key pair name (without .pem extension): " KEY_NAME
fi

KEY_FILE="$HOME/.ssh/${KEY_NAME}.pem"
if [ ! -f "$KEY_FILE" ]; then
    echo -e "${YELLOW}Key file not found at $KEY_FILE${NC}"
    read -p "Enter full path to your private key file: " KEY_FILE
    if [ ! -f "$KEY_FILE" ]; then
        echo -e "${RED}Error: Key file not found at $KEY_FILE${NC}"
        exit 1
    fi
fi

# Set correct permissions on key file
chmod 400 "$KEY_FILE" 2>/dev/null || true

echo -e "${GREEN}Pushing docker-compose.prod.yml to instance: $INSTANCE_IP${NC}"
echo -e "${GREEN}Using key file: $KEY_FILE${NC}"
echo ""

# Get the project root directory (parent of infrastructure)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Create app directory on remote if it doesn't exist
ssh -i "$KEY_FILE" -o StrictHostKeyChecking=no ec2-user@$INSTANCE_IP "mkdir -p /opt/goatbot" || true

echo -e "${BLUE}Copying docker-compose.prod.yml...${NC}"

# Copy production docker-compose file
if [ -f "$PROJECT_ROOT/docker-compose.prod.yml" ]; then
    echo -e "${YELLOW}Copying docker-compose.prod.yml...${NC}"
    scp -i "$KEY_FILE" -o StrictHostKeyChecking=no "$PROJECT_ROOT/docker-compose.prod.yml" ec2-user@$INSTANCE_IP:/opt/goatbot/docker-compose.yml
    echo -e "${GREEN}✓ docker-compose.prod.yml copied successfully${NC}"
else
    echo -e "${RED}Error: docker-compose.prod.yml not found at $PROJECT_ROOT/docker-compose.prod.yml${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ docker-compose.prod.yml pushed successfully!${NC}"
echo ""
echo -e "${YELLOW}Note: Make sure .env.caddy, .env.backend, and .env.chat files exist on the remote instance${NC}"
echo -e "${YELLOW}      in /opt/goatbot/ before starting the containers.${NC}"
echo ""
