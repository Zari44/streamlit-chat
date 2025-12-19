#!/bin/bash
# Helper script to deploy application files to the EC2 instance

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if terraform output is available
if ! command -v terraform &> /dev/null; then
    echo -e "${RED}Error: terraform command not found${NC}"
    exit 1
fi

# Get instance IP from Terraform output
INSTANCE_IP=$(terraform output -raw instance_public_ip 2>/dev/null || echo "")
if [ -z "$INSTANCE_IP" ]; then
    echo -e "${RED}Error: Could not get instance IP from Terraform output${NC}"
    echo "Make sure you've run 'terraform apply' first"
    exit 1
fi

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

echo -e "${GREEN}Deploying to instance: $INSTANCE_IP${NC}"
echo -e "${GREEN}Using key file: $KEY_FILE${NC}"
echo ""

# Get the project root directory (parent of infrastructure)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Files and directories to copy
FILES_TO_COPY=(
    "backend"
    "streamlit-chat"
    "shared"
    "Caddyfile"
    "docker-compose.yml"
    "pyproject.toml"
    "uv.lock"
)

echo -e "${YELLOW}Copying application files...${NC}"

# Create directory on remote if it doesn't exist
ssh -i "$KEY_FILE" -o StrictHostKeyChecking=no ec2-user@$INSTANCE_IP "mkdir -p /opt/goatbot" || true

# Copy each file/directory
for item in "${FILES_TO_COPY[@]}"; do
    if [ -e "$PROJECT_ROOT/$item" ]; then
        echo "Copying $item..."
        scp -i "$KEY_FILE" -o StrictHostKeyChecking=no -r "$PROJECT_ROOT/$item" ec2-user@$INSTANCE_IP:/opt/goatbot/
    else
        echo -e "${YELLOW}Warning: $item not found, skipping...${NC}"
    fi
done

echo ""
echo -e "${GREEN}Files copied successfully!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. SSH into the instance:"
echo "   ssh -i $KEY_FILE ec2-user@$INSTANCE_IP"
echo ""
echo "2. Navigate to the app directory:"
echo "   cd /opt/goatbot"
echo ""
echo "3. Start the application:"
echo "   docker-compose up -d"
echo ""
echo "4. View logs:"
echo "   docker-compose logs -f"
echo ""
