#!/bin/bash

# Security Hardening Script for Ubuntu Server
# This script applies additional security measures

echo "=================================="
echo "Applying Security Hardening"
echo "=================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Update system packages
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install fail2ban for intrusion prevention
echo "Installing fail2ban..."
apt-get install -y fail2ban

# Configure fail2ban
echo "Configuring fail2ban..."
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3
EOF

# Start and enable fail2ban
systemctl enable fail2ban
systemctl restart fail2ban

# Disable root login over SSH
echo "Securing SSH configuration..."
sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config

# Disable password authentication (use key-based auth)
# Uncomment the following lines if you have SSH keys set up
# sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
# sed -i 's/^PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

# Restart SSH service
systemctl restart sshd

# Set proper file permissions
echo "Setting file permissions..."
if [ -d "/var/www/secure-file-hosting" ]; then
    chown -R www-data:www-data /var/www/secure-file-hosting
    chmod -R 755 /var/www/secure-file-hosting
    chmod -R 700 /var/www/secure-file-hosting/uploads
fi

# Install and configure automatic security updates
echo "Configuring automatic security updates..."
apt-get install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades

# Install additional security tools
echo "Installing additional security tools..."
apt-get install -y ufw fail2ban apparmor

# Enable AppArmor
systemctl enable apparmor
systemctl start apparmor

echo ""
echo "=================================="
echo "Security Hardening Complete!"
echo "=================================="
echo ""
echo "Applied security measures:"
echo "1. System packages updated"
echo "2. Fail2ban installed and configured"
echo "3. SSH root login disabled"
echo "4. Automatic security updates enabled"
echo "5. AppArmor enabled"
echo ""
echo "IMPORTANT: Review and test all settings!"
echo "Check fail2ban status: sudo systemctl status fail2ban"
