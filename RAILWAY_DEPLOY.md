# Railway Deployment Guide

## Quick Deploy Steps

1. **Go to Railway**: https://railway.app/
2. **Sign up** with your GitHub account
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose: `Vaibhavasri2005/secure-file-hosting-server`
6. Railway will automatically detect and deploy

## Environment Variables to Set

In Railway dashboard, go to **Variables** tab and add:

```
FLASK_ENV=production
SECRET_KEY=your_secret_key_from_.env_file
PORT=5000
```

## After Deployment

1. Go to **Settings** tab
2. Click **"Generate Domain"**
3. Your app will be live at: `https://your-app-name.up.railway.app`

## Important Notes

⚠️ **Uploaded Files**: Railway's free tier has ephemeral storage. Files will be deleted on restart.
⚠️ **Users Data**: The users.json file may reset on restart.

For production use, consider:
- Adding a database (PostgreSQL/MongoDB)
- Using cloud storage (AWS S3/Cloudinary) for file uploads

## Your Project is Ready!

All necessary files have been created:
- ✅ Procfile
- ✅ railway.json
- ✅ requirements.txt (with gunicorn)
- ✅ wsgi.py

Just push to GitHub and deploy on Railway!
