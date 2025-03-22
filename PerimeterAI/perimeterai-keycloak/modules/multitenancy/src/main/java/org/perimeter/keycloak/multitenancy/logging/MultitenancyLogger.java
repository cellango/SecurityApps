package org.perimeter.keycloak.multitenancy.logging;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.logging.*;

public class MultitenancyLogger {
    private static final Logger LOGGER = Logger.getLogger(MultitenancyLogger.class.getName());
    private static final String LOG_DIR = "/var/log/keycloak/multitenancy";
    private static final String LOG_FILE_PREFIX = "multitenancy";
    private static final int MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
    private static final int MAX_FILES = 10;

    static {
        try {
            setupLogger();
        } catch (IOException e) {
            System.err.println("Failed to setup logger: " + e.getMessage());
        }
    }

    private static void setupLogger() throws IOException {
        // Create log directory if it doesn't exist
        File logDir = new File(LOG_DIR);
        if (!logDir.exists()) {
            logDir.mkdirs();
        }

        // Create file handler
        String pattern = LOG_DIR + "/" + LOG_FILE_PREFIX + "-%g.log";
        FileHandler fileHandler = new FileHandler(pattern, MAX_FILE_SIZE, MAX_FILES, true);
        
        // Create formatter
        Formatter formatter = new Formatter() {
            @Override
            public String format(LogRecord record) {
                LocalDateTime datetime = LocalDateTime.now();
                String timestamp = datetime.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
                return String.format("[%s] %s %s: %s%n",
                    timestamp,
                    record.getLevel(),
                    record.getSourceClassName(),
                    formatMessage(record)
                );
            }
        };

        fileHandler.setFormatter(formatter);
        LOGGER.addHandler(fileHandler);
        LOGGER.setLevel(Level.INFO);
    }

    // Tenant Operations Logging
    public static void logTenantCreation(String tenantId, String adminEmail) {
        LOGGER.info(String.format("Tenant created - ID: %s, Admin: %s", tenantId, adminEmail));
    }

    public static void logTenantUpdate(String tenantId, String field, String oldValue, String newValue) {
        LOGGER.info(String.format("Tenant updated - ID: %s, Field: %s, Old: %s, New: %s",
            tenantId, field, oldValue, newValue));
    }

    public static void logTenantDeletion(String tenantId) {
        LOGGER.info(String.format("Tenant deleted - ID: %s", tenantId));
    }

    // Audit Operations Logging
    public static void logAuditEvent(String eventType, String tenantId, String actorId) {
        LOGGER.info(String.format("Audit event - Type: %s, Tenant: %s, Actor: %s",
            eventType, tenantId, actorId));
    }

    public static void logRetentionExecution(int deletedCount) {
        LOGGER.info(String.format("Retention policy executed - Deleted %d audit logs", deletedCount));
    }

    // Error Logging
    public static void logError(String operation, String error, Throwable throwable) {
        LOGGER.log(Level.SEVERE, String.format("Error in %s: %s", operation, error), throwable);
    }

    // Security Logging
    public static void logSecurityEvent(String eventType, String userId, String resource) {
        LOGGER.warning(String.format("Security event - Type: %s, User: %s, Resource: %s",
            eventType, userId, resource));
    }

    public static void logAccessDenied(String userId, String resource) {
        LOGGER.warning(String.format("Access denied - User: %s, Resource: %s",
            userId, resource));
    }

    // Performance Logging
    public static void logPerformanceMetric(String operation, long durationMs) {
        LOGGER.fine(String.format("Performance - Operation: %s, Duration: %dms",
            operation, durationMs));
    }
}
