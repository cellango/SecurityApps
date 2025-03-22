var module = angular.module('tenant');

module.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/realms/:realm/tenant', {
            templateUrl: resourceUrl + '/partials/tenant.html',
            controller: 'TenantCtrl',
            resolve: {
                realm: function(RealmLoader) {
                    return RealmLoader();
                }
            }
        });
}]);

module.controller('TenantCtrl', function($scope, realm, $http) {
    $scope.realm = realm;
    $scope.tenants = [];

    $scope.loadTenants = function() {
        $http.get(authUrl + '/admin/realms/' + realm.realm + '/tenants')
            .then(function(response) {
                $scope.tenants = response.data;
            });
    };

    $scope.createTenant = function(tenant) {
        $http.post(authUrl + '/admin/realms/' + realm.realm + '/tenants', tenant)
            .then(function() {
                $scope.loadTenants();
                Notifications.success('Tenant created successfully.');
            });
    };

    $scope.updateTenant = function(tenant) {
        $http.put(authUrl + '/admin/realms/' + realm.realm + '/tenants/' + tenant.id, tenant)
            .then(function() {
                $scope.loadTenants();
                Notifications.success('Tenant updated successfully.');
            });
    };

    $scope.deleteTenant = function(tenant) {
        $http.delete(authUrl + '/admin/realms/' + realm.realm + '/tenants/' + tenant.id)
            .then(function() {
                $scope.loadTenants();
                Notifications.success('Tenant deleted successfully.');
            });
    };

    $scope.loadTenants();
});

module.config(function($provide) {
    $provide.decorator('RealmTabsCtrl', function($delegate) {
        var oldBuildTabs = $delegate.prototype.buildTabs;
        $delegate.prototype.buildTabs = function() {
            var tabs = oldBuildTabs.call(this);
            tabs.push({
                id: 'tenant',
                href: '#/realms/' + this.realm.realm + '/tenant',
                name: 'Tenant Management',
                show: true
            });
            return tabs;
        };
        return $delegate;
    });
});
