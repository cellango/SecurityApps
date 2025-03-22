<![CDATA[<!DOCTYPE html>
<html>
<head>
    <title>${msg("consoleTitle")}</title>
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta name="robots" content="noindex, nofollow">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="${resourceUrl}/img/favicon.ico">
    <#if properties.styles?has_content>
        <#list properties.styles?split(' ') as style>
            <link href="${resourceUrl}/${style}" rel="stylesheet"/>
        </#list>
    </#if>
</head>
<body>
    <div id="kc-navigation" class="navbar navbar-default navbar-pf" role="navigation">
        <ul class="nav navbar-nav navbar-primary">
            <li><a href="#/realms/${realm.realm}/tenant">${msg("tenantManagement")}</a></li>
        </ul>
    </div>
    
    <div id="kc-content">
        <div id="kc-content-wrapper">
            <div data-ng-view></div>
        </div>
    </div>

    <script src="${resourceUrl}/js/tenant.js" type="text/javascript"></script>
    <script src="${resourceUrl}/js/routes.js" type="text/javascript"></script>
</body>
</html>]]>
