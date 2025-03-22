package org.perimeter.keycloak.multitenancy.model;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "audit_event_type")
public class AuditEventType {
    
    @Id
    private String id;
    
    @Column(nullable = false, unique = true)
    private String name;
    
    @Column
    private String description;
    
    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }

    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
