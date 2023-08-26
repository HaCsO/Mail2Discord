import discord
import imaplib
import email
from discord.ext import commands
import configparser

cfg = configparser.ConfigParser()
cfg.read(os.getcwd() + "/config.cfg")
only_channel = int(cfg["GENERAL"]["channel_id"])
TOKEN = cfg["GENERAL"]["token"]
GMAIL_USER = cfg["GENERAL"]["gmail_user"]
GMAIL_PASSWORD = cfg["GENERAL"]["gmail_pass"]
TARGET_EMAIL = cfg["GENERAL"]["target_mail"]

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents, debug_guilds=[686268385138573487])

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
    await bot.get_channel(only_channel).send(f"`{finded}`" if finded else (f"`{dat[151][-11:-5]}`" if len(dat) else "Code not found!"))
    await ctx.respond(f"Смотри в <#{only_channel}>") # hardcoooode!!!

bot.run(TOKEN)