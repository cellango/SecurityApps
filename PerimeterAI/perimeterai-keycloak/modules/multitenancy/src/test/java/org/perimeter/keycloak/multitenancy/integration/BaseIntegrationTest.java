package org.perimeter.keycloak.multitenancy.integration;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.keycloak.models.KeycloakSession;
import org.keycloak.services.DefaultKeycloakSession;
import org.keycloak.services.DefaultKeycloakSessionFactory;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@Testcontainers
public abstract class BaseIntegrationTest {

    @Container
    private static final PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
        .withDatabaseName("keycloak_test")
        .withUsername("test")
        .withPassword("test");

    private DefaultKeycloakSessionFactory sessionFactory;
    private KeycloakSession session;

    @BeforeEach
    void setUpBase() {
        sessionFactory = new DefaultKeycloakSessionFactory();
        sessionFactory.init();
        session = sessionFactory.create();
        session.getTransactionManager().begin();
    }

    @AfterEach
    void tearDownBase() {
        if (session != null) {
            if (session.getTransactionManager().isActive()) {
                session.getTransactionManager().rollback();
            }
            session.close();
        }
        if (sessionFactory != null) {
            sessionFactory.close();
        }
    }

    protected KeycloakSession getKeycloakSession() {
        return session;
    }

    protected void commitTransaction() {
        session.getTransactionManager().commit();
        session.getTransactionManager().begin();
    }

    protected void rollbackTransaction() {
        session.getTransactionManager().rollback();
        session.getTransactionManager().begin();
    }
}
