from SJM.Cache.admins import admins
from TrickyAbhi.main import call_py
from pyrogram import Client, filters
from SJM.decorators import authorized_users_only
from SJM.filters import command, other_filters
from SJM.queues import QUEUE, clear_queue
from SJM.utils import skip_current_song, skip_item
from config import BOT_USERNAME, GROUP_SUPPORT, IMG_3, UPDATES_CHANNEL
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 Go Back", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🗑 Close", callback_data="cls")]]
)


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}", f"تحديث", f"حديث"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅تم إعادة تحميل البوت ** بشكل صحيح! **  \n✅ ** تم تحديث قائمة المسؤولين ** **! **"
    )


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "vskip", f"تخطي", f"خطي"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="• Mᴇɴᴜ", callback_data="cbmenu"
                ),
                InlineKeyboardButton(
                    text="• Cʟᴏsᴇ", callback_data="cls"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ قائمة التشغيل فارغه")
        elif op == 1:
            await m.reply("✅ قوائم الانتظار ** فارغة. ** \n\n** • خروج المستخدم من الدردشة الصوتية **")
        elif op == 2:
            await m.reply("🗑️ **🗑️مسح قوائم الانتظار ** \n \n ** • مغادرة المستخدم الآلي للدردشة الصوتية **")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"⏭ **Skipped to the next track.**\n\n🏷 **الاسم:** [{op[0]}]({op[1]})\n💭 **المجموعه:** `{chat_id}`\n💡 **الحاله:** `Playing`\n🎧 **طلب بواسطه:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **removed song from queue:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["stop", f"stop@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}", "vstop", f"انهاء", f"نهاء"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ تم ايقاف التشغيل**")
        except Exception as e:
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **nothing is streaming**")


@Client.on_message(
    command(["pause", f"pause@{BOT_USERNAME}", "vpause", f"ايقاف"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "⏸ **تم ايقاف المسار موقتآ**\n\n• **لٲستئناف البث استخدم**\n» /resume الامر"
            )
        except Exception as e:
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **قائمة التشغيل فارغه**")


@Client.on_message(
    command(["resume", f"resume@{BOT_USERNAME}", "vresume", f"كمل", f"استئناف", f"ستئناف", f"استئنف", f"استكمال", f"استكمل"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▶️ **تم استئناف المسار**\n\n• **لايقاف البث موقتآ استخدم**\n» /pause الامر"
            )
        except Exception as e:
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **قائمة التشغيل فارغه**")


@Client.on_message(
    command(["mute", f"mute@{BOT_USERNAME}", "vmute", f"ميوت", f"يوت"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "🔇 **تم كتم الصوت**\n\n• **لرفع الكتم استخدم**\n» /unmute الامر"
            )
        except Exception as e:
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **قائمة التشغيل فارغه**")


@Client.on_message(
    command(["unmute", f"unmute@{BOT_USERNAME}", "vunmute", f"فك_ميوت"]) & other_filters
)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "🔊 **تم رفع الكتم**\n\n• **لكتم الصوت استخدم**\n» /mute الامر."
            )
        except Exception as e:
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **قائمة التشغيل فارغه**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "⏸ توقف البث موقت", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ قائمة التشغيل فارغه", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "▶️ تم استئناف البث", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ قائمة التشغيل فارغه", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("✅ **تم ايقاف التشغيل**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"🚫 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ قائمة التشغيل فارغه", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 تم كتم الصوت", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ قائمة التشغيل فارغه", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 تم تشغيل الصوت", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ قائمة التشغيل فارغه", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"✅ **تم ضبط الصوت على** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **قائمة التشغيل فارغه**")

        
@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "💬 توقف البث موقت", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"💬 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 قائمة التشغيل فارغه", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "💬 تم استئناف البث", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"💬 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 قائمة التشغيل فارغه", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("💬 **تم ايقاف التشغيل**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"💬 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 قائمة التشغيل فارغه", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "💬 تم كتم الصوت", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"💬 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 قائمة التشغيل فارغه", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "💬 تم تشغيل الصوت", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"💬 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 قائمة التشغيل فارغه", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"💬 **تم ضبط الصوت على** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"💬 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("💬 **قائمة التشغيل فارغه**")
        
        
        # whats up  by Herox
