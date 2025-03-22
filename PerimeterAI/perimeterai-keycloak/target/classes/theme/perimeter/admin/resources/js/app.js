// Initialize the tenant module with dependencies
var module = angular.module('tenant', ['ngRoute', 'ngResource', 'keycloak']);

// Configure routes
module.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/realms/:realm/tenant', {
            templateUrl: resourceUrl + '/partials/tenant-management.html',
            controller: 'TenantCtrl',
            resolve: {
                realm: function(RealmLoader) {
                    return RealmLoader();
                }
            }
        });
}]);

// Configure realm tabs
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
