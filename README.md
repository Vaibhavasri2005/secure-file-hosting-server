# Secure File Hosting Server

A secure, cloud-based file hosting system similar to a mini version of Google Drive or Dropbox. Built with Python Flask, featuring user authentication, file management, and comprehensive security measures.

## 🚀 Features

- **User Authentication**: Secure login/registration system with password hashing
- **File Management**: Upload, download, and delete files through a web interface
- **Security**: Firewall configuration, rate limiting, and security headers
- **User Isolation**: Each user has their own private file storage
- **Modern UI**: Clean, responsive web interface
- **File Type Support**: Images, documents, archives, videos, and more
- **File Size Limit**: Up to 100MB per file

## 📋 Prerequisites

- Ubuntu Server (20.04 or later recommended)
- Python 3.8 or higher
- Root or sudo access
- At least 2GB RAM
- 20GB+ storage space

## 🛠️ Installation

### 1. Prepare Your Server

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install required system packages
sudo apt-get install -y python3 python3-pip python3-venv git nginx
```

### 2. Clone or Upload Project

```bash
# Create application directory
sudo mkdir -p /var/www/secure-file-hosting
cd /var/www/secure-file-hosting

# Upload your project files here
# Or clone from your repository:
# git clone <your-repo-url> .
```

### 3. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

Update the following in `.env`:
```
SECRET_KEY=your-unique-secret-key-here-change-this-to-random-string
FLASK_ENV=production
MAX_CONTENT_LENGTH=104857600
UPLOAD_FOLDER=uploads
```

**Generate a secure secret key:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Set Permissions

```bash
# Set proper ownership
sudo chown -R www-data:www-data /var/www/secure-file-hosting

# Set directory permissions
sudo chmod -R 755 /var/www/secure-file-hosting
sudo chmod -R 700 /var/www/secure-file-hosting/uploads
```

### 6. Configure Firewall

```bash
# Make firewall script executable
chmod +x security/setup_firewall.sh

# Run firewall configuration
sudo ./security/setup_firewall.sh
```

### 7. Apply Security Hardening

```bash
# Make security script executable
chmod +x security/security_hardening.sh

# Run security hardening
sudo ./security/security_hardening.sh
```

### 8. Set Up Web Server

#### Option A: Using Nginx (Recommended)

```bash
# Copy Nginx configuration
sudo cp security/nginx.conf /etc/nginx/sites-available/secure-file-hosting

# Update server_name in the config
sudo nano /etc/nginx/sites-available/secure-file-hosting
# Change 'your-domain.com' to your actual domain or IP

# Enable the site
sudo ln -s /etc/nginx/sites-available/secure-file-hosting /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

#### Option B: Using Apache

```bash
# Install Apache and mod_wsgi
sudo apt-get install -y apache2 libapache2-mod-wsgi-py3

# Enable required modules
sudo a2enmod wsgi headers rewrite ssl

# Copy Apache configuration
sudo cp security/apache.conf /etc/apache2/sites-available/secure-file-hosting.conf

# Update configuration
sudo nano /etc/apache2/sites-available/secure-file-hosting.conf
# Change 'your-domain.com' to your actual domain or IP

# Enable the site
sudo a2ensite secure-file-hosting.conf

# Disable default site
sudo a2dissite 000-default.conf

# Test Apache configuration
sudo apache2ctl configtest

# Restart Apache
sudo systemctl restart apache2
```

### 9. Set Up Gunicorn Service

```bash
# Create log directory
sudo mkdir -p /var/log/gunicorn
sudo chown www-data:www-data /var/log/gunicorn

# Copy systemd service file
sudo cp security/secure-file-hosting.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable secure-file-hosting
sudo systemctl start secure-file-hosting

# Check status
sudo systemctl status secure-file-hosting
```

### 10. Configure SSL (Optional but Recommended)

```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# For Nginx:
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# For Apache:
# sudo apt-get install python3-certbot-apache
# sudo certbot --apache -d your-domain.com -d www.your-domain.com

# Certificates will auto-renew
```

## 🚦 Running the Application

### Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run Flask development server
python app.py
```

Access at: `http://localhost:5000`

### Production Mode

The application should be running via systemd service:

```bash
# Check service status
sudo systemctl status secure-file-hosting

# View logs
sudo journalctl -u secure-file-hosting -f

# Restart service
sudo systemctl restart secure-file-hosting
```

Access at: `http://your-domain.com` or `http://your-server-ip`

## 🔐 Default Credentials

**Username:** `admin`  
**Password:** `admin123`

**⚠️ IMPORTANT: Change the default admin password immediately after first login!**

## 📁 Project Structure

