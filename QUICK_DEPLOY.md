# 🚀 Quick Deployment Guide

Your Code-Switching Benchmark is now ready to be deployed! Here's exactly what to do:

## ✅ What's Already Done

I've prepared everything you need:
- ✅ Added `render.yaml` for automatic Render deployment
- ✅ Updated `requirements_web.txt` with gunicorn production server
- ✅ Modified `app.py` to work with cloud hosting
- ✅ Added Python version files (`runtime.txt`, `.python-version`)
- ✅ Created comprehensive deployment documentation
- ✅ Updated README with deployment instructions
- ✅ Pushed everything to GitHub

## 🎯 Deploy to Render (Recommended - 5 Minutes)

### Step 1: Sign Up for Render
1. Go to **[render.com](https://render.com/)**
2. Click **"Get Started"** or **"Sign Up"**
3. **Sign up with your GitHub account** (easiest option)

### Step 2: Create New Web Service
1. Once logged in, click **"New +"** in the top right
2. Select **"Web Service"**
3. Click **"Connect account"** if you haven't connected GitHub yet

### Step 3: Select Your Repository
1. Find **`JaseCR/codeswitch-benchmark`** in the list
2. Click **"Connect"**

### Step 4: Configure Service
Render will auto-detect most settings from `render.yaml`, but verify:

- **Name**: `codeswitch-benchmark` (or choose your own)
- **Environment**: Python (should be auto-detected)
- **Branch**: `main`
- **Build Command**: `pip install -r requirements_web.txt`
- **Start Command**: `gunicorn app:app`
- **Instance Type**: **Free** (select this!)

### Step 5: Deploy!
1. Click **"Create Web Service"** at the bottom
2. Wait 2-5 minutes while Render builds and deploys your app
3. You'll see a URL like: `https://codeswitch-benchmark.onrender.com`

### Step 6: Test Your Live Site
1. Click on the URL Render provides
2. Your app should load! 🎉
3. Test it by entering an API key and running a test

### Step 7: Share Your URL
Update your README with the live URL:
```markdown
🌐 **[Try the Live Demo](https://your-app-name.onrender.com)**
```

---

## 🌐 Alternative: Deploy to Railway (Also Free!)

If you prefer Railway:

1. Go to **[railway.app](https://railway.app/)**
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose **`JaseCR/codeswitch-benchmark`**
5. Railway auto-detects everything and deploys
6. Get your URL: `https://your-app.railway.app`

---

## 📝 Important Notes

### Free Tier Behavior
- **Render Free**: App "sleeps" after 15 min of inactivity
  - First request after sleep takes ~30 seconds to wake up
  - Subsequent requests are fast
  - This is normal for free tier!

### User Experience
- Users will need their own API keys (this is good for security!)
- API keys from:
  - [Gemini](https://makersuite.google.com/app/apikey) - Free
  - [Mistral](https://console.mistral.ai/) - Free trial
  - [Cohere](https://dashboard.cohere.ai/) - Free trial

### Monitoring
- Check Render dashboard for:
  - Deployment logs
  - Error messages
  - Usage statistics
  - App status

---

## 🎨 Customize Your Deployment

### Custom Domain (Optional)
On paid tiers, you can add a custom domain like:
- `benchmark.yourdomain.com`
- `codeswitch.yourdomain.com`

### Environment Variables (If Needed)
If you want to add any config:
1. Go to Render dashboard
2. Select your service
3. Go to "Environment" tab
4. Add variables

---

## 🐛 Troubleshooting

### Build Fails
- Check the "Logs" tab in Render dashboard
- Ensure `requirements_web.txt` has all dependencies
- Verify Python version matches `runtime.txt`

### App Won't Load
- Wait for first deploy to complete (can take 3-5 minutes)
- Check if app is "Live" in Render dashboard
- Review logs for error messages

### API Errors
- Users need valid API keys
- Keys must have proper permissions
- Some APIs have rate limits

---

## 🎉 You're Done!

Your Code-Switching Benchmark is now:
- ✅ Live on the internet
- ✅ Accessible to anyone with the URL
- ✅ Professional and production-ready
- ✅ Free to host (on free tier)

Share it with:
- Colleagues and researchers
- Social media (#NLP #CodeSwitching #AI)
- Academic communities
- Your portfolio/CV

---

## 📧 Questions?

- Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed troubleshooting
- Review Render's documentation
- Open an issue on GitHub

Happy deploying! 🚀

