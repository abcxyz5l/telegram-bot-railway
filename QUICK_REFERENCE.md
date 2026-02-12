# 🚀 Quick Reference - New Features

## ⏰ SCHEDULING COMMANDS

### Schedule an Attack
```
/schedule 9876543210 5 20:30
```
- Phone: 10 digits
- Duration: 1-60 minutes
- Time: HH:MM (24-hour format)

### View Your Schedules
```
/schedules
```

### Cancel a Schedule
```
/cancel a1b2c3d4
```

---

## 🕵️ ADMIN MONITORING

### What You See (Automatically):

**When user starts bombing:**
```
🔔 NEW BOMBING ACTIVITY

👤 User: @username (123456789)
📱 Target: +919876543210
⏰ Duration: 5 min
```

**When user stops:**
```
🛑 BOMBING STOPPED

📊 Success: 245
❌ Failed: 12
```

**When user schedules:**
```
📅 NEW SCHEDULED ATTACK

👤 User: @username
📱 Target: +919876543210
📅 Scheduled: 2026-02-12 20:30:00
```

---

## 📝 EXAMPLES

### Example 1: Schedule for Tonight
```
/schedule 9876543210 10 23:00
```
→ Bombs at 11 PM tonight for 10 minutes

### Example 2: Schedule for Tomorrow Morning
```
/schedule 9876543210 5 09:00
```
→ If it's past 9 AM, schedules for tomorrow 9 AM

### Example 3: View & Cancel
```
/schedules              # See all schedules
/cancel a1b2c3d4       # Cancel specific one
```

---

## ⚡ QUICK TIPS

✅ **Time Format:** Use 24-hour (14:30 not 2:30 PM)
✅ **Auto Tomorrow:** Past times schedule for next day
✅ **Blocked Numbers:** Can't schedule blocked numbers
✅ **Silent Monitoring:** Users never know you're watching
✅ **Auto Execute:** Schedules run automatically

---

**That's it! Simple and powerful! 🎯**
