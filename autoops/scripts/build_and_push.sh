#!/bin/bash
# AutoOps Build and Push Script
# Script to build and push Docker images to registry

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Default values
REGISTRY_URL=${REGISTRY_URL:-""}
REGISTRY_USERNAME=${REGISTRY_USERNAME:-""}
REGISTRY_TOKEN=${REGISTRY_TOKEN:-""}
IMAGE_NAME=${IMAGE_NAME:-"autoops/model-service"}
TAG=${TAG:-"latest"}
PUSH=${PUSH:-"false"}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --registry-url)
            REGISTRY_URL="$2"
            shift 2
            ;;
        --username)
            REGISTRY_USERNAME="$2"
            shift 2
            ;;
        --token)
            REGISTRY_TOKEN="$2"
            shift 2
            ;;
        --image-name)
            IMAGE_NAME="$2"
            shift 2
            ;;
        --tag)
            TAG="$2"
            shift 2
            ;;
        --push)
            PUSH="true"
            shift
            ;;
        --help|-h)
            echo "AutoOps Build and Push Script"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --registry-url URL     Container registry URL"
            echo "  --username USER        Registry username"
            echo "  --token TOKEN          Registry token/password"
            echo "  --image-name NAME      Image name (default: autoops/model-service)"
            echo "  --tag TAG              Image tag (default: latest)"
            echo "  --push                 Push image to registry"
            echo "  --help, -h             Show this help message"
            echo ""
            echo "Environment Variables:"
            echo "  REGISTRY_URL           Container registry URL"
            echo "  REGISTRY_USERNAME      Registry username"
            echo "  REGISTRY_TOKEN         Registry token/password"
            echo "  IMAGE_NAME             Image name"
            echo "  TAG                    Image tag"
            echo "  PUSH                   Set to 'true' to push image"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

print_status "AutoOps Build and Push Script"
print_status "=============================="

# Check if Docker is available
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    print_success "Docker is available"
}

# Build Docker image
build_image() {
    print_status "Building Docker image..."
    
    # Change to model service directory
    cd services/model_service
    
    # Build the image
    docker build -t "${IMAGE_NAME}:${TAG}" .
    
    if [ $? -eq 0 ]; then
        print_success "Docker image built successfully: ${IMAGE_NAME}:${TAG}"
    else
        print_error "Docker build failed"
        exit 1
    fi
    
    # Also tag as latest if not already
    if [ "$TAG" != "latest" ]; then
        docker tag "${IMAGE_NAME}:${TAG}" "${IMAGE_NAME}:latest"
        print_success "Tagged as latest: ${IMAGE_NAME}:latest"
    fi
}

# Login to registry
login_registry() {
    if [ -n "$REGISTRY_URL" ] && [ -n "$REGISTRY_USERNAME" ] && [ -n "$REGISTRY_TOKEN" ]; then
        print_status "Logging in to registry: $REGISTRY_URL"
        echo "$REGISTRY_TOKEN" | docker login "$REGISTRY_URL" -u "$REGISTRY_USERNAME" --password-stdin
        
        if [ $? -eq 0 ]; then
            print_success "Successfully logged in to registry"
        else
            print_error "Failed to login to registry"
            exit 1
        fi
    else
        print_warning "Registry credentials not provided - skipping login"
    fi
}

# Push image to registry
push_image() {
    if [ "$PUSH" = "true" ] && [ -n "$REGISTRY_URL" ]; then
        print_status "Pushing image to registry..."
        
        # Tag image with registry URL
        FULL_IMAGE_NAME="${REGISTRY_URL}/${IMAGE_NAME}:${TAG}"
        docker tag "${IMAGE_NAME}:${TAG}" "$FULL_IMAGE_NAME"
        
        # Push image
        docker push "$FULL_IMAGE_NAME"
        
        if [ $? -eq 0 ]; then
            print_success "Image pushed successfully: $FULL_IMAGE_NAME"
        else
            print_error "Failed to push image"
            exit 1
        fi
        
        # Also push latest tag if not already latest
        if [ "$TAG" != "latest" ]; then
            LATEST_IMAGE_NAME="${REGISTRY_URL}/${IMAGE_NAME}:latest"
            docker tag "${IMAGE_NAME}:latest" "$LATEST_IMAGE_NAME"
            docker push "$LATEST_IMAGE_NAME"
            print_success "Latest tag pushed: $LATEST_IMAGE_NAME"
        fi
    else
        print_status "Skipping push (use --push to enable)"
    fi
}

# Show image information
show_image_info() {
    print_status "Image information:"
    echo "  Image: ${IMAGE_NAME}:${TAG}"
    echo "  Registry: ${REGISTRY_URL:-"local"}"
    echo "  Push enabled: $PUSH"
    
    # Show image size
    if command -v docker &> /dev/null; then
        IMAGE_SIZE=$(docker images --format "table {{.Size}}" "${IMAGE_NAME}:${TAG}" | tail -n 1)
        echo "  Size: $IMAGE_SIZE"
    fi
}

# Main execution
main() {
    print_status "Starting build process..."
    
    # Check Docker
    check_docker
    
    # Build image
    build_image
    
    # Login to registry if credentials provided
    login_registry
    
    # Push image if requested
    push_image
    
    # Show image information
    show_image_info
    
    print_success "Build process completed successfully!"
}

# Run main function
main
