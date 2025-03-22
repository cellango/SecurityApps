module.controller('TenantCtrl', function($scope, $http, Notifications, Dialog) {
    $scope.tenants = [];
    $scope.tenant = {};
    $scope.showTenantForm = false;
    $scope.editMode = false;

    // Load tenants
    $scope.loadTenants = function() {
        $http.get(authUrl + '/admin/realms/' + realm.realm + '/tenants')
            .then(function(response) {
                $scope.tenants = response.data;
            })
            .catch(function(error) {
                Notifications.error('Error loading tenants: ' + error.data.errorMessage);
            });
    };

    // Show add tenant form
    $scope.showAddTenant = function() {
        $scope.tenant = {
            status: 'active'
        };
        $scope.showTenantForm = true;
        $scope.editMode = false;
    };

    // Edit tenant
    $scope.editTenant = function(tenant) {
        $scope.tenant = angular.copy(tenant);
        $scope.showTenantForm = true;
        $scope.editMode = true;
    };

    // Save tenant
    $scope.saveTenant = function() {
        if ($scope.editMode) {
            $http.put(authUrl + '/admin/realms/' + realm.realm + '/tenants/' + $scope.tenant.id, $scope.tenant)
                .then(function() {
                    Notifications.success('Tenant updated successfully');
                    $scope.loadTenants();
                    $scope.cancelEdit();
                })
                .catch(function(error) {
                    Notifications.error('Error updating tenant: ' + error.data.errorMessage);
                });
        } else {
            $http.post(authUrl + '/admin/realms/' + realm.realm + '/tenants', $scope.tenant)
                .then(function() {
                    Notifications.success('Tenant created successfully');
                    $scope.loadTenants();
                    $scope.cancelEdit();
                })
                .catch(function(error) {
                    Notifications.error('Error creating tenant: ' + error.data.errorMessage);
                });
        }
    };

    // Delete tenant
    $scope.deleteTenant = function(tenant) {
        Dialog.confirmDelete(tenant.name, 'tenant', function() {
            $http.delete(authUrl + '/admin/realms/' + realm.realm + '/tenants/' + tenant.id)
                .then(function() {
                    Notifications.success('Tenant deleted successfully');
                    $scope.loadTenants();
                })
                .catch(function(error) {
                    Notifications.error('Error deleting tenant: ' + error.data.errorMessage);
                });
        });
    };

    // Cancel edit/add
    $scope.cancelEdit = function() {
        $scope.tenant = {};
        $scope.showTenantForm = false;
        $scope.editMode = false;
    };

    // Initial load
    $scope.loadTenants();
});
