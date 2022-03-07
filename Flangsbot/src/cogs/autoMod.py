from discord import utils
from discord.message import Message
from discord.ext.commands import command, Cog


#NOTE: For each user that chats in the guild, the bot will check if the user 
# is in the database, if not, the bot will instance in the user the Automod checker
# to verify the user metadata.

content_message: str = ''
last_message: str = ''
last_content_message: str = ''
spam_counter: int = 0

async def AntiScam(message, whitelist):
    global current_message, last_content_message, last_message, spam_counter

    _message_content = f'{message.author.id}: {message.content}'
    _message_content = _message_content.replace("'", "`")

    if _message_content == last_message:
        spam_counter += 1
        await message.delete()
    else:
        last_message = message
        spam_counter = 0

    #TODO: Check if the user is admin or similar, because he can bypass the spam checker.
    if len(message.mentions) > 10 and message.author.id not in whitelist:
        await message.delete()
        spam_counter = 2

#TODO: Add a checker for the user to verify if the user is in the database.
async def UserAutoChecker(message, spam_counter, whitelist):
    ...
    

class AutoMod(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.whitelist = [] #TODO: Get from database the whitelist.
        self.log_channel = None
        self.mute_role = None
        self.verified_role = None

    @Cog.listener()
    async def on_message(self, message):
        if message.content != '':
            pass

def setup(bot):
    bot.add_cog(AutoMod(bot))