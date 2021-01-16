#!/usr/bin/python

import re
import discord as ds
from lib.input import *

# very important art :)
art = """
 \033[1m_________________________________\033[0m
\033[1m<\033[0m \033[96m\033[1mrmds\033[0m \033[1mv\033[0m\033[92m1.0\033[0m: \033[4mDiscord Cleanup Tool\033[0m \033[1m>\033[0m
 \033[1m---------------------------------\033[0m
        \   ^__^
         \  (oo)\_______
            (__)\       )\/
                ||----w |
                ||     ||
"""


print(art)

# reading the auth token
authfile = open("auth.txt", "r")
authToken = authfile.readlines()[0]

c = ds.Client()

async def get_target_server(c):
	inp = get_value_of_key("-i") or input("Input target server: ")
	target = c.get_guild(int(inp))

	if( target != None ):
		await attack_server(target, c)
		await c.close()
	else:
		print(f"\nUnknown server {inp}")
		print(f"Target Object: {target}")

		return await get_target_server(c)

@c.event
async def on_ready():
	print(f"\033[92mLogged in as: {c.user}\033[0m")
	await get_target_server(c)

async def attack_server(server, c):
	print(f"Wiping server: \033[1m {server} \033[0m")

	if( not key_valid("--noask") ):
		print(f"\nAll of your messages in \033[1m{server}\033[0m will be \033[1m\033[91mDELETED FOREVER\033[0m!\033[0m")
		ask = input("Are you sure?! (y/n): ")
		if( not ask == "y" ):
			print("Aborting...")
			return

	for channel in server.channels:
		if( str(channel.type) == "text" ):
			try:
				await send_payload(channel, c)
			except Exception as err:
				print(f"Unable to wipe channel: {channel} err: {err}")
				pass


async def get_user_messages(channel, c):
	messages = await channel.history(limit=9999).flatten()

	for m in messages:
		if( m.author != c.user ):
			messages.remove(m)

	return messages, len(messages)

async def send_payload(channel, c):
	user_messages, user_messages_len = await get_user_messages(channel, c)

	print(f"\n\t\t#{channel}")

	for i, m in enumerate(user_messages):
		try:
			print(f"[{i+1}/{user_messages_len}]\t \033[1m\033[91mrm\033[0m \t({m.id}) : \"{m.content}\"")
		except Exception as err:
			print(f"err: {err}")
			pass




c.run(authToken, bot=False)
