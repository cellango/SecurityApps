#!/bin/bash

# Default values
USE_KUBERNETES=false
ENVIRONMENT="dev"
CLOUD_PROVIDER=""

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -e, --environment <dev|prod>    Specify environment (default: dev)"
    echo "  -k, --kubernetes                Deploy to Kubernetes"
    echo "  -c, --cloud <aws|azure>         Specify cloud provider"
    echo "  -h, --help                      Display this help message"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -k|--kubernetes)
            USE_KUBERNETES=true
            shift
            ;;
        -c|--cloud)
            CLOUD_PROVIDER="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Function to deploy infrastructure
deploy_infrastructure() {
    echo "Deploying infrastructure to $CLOUD_PROVIDER..."
    
    cd devops/terraform
    
    # Initialize Terraform
    terraform init -backend-config="environments/${ENVIRONMENT}/backend.tfvars"
    
    # Apply Terraform configuration
    terraform apply \
        -var-file="environments/${ENVIRONMENT}/terraform.tfvars" \
        -var="cloud_provider=${CLOUD_PROVIDER}" \
        -auto-approve
        
    # Update Ansible inventory
    ./update-inventory.sh ${ENVIRONMENT} ${CLOUD_PROVIDER}
    
    # Run Ansible playbooks
    cd ../ansible
    ansible-playbook -i inventory/${CLOUD_PROVIDER}.yml playbooks/setup-kubernetes.yml
}

# Function for Kubernetes deployment
deploy_kubernetes() {
    echo "Deploying to Kubernetes in $ENVIRONMENT environment on $CLOUD_PROVIDER..."
    
    # Get cluster credentials based on cloud provider
    if [ "$CLOUD_PROVIDER" = "aws" ]; then
        aws eks update-kubeconfig --name perimeter-${ENVIRONMENT}-cluster --region $(terraform output -raw region)
    elif [ "$CLOUD_PROVIDER" = "azure" ]; then
        az aks get-credentials --resource-group perimeter-${ENVIRONMENT}-rg --name perimeter-${ENVIRONMENT}-cluster
    fi
    
    # Apply Kubernetes configurations
    kubectl apply -k kubernetes/overlays/${ENVIRONMENT}
}

# Main deployment logic
if [ -n "$CLOUD_PROVIDER" ]; then
    deploy_infrastructure
fi

if [ "$USE_KUBERNETES" = true ]; then
    deploy_kubernetes
fi
