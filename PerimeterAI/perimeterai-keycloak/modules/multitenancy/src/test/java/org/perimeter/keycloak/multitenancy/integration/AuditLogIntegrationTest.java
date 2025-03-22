package org.perimeter.keycloak.multitenancy.integration;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.keycloak.models.KeycloakSession;
import org.perimeter.keycloak.multitenancy.model.AuditLog;
import org.perimeter.keycloak.multitenancy.model.Tenant;
import org.perimeter.keycloak.multitenancy.repository.AuditRepository;
import org.perimeter.keycloak.multitenancy.service.AuditService;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class AuditLogIntegrationTest extends BaseIntegrationTest {
    
    private AuditRepository auditRepository;
    private AuditService auditService;
    private Tenant testTenant;
    
    @BeforeEach
    void setUp() {
        KeycloakSession session = getKeycloakSession();
        auditRepository = new AuditRepository(session);
        auditService = new AuditService(session);
        
        // Create a test tenant
        testTenant = createTestTenant();
    }
    
    @Test
    void testAuditLogCreation() {
        // When
        auditService.logTenantEvent("TENANT_CREATED", testTenant, "test-admin", 
            Map.of("details", "Test tenant creation"));
        
        // Then
        List<AuditLog> logs = auditRepository.findByTenant(testTenant);
        assertFalse(logs.isEmpty());
        AuditLog log = logs.get(0);
        assertEquals("TENANT_CREATED", log.getEventType().getName());
        assertEquals("test-admin", log.getActorId());
        assertNotNull(log.getTimestamp());
    }
    
    @Test
    void testAuditLogPagination() {
        // Given
        for (int i = 0; i < 25; i++) {
            auditService.logTenantEvent("TENANT_UPDATED", testTenant, "test-admin", 
                Map.of("update", "Update " + i));
        }
        
        // When
        List<AuditLog> firstPage = auditRepository.findByTenantIdPaginated(
            testTenant.getId(), null, null, 0, 10);
        List<AuditLog> secondPage = auditRepository.findByTenantIdPaginated(
            testTenant.getId(), null, null, 1, 10);
        
        // Then
        assertEquals(10, firstPage.size());
        assertEquals(10, secondPage.size());
        assertNotEquals(firstPage.get(0).getId(), secondPage.get(0).getId());
    }
    
    @Test
    void testAuditLogRetention() {
        // Given
        LocalDateTime oldDate = LocalDateTime.now().minusDays(400);
        AuditLog oldLog = createAuditLog(oldDate);
        AuditLog recentLog = createAuditLog(LocalDateTime.now());
        
        // When
        int deletedCount = auditService.executeRetentionPolicy(365);
        
        // Then
        assertTrue(deletedCount > 0);
        assertNull(auditRepository.findById(oldLog.getId()).orElse(null));
        assertNotNull(auditRepository.findById(recentLog.getId()).orElse(null));
    }
    
    @Test
    void testAuditLogSearch() {
        // Given
        String actorId = "search-test-admin";
        auditService.logTenantEvent("TENANT_CREATED", testTenant, actorId, null);
        auditService.logTenantEvent("TENANT_UPDATED", testTenant, actorId, null);
        
        // When
        List<AuditLog> logs = auditRepository.findByActorIdPaginated(actorId, 0, 10);
        
        // Then
        assertEquals(2, logs.size());
        assertEquals(actorId, logs.get(0).getActorId());
    }
    
    @Test
    void testAuditLogDateRange() {
        // Given
        LocalDateTime start = LocalDateTime.now().minusDays(1);
        LocalDateTime end = LocalDateTime.now().plusDays(1);
        
        auditService.logTenantEvent("TENANT_CREATED", testTenant, "test-admin", null);
        
        // When
        List<AuditLog> logs = auditRepository.findByTenantIdPaginated(
            testTenant.getId(), start, end, 0, 10);
        
        // Then
        assertFalse(logs.isEmpty());
        assertTrue(logs.get(0).getTimestamp().isAfter(start));
        assertTrue(logs.get(0).getTimestamp().isBefore(end));
    }
    
    private Tenant createTestTenant() {
        Tenant tenant = new Tenant();
        tenant.setId(UUID.randomUUID().toString());
        tenant.setName("Test Tenant");
        tenant.setAdminEmail("admin@test.com");
        tenant.setStatus(Tenant.TenantStatus.ACTIVE);
        return tenant;
    }
    
    private AuditLog createAuditLog(LocalDateTime timestamp) {
        AuditLog log = new AuditLog();
        log.setId(UUID.randomUUID().toString());
        log.setTenant(testTenant);
        log.setEventType(auditRepository.findEventTypeByName("TENANT_CREATED").get());
        log.setActorId("test-admin");
        log.setActorType("ADMIN");
        log.setTimestamp(timestamp);
        return auditRepository.create(log);
    }
}
