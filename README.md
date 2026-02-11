# 💀 Telegram Bomber Bot

A powerful Telegram bot with admin controls and user management system.

## 🌟 Features

- 👑 **Admin Control System** - Full admin panel with user management
- 🔐 **Access Control** - Only authorized users can use the bot
- 💾 **JSON Storage** - User data stored in easy-to-read JSON format
- 📊 **Statistics Tracking** - Track user activity and bot performance
- 🎨 **Beautiful UI** - Enhanced interface with emojis and formatting
- ☁️ **Railway Ready** - Easy deployment to Railway.com

## 📋 Commands

### User Commands (Authorized Users Only)
- `/start` - Show welcome message and available commands
- `/bomb <phone> <duration>` - Start bombing attack
- `/stop` - Stop active bombing
- `/stats` - Show live statistics

### Admin Commands (Admin Only)
- `/add <userid>` - Add user to authorized list
- `/remove <userid>` - Remove user from authorized list
- `/users` - List all authorized users
- `/info <userid>` - Get detailed user information
- `/botinfo` - Show bot statistics and information

## 🚀 Deployment to Railway.com

### Step 1: Prepare Your Repository
1. Make sure all files are committed to Git:
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push
   ```

### Step 2: Deploy to Railway
1. Go to [Railway.com](https://railway.app/)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Railway will automatically detect the Procfile and deploy

### Step 3: Configure (Optional)
- Railway will automatically install dependencies from `requirements.txt`
- The bot will start automatically using the `Procfile`

## 🔧 Local Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the bot:
   ```bash
   python main.py
   ```

## 📁 File Structure

```
sambmbr/
├── main.py                    # Main bot code
├── requirements.txt           # Python dependencies
├── Procfile                   # Railway deployment config
├── authorized_users.json      # User database (auto-created)
└── README.md                  # This file
```

## 🔐 Admin Configuration

The admin ID is hardcoded in `main.py`:
```python
ADMIN_ID = 7678087570
```

## 💾 User Data Storage

User data is stored in `authorized_users.json` with the following structure:
```json
{
  "123456789": {
    "user_id": 123456789,
    "username": "example_user",
    "added_by": 7678087570,
    "added_at": "2026-02-11 21:00:00",
    "total_attacks": 5,
    "last_attack": "2026-02-11 21:30:00"
  }
}
```

## 📊 API Information

- **Total APIs:** 30+ bombing APIs
- **Success Rate:** Varies by API availability
- **Auto-Retry:** Enabled with 2-second intervals

## ⚠️ Important Notes

1. **Access Control:** Unauthorized users will see "ACCESS DENIED" message
2. **Admin Powers:** Only admin can add/remove users
3. **User Stats:** All user activity is tracked and stored
4. **JSON Backup:** Keep `authorized_users.json` backed up

## 🎯 Usage Examples

### For Admin:
```
/add 123456789          # Add user
/remove 123456789       # Remove user
/users                  # List all users
/info 123456789         # Get user info
/botinfo                # Bot statistics
```

### For Authorized Users:
```
/bomb 9876543210 5      # Bomb for 5 minutes
/stats                  # Check progress
/stop                   # Stop bombing
```

## 🛡️ Security Features

- ✅ Admin-only commands protected
- ✅ User authorization required
- ✅ Access denied for unauthorized users
- ✅ User ID verification
- ✅ Activity tracking

## 📞 Support

- **Owner:** @SamZGamer
- **Channel:** @DINOCHECKER

## ⚖️ Disclaimer

This bot is for educational purposes only. Use responsibly and in accordance with local laws.

---

Made with ❤️ by @SamZGamer
