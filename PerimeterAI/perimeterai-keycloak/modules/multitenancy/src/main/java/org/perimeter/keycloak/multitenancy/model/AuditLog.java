package org.perimeter.keycloak.multitenancy.model;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "audit_log")
public class AuditLog {
    
    @Id
    private String id;
    
    @ManyToOne
    @JoinColumn(name = "event_type_id", nullable = false)
    private AuditEventType eventType;
    
    @ManyToOne
    @JoinColumn(name = "tenant_id", nullable = false)
    private Tenant tenant;
    
    @Column(name = "actor_id", nullable = false)
    private String actorId;
    
    @Column(name = "actor_type", nullable = false)
    private String actorType;
    
    @Column(nullable = false)
    private LocalDateTime timestamp;
    
    @Column(columnDefinition = "jsonb")
    private String details;
    
    @Column(name = "ip_address")
    private String ipAddress;
    
    @Column(name = "user_agent")
    private String userAgent;

    @PrePersist
    protected void onCreate() {
        timestamp = LocalDateTime.now();
    }

    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public AuditEventType getEventType() { return eventType; }
    public void setEventType(AuditEventType eventType) { this.eventType = eventType; }
    
    public Tenant getTenant() { return tenant; }
    public void setTenant(Tenant tenant) { this.tenant = tenant; }
    
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
