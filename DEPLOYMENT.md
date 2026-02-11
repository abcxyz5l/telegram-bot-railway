# 🚀 Railway Deployment Guide

## Quick Deploy Steps

### 1️⃣ Push to GitHub
```bash
git add .
git commit -m "Bot ready for deployment"
git push origin main
```

### 2️⃣ Deploy on Railway
1. Go to https://railway.app/
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `telegram-bot-railway`
5. Railway will auto-detect and deploy

### 3️⃣ Monitor Deployment
- Check the **Deployments** tab for build logs
- Look for: `🤖 BOMBER BOT STARTED!`
- If you see this, your bot is running!

## 🔧 Troubleshooting

### Bot Not Starting?
Check the logs in Railway dashboard:
- Click on your deployment
- Go to **"Deployments"** tab
- Click on the latest deployment
- View logs for errors

### Common Issues

**Issue:** `Bot failed to start`
**Solution:** Check if BOT_TOKEN is correct in main.py

**Issue:** `Module not found`
**Solution:** Make sure requirements.txt is committed

**Issue:** `No Procfile found`
**Solution:** Make sure Procfile exists with: `worker: python main.py`

## ✅ Verification

Once deployed, test your bot:
1. Open Telegram
2. Search for your bot
3. Send `/start`
4. You should see the welcome message!

## 📊 Bot Status

After deployment, your bot will:
- ✅ Run 24/7 on Railway
- ✅ Auto-restart if it crashes
- ✅ Store user data in JSON file
- ✅ Be accessible from anywhere

## 🎯 Admin Setup

1. Send `/start` to your bot
2. Your ID (7678087570) is already admin
3. Use `/add <userid>` to authorize users
4. Use `/users` to see all authorized users

## 💡 Tips

- Keep your Railway dashboard open to monitor logs
- The bot will create `authorized_users.json` automatically
- All user data persists across restarts
- Use `/botinfo` to check bot statistics

## 🆘 Need Help?

If deployment fails:
1. Check Railway logs for specific errors
2. Verify all files are committed to Git
3. Make sure BOT_TOKEN is valid
4. Check Python version (should use 3.9+)

---

**Ready to deploy?** Just push to GitHub and deploy on Railway! 🚀
