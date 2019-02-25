#!/usr/bin/python3.6

import discord
from datetime import datetime
import pytz
import sys

TOKEN = "NTQ5MzYyMzk4NTE2MDg0Nzc3.D1Sxgw.cz0Ent5pOqirGgG-zRXxJQvyhdo"

client = discord.Client()


@client.event
async def on_message(message):
    msg = message.content
    author = message.author
    channel = message.channel
    server = message.server

    if author == client.user:
        return

    verify_channel = discord.utils.get(server.channels, name="verify")

    if verify_channel is None:
        await client.send_message(server.owner, "**Error**: There is no channel named \"verify\" in your server, " +
                                  server.name + "! Please add one so that users can be verified.")
        return

    if channel.id == verify_channel.id:

        if msg.lower().strip() == "verify":
            verified_role = discord.utils.get(server.roles, name="Verified")
            if verified_role is not None:
                await client.add_roles(author, verified_role)
                print("Verified user " + author.name + " (ID: " + author.id + ") in server " +
                      server.name + " (ID: " + server.id + ")")
            else:
                await client.send_message(server.owner, "**Error**: There is no role named \"Verified\" in your " +
                                                        "server, " + server.name + "! Please add one so that "
                                                                                   "users can be verified.")

        await client.delete_message(message)

    sys.stdout.flush()

    return


@client.event
async def on_ready():
    date_format = '%I:%M:%S %p'
    date = datetime.now(tz=pytz.utc).astimezone(pytz.timezone('US/Pacific'))
    time = date.strftime(date_format)

    msg1 = "Logged in as " + str(client.user.name) + " with ID " + \
           str(client.user.id) + " at " + str(time) + "."
    print(msg1)
    print("-" * len(msg1))
    print("Logs/Errors:")

    game = discord.Game(name="the verification game")
    await client.change_presence(game=game)

print("Starting up VerifyBot...")
sys.stdout.flush()

client.run(TOKEN)

client.loop.run_until_complete(client.logout())
