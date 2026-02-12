@authorized_only
async def schedule_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "No username"
    
    if len(context.args) < 3:
        await update.message.reply_text(
            "❌ **Invalid Usage!**\n\n"
            "📝 **Correct Format:**\n"
            "`/schedule <phone> <duration> <time>`\n\n"
            "🎯 **Examples:**\n"
            "`/schedule 9876543210 5 20:30` - Today at 8:30 PM\n"
            "`/schedule 9876543210 10 14:00` - Today at 2:00 PM\n"
            "`/schedule 9876543210 5 23:45` - Today at 11:45 PM\n\n"
            "⏰ **Time Format:** HH:MM (24-hour format)\n"
            "📅 **Note:** Schedules for today only",
            parse_mode='Markdown'
        )
        return
    
    phone = context.args[0]
    duration_str = context.args[1]
    time_str = context.args[2]
    
    # Validate phone
    if not phone.isdigit() or len(phone) != 10:
        await update.message.reply_text("❌ Invalid phone number! Please enter 10 digits.")
        return
    
    # Validate duration
    try:
        duration = int(duration_str)
        if duration <= 0 or duration > 60:
            await update.message.reply_text("❌ Invalid duration! Use 1-60 minutes.")
            return
    except ValueError:
        await update.message.reply_text("❌ Invalid duration! Use numbers only.")
        return
    
    # Parse time
    try:
        hour, minute = map(int, time_str.split(':'))
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValueError
        
        # Create scheduled datetime for today
        now = datetime.now()
        scheduled_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If time has passed today, schedule for tomorrow
        if scheduled_dt <= now:
            scheduled_dt += timedelta(days=1)
        
        scheduled_time_str = scheduled_dt.strftime("%Y-%m-%d %H:%M:%S")
        
    except ValueError:
        await update.message.reply_text("❌ Invalid time format! Use HH:MM (24-hour format)\nExample: 14:30 for 2:30 PM")
        return
    
    # Check if number is blocked
    if bomber.blocked_manager.is_blocked(phone):
        await update.message.reply_text(
            "🚫 **RESTRICTED NUMBER**\n\n"
            f"❌ The number `+91{phone}` is blocked and cannot be scheduled!",
            parse_mode='Markdown'
        )
        return
    
    # Add schedule
    schedule_id = bomber.schedule_manager.add_schedule(
        user_id=user_id,
        phone=phone,
        duration=duration,
        scheduled_time=scheduled_time_str,
        username=username
    )
    
    # Calculate time until execution
    time_diff = scheduled_dt - now
    hours = int(time_diff.total_seconds() // 3600)
    minutes = int((time_diff.total_seconds() % 3600) // 60)
    
    await update.message.reply_text(
        f"⏰ **ATTACK SCHEDULED!**\n\n"
        f"🆔 **Schedule ID:** `{schedule_id}`\n"
        f"📱 **Target:** `+91{phone}`\n"
        f"⏰ **Duration:** {duration} minutes\n"
        f"📅 **Scheduled For:** {scheduled_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"⏳ **Starts In:** {hours}h {minutes}m\n\n"
        f"✅ Attack will start automatically!\n"
        f"🗑️ Use `/cancel {schedule_id}` to cancel",
        parse_mode='Markdown'
    )
    
    # Notify admin
    try:
        user_data = bomber.user_manager.get_user_info(user_id)
        custom_name = user_data.get('username', None) if user_data else None
        
        admin_msg = (
            f"📅 **NEW SCHEDULED ATTACK**\n\n"
            f"👤 **User:** @{username} (`{user_id}`)\n"
        )
        if custom_name:
            admin_msg += f"📛 **Name:** {custom_name}\n"
        admin_msg += (
            f"📱 **Target:** `+91{phone}`\n"
            f"⏰ **Duration:** {duration} min\n"
            f"📅 **Scheduled:** {scheduled_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"🆔 **ID:** `{schedule_id}`"
        )
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_msg,
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Failed to notify admin about schedule: {e}")

@authorized_only
async def view_schedules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    schedules = bomber.schedule_manager.get_user_schedules(user_id)
    
    if not schedules:
        await update.message.reply_text("📋 You have no scheduled attacks!")
        return
    
    message = "📅 **YOUR SCHEDULED ATTACKS**\n\n"
    
    for idx, (schedule_id, schedule) in enumerate(schedules.items(), 1):
        phone = schedule['phone']
        duration = schedule['duration']
        scheduled_time = schedule['scheduled_time']
        
        # Calculate time remaining
        scheduled_dt = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")
        time_diff = scheduled_dt - datetime.now()
        
        if time_diff.total_seconds() > 0:
            hours = int(time_diff.total_seconds() // 3600)
            minutes = int((time_diff.total_seconds() % 3600) // 60)
            time_remaining = f"{hours}h {minutes}m"
        else:
            time_remaining = "Executing soon..."
        
        message += (
            f"**{idx}. ID:** `{schedule_id}`\n"
            f"   ├ Target: `+91{phone}`\n"
            f"   ├ Duration: {duration} min\n"
            f"   ├ Scheduled: {scheduled_time}\n"
            f"   └ Starts in: {time_remaining}\n\n"
        )
    
    message += f"📊 **Total Scheduled:** {len(schedules)}\n"
    message += f"🗑️ Use `/cancel <id>` to cancel"
    
    await update.message.reply_text(message, parse_mode='Markdown')

@authorized_only
async def cancel_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if len(context.args) != 1:
        await update.message.reply_text(
            "❌ **Invalid Usage!**\n\n"
            "📝 **Correct Format:**\n"
            "`/cancel <schedule_id>`\n\n"
            "🎯 **Example:**\n"
            "`/cancel a1b2c3d4`\n\n"
            "💡 Use `/schedules` to see your schedule IDs",
            parse_mode='Markdown'
        )
        return
    
    schedule_id = context.args[0]
    
    if bomber.schedule_manager.cancel_schedule(schedule_id, user_id):
        await update.message.reply_text(
            f"✅ **Schedule Cancelled!**\n\n"
            f"🆔 **Schedule ID:** `{schedule_id}`\n"
            f"🗑️ The scheduled attack has been removed.",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            f"❌ **Schedule Not Found!**\n\n"
            f"Schedule ID `{schedule_id}` doesn't exist or doesn't belong to you.\n\n"
            f"💡 Use `/schedules` to see your active schedules.",
            parse_mode='Markdown'
        )
