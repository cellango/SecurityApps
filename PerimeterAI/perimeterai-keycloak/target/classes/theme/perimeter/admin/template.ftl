<![CDATA[<#macro mainLayout active bodyClass>
<!DOCTYPE html>
<html>
<head>
    <title>${msg("consoleTitle")}</title>
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta name="robots" content="noindex, nofollow">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="${resourceUrl}/img/favicon.ico">

    <script>
        var authServerUrl = '${authServerUrl}';
        var resourceUrl = '${resourceUrl}';
        var consoleBaseUrl = '${consoleBaseUrl}';
        var masterRealm = '${masterRealm}';
        var resourceVersion = '${resourceVersion}';
    </script>

    <!-- Base UI -->
    <link rel="stylesheet" href="${resourceCommonUrl}/node_modules/patternfly/dist/css/patternfly.min.css">
    <link rel="stylesheet" href="${resourceCommonUrl}/node_modules/patternfly/dist/css/patternfly-additions.min.css">
    <link rel="stylesheet" href="${resourceCommonUrl}/lib/pficon/pficon.css">
    <link rel="stylesheet" href="${resourceUrl}/css/perimeter.css">

    <!-- Angular -->
    <script src="${resourceCommonUrl}/node_modules/jquery/dist/jquery.min.js"></script>
    <script src="${resourceCommonUrl}/node_modules/angular/angular.min.js"></script>
    <script src="${resourceCommonUrl}/node_modules/angular-resource/angular-resource.min.js"></script>
    <script src="${resourceCommonUrl}/node_modules/angular-route/angular-route.min.js"></script>
    <script src="${resourceCommonUrl}/node_modules/angular-cookies/angular-cookies.min.js"></script>
    <script src="${resourceCommonUrl}/node_modules/angular-sanitize/angular-sanitize.min.js"></script>
    <script src="${resourceCommonUrl}/node_modules/angular-translate/dist/angular-translate.min.js"></script>
    <script src="${resourceCommonUrl}/node_modules/angular-translate-loader-url/angular-translate-loader-url.min.js"></script>
    <script src="${resourceCommonUrl}/node_modules/angular-ui-bootstrap/dist/ui-bootstrap-tpls.js"></script>
    <script src="${resourceCommonUrl}/node_modules/filesaver/FileSaver.js"></script>

    <!-- Keycloak -->
    <script src="${authServerUrl}/js/keycloak.js"></script>
    <script src="${resourceCommonUrl}/lib/keycloak.js"></script>

    <script>
        var module = angular.module('tenant', ['ngRoute', 'ngResource', 'keycloak']);
        var resourceUrl = '${resourceUrl}';
        var authUrl = '${authUrl}';
        var consoleBaseUrl = '${consoleBaseUrl}';
    </script>

    <#if properties.scripts?has_content>
        <#list properties.scripts?split(' ') as script>
            <script src="${resourceUrl}/${script}" type="text/javascript"></script>
        </#list>
    </#if>
</head>
<body class="${bodyClass}">
    <div id="wrapper" class="wrapper">
        <!-- Navigation -->
        <div class="navbar navbar-default navbar-pf" role="navigation">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="#/">
                    <h1>Keycloak Admin Console</h1>
                </a>
            </div>
            <div class="collapse navbar-collapse">
                <ul class="nav navbar-nav navbar-utility">
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            <span class="pficon pficon-user"></span>
                            ${msg("loggedInAs")} <strong>${auth.user.displayName}</strong> <b class="caret"></b>
                        </a>
                        <ul class="dropdown-menu">
                            <li><a href="#/account">Manage Account</a></li>
                            <li><a href="#/signout">Sign Out</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>

        <div class="container-fluid">
            <div class="row">
                <div class="col-sm-3 col-md-2 sidebar-pf sidebar-pf-left">
                    <div class="realm-selector">
                        <h2><span>Realm:</span> ${realm.name}</h2>
                    </div>
                    <div class="nav-category">
                        <h2>Configure</h2>
                        <ul class="nav nav-pills nav-stacked">
                            <li class="nav-item">
                                <a href="#/realms/${realm.realm}/tenant" class="nav-link">
                                    <span class="pficon pficon-users"></span>
                                    <span class="list-group-item-value">Tenant Management</span>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="col-sm-9 col-md-10 col-sm-push-3 col-md-push-2">
                    <#nested "content">
                </div>
            </div>
        </div>
    </div>

    <!-- Custom Scripts -->
    <script src="${resourceUrl}/js/app.js"></script>
    <script src="${resourceUrl}/js/controllers.js"></script>
</body>
</html>
</#macro>]]>
