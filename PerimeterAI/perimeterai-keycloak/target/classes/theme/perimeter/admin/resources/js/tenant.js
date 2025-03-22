// Tenant Management Controller
module.controller('TenantListCtrl', function($scope, $http) {
    $scope.tenants = [];

    // Load tenants
    $scope.loadTenants = function() {
        $http.get('/auth/admin/realms/' + realm.realm + '/tenants')
            .then(function(response) {
                $scope.tenants = response.data;
            });
    };

    // Add tenant
    $scope.addTenant = function() {
        // Implementation for adding tenant
    };

    // Edit tenant
    $scope.editTenant = function(tenant) {
        // Implementation for editing tenant
    };

    // Delete tenant
    $scope.deleteTenant = function(tenant) {
        // Implementation for deleting tenant
    };

    // Load tenants on controller initialization
    $scope.loadTenants();
});
