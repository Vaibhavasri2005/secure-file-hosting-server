#!/bin/bash

# Firewall Configuration Script for Ubuntu Server
# This script configures UFW (Uncomplicated Firewall) for the Secure File Hosting Server

echo "=================================="
echo "Configuring Firewall (UFW)"
echo "=================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Install UFW if not already installed
echo "Checking UFW installation..."
if ! command -v ufw &> /dev/null; then
    echo "Installing UFW..."
    apt-get update
    apt-get install -y ufw
fi

# Reset UFW to default settings
echo "Resetting UFW to default settings..."
ufw --force reset

# Set default policies
echo "Setting default policies..."
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (CRITICAL - don't lock yourself out!)
echo "Allowing SSH (port 22)..."
ufw allow 22/tcp comment 'SSH Access'

# Allow HTTP (port 80)
echo "Allowing HTTP (port 80)..."
ufw allow 80/tcp comment 'HTTP Web Traffic'

# Allow HTTPS (port 443)
echo "Allowing HTTPS (port 443)..."
ufw allow 443/tcp comment 'HTTPS Web Traffic'

# Allow Flask development server (port 5000) - ONLY FOR DEVELOPMENT
# Comment this out in production!
echo "Allowing Flask development server (port 5000) - DEVELOPMENT ONLY..."
ufw allow 5000/tcp comment 'Flask Development Server'

# Enable rate limiting on SSH to prevent brute force attacks
echo "Enabling rate limiting on SSH..."
ufw limit 22/tcp

# Enable UFW
echo "Enabling UFW..."
ufw --force enable

# Display status
echo ""
echo "=================================="
echo "Firewall Configuration Complete!"
echo "=================================="
ufw status verbose

echo ""
echo "IMPORTANT NOTES:"
echo "1. SSH is allowed on port 22 (rate limited)"
echo "2. HTTP is allowed on port 80"
echo "3. HTTPS is allowed on port 443"
echo "4. Flask dev server is allowed on port 5000 (REMOVE IN PRODUCTION)"
echo "5. All other incoming connections are blocked"
echo ""
echo "To disable the firewall: sudo ufw disable"
echo "To check status: sudo ufw status verbose"
