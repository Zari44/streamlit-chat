#!/bin/bash
# Script to build Docker images from current code and push them to the remote instance

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

echo -e "${GREEN}Building and pushing Docker images to instance: $INSTANCE_IP${NC}"
echo -e "${GREEN}Using key file: $KEY_FILE${NC}"
echo ""

# Get the project root directory (parent of infrastructure)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# Image names
export BACKEND_IMAGE="goatbot-backend"
export STREAMLIT_IMAGE="goatbot-streamlit"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Temporary directory for tar files
TEMP_DIR=$(mktemp -d)
trap 'rm -rf ${TEMP_DIR}' EXIT

echo -e "${BLUE}Step 1: Building Docker images...${NC}"
echo ""

# Build backend image
# echo -e "${YELLOW}Building backend image...${NC}"
# docker build -t "$BACKEND_IMAGE:$TIMESTAMP" -f backend/Dockerfile .
# docker tag "$BACKEND_IMAGE:$TIMESTAMP" "$BACKEND_IMAGE:latest"
# echo -e "${GREEN}✓ Backend image built successfully${NC}"

# Build streamlit-chat image
echo -e "${YELLOW}Building streamlit-chat image...${NC}"
docker build -t "$STREAMLIT_IMAGE:$TIMESTAMP" -f streamlit-chat/Dockerfile .
docker tag "$STREAMLIT_IMAGE:$TIMESTAMP" "$STREAMLIT_IMAGE:latest"
echo -e "${GREEN}✓ Streamlit-chat image built successfully${NC}"

echo ""
echo -e "${BLUE}Step 2: Saving Docker images to tar files...${NC}"

# Save images to tar files
STREAMLIT_TAR="$TEMP_DIR/${STREAMLIT_IMAGE}.tar"

# echo -e "${YELLOW}Saving backend image...${NC}"
# docker save "$BACKEND_IMAGE:latest" -o "$BACKEND_TAR"
# echo -e "${GREEN}✓ Backend image saved${NC}"

echo -e "${YELLOW}Saving streamlit-chat image...${NC}"
docker save "$STREAMLIT_IMAGE:latest" -o "$STREAMLIT_TAR"
echo -e "${GREEN}✓ Streamlit-chat image saved${NC}"

echo ""
echo -e "${BLUE}Step 3: Transferring images to remote instance...${NC}"

# Create directory on remote if it doesn't exist
ssh -i "$KEY_FILE" -o StrictHostKeyChecking=no ec2-user@$INSTANCE_IP "mkdir -p /tmp/goatbot-images" || true

# Transfer tar files
# echo -e "${YELLOW}Transferring backend image...${NC}"
# scp -i "$KEY_FILE" -o StrictHostKeyChecking=no "$BACKEND_TAR" ec2-user@$INSTANCE_IP:/tmp/goatbot-images/
# echo -e "${GREEN}✓ Backend image transferred${NC}"

echo -e "${YELLOW}Transferring streamlit-chat image...${NC}"
scp -i "$KEY_FILE" -o StrictHostKeyChecking=no "${STREAMLIT_TAR}" ec2-user@$INSTANCE_IP:/tmp/goatbot-images/
echo -e "${GREEN}✓ Streamlit-chat image transferred${NC}"

echo ""
echo -e "${BLUE}Step 4: Loading images on remote instance...${NC}"

