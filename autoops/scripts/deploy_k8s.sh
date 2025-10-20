#!/bin/bash
# AutoOps Kubernetes Deployment Script
# Script to deploy AutoOps to Kubernetes cluster

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
NAMESPACE=${NAMESPACE:-"autoops"}
KUBECONFIG=${KUBECONFIG:-""}
CONTEXT=${CONTEXT:-""}
DRY_RUN=${DRY_RUN:-"false"}
WAIT=${WAIT:-"true"}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        --kubeconfig)
            KUBECONFIG="$2"
            shift 2
            ;;
        --context)
            CONTEXT="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN="true"
            shift
            ;;
        --no-wait)
            WAIT="false"
            shift
            ;;
        --help|-h)
            echo "AutoOps Kubernetes Deployment Script"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --namespace NAMESPACE   Kubernetes namespace (default: autoops)"
            echo "  --kubeconfig PATH      Path to kubeconfig file"
            echo "  --context CONTEXT      Kubernetes context"
            echo "  --dry-run              Show what would be deployed"
            echo "  --no-wait              Don't wait for deployment to be ready"
            echo "  --help, -h             Show this help message"
            echo ""
            echo "Environment Variables:"
            echo "  NAMESPACE              Kubernetes namespace"
            echo "  KUBECONFIG             Path to kubeconfig file"
            echo "  CONTEXT                Kubernetes context"
            echo "  DRY_RUN                Set to 'true' for dry run"
            echo "  WAIT                   Set to 'false' to not wait for deployment"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

print_status "AutoOps Kubernetes Deployment"
print_status "============================="

# Check if kubectl is available
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed or not in PATH"
        exit 1
    fi
    print_success "kubectl is available"
}

# Set kubectl context
setup_kubectl() {
    if [ -n "$KUBECONFIG" ]; then
        export KUBECONFIG="$KUBECONFIG"
        print_status "Using kubeconfig: $KUBECONFIG"
    fi
    
    if [ -n "$CONTEXT" ]; then
        kubectl config use-context "$CONTEXT"
        print_success "Switched to context: $CONTEXT"
    fi
    
    # Verify connection
    kubectl cluster-info --request-timeout=10s > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_success "Connected to Kubernetes cluster"
    else
        print_error "Failed to connect to Kubernetes cluster"
        exit 1
    fi
}

# Create namespace
create_namespace() {
    print_status "Creating namespace: $NAMESPACE"
    
    if [ "$DRY_RUN" = "true" ]; then
        kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml
    else
        kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -
        print_success "Namespace created/updated: $NAMESPACE"
    fi
}

# Deploy base infrastructure
deploy_base() {
    print_status "Deploying base infrastructure..."
    
    BASE_DIR="infra/k8s/base"
    
    if [ -d "$BASE_DIR" ]; then
        for file in "$BASE_DIR"/*.yaml; do
            if [ -f "$file" ]; then
                print_status "Applying: $(basename "$file")"
                if [ "$DRY_RUN" = "true" ]; then
                    kubectl apply -f "$file" --dry-run=client
                else
                    kubectl apply -f "$file"
                fi
            fi
        done
        print_success "Base infrastructure deployed"
    else
        print_warning "Base infrastructure directory not found: $BASE_DIR"
    fi
}

# Deploy model service
deploy_model_service() {
    print_status "Deploying model service..."
    
    PRODUCTION_DIR="infra/k8s/overlays/production"
    
    if [ -d "$PRODUCTION_DIR" ]; then
        for file in "$PRODUCTION_DIR"/*.yaml; do
            if [ -f "$file" ]; then
                print_status "Applying: $(basename "$file")"
                if [ "$DRY_RUN" = "true" ]; then
                    kubectl apply -f "$file" --dry-run=client
                else
                    kubectl apply -f "$file"
                fi
            fi
        done
        print_success "Model service deployed"
    else
        print_warning "Production overlay directory not found: $PRODUCTION_DIR"
    fi
}

# Wait for deployment
wait_for_deployment() {
    if [ "$WAIT" = "true" ] && [ "$DRY_RUN" = "false" ]; then
        print_status "Waiting for deployment to be ready..."
        
        # Wait for model service deployment
        kubectl wait --for=condition=available --timeout=300s deployment/model-service -n "$NAMESPACE" || {
            print_warning "Deployment did not become ready within timeout"
        }
        
        # Wait for Prometheus deployment
        kubectl wait --for=condition=available --timeout=300s deployment/prometheus -n "$NAMESPACE" || {
            print_warning "Prometheus deployment did not become ready within timeout"
        }
        
        # Wait for Grafana deployment
        kubectl wait --for=condition=available --timeout=300s deployment/grafana -n "$NAMESPACE" || {
            print_warning "Grafana deployment did not become ready within timeout"
        }
        
        print_success "Deployment is ready"
    fi
}

# Show deployment status
show_status() {
    print_status "Deployment status:"
    
    echo ""
    echo "Namespaces:"
    kubectl get namespaces | grep "$NAMESPACE" || echo "  No namespace found"
    
    echo ""
    echo "Pods:"
    kubectl get pods -n "$NAMESPACE" || echo "  No pods found"
    
    echo ""
    echo "Services:"
    kubectl get services -n "$NAMESPACE" || echo "  No services found"
    
    echo ""
    echo "Deployments:"
    kubectl get deployments -n "$NAMESPACE" || echo "  No deployments found"
}

# Show access information
show_access_info() {
    print_status "Access information:"
    
    # Get service information
    MODEL_SERVICE_IP=$(kubectl get service model-service -n "$NAMESPACE" -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
    MODEL_SERVICE_PORT=$(kubectl get service model-service -n "$NAMESPACE" -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || echo "8000")
    
    if [ -n "$MODEL_SERVICE_IP" ]; then
        echo "  Model Service: http://$MODEL_SERVICE_IP:$MODEL_SERVICE_PORT"
        echo "  API Docs: http://$MODEL_SERVICE_IP:$MODEL_SERVICE_PORT/docs"
        echo "  Health: http://$MODEL_SERVICE_IP:$MODEL_SERVICE_PORT/health"
        echo "  Metrics: http://$MODEL_SERVICE_IP:$MODEL_SERVICE_PORT/metrics"
    else
        echo "  Model Service: Use 'kubectl port-forward' to access locally"
        echo "  Port forward: kubectl port-forward service/model-service 8000:8000 -n $NAMESPACE"
    fi
    
    # Get Grafana information
    GRAFANA_IP=$(kubectl get service grafana -n "$NAMESPACE" -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
    GRAFANA_PORT=$(kubectl get service grafana -n "$NAMESPACE" -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || echo "3000")
    
    if [ -n "$GRAFANA_IP" ]; then
        echo "  Grafana: http://$GRAFANA_IP:$GRAFANA_PORT"
    else
        echo "  Grafana: Use 'kubectl port-forward' to access locally"
        echo "  Port forward: kubectl port-forward service/grafana 3000:3000 -n $NAMESPACE"
    fi
}

# Main execution
main() {
    print_status "Starting deployment process..."
    
    # Check kubectl
    check_kubectl
    
    # Setup kubectl
    setup_kubectl
    
    # Create namespace
    create_namespace
    
    # Deploy base infrastructure
    deploy_base
    
    # Deploy model service
    deploy_model_service
    
    # Wait for deployment
    wait_for_deployment
    
    # Show status
    show_status
    
    # Show access information
    show_access_info
    
    print_success "Deployment completed successfully!"
}

# Run main function
main
