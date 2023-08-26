import discord
import imaplib
import email
from discord.ext import commands

TOKEN = ""
GMAIL_USER = ""
GMAIL_PASSWORD = ""
TARGET_EMAIL = ""

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents, debug_guilds=[564902261327921186])

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.slash_command()
async def check_emails(ctx):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(GMAIL_USER, GMAIL_PASSWORD)
    mail.select('inbox')
    _, data = mail.search(None, f'FROM "{TARGET_EMAIL}"')
    email_ids = data[0].split()

    _, msg_data = mail.fetch(email_ids[-1], '(RFC822)')
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                email_content = part.get_payload(decode=True).decode('utf-8')
                break
    else:
        email_content = msg.get_payload(decode=True).decode('utf-8')
    dat = email_content.split("\n")
    finded = False
    for i in dat:
        if finded:
            finded = i
            break
        if len(i) and i[-1] == ":":
            finded = True
    mail.logout()
    await ctx.respond(finded if finded else "No code found!")

bot.run(TOKEN)