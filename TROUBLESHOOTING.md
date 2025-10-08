# 🔧 Deployment Troubleshooting Guide

If your deployment failed, here are common issues and solutions:

## ✅ Recent Fixes Applied

**Latest commit includes:**
- ✅ Pinned specific package versions to avoid conflicts
- ✅ Updated gunicorn configuration with proper workers and timeout
- ✅ Fixed data directory creation on startup
- ✅ Updated Python version to 3.9.18
- ✅ Added missing dependencies (werkzeug, scikit-learn)
- ✅ Improved error handling

**These fixes should resolve most deployment issues!**

---

## 🐛 Common Issues & Solutions

### Issue 1: Build Fails with Package Conflicts

**Error:** `ERROR: pip's dependency resolver does not currently take into account all the packages...`

**Solution:**
The latest update pins specific versions. If still failing:
1. Check Render logs for specific package conflicts
2. Try updating `requirements_web.txt` with these stable versions:
   ```
   flask==3.0.0
   numpy==1.24.3
   pandas==2.0.3
   ```

### Issue 2: App Crashes on Startup

**Error:** `Exited with status 1`

**Possible causes:**
1. **Missing data directory** - Fixed in latest commit
2. **Import errors** - Check all adapters are in `src/adapters/`
3. **Port binding** - Fixed in render.yaml

**Solution:**
- Latest commit creates data directories automatically
- Ensure all files pushed to GitHub
- Check logs: `Services` → Your app → `Logs` tab

### Issue 3: Module Not Found Errors

**Error:** `ModuleNotFoundError: No module named 'adapters'`

**Solution:**
Ensure your file structure looks like this:
```
codeswitch-benchmark/
├── app.py
├── src/
│   ├── __init__.py
│   └── adapters/
│       ├── __init__.py
│       ├── gemini_adapter.py
│       ├── mistral_adapter.py
│       └── cohere_adapter.py
```

### Issue 4: Matplotlib Backend Issues

**Error:** `ImportError: cannot import name '_get_running_interactive_framework'`

**Solution:**
Already fixed in app.py with `matplotlib.use('Agg')` before importing pyplot.

### Issue 5: Gunicorn Won't Start

**Error:** `Failed to find application object 'app'`

**Solution:**
Check `render.yaml` has:
```yaml
startCommand: "gunicorn --bind 0.0.0.0:$PORT app:app --workers 1 --threads 2 --timeout 120"
```

### Issue 6: Out of Memory

**Error:** `Process killed (out of memory)`

**Solution:**
Free tier has limited RAM. To reduce memory usage:
1. Already using 1 worker (minimum)
2. Consider upgrading to paid tier
3. Remove matplotlib if not needed (use Plotly only)

---

## 📊 Checking Deployment Status

### On Render:
1. Go to your Render dashboard
2. Click on your service
3. Check the **"Events"** tab for deployment status
4. Check the **"Logs"** tab for error messages

### Successful Deployment Shows:
```
==> Build successful 🎉
==> Deploying...
==> Your service is live 🎉
```

### Failed Deployment Shows:
```
==> Build failed
Exited with status 1
```

---

## 🔍 Reading Logs

### Understanding Render Logs:

**Build Phase:**
```
==> Cloning from GitHub...
==> Installing dependencies...
pip install -r requirements_web.txt
```
Look for: Package installation errors

**Deploy Phase:**
```
==> Starting service with 'gunicorn app:app'
```
Look for: Import errors, module not found

**Runtime Phase:**
```
[worker] Booting worker with pid: 123
```
Look for: Application crashes, port errors

---

## 🚀 Force Redeploy

If changes don't seem to apply:

### On Render:
1. Go to your service dashboard
2. Click **"Manual Deploy"** dropdown
3. Select **"Clear build cache & deploy"**
4. Wait for new build to complete

### From Git:
```bash
git commit --allow-empty -m "Trigger rebuild"
git push origin main
```

---

## 🔧 Alternative: Simplify Requirements

If all else fails, use minimal requirements:

```txt
flask==3.0.0
gunicorn==21.2.0
plotly==5.18.0
pandas==2.0.3
numpy==1.24.3
google-generativeai==0.3.2
mistralai==0.1.8
cohere==4.37
python-dotenv==1.0.0
```

Remove matplotlib and seaborn if not critical.

---

## 📞 Getting Help

### 1. Check Render Documentation
- [Render Python Docs](https://render.com/docs/deploy-flask)
- [Build failures](https://render.com/docs/troubleshooting-builds)

### 2. Check Our Logs
```bash
# View recent deployment logs on Render
Dashboard → Your Service → Logs tab
```

### 3. Test Locally
```bash
# Install exact deployment requirements
pip install -r requirements_web.txt

# Test with gunicorn locally
gunicorn app:app --bind 0.0.0.0:5001

# Visit http://localhost:5001
```

### 4. Common Quick Fixes
```bash
# Update render.yaml to use fewer workers
startCommand: "gunicorn --bind 0.0.0.0:$PORT app:app --workers 1"

# Simplify Python version
PYTHON_VERSION: 3.9
```

---

## ✅ Verify Deployment Checklist

Before deploying, ensure:
- [ ] All files committed and pushed to GitHub
- [ ] `requirements_web.txt` has all dependencies
- [ ] `render.yaml` is in root directory
- [ ] `app.py` uses `PORT` environment variable
- [ ] `src/adapters/` has all adapter files
- [ ] No syntax errors in Python files
- [ ] `.gitignore` doesn't exclude necessary files

---

## 🎯 Current Configuration (Latest)

Your repo now has:
```yaml
# render.yaml
buildCommand: "pip install --upgrade pip && pip install -r requirements_web.txt"
startCommand: "gunicorn --bind 0.0.0.0:$PORT app:app --workers 1 --threads 2 --timeout 120"
PYTHON_VERSION: 3.9.18
```

This should work for most deployments! 🚀

---

## 💡 Success Signs

When deployment works:
1. ✅ Build completes without errors
2. ✅ Service shows "Live" status (green)
3. ✅ URL opens and shows the dashboard
4. ✅ Can navigate through pages
5. ✅ Can submit test (with valid API key)

---

## 🆘 Still Having Issues?

1. **Share the full error log** from Render
2. **Check** which step fails (Build? Deploy? Runtime?)
3. **Look for** specific error messages
4. **Try** Railway as alternative: [railway.app](https://railway.app/)

The latest commit should fix most issues. Try deploying again! 🚀

