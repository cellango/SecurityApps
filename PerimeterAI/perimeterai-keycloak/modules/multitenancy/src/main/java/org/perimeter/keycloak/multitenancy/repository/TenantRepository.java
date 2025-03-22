package org.perimeter.keycloak.multitenancy.repository;

import org.keycloak.connections.jpa.JpaConnectionProvider;
import org.keycloak.models.KeycloakSession;
import org.perimeter.keycloak.multitenancy.model.Tenant;

import javax.persistence.EntityManager;
import javax.persistence.TypedQuery;
import java.util.List;
import java.util.Optional;

public class TenantRepository {
    private final EntityManager em;

    public TenantRepository(KeycloakSession session) {
        this.em = session.getProvider(JpaConnectionProvider.class).getEntityManager();
    }

    public Tenant create(Tenant tenant) {
        em.persist(tenant);
        return tenant;
    }

    public Optional<Tenant> findById(String id) {
        return Optional.ofNullable(em.find(Tenant.class, id));
    }

    public Optional<Tenant> findByRealmId(String realmId) {
        TypedQuery<Tenant> query = em.createQuery(
            "SELECT t FROM Tenant t WHERE t.realmId = :realmId", Tenant.class);
        query.setParameter("realmId", realmId);
        List<Tenant> results = query.getResultList();
        return results.isEmpty() ? Optional.empty() : Optional.of(results.get(0));
    }

    public List<Tenant> findAll() {
        return em.createQuery("SELECT t FROM Tenant t", Tenant.class)
                 .getResultList();
    }

    public Tenant update(Tenant tenant) {
        return em.merge(tenant);
    }

    public void delete(String id) {
        findById(id).ifPresent(tenant -> {
            tenant.setStatus(Tenant.TenantStatus.DELETED);
            update(tenant);
        });
    }

    public List<Tenant> findByStatus(Tenant.TenantStatus status) {
        TypedQuery<Tenant> query = em.createQuery(
            "SELECT t FROM Tenant t WHERE t.status = :status", Tenant.class);
        query.setParameter("status", status);
        return query.getResultList();
    }
}
