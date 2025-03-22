package org.perimeter.keycloak.multitenancy.repository;

import org.keycloak.connections.jpa.JpaConnectionProvider;
import org.keycloak.models.KeycloakSession;
import org.perimeter.keycloak.multitenancy.model.AuditEventType;
import org.perimeter.keycloak.multitenancy.model.AuditLog;
import org.perimeter.keycloak.multitenancy.model.Tenant;

import javax.persistence.EntityManager;
import javax.persistence.TypedQuery;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public class AuditRepository {
    private final EntityManager em;

    public AuditRepository(KeycloakSession session) {
        this.em = session.getProvider(JpaConnectionProvider.class).getEntityManager();
    }

    public AuditLog create(AuditLog auditLog) {
        em.persist(auditLog);
        return auditLog;
    }

    public Optional<AuditEventType> findEventTypeByName(String name) {
        TypedQuery<AuditEventType> query = em.createQuery(
            "SELECT e FROM AuditEventType e WHERE e.name = :name", AuditEventType.class);
        query.setParameter("name", name);
        List<AuditEventType> results = query.getResultList();
        return results.isEmpty() ? Optional.empty() : Optional.of(results.get(0));
    }

    public List<AuditLog> findByTenant(Tenant tenant) {
        TypedQuery<AuditLog> query = em.createQuery(
            "SELECT a FROM AuditLog a WHERE a.tenant = :tenant ORDER BY a.timestamp DESC", 
            AuditLog.class);
        query.setParameter("tenant", tenant);
        return query.getResultList();
    }

    public List<AuditLog> findByTenantAndDateRange(Tenant tenant, LocalDateTime start, LocalDateTime end) {
        TypedQuery<AuditLog> query = em.createQuery(
            "SELECT a FROM AuditLog a WHERE a.tenant = :tenant " +
            "AND a.timestamp BETWEEN :start AND :end ORDER BY a.timestamp DESC", 
            AuditLog.class);
        query.setParameter("tenant", tenant);
        query.setParameter("start", start);
        query.setParameter("end", end);
        return query.getResultList();
    }

    public List<AuditLog> findByEventType(AuditEventType eventType) {
        TypedQuery<AuditLog> query = em.createQuery(
            "SELECT a FROM AuditLog a WHERE a.eventType = :eventType ORDER BY a.timestamp DESC", 
            AuditLog.class);
        query.setParameter("eventType", eventType);
        return query.getResultList();
    }

    public List<AuditLog> findByActorId(String actorId) {
        TypedQuery<AuditLog> query = em.createQuery(
            "SELECT a FROM AuditLog a WHERE a.actorId = :actorId ORDER BY a.timestamp DESC", 
            AuditLog.class);
        query.setParameter("actorId", actorId);
        return query.getResultList();
    }

    public List<AuditLog> findByTenantIdPaginated(String tenantId, LocalDateTime from, LocalDateTime to, int page, int size) {
        String queryStr = "SELECT a FROM AuditLog a WHERE a.tenant.id = :tenantId";
        if (from != null && to != null) {
            queryStr += " AND a.timestamp BETWEEN :from AND :to";
        }
        queryStr += " ORDER BY a.timestamp DESC";
        
        TypedQuery<AuditLog> query = em.createQuery(queryStr, AuditLog.class);
        query.setParameter("tenantId", tenantId);
        if (from != null && to != null) {
            query.setParameter("from", from);
            query.setParameter("to", to);
        }
        
        query.setFirstResult(page * size);
        query.setMaxResults(size);
        
        return query.getResultList();
    }

    public List<AuditLog> findByActorIdPaginated(String actorId, int page, int size) {
        TypedQuery<AuditLog> query = em.createQuery(
            "SELECT a FROM AuditLog a WHERE a.actorId = :actorId ORDER BY a.timestamp DESC",
            AuditLog.class);
        query.setParameter("actorId", actorId);
        query.setFirstResult(page * size);
        query.setMaxResults(size);
        return query.getResultList();
    }

    public List<AuditLog> findByEventTypePaginated(String eventTypeName, int page, int size) {
        TypedQuery<AuditLog> query = em.createQuery(
            "SELECT a FROM AuditLog a WHERE a.eventType.name = :eventTypeName ORDER BY a.timestamp DESC",
            AuditLog.class);
        query.setParameter("eventTypeName", eventTypeName);
        query.setFirstResult(page * size);
        query.setMaxResults(size);
        return query.getResultList();
    }

    public int deleteAuditLogsBefore(LocalDateTime timestamp) {
        return em.createQuery("DELETE FROM AuditLog a WHERE a.timestamp < :timestamp")
            .setParameter("timestamp", timestamp)
            .executeUpdate();
    }
}