# Load images on remote instance
ssh -i "$KEY_FILE" -o StrictHostKeyChecking=no ec2-user@$INSTANCE_IP << 'EOF'
    echo "Loading backend image..."
    docker load -i /tmp/goatbot-images/${BACKEND_IMAGE}.tar
    echo "Loading streamlit-chat image..."
    docker load -i /tmp/goatbot-images/${STREAMLIT_IMAGE}.tar
    echo "Cleaning up tar files..."
    rm -f /tmp/goatbot-images/*.tar
    echo "Images loaded successfully!"
EOF

echo ""
echo -e "${BLUE}Step 5: Copying production configuration files...${NC}"

# Create app directory on remote if it doesn't exist
ssh -i "$KEY_FILE" -o StrictHostKeyChecking=no ec2-user@$INSTANCE_IP "mkdir -p /opt/goatbot" || true

# Copy production Caddyfile
if [ -f "$PROJECT_ROOT/Caddyfile.prod" ]; then
    echo -e "${YELLOW}Copying Caddyfile.prod...${NC}"
    scp -i "$KEY_FILE" -o StrictHostKeyChecking=no "$PROJECT_ROOT/Caddyfile.prod" ec2-user@$INSTANCE_IP:/opt/goatbot/Caddyfile
    echo -e "${GREEN}✓ Caddyfile.prod copied${NC}"
else
    echo -e "${YELLOW}Warning: Caddyfile.prod not found, skipping...${NC}"
fi

# Copy production docker-compose file
if [ -f "$PROJECT_ROOT/docker-compose.prod.yml" ]; then
    echo -e "${YELLOW}Copying docker-compose.prod.yml...${NC}"
    scp -i "$KEY_FILE" -o StrictHostKeyChecking=no "$PROJECT_ROOT/docker-compose.prod.yml" ec2-user@$INSTANCE_IP:/opt/goatbot/docker-compose.prod.yml
    echo -e "${GREEN}✓ docker-compose.prod.yml copied${NC}"
else
    echo -e "${YELLOW}Warning: docker-compose.prod.yml not found, skipping...${NC}"
fi

echo ""
echo -e "${GREEN}✓ All Docker images built and pushed successfully!${NC}"
echo ""
echo -e "${YELLOW}Next steps to start the containers:${NC}"
echo ""
echo -e "${BLUE}Option 1: Using docker-compose (recommended)${NC}"
echo "1. SSH into the instance:"
echo "   ssh -i $KEY_FILE ec2-user@$INSTANCE_IP"
echo ""
echo "2. Navigate to the app directory:"
echo "   cd /opt/goatbot"
echo ""
echo "3. Stop existing containers (if running):"
echo "   docker-compose down"
echo ""
echo "4. Start containers using pre-built images:"
echo "   docker-compose -f docker-compose.prod.yml up -d"
echo ""
echo "5. View logs:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo -e "${BLUE}Option 2: Using docker commands directly${NC}"
echo "1. SSH into the instance:"
echo "   ssh -i $KEY_FILE ec2-user@$INSTANCE_IP"
echo ""
echo "2. Create network (if it doesn't exist):"
echo "   docker network create goatbot-network || true"
echo ""
echo "3. Stop and remove existing containers:"
echo "   docker stop goatbot-backend goatbot-streamlit goatbot-caddy 2>/dev/null || true"
echo "   docker rm goatbot-backend goatbot-streamlit goatbot-caddy 2>/dev/null || true"
echo ""
echo "4. Start backend:"
echo "   docker run -d --name goatbot-backend --network goatbot-network \\"
echo "     -e STREAMLIT_URL=http://streamlit-chat:8501 \\"
echo "     -v /opt/goatbot/chat_sessions.db:/data/chat_sessions.db \\"
echo "     --restart unless-stopped goatbot-backend:latest"
echo ""
echo "5. Start streamlit-chat:"
echo "   docker run -d --name goatbot-streamlit --network goatbot-network \\"
echo "     -v /opt/goatbot/chat_sessions.db:/data/chat_sessions.db \\"
echo "     --restart unless-stopped goatbot-streamlit:latest"
echo ""
echo "6. Start caddy:"
echo "   docker run -d --name goatbot-caddy --network goatbot-network \\"
echo "     -p 80:80 -p 443:443 \\"
echo "     -v /opt/goatbot/Caddyfile:/etc/caddy/Caddyfile:ro \\"
echo "     -v caddy_data:/data -v caddy_config:/config \\"
echo "     --restart unless-stopped caddy:latest caddy run --config /etc/caddy/Caddyfile --watch"
echo ""
