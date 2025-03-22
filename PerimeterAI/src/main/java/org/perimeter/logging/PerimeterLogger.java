package org.perimeter.logging;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.logging.*;

public class PerimeterLogger {
    private static final Logger LOGGER = Logger.getLogger(PerimeterLogger.class.getName());
    private static final String LOG_DIR = "/var/log/perimeterai";
    private static final String LOG_FILE_PREFIX = "perimeterai";
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

        // Create file handler with rotation
        String pattern = LOG_DIR + File.separator + LOG_FILE_PREFIX + "-%g.log";
        FileHandler fileHandler = new FileHandler(pattern, MAX_FILE_SIZE, MAX_FILES, true);
        
        // Create custom formatter
        fileHandler.setFormatter(new Formatter() {
            @Override
            public String format(LogRecord record) {
                LocalDateTime datetime = LocalDateTime.now();
                String timestamp = datetime.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
                return String.format("[%s] [%s] %s - %s%n",
                    timestamp,
                    record.getLevel(),
                    record.getSourceClassName(),
                    formatMessage(record)
                );
            }
        });

        // Add handler to logger
        LOGGER.addHandler(fileHandler);
        LOGGER.setLevel(Level.INFO);
    }

    // Signature Operations
    public static void logSignatureRequest(String documentId, String userId) {
        LOGGER.info(String.format("Signature requested - Document: %s, User: %s", documentId, userId));
    }

    public static void logSignatureComplete(String documentId, String userId) {
        LOGGER.info(String.format("Signature completed - Document: %s, User: %s", documentId, userId));
    }

    public static void logSignatureVerification(String documentId, boolean isValid) {
        LOGGER.info(String.format("Signature verified - Document: %s, Valid: %s", documentId, isValid));
    }

    // Certificate Operations
    public static void logCertificateCreation(String certificateId, String subject) {
        LOGGER.info(String.format("Certificate created - ID: %s, Subject: %s", certificateId, subject));
    }

    public static void logCertificateRevocation(String certificateId, String reason) {
        LOGGER.info(String.format("Certificate revoked - ID: %s, Reason: %s", certificateId, reason));
    }

    // Authentication Events
    public static void logAuthenticationAttempt(String userId, boolean success) {
        LOGGER.info(String.format("Authentication attempt - User: %s, Success: %s", userId, success));
    }

    public static void logAuthorizationCheck(String userId, String resource, boolean granted) {
        LOGGER.info(String.format("Authorization check - User: %s, Resource: %s, Granted: %s", 
            userId, resource, granted));
    }

    // Error Logging
    public static void logError(String operation, String error, Throwable throwable) {
        LOGGER.log(Level.SEVERE, String.format("Error in %s: %s", operation, error), throwable);
    }

    // Security Events
    public static void logSecurityEvent(String eventType, String userId, String details) {
        LOGGER.warning(String.format("Security event - Type: %s, User: %s, Details: %s",
            eventType, userId, details));
    }

    // System Events
    public static void logSystemEvent(String eventType, String details) {
        LOGGER.info(String.format("System event - Type: %s, Details: %s", eventType, details));
    }

    // Performance Metrics
    public static void logPerformanceMetric(String operation, long durationMs) {
        LOGGER.fine(String.format("Performance metric - Operation: %s, Duration: %dms",
            operation, durationMs));
    }

    // API Calls
    public static void logApiCall(String endpoint, String method, int statusCode) {
        LOGGER.info(String.format("API call - Endpoint: %s, Method: %s, Status: %d",
            endpoint, method, statusCode));
    }
}
