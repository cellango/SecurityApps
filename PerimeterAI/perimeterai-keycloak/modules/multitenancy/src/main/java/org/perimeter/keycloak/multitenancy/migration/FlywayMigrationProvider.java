package org.perimeter.keycloak.multitenancy.migration;

import org.flywaydb.core.Flyway;
import org.keycloak.Config;
import org.keycloak.connections.jpa.JpaConnectionProvider;
import org.keycloak.models.KeycloakSession;
import org.keycloak.models.KeycloakSessionFactory;
import org.keycloak.provider.Provider;
import org.keycloak.provider.ProviderFactory;

import javax.sql.DataSource;

public class FlywayMigrationProvider implements Provider {
    private final KeycloakSession session;

    public FlywayMigrationProvider(KeycloakSession session) {
        this.session = session;
    }

    public void migrate() {
        JpaConnectionProvider jpaProvider = session.getProvider(JpaConnectionProvider.class);
        DataSource dataSource = jpaProvider.getDataSource();

        Flyway flyway = Flyway.configure()
            .dataSource(dataSource)
            .locations("db/migration")
            .baselineOnMigrate(true)
            .load();

        flyway.migrate();
    }

    @Override
    public void close() {
    }

    public static class Factory implements ProviderFactory<FlywayMigrationProvider> {
        @Override
        public FlywayMigrationProvider create(KeycloakSession session) {
            return new FlywayMigrationProvider(session);
        }

        @Override
        public void init(Config.Scope config) {
        }

        @Override
        public void postInit(KeycloakSessionFactory factory) {
            // Run migrations on startup
            KeycloakSession session = factory.create();
            try {
                session.getTransactionManager().begin();
                FlywayMigrationProvider provider = session.getProvider(FlywayMigrationProvider.class);
                provider.migrate();
                session.getTransactionManager().commit();
            } catch (Exception e) {
                session.getTransactionManager().rollback();
                throw new RuntimeException("Failed to run Flyway migrations", e);
            } finally {
                session.close();
            }
        }

        @Override
        public void close() {
        }

        @Override
        public String getId() {
            return "flyway";
        }
    }
}
