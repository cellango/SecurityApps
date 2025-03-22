package org.perimeter.keycloak.multitenancy.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.keycloak.models.KeycloakSession;
import org.perimeter.keycloak.multitenancy.model.AuditEventType;
import org.perimeter.keycloak.multitenancy.model.AuditLog;
import org.perimeter.keycloak.multitenancy.model.Tenant;
import org.perimeter.keycloak.multitenancy.repository.AuditRepository;

import javax.ws.rs.core.HttpHeaders;
import java.util.Timer;
import java.util.TimerTask;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import java.time.LocalDateTime;

public class AuditService {
    private final KeycloakSession session;
    private final AuditRepository auditRepository;
    private final ObjectMapper objectMapper;

    public AuditService(KeycloakSession session) {
        this.session = session;
        this.auditRepository = new AuditRepository(session);
        this.objectMapper = new ObjectMapper();
    }

    public void logTenantEvent(String eventTypeName, Tenant tenant, String actorId, Object details) {
        try {
            AuditLog auditLog = new AuditLog();
            auditLog.setId(UUID.randomUUID().toString());
            
            // Set event type
            AuditEventType eventType = auditRepository.findEventTypeByName(eventTypeName)
                .orElseThrow(() -> new IllegalArgumentException("Invalid event type: " + eventTypeName));
            auditLog.setEventType(eventType);
            
            // Set tenant and actor information
            auditLog.setTenant(tenant);
            auditLog.setActorId(actorId);
            auditLog.setActorType(determineActorType(actorId));
            
            // Set request details
            HttpHeaders headers = session.getContext().getRequestHeaders();
            if (headers != null) {
                auditLog.setIpAddress(session.getContext().getConnection().getRemoteAddr());
                auditLog.setUserAgent(headers.getHeaderString("User-Agent"));
            }
            
            // Set event details
            if (details != null) {
                auditLog.setDetails(objectMapper.writeValueAsString(details));
            }
            
            auditRepository.create(auditLog);
        } catch (Exception e) {
            throw new RuntimeException("Failed to create audit log", e);
        }
    }

    private String determineActorType(String actorId) {
        // Implement logic to determine if actor is admin, user, system, etc.
        if (actorId.startsWith("system-")) {
            return "SYSTEM";
        } else if (actorId.startsWith("admin-")) {
            return "ADMIN";
        } else {
            return "USER";
        }
    }

    public int executeRetentionPolicy(int retentionDays) {
        LocalDateTime cutoffDate = LocalDateTime.now().minusDays(retentionDays);
        return auditRepository.deleteAuditLogsBefore(cutoffDate);
    }

    public void scheduleRetentionPolicy(int retentionDays) {
        // Schedule daily retention policy execution
        Timer timer = new Timer(true);
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                try {
                    executeRetentionPolicy(retentionDays);
                } catch (Exception e) {
                    // Log error but don't stop the timer
                    e.printStackTrace();
                }
            }
        }, 0, TimeUnit.DAYS.toMillis(1));
    }
}
