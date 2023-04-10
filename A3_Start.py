import os
import discord
from dotenv import load_dotenv
from datetime import datetime
import csv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
fname = "memberLogon.csv"

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


def get_members():
    members = []
    if os.path.isfile(fname):
        with open(fname, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                members.append(row[0])
    return members


def write_to_csv(member, action):
    with open(fname, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([member.name, action, datetime.now()])


@client.event
async def on_ready():
    print(f'{client.user} connected to Discord!')
    members = get_members()
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    for member in guild.members:
        if str(member.id) not in members:
            members.append(str(member.id))
            write_to_csv(member, "joined")
    print("Initial members:", members)


@client.event
async def on_member_join(member):
    members = get_members()
    if str(member.id) not in members:
        members.append(str(member.id))
        write_to_csv(member, "joined")
    print("Updated members:", members)


@client.event
async def on_member_remove(member):
    members = get_members()
    if str(member.id) in members:
        members.remove(str(member.id))
        write_to_csv(member, "left")
    print("Updated members:", members)


client.run(TOKEN)