package org.perimeter.keycloak.multitenancy;

import org.keycloak.Config;
import org.keycloak.models.KeycloakSession;
import org.keycloak.models.KeycloakSessionFactory;
import org.keycloak.provider.ProviderFactory;

public class MultiTenancyProviderFactory implements ProviderFactory<MultiTenancyProvider> {

    @Override
    public MultiTenancyProvider create(KeycloakSession session) {
        return new MultiTenancyProvider(session);
    }

    @Override
    public void init(Config.Scope config) {
        // Initialize any configuration
    }

    @Override
    public void postInit(KeycloakSessionFactory factory) {
        // Post-initialization tasks
    }

    @Override
    public void close() {
        // Cleanup
    }

    @Override
    public String getId() {
        return "multitenancy";
    }
}
