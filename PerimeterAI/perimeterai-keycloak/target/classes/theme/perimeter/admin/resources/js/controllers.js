module.controller('TenantCtrl', function($scope, $http, realm) {
    $scope.realm = realm;
    $scope.tenants = [];

    // Load tenants
    $scope.loadTenants = function() {
        // Mock data for now
        $scope.tenants = [
            {
                name: 'Tenant 1',
                id: '1',
                description: 'First tenant',
                status: 'Active'
            },
            {
                name: 'Tenant 2',
                id: '2',
                description: 'Second tenant',
                status: 'Active'
            }
        ];
    };

    // Add tenant
    $scope.addTenant = function() {
        var newTenant = {
            name: $scope.newTenant.name,
            id: $scope.newTenant.id,
            description: $scope.newTenant.description,
            status: 'Active'
        };
        $scope.tenants.push(newTenant);
        $scope.newTenant = {};
    };

    // Edit tenant
    $scope.editTenant = function(tenant) {
        tenant.editing = true;
        $scope.editingTenant = angular.copy(tenant);
    };

    // Save tenant
    $scope.saveTenant = function(tenant) {
        var index = $scope.tenants.indexOf(tenant);
        $scope.tenants[index] = angular.copy($scope.editingTenant);
        tenant.editing = false;
    };

    // Delete tenant
    $scope.deleteTenant = function(tenant) {
        var index = $scope.tenants.indexOf(tenant);
        if (index > -1) {
            $scope.tenants.splice(index, 1);
        }
    };

    // Cancel editing
    $scope.cancelEdit = function(tenant) {
        tenant.editing = false;
    };

    // Load tenants on controller initialization
    $scope.loadTenants();
});
