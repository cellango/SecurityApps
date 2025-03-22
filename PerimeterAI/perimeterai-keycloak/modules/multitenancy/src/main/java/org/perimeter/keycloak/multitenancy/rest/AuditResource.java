package org.perimeter.keycloak.multitenancy.rest;

import org.keycloak.models.KeycloakSession;
import org.keycloak.services.resources.admin.AdminAuth;
import org.perimeter.keycloak.multitenancy.model.AuditLog;
import org.perimeter.keycloak.multitenancy.repository.AuditRepository;
import org.perimeter.keycloak.multitenancy.service.AuditService;

import javax.ws.rs.*;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.stream.Collectors;

@Path("/audit")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class AuditResource {

    private final KeycloakSession session;
    private final AdminAuth auth;
    private final AuditRepository auditRepository;
    private final AuditService auditService;

    public AuditResource(@Context KeycloakSession session, AdminAuth auth) {
        this.session = session;
        this.auth = auth;
        this.auditRepository = new AuditRepository(session);
        this.auditService = new AuditService(session);
    }

    @GET
    @Path("/tenant/{tenantId}")
    public Response getAuditLogsByTenant(
            @PathParam("tenantId") String tenantId,
            @QueryParam("from") String fromDate,
            @QueryParam("to") String toDate,
            @QueryParam("page") @DefaultValue("0") int page,
            @QueryParam("size") @DefaultValue("20") int size) {
        
        validateAdminAccess();

        LocalDateTime from = fromDate != null ? LocalDateTime.parse(fromDate, DateTimeFormatter.ISO_DATE_TIME) : null;
        LocalDateTime to = toDate != null ? LocalDateTime.parse(toDate, DateTimeFormatter.ISO_DATE_TIME) : null;

        List<AuditLogRepresentation> logs = auditRepository.findByTenantIdPaginated(
                tenantId, from, to, page, size).stream()
                .map(this::toRepresentation)
                .collect(Collectors.toList());

        return Response.ok(logs).build();
    }

    @GET
    @Path("/actor/{actorId}")
    public Response getAuditLogsByActor(
            @PathParam("actorId") String actorId,
            @QueryParam("from") String fromDate,
            @QueryParam("to") String toDate,
            @QueryParam("page") @DefaultValue("0") int page,
            @QueryParam("size") @DefaultValue("20") int size) {
        
        validateAdminAccess();

        List<AuditLogRepresentation> logs = auditRepository.findByActorIdPaginated(
                actorId, page, size).stream()
                .map(this::toRepresentation)
                .collect(Collectors.toList());

        return Response.ok(logs).build();
    }

    @GET
    @Path("/event-type/{eventType}")
    public Response getAuditLogsByEventType(
            @PathParam("eventType") String eventType,
            @QueryParam("from") String fromDate,
            @QueryParam("to") String toDate,
            @QueryParam("page") @DefaultValue("0") int page,
            @QueryParam("size") @DefaultValue("20") int size) {
        
        validateAdminAccess();

        List<AuditLogRepresentation> logs = auditRepository.findByEventTypePaginated(
                eventType, page, size).stream()
                .map(this::toRepresentation)
                .collect(Collectors.toList());

        return Response.ok(logs).build();
    }

    @DELETE
    @Path("/retention/execute")
    public Response executeRetentionPolicy(
            @QueryParam("retentionDays") @DefaultValue("365") int retentionDays) {
        
        validateAdminAccess();

        int deletedCount = auditService.executeRetentionPolicy(retentionDays);
        
        return Response.ok(new RetentionResult(deletedCount)).build();
    }

    private void validateAdminAccess() {
        if (!auth.hasRealmRole("admin")) {
            throw new ForbiddenException("Requires admin role");
        }
    }

    private AuditLogRepresentation toRepresentation(AuditLog auditLog) {
        AuditLogRepresentation rep = new AuditLogRepresentation();
        rep.setId(auditLog.getId());
        rep.setEventType(auditLog.getEventType().getName());
        rep.setTenantId(auditLog.getTenant().getId());
        rep.setActorId(auditLog.getActorId());
        rep.setActorType(auditLog.getActorType());
        rep.setTimestamp(auditLog.getTimestamp());
        rep.setDetails(auditLog.getDetails());
        rep.setIpAddress(auditLog.getIpAddress());
        rep.setUserAgent(auditLog.getUserAgent());
        return rep;
    }

    public static class AuditLogRepresentation {
        private String id;
        private String eventType;
        private String tenantId;
        private String actorId;
        private String actorType;
        private LocalDateTime timestamp;
        private String details;
        private String ipAddress;
        private String userAgent;

        // Getters and setters
        public String getId() { return id; }
        public void setId(String id) { this.id = id; }
        
        public String getEventType() { return eventType; }
        public void setEventType(String eventType) { this.eventType = eventType; }
        
        public String getTenantId() { return tenantId; }
        public void setTenantId(String tenantId) { this.tenantId = tenantId; }
        
        public String getActorId() { return actorId; }
        public void setActorId(String actorId) { this.actorId = actorId; }
        
        public String getActorType() { return actorType; }
        public void setActorType(String actorType) { this.actorType = actorType; }
        
        public LocalDateTime getTimestamp() { return timestamp; }
        public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }
        
        public String getDetails() { return details; }
        public void setDetails(String details) { this.details = details; }
        
        public String getIpAddress() { return ipAddress; }
        public void setIpAddress(String ipAddress) { this.ipAddress = ipAddress; }
        
        public String getUserAgent() { return userAgent; }
        public void setUserAgent(String userAgent) { this.userAgent = userAgent; }
    }

    public static class RetentionResult {
        private final int deletedCount;

        public RetentionResult(int deletedCount) {
            this.deletedCount = deletedCount;
        }

        public int getDeletedCount() {
            return deletedCount;
        }
    }
}
