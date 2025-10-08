# Deployment Guide

This guide will help you deploy the Code-Switching Benchmark web application to make it publicly accessible.

## 🚀 Quick Deploy to Render (Recommended)

Render offers free hosting for web applications. Follow these steps:

### Step 1: Push to GitHub

Make sure all your changes are committed and pushed to GitHub:

```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

### Step 2: Deploy on Render

1. Go to [Render.com](https://render.com/) and sign up/login with your GitHub account
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `JaseCR/codeswitch-benchmark`
4. Configure the service:
   - **Name**: `codeswitch-benchmark` (or any name you prefer)
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements_web.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`
5. Click **"Create Web Service"**

### Step 3: Wait for Deployment

Render will automatically:
- Install dependencies
- Build your application
- Deploy it to a public URL like: `https://codeswitch-benchmark.onrender.com`

The first deployment takes 2-5 minutes. After that, your app will be live! 🎉

---

## 🌐 Alternative: Deploy to Railway

Railway is another excellent free hosting option:

1. Go to [Railway.app](https://railway.app/)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Railway will auto-detect it's a Flask app and deploy it

Your app will be live at: `https://your-app.railway.app`

---

## 🔧 Alternative: Deploy to Heroku

If you prefer Heroku:

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login to Heroku:
   ```bash
   heroku login
   ```
3. Create a new Heroku app:
   ```bash
   heroku create codeswitch-benchmark
   ```
4. Deploy:
   ```bash
   git push heroku main
   ```
5. Open your app:
   ```bash
   heroku open
   ```

---

## 📝 Important Notes

### User API Keys

Users will need to provide their own API keys when using the live website:
- **Gemini API Key**: [Get from Google AI Studio](https://makersuite.google.com/app/apikey)
- **Mistral API Key**: [Get from Mistral Console](https://console.mistral.ai/)
- **Cohere API Key**: [Get from Cohere Dashboard](https://dashboard.cohere.ai/)

API keys are **never stored on the server** - they're only used for the current session and sent directly to the respective AI services.

### Free Tier Limitations

- **Render Free**: App may spin down after 15 minutes of inactivity (first request takes ~30 seconds to wake up)
- **Railway Free**: 500 hours/month, $5 credit
- **Heroku Free**: No longer available (requires paid plan)

### Performance Tips

For better performance on free tier:
- The app is optimized for minimal resource usage
- Results are cached in JSON files for faster subsequent loads
- Consider upgrading to a paid tier if you get heavy traffic

---

## 🔒 Security

The application is designed with security in mind:
- No API keys are stored on the server
- All API calls are made client-side or proxy through the server securely
- User data is not persisted beyond the current session
- HTTPS is enforced on all major platforms

---

## 🎯 Post-Deployment

After deployment, you can:

1. **Share the URL** with colleagues, researchers, or on social media
2. **Add it to your GitHub README** as a live demo link
3. **Monitor usage** through Render/Railway/Heroku dashboards
4. **Set up custom domain** (available on paid tiers)

---

## 🐛 Troubleshooting

### App won't start
- Check logs in Render/Railway dashboard
- Ensure all dependencies are in `requirements_web.txt`
- Verify Python version matches `runtime.txt`

### API errors
- Remind users they need valid API keys
- Check API rate limits haven't been exceeded
- Verify API services are operational

### Slow performance
- Free tier apps "sleep" after inactivity
- First request after sleep takes longer
- Consider upgrading for always-on service

---

## 📧 Need Help?

If you encounter issues:
1. Check the platform-specific documentation
2. Review deployment logs for error messages
3. Ensure environment variables are set correctly
4. Open an issue on GitHub

Happy deploying! 🚀