```
secure-file-hosting/
├── app.py                      # Main Flask application
├── auth.py                     # Authentication manager
├── file_manager.py             # File operations manager
├── config.py                   # Configuration settings
├── wsgi.py                     # WSGI entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── templates/                  # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── 404.html
│   └── 500.html
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── security/                   # Security configurations
│   ├── setup_firewall.sh
│   ├── security_hardening.sh
│   ├── nginx.conf
│   ├── apache.conf
│   └── secure-file-hosting.service
└── uploads/                    # User file storage (auto-created)
```

## 🔒 Security Features

### 1. **Authentication & Authorization**
- Password hashing using SHA-256
- Session-based authentication with Flask-Login
- User isolation (users can only access their own files)

### 2. **Firewall Configuration**
- UFW firewall rules
- Rate limiting on SSH (prevents brute force)
- Only necessary ports open (22, 80, 443)

### 3. **Web Server Security**
- Security headers (X-Frame-Options, CSP, etc.)
- Rate limiting on login and upload endpoints
- File size restrictions (100MB limit)
- File type validation

### 4. **System Security**
- Fail2ban for intrusion prevention
- Automatic security updates
- SSH hardening (root login disabled)
- AppArmor enabled
- Proper file permissions

### 5. **Application Security**
- CSRF protection
- SQL injection prevention (using secure file storage)
- Path traversal prevention
- Secure filename handling

## 🧪 Testing

### Test Local Development

```bash
# Start the application
python app.py

# Open browser and navigate to:
http://localhost:5000

# Test features:
1. Register a new user
2. Login with credentials
3. Upload a file
4. Download the file
5. Delete the file
6. Logout
```

### Test Production Deployment

```bash
# Check service status
sudo systemctl status secure-file-hosting

# Check Nginx/Apache status
sudo systemctl status nginx
# or
sudo systemctl status apache2

# Test firewall
sudo ufw status verbose

# View application logs
sudo journalctl -u secure-file-hosting -n 50
```

## 📊 Monitoring

### View Application Logs

```bash
# Gunicorn access logs
sudo tail -f /var/log/gunicorn/access.log

# Gunicorn error logs
sudo tail -f /var/log/gunicorn/error.log

# Nginx logs
sudo tail -f /var/log/nginx/secure-file-hosting-access.log
sudo tail -f /var/log/nginx/secure-file-hosting-error.log

# System logs
sudo journalctl -u secure-file-hosting -f
```

### Check System Resources

```bash
# Disk usage
df -h

# Memory usage
free -h

# CPU usage
top

# Active connections
sudo netstat -tulpn | grep LISTEN
```

## 🐛 Troubleshooting

### Application Won't Start

```bash
# Check service status
sudo systemctl status secure-file-hosting

# View detailed logs
sudo journalctl -u secure-file-hosting -n 100 --no-pager

# Check Python dependencies
source venv/bin/activate
pip list

# Verify file permissions
ls -la /var/www/secure-file-hosting
```

### Can't Access Website

```bash
# Check web server status
sudo systemctl status nginx
# or
sudo systemctl status apache2

# Check if port is listening
sudo netstat -tlnp | grep :80

# Check firewall rules
sudo ufw status verbose

# Test Nginx configuration
sudo nginx -t
```

### File Upload Fails

```bash
# Check upload directory permissions
ls -la /var/www/secure-file-hosting/uploads/

# Check disk space
df -h

# Check Nginx/Apache upload size limit
# Nginx: client_max_body_size in nginx.conf
# Apache: LimitRequestBody in apache.conf
```

### Database/User Issues

```bash
# Check users.json file
cat /var/www/secure-file-hosting/users.json

# Reset users file (creates default admin user)
rm /var/www/secure-file-hosting/users.json
sudo systemctl restart secure-file-hosting
```

## 🔧 Maintenance

### Backup

```bash
# Backup user data
sudo tar -czf backup-$(date +%Y%m%d).tar.gz \
    /var/www/secure-file-hosting/uploads/ \
    /var/www/secure-file-hosting/users.json

# Download backup to local machine
# scp user@server:/path/to/backup-*.tar.gz ./
```

### Update Application

```bash
# Pull latest code
cd /var/www/secure-file-hosting
git pull

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl restart secure-file-hosting
```

### System Updates

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Reboot if kernel updated
sudo reboot
```

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [UFW Guide](https://help.ubuntu.com/community/UFW)
- [Let's Encrypt](https://letsencrypt.org/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open-source and available for educational purposes.

## ⚠️ Disclaimer

This application is designed for educational purposes to demonstrate Linux administration, cloud server management, and web security concepts. For production use, consider additional security measures and thorough security audits.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review application logs
3. Open an issue on the repository

---

**Built with ❤️ for learning Linux, Cloud Computing, and Web Security**
