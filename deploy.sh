#!/bin/bash

# Quick Deployment Script for Secure File Hosting Server
# This script automates the deployment process on a fresh Ubuntu server

set -e  # Exit on any error

echo "========================================"
echo "Secure File Hosting Server Deployment"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Variables (customize these)
APP_DIR="/var/www/secure-file-hosting"
APP_USER="www-data"
DOMAIN="your-domain.com"
USE_NGINX=true  # Set to false to use Apache instead

echo "Configuration:"
echo "- Application Directory: $APP_DIR"
echo "- Application User: $APP_USER"
echo "- Domain: $DOMAIN"
echo "- Web Server: $([ "$USE_NGINX" = true ] && echo "Nginx" || echo "Apache")"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

# Step 1: Update system
echo ""
echo "Step 1: Updating system packages..."
apt-get update
apt-get upgrade -y

# Step 2: Install dependencies
echo ""
echo "Step 2: Installing dependencies..."
apt-get install -y python3 python3-pip python3-venv git ufw fail2ban

if [ "$USE_NGINX" = true ]; then
    apt-get install -y nginx
else
    apt-get install -y apache2 libapache2-mod-wsgi-py3
fi

# Step 3: Create application directory (if deploying)
echo ""
echo "Step 3: Setting up application directory..."
if [ ! -d "$APP_DIR" ]; then
    mkdir -p "$APP_DIR"
fi

# Note: At this point, you should have uploaded your application files to $APP_DIR

# Step 4: Set up Python virtual environment
echo ""
echo "Step 4: Creating Python virtual environment..."
cd "$APP_DIR"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Step 5: Configure environment
echo ""
echo "Step 5: Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    sed -i "s/your-secret-key-here-change-in-production/$SECRET_KEY/" .env
    sed -i "s/FLASK_ENV=development/FLASK_ENV=production/" .env
fi

# Step 6: Set permissions
echo ""
echo "Step 6: Setting file permissions..."
chown -R $APP_USER:$APP_USER "$APP_DIR"
chmod -R 755 "$APP_DIR"
mkdir -p "$APP_DIR/uploads"
chmod -R 700 "$APP_DIR/uploads"

# Step 7: Configure firewall
echo ""
echo "Step 7: Configuring firewall..."
if [ -f "$APP_DIR/security/setup_firewall.sh" ]; then
    chmod +x "$APP_DIR/security/setup_firewall.sh"
    bash "$APP_DIR/security/setup_firewall.sh"
fi

# Step 8: Apply security hardening
echo ""
echo "Step 8: Applying security hardening..."
if [ -f "$APP_DIR/security/security_hardening.sh" ]; then
    chmod +x "$APP_DIR/security/security_hardening.sh"
    bash "$APP_DIR/security/security_hardening.sh"
fi

# Step 9: Set up Gunicorn service
echo ""
echo "Step 9: Setting up Gunicorn service..."
mkdir -p /var/log/gunicorn
chown $APP_USER:$APP_USER /var/log/gunicorn

if [ -f "$APP_DIR/security/secure-file-hosting.service" ]; then
    cp "$APP_DIR/security/secure-file-hosting.service" /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable secure-file-hosting
    systemctl start secure-file-hosting
fi

# Step 10: Configure web server
echo ""
echo "Step 10: Configuring web server..."

if [ "$USE_NGINX" = true ]; then
    # Configure Nginx
    if [ -f "$APP_DIR/security/nginx.conf" ]; then
        cp "$APP_DIR/security/nginx.conf" /etc/nginx/sites-available/secure-file-hosting
        sed -i "s/your-domain.com/$DOMAIN/g" /etc/nginx/sites-available/secure-file-hosting
        sed -i "s|/var/www/secure-file-hosting|$APP_DIR|g" /etc/nginx/sites-available/secure-file-hosting
        
        ln -sf /etc/nginx/sites-available/secure-file-hosting /etc/nginx/sites-enabled/
        rm -f /etc/nginx/sites-enabled/default
        
        nginx -t && systemctl restart nginx
    fi
else
    # Configure Apache
    if [ -f "$APP_DIR/security/apache.conf" ]; then
        cp "$APP_DIR/security/apache.conf" /etc/apache2/sites-available/secure-file-hosting.conf
        sed -i "s/your-domain.com/$DOMAIN/g" /etc/apache2/sites-available/secure-file-hosting.conf
        sed -i "s|/var/www/secure-file-hosting|$APP_DIR|g" /etc/apache2/sites-available/secure-file-hosting.conf
        
        a2enmod wsgi headers rewrite
        a2ensite secure-file-hosting.conf
        a2dissite 000-default.conf
        
        apache2ctl configtest && systemctl restart apache2
    fi
fi

# Step 11: Display status
echo ""
echo "========================================"
echo "Deployment Complete!"
echo "========================================"
echo ""
echo "Service Status:"
systemctl status secure-file-hosting --no-pager | head -n 5
echo ""

if [ "$USE_NGINX" = true ]; then
    systemctl status nginx --no-pager | head -n 3
else
    systemctl status apache2 --no-pager | head -n 3
fi

echo ""
echo "Firewall Status:"
ufw status numbered | head -n 10
echo ""
echo "========================================"
echo "Access your application at:"
echo "http://$DOMAIN"
echo ""
echo "Default credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "IMPORTANT: Change the default password!"
echo "========================================"
echo ""
echo "Useful commands:"
echo "- View logs: sudo journalctl -u secure-file-hosting -f"
echo "- Restart app: sudo systemctl restart secure-file-hosting"
echo "- Check status: sudo systemctl status secure-file-hosting"
echo ""
echo "To set up SSL certificate (recommended):"
echo "sudo apt-get install certbot python3-certbot-nginx"
echo "sudo certbot --nginx -d $DOMAIN"
echo ""
