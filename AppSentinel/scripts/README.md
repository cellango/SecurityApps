# AppSentinel Scripts

This directory contains utility scripts for managing the AppSentinel project.

## Available Scripts

### cleanup.sh

A robust utility script for cleaning up Docker resources associated with AppSentinel components.

#### Features

- **Comprehensive Cleanup**: Removes containers, networks, and optionally volumes
- **Smart Detection**: Only removes resources related to AppSentinel
- **Safe Execution**: Checks for Docker daemon and existing resources
- **Detailed Logging**: Provides timestamped, color-coded feedback
- **Error Handling**: Gracefully handles errors and provides feedback

#### Usage

```bash
# Make the script executable (first time only)
chmod +x scripts/cleanup.sh

# Run the cleanup script
./scripts/cleanup.sh
```

#### What it Does

1. **Container Cleanup**
   - Stops all running AppSentinel containers
   - Removes stopped containers with "appinventory" or "appscore" prefixes

2. **Network Cleanup**
   - Removes Docker networks associated with AppSentinel

3. **Image Cleanup**
   - Removes dangling images to free up disk space

4. **Optional Features** (commented out by default)
   - Volume cleanup (can be uncommented if needed)

#### Output

The script provides detailed, color-coded output:
- 🟢 Green: Success messages and completed operations
- 🟡 Yellow: Warnings and non-critical issues
- 🔴 Red: Errors and critical issues

#### Example Output
```
[2025-01-02 20:30:00] [INFO] Starting AppSentinel cleanup process...
[2025-01-02 20:30:01] [INFO] Stopping containers...
[2025-01-02 20:30:02] [INFO] Removing containers...
[2025-01-02 20:30:03] [INFO] Removing networks...
[2025-01-02 20:30:04] [SUCCESS] Cleanup completed successfully!
```

#### Error Handling

The script handles various error conditions:
- Docker daemon not running
- Permission issues
- Resource already removed
- Network in use

#### Integration with Makefile

You can integrate this script with your Makefile by adding:

```makefile
clean:
    ./scripts/cleanup.sh
```

Then use:
```bash
make clean
```

#### Customization

- To enable volume cleanup, uncomment the volume removal section
- Adjust the container prefix detection by modifying the grep patterns
- Modify the logging levels or colors in the script header
