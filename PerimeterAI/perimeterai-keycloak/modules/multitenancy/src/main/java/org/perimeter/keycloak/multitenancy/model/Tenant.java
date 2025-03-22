package org.perimeter.keycloak.multitenancy.model;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "tenant")
public class Tenant {
    
    @Id
    private String id;
    
    @Column(name = "realm_id", nullable = false, unique = true)
    private String realmId;
    
    @Column(nullable = false)
    private String name;
    
    @Column(name = "admin_email", nullable = false)
    private String adminEmail;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private TenantStatus status;
    
    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;
    
    @Column(columnDefinition = "jsonb")
    private String config;

    // Enum for tenant status
    public enum TenantStatus {
        ACTIVE,
        INACTIVE,
        SUSPENDED,
        DELETED
    }

    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public String getRealmId() { return realmId; }
    public void setRealmId(String realmId) { this.realmId = realmId; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getAdminEmail() { return adminEmail; }
    public void setAdminEmail(String adminEmail) { this.adminEmail = adminEmail; }
    
    public TenantStatus getStatus() { return status; }
    public void setStatus(TenantStatus status) { this.status = status; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    
    public String getConfig() { return config; }
    public void setConfig(String config) { this.config = config; }

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
