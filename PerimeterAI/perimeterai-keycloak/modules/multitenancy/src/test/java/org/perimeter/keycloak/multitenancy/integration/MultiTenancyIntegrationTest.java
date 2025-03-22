package org.perimeter.keycloak.multitenancy.integration;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.keycloak.models.KeycloakSession;
import org.perimeter.keycloak.multitenancy.model.Tenant;
import org.perimeter.keycloak.multitenancy.repository.TenantRepository;
import org.perimeter.keycloak.multitenancy.service.AuditService;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class MultiTenancyIntegrationTest extends BaseIntegrationTest {
    
    private TenantRepository tenantRepository;
    private AuditService auditService;
    
    @BeforeEach
    void setUp() {
        KeycloakSession session = getKeycloakSession();
        tenantRepository = new TenantRepository(session);
        auditService = new AuditService(session);
    }
    
    @Test
    void testCreateTenant() {
        // Given
        Tenant tenant = new Tenant();
        tenant.setId(UUID.randomUUID().toString());
        tenant.setName("Test Tenant");
        tenant.setAdminEmail("admin@test.com");
        tenant.setStatus(Tenant.TenantStatus.ACTIVE);
        
        // When
        Tenant createdTenant = tenantRepository.create(tenant);
        
        // Then
        assertNotNull(createdTenant.getId());
        assertEquals("Test Tenant", createdTenant.getName());
        assertEquals(Tenant.TenantStatus.ACTIVE, createdTenant.getStatus());
        
        // Verify audit log
        auditService.logTenantEvent("TENANT_CREATED", createdTenant, "test-admin", null);
    }
    
    @Test
    void testUpdateTenant() {
        // Given
        Tenant tenant = createTestTenant();
        
        // When
        tenant.setName("Updated Tenant");
        Tenant updatedTenant = tenantRepository.update(tenant);
        
        // Then
        assertEquals("Updated Tenant", updatedTenant.getName());
        
        // Verify audit log
        auditService.logTenantEvent("TENANT_UPDATED", updatedTenant, "test-admin", null);
    }
    
    @Test
    void testDeleteTenant() {
        // Given
        Tenant tenant = createTestTenant();
        
        // When
        tenantRepository.delete(tenant.getId());
        
        // Then
        Tenant deletedTenant = tenantRepository.findById(tenant.getId()).orElse(null);
        assertNotNull(deletedTenant);
        assertEquals(Tenant.TenantStatus.DELETED, deletedTenant.getStatus());
        
        // Verify audit log
        auditService.logTenantEvent("TENANT_DELETED", deletedTenant, "test-admin", null);
    }
    
    private Tenant createTestTenant() {
        Tenant tenant = new Tenant();
        tenant.setId(UUID.randomUUID().toString());
        tenant.setName("Test Tenant");
        tenant.setAdminEmail("admin@test.com");
        tenant.setStatus(Tenant.TenantStatus.ACTIVE);
        return tenantRepository.create(tenant);
    }
}
