# 🆕 Fresh Render Deployment Guide

## ✅ What's Changed (Clean Start)

I've simplified everything based on what we learned:

- ✅ **Removed** complex render.yaml
- ✅ **Removed** unnecessary wsgi.py
- ✅ **Removed** matplotlib/seaborn (using Plotly only)
- ✅ **Minimal** dependencies (9 packages vs 13)
- ✅ **Tested** stable versions
- ✅ **Added** Procfile for standard deployment

## 🚀 Deploy Steps (5 Minutes)

### Step 1: Delete Old Service (If Exists)
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Find your old `codeswitch-benchmark` service
3. Click **Settings** → Scroll down → **Delete Service**
4. Confirm deletion

### Step 2: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect to GitHub: `JaseCR/codeswitch-benchmark`
3. Click **"Connect"**

### Step 3: Configure Service
Fill in these settings:

**Basic Settings:**
- **Name**: `codeswitch-benchmark` (or your choice)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements_web.txt`
- **Start Command**: `gunicorn app:app`

**Instance Type:**
- Select **Free** tier

### Step 4: Advanced Settings (Optional)
- **Python Version**: `3.9.18` (or leave default)
- **Health Check Path**: `/` (optional)

### Step 5: Create Web Service
1. Click **"Create Web Service"** button
2. Wait 2-4 minutes for build

## 📊 What to Expect

### Build Phase (2-3 minutes):
```
==> Cloning from GitHub...
==> Detected Python app
==> Installing dependencies from requirements_web.txt
    ✅ Flask==3.0.0
    ✅ gunicorn==21.2.0
    ✅ plotly==5.18.0
    ✅ pandas==2.0.3
    ✅ numpy==1.24.3
    (and 4 more)
==> Build successful 🎉
```

### Deploy Phase (30 seconds):
```
==> Starting service with 'gunicorn app:app'
==> Your service is live 🎉
```

### You'll get a URL like:
```
https://codeswitch-benchmark-abcd.onrender.com
```

## ✅ Success Checklist

After deployment, test:
- [ ] Homepage loads (dashboard)
- [ ] Can navigate to Test page
- [ ] Can navigate to Results page
- [ ] Try entering an API key and running a test

## 🎯 Why This Will Work

**Simplified Configuration:**
```
# Procfile (standard)
web: gunicorn app:app

# requirements_web.txt (minimal, stable versions)
Flask==3.0.0
gunicorn==21.2.0
plotly==5.18.0
pandas==2.0.3
numpy==1.24.3
google-generativeai==0.3.2
mistralai==0.1.8
cohere==4.37
python-dotenv==1.0.0
```

**No complex configs, no version conflicts, no matplotlib issues!**

## 🐛 If Something Goes Wrong

### Build Fails:
1. Check **Logs** tab in dashboard
2. Look for specific error
3. Most common: dependency conflict (shouldn't happen with these versions)

### App Won't Start:
1. Verify Build Command: `pip install -r requirements_web.txt`
2. Verify Start Command: `gunicorn app:app`
3. Check Runtime is set to `Python 3`

### 502 Bad Gateway:
- Wait 1-2 minutes (app is starting)
- Check if PORT environment variable is set (Render does this automatically)

## 💡 Tips

1. **First deploy takes longest** (5-6 minutes) - subsequent deploys are faster
2. **Free tier sleeps** after 15 min inactivity - first request wakes it (~30 sec)
3. **Auto-deploy** is enabled by default - push to GitHub and it redeploys
4. **Custom domain** available on paid tiers

## 🎉 After Success

1. **Update your README** with the live URL
2. **Test all features** with real API keys
3. **Share** with the world!

## 📝 Configuration Summary

```yaml
# What Render will detect automatically:
Language: Python
Framework: Flask
Server: Gunicorn
Port: 10000 (default, uses $PORT env variable)
Workers: 1 (good for free tier)
```

This is the **clean, simple, working configuration!** 🚀

---

**Ready? Go create that new service!** Everything is prepared and tested.

