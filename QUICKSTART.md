# Quick Start Guide - Secure File Hosting Server

This guide will help you quickly deploy the Secure File Hosting Server on Ubuntu.

## 🚀 Quick Deployment (Automated)

### Prerequisites
- Fresh Ubuntu Server (20.04 or later)
- Root or sudo access
- Domain name (optional but recommended)

### Deployment Steps

1. **Upload Project Files**
   ```bash
   # Create directory
   sudo mkdir -p /var/www/secure-file-hosting
   
   # Upload all project files to this directory
   # Use SCP, SFTP, or Git
   ```

2. **Run Automated Deployment**
   ```bash
   cd /var/www/secure-file-hosting
   
   # Make deployment script executable
   sudo chmod +x deploy.sh
   
   # Edit configuration in deploy.sh (optional)
   sudo nano deploy.sh
   # Change DOMAIN to your domain name
   
   # Run deployment
   sudo ./deploy.sh
   ```

3. **Access Your Application**
   ```
   http://your-domain.com
   or
   http://your-server-ip
   ```

4. **Login with Default Credentials**
   - Username: `admin`
   - Password: `admin123`
   
   **⚠️ Change password immediately after first login!**

## 🔧 Manual Deployment (Step by Step)

If you prefer manual deployment or the automated script fails:

### 1. Update System
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. Install Dependencies
```bash
sudo apt-get install -y python3 python3-pip python3-venv git nginx ufw
```

### 3. Set Up Application
```bash
cd /var/www/secure-file-hosting

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Create .env file
cp .env.example .env

# Generate secret key
python3 -c "import secrets; print(secrets.token_hex(32))"

# Edit .env and add the secret key
nano .env
```

### 5. Set Permissions
```bash
sudo chown -R www-data:www-data /var/www/secure-file-hosting
sudo chmod -R 755 /var/www/secure-file-hosting
```

### 6. Configure Firewall
```bash
sudo chmod +x security/setup_firewall.sh
sudo ./security/setup_firewall.sh
```

### 7. Set Up Gunicorn Service
```bash
sudo cp security/secure-file-hosting.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable secure-file-hosting
sudo systemctl start secure-file-hosting
```

### 8. Configure Nginx
```bash
sudo cp security/nginx.conf /etc/nginx/sites-available/secure-file-hosting
sudo nano /etc/nginx/sites-available/secure-file-hosting
# Update server_name with your domain

sudo ln -s /etc/nginx/sites-available/secure-file-hosting /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```

### 9. Set Up SSL (Optional)
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 🧪 Test Your Deployment

### 1. Check Services
```bash
sudo systemctl status secure-file-hosting
sudo systemctl status nginx
```

### 2. Test Application
```bash
# From your local machine
curl http://your-server-ip

# Should return HTML content
```

### 3. Test File Upload
1. Open browser: `http://your-server-ip`
2. Login with admin/admin123
3. Upload a test file
4. Download the file
5. Delete the file

## 📊 Monitoring

### View Logs
```bash
# Application logs
sudo journalctl -u secure-file-hosting -f

# Nginx logs
sudo tail -f /var/log/nginx/secure-file-hosting-access.log
```

### Check Resources
```bash
# Disk space
df -h

# Memory
free -h

# Processes
htop
```

## 🐛 Common Issues

### Port 80 Already in Use
```bash
# Check what's using port 80
sudo netstat -tlnp | grep :80

# Stop conflicting service
sudo systemctl stop apache2  # if Apache is running
```

### Permission Denied Errors
```bash
# Fix permissions
sudo chown -R www-data:www-data /var/www/secure-file-hosting
sudo chmod -R 755 /var/www/secure-file-hosting
sudo chmod -R 700 /var/www/secure-file-hosting/uploads
```

### Service Won't Start
```bash
# Check logs for errors
sudo journalctl -u secure-file-hosting -n 50

# Common fixes:
# 1. Verify virtual environment
# 2. Check Python dependencies
# 3. Verify file permissions
```

## 🔒 Security Checklist

After deployment, verify:

- [ ] Changed default admin password
- [ ] Firewall is active (`sudo ufw status`)
- [ ] SSL certificate installed (for production)
- [ ] Fail2ban is running (`sudo systemctl status fail2ban`)
- [ ] Root SSH login is disabled
- [ ] Regular backups scheduled

## 📚 Next Steps

1. **Set up SSL**: Use Let's Encrypt for free SSL certificates
2. **Configure backups**: Schedule regular backups of uploads and users.json
3. **Monitor logs**: Set up log rotation and monitoring
4. **Update regularly**: Keep system and dependencies updated
5. **Add users**: Create additional user accounts as needed

## 📞 Getting Help

If you encounter issues:

1. Check the main README.md for detailed documentation
2. Review logs: `sudo journalctl -u secure-file-hosting -f`
3. Verify all services are running
4. Check firewall rules: `sudo ufw status verbose`

## 🎉 Success!

Your Secure File Hosting Server is now running!

Access it at: `http://your-domain.com`

Default login:
- Username: `admin`
- Password: `admin123`

**Remember to change the default password!**
