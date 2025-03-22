provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "perimeter-${var.environment}-rg"
  location = var.region
}

resource "azurerm_kubernetes_cluster" "main" {
  name                = var.cluster_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "perimeter-${var.environment}"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }
}
