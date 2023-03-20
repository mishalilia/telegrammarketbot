from os import getenv


async def is_admin(bot, user_id):
    chat_admins = [adm.user.id for adm in await bot.get_chat_administrators(getenv("ADMIN_CHAT"))]
    if user_id in chat_admins:
        return True
    else:
        return False
