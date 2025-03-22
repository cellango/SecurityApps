-- Audit Event Types
CREATE TABLE audit_event_type (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Insert default event types
INSERT INTO audit_event_type (id, name, description) VALUES
    ('1', 'TENANT_CREATED', 'A new tenant was created'),
    ('2', 'TENANT_UPDATED', 'Tenant information was updated'),
    ('3', 'TENANT_DELETED', 'Tenant was marked as deleted'),
    ('4', 'TENANT_ACTIVATED', 'Tenant was activated'),
    ('5', 'TENANT_DEACTIVATED', 'Tenant was deactivated'),
    ('6', 'TENANT_CONFIG_UPDATED', 'Tenant configuration was updated');

-- Audit Log
CREATE TABLE audit_log (
    id VARCHAR(36) PRIMARY KEY,
    event_type_id VARCHAR(36) NOT NULL,
    tenant_id VARCHAR(36) NOT NULL,
    actor_id VARCHAR(255) NOT NULL,
    actor_type VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    details JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    CONSTRAINT fk_audit_event_type FOREIGN KEY (event_type_id) REFERENCES audit_event_type(id),
    CONSTRAINT fk_audit_tenant FOREIGN KEY (tenant_id) REFERENCES tenant(id)
);

-- Create indexes for better query performance
CREATE INDEX idx_audit_log_tenant_id ON audit_log(tenant_id);
CREATE INDEX idx_audit_log_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_log_event_type ON audit_log(event_type_id);
