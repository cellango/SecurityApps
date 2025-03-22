// Add tenant routes
module.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/realms/:realm/tenant', {
            templateUrl: resourceUrl + '/partials/tenant-list.html',
            controller: 'TenantListCtrl'
        });
}]);
