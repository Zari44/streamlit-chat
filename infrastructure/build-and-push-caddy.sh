#!/bin/bash
# Script to build and push the Caddy Docker image to the remote instance

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

# Check if docker command is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: docker command not found${NC}"
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

echo -e "${GREEN}Building and pushing Caddy Docker image to instance: $INSTANCE_IP${NC}"
echo -e "${GREEN}Using key file: $KEY_FILE${NC}"
echo ""

# Get the project root directory (parent of infrastructure)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# Image name
CADDY_IMAGE="goatbot-caddy"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Temporary directory for tar files
TEMP_DIR=$(mktemp -d)
trap 'rm -rf ${TEMP_DIR}' EXIT

echo -e "${BLUE}Step 1: Building Caddy Docker image...${NC}"
echo ""

# Check if Dockerfile exists
if [ ! -f "$PROJECT_ROOT/caddy/Dockerfile" ]; then
    echo -e "${RED}Error: caddy/Dockerfile not found${NC}"
    exit 1
fi

echo -e "${YELLOW}Building Caddy image with Route 53 DNS plugin...${NC}"
docker build -t "$CADDY_IMAGE:$TIMESTAMP" -f caddy/Dockerfile .
docker tag "$CADDY_IMAGE:$TIMESTAMP" "$CADDY_IMAGE:latest"
echo -e "${GREEN}✓ Caddy image built successfully${NC}"

echo ""
echo -e "${BLUE}Step 2: Saving Docker image to tar file...${NC}"

# Save image to tar file
CADDY_TAR="$TEMP_DIR/${CADDY_IMAGE}.tar"

echo -e "${YELLOW}Saving Caddy image...${NC}"
docker save "$CADDY_IMAGE:latest" -o "$CADDY_TAR"
echo -e "${GREEN}✓ Caddy image saved${NC}"

echo ""
echo -e "${BLUE}Step 3: Transferring image to remote instance...${NC}"

# Create directory on remote if it doesn't exist
ssh -i "$KEY_FILE" -o StrictHostKeyChecking=no ec2-user@$INSTANCE_IP "mkdir -p /tmp/goatbot-images" || true

# Transfer tar file
echo -e "${YELLOW}Transferring Caddy image...${NC}"
scp -i "$KEY_FILE" -o StrictHostKeyChecking=no "$CADDY_TAR" ec2-user@$INSTANCE_IP:/tmp/goatbot-images/
echo -e "${GREEN}✓ Caddy image transferred${NC}"

echo ""
echo -e "${BLUE}Step 4: Loading image on remote instance...${NC}"

# Load image on remote instance
ssh -i "$KEY_FILE" -o StrictHostKeyChecking=no ec2-user@$INSTANCE_IP << 'EOF'
    echo "Loading Caddy image..."
    docker load -i /tmp/goatbot-images/${CADDY_IMAGE}.tar
    echo "Cleaning up tar file..."
    rm -f /tmp/goatbot-images/${CADDY_IMAGE}.tar
    echo "Caddy image loaded successfully!"
EOF

echo ""
echo -e "${GREEN}✓ Caddy Docker image built and pushed successfully!${NC}"
echo ""
