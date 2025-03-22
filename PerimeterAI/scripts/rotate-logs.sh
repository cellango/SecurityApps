#!/bin/bash

# Configuration
LOG_DIR="/var/log/perimeterai"
MAX_SIZE_MB=10
MAX_FILES=10
COMPRESS=true
RETENTION_DAYS=30

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Function to get file size in MB
get_file_size_mb() {
    local file="$1"
    local size=$(stat -f %z "$file" 2>/dev/null)
    echo $(( size / 1024 / 1024 ))
}

# Function to rotate a single log file
rotate_log() {
    local log_file="$1"
    local base_name=$(basename "$log_file" .log)
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local rotated_file="${LOG_DIR}/${base_name}-${timestamp}.log"

    # Rotate the file
    mv "$log_file" "$rotated_file"
    touch "$log_file"
    chmod 0640 "$log_file"

    # Compress if enabled
    if [ "$COMPRESS" = true ]; then
        gzip "$rotated_file"
    fi

    echo "Rotated $log_file to $rotated_file"
}

# Function to clean up old log files
cleanup_old_logs() {
    find "$LOG_DIR" -name "*.log*" -o -name "*.gz" -mtime +"$RETENTION_DAYS" -delete
    echo "Cleaned up logs older than $RETENTION_DAYS days"
}

# Main rotation logic
for log_file in "$LOG_DIR"/*.log; do
    # Skip if no log files found
    [ -e "$log_file" ] || continue

    # Get current file size
    size_mb=$(get_file_size_mb "$log_file")

    # Rotate if file exceeds max size
    if [ "$size_mb" -ge "$MAX_SIZE_MB" ]; then
        echo "Log file $log_file exceeds $MAX_SIZE_MB MB, rotating..."
        rotate_log "$log_file"
    fi
done

# Clean up old files
cleanup_old_logs

# Count and maintain max files
total_logs=$(find "$LOG_DIR" -name "*.log*" -o -name "*.gz" | wc -l)
if [ "$total_logs" -gt "$MAX_FILES" ]; then
    echo "Too many log files, removing oldest..."
    excess_count=$((total_logs - MAX_FILES))
    find "$LOG_DIR" -name "*.log*" -o -name "*.gz" -printf "%T@ %p\n" | \
        sort -n | head -n "$excess_count" | cut -d' ' -f2- | xargs rm -f
fi

echo "Log rotation completed successfully"
