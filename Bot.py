from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio
import random

# Botun tokeni
TOKEN = "7590293581:AAGF91tqIGGWjFOAMKAwT9qjTBXWsNulVHs"

# Qrup üzvlərini saxlamaq üçün siyahı
group_members = {}

# Emojilər və maraqlı sözlər
emojis = ["🔥", "🚀", "✨", "💥", "💡", "💎", "🌟", "⚡", "🎯", "🎉", "🎵", "💫"]
phrases = [
    "Hamı buradadırmı? 🤔", "Söhbətə qatılın! 🎤", "Siz hardasınız? 🧐", "Maraqlı bir şey danışaq! 😃",
    "Gəlin aktiv olaq! 🚀", "Bir az hərəkət edək! 💃", "Əylənək! 🎉", "Yeni nəsə öyrənək! 📚",
    "İştirak edin! 🗣", "Gəlin oyuna başlayaq! 🎮", "Bura sakitdir, canlandıraq! 🔥", "Kim burada? ✋"
]

# Yeni istifadəçi mesaj yazanda yadda saxlamaq
async def save_users(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id not in group_members:
        group_members[chat_id] = set()

    group_members[chat_id].add((user.id, user.username, user.first_name))

# Etiketləmə funksiyası
async def tag_users(update: Update, context: CallbackContext, mode="group", emojis_enabled=False, phrases_enabled=False):
    chat_id = update.effective_chat.id
    bot = context.bot

    # Botun admin olub-olmadığını yoxla
    bot_member = await bot.get_chat_member(chat_id, bot.id)
    if bot_member.status not in ["administrator", "creator"]:
        await update.message.reply_text("❌ Botun admin hüquqları yoxdur! Adminlik verin.")
        return

    # Əgər qrupda üzv yoxdur, xəbərdarlıq et
    if chat_id not in group_members or not group_members[chat_id]:
        await update.message.reply_text("❌ Tag ediləcək istifadəçi tapılmadı! (Qrupda aktiv istifadəçi yoxdur)")
        return
    
    tag_list = []
    for user_id, username, first_name in group_members[chat_id]:
        tag_text = f"@{username}" if username else f"[{first_name}](tg://user?id={user_id})"
        
        if emojis_enabled:
            tag_text = f"{random.choice(emojis)} {tag_text} {random.choice(emojis)}"
        if phrases_enabled:
            tag_text = f"{random.choice(phrases)}\n{tag_text}"
        
        tag_list.append(tag_text)

    # Qruplaşdırma
    group_size = 4 if mode == "group" else 1 if mode == "single" else 3
    tagged_count = 0

    await update.message.reply_text("✅ Tag prosesi başladı ...💬")

    for i in range(0, len(tag_list), group_size):
        await update.message.reply_text("\n".join(tag_list[i:i+group_size]), parse_mode="Markdown")
        tagged_count += len(tag_list[i:i+group_size])
        await asyncio.sleep(2)  # Flood riskinə qarşı
    
    await update.message.reply_text(f"✅ Tag prosesi başa çatdi ...💭\n🔹 **Toplam tag edilən:** {tagged_count}")

# Start əmri
async def start(update: Update, context: CallbackContext):
    if update.message.chat.type != "private":
        return
    
    keyboard = [
        [InlineKeyboardButton("🧬..Dəstək Qrupu", url="https://t.me/FlexDestekGroup")],
        [InlineKeyboardButton("🧑‍💻..Rəsmi Kanal", url="https://t.me/FlexBotlar")],
        [InlineKeyboardButton("💭..Bot Programist", url="https://t.me/ismayil1ov")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "❗ **Sadəcə aktiv olub mesaj yazan userlərinizi tağ edə bilərsiniz...💬**\n\n"
        "👋 Salam ..💬🧑‍💻 Mən qrupda istifadəçiləri etiketləyib xəbərdar etmək üçün buradayam!\n\n"
        "📚 **Bot Əmrləri:**\n"
        "• `/tag` - 4lü qruplarla tag etməyə başlayacaq\n"
        "• `/tktag` - Tək-tək tag etməyə başlayacaq\n"
        "• `/adtag` - Adminləri tag etməyə başlayır\n"
        "• `/etag` - Emojilər ilə tag edir\n"
        "• `/stag` - Maraqlı sözlərlə tag edir\n"
        "• `/stop` - Tag prosesini dayandırır\n"
        "• `/reload` - Botu yeniləyir",
        reply_markup=reply_markup
    )

async def stop(update: Update, context: CallbackContext):
    await update.message.reply_text("🛑 Tag prosesi dayandırıldı. 💭")

async def reload(update: Update, context: CallbackContext):
    await update.message.reply_text("🔄 Bot yenidən başladılır...")

# Botu başladan funksiya
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tag", lambda u, c: asyncio.create_task(tag_users(u, c, mode="group"))))
    app.add_handler(CommandHandler("tktag", lambda u, c: asyncio.create_task(tag_users(u, c, mode="single"))))
    app.add_handler(CommandHandler("adtag", lambda u, c: asyncio.create_task(tag_users(u, c, mode="admin"))))
    app.add_handler(CommandHandler("etag", lambda u, c: asyncio.create_task(tag_users(u, c, mode="group", emojis_enabled=True))))
    app.add_handler(CommandHandler("stag", lambda u, c: asyncio.create_task(tag_users(u, c, mode="group", phrases_enabled=True))))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("reload", reload))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_users))

    app.run_polling()

if __name__ == "__main__":
    main()
