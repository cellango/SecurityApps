#!/bin/bash

# Set up permissions
chmod +x rotate-logs.sh

# Create cron job for log rotation (runs daily at 1 AM)
(crontab -l 2>/dev/null; echo "0 1 * * * $(pwd)/rotate-logs.sh >> $(pwd)/rotation.log 2>&1") | crontab -

# Set up logrotate configuration
if [ -d "/etc/logrotate.d" ]; then
    sudo cp logrotate/perimeterai /etc/logrotate.d/
    sudo chmod 644 /etc/logrotate.d/perimeterai
    echo "Logrotate configuration installed"
else
    echo "Logrotate directory not found. Please install logrotate first."
    exit 1
fi

# Create log directory with proper permissions
sudo mkdir -p /var/log/perimeterai
sudo chown -R $USER:$USER /var/log/perimeterai
sudo chmod 755 /var/log/perimeterai

echo "Log rotation setup completed successfully"
