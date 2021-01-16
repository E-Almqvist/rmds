#!/usr/bin/python

import re
import discord as ds

# reading the auth token
authfile = open("auth.txt", "r")
authToken = authfile.readlines()[0]

c = ds.Client()

async def get_target_server(c):
	inp = input("Input target server: ")
	target = c.get_guild(int(inp))

	if( target != None ):
		await attack_server(target, c)

		print("\nDone.")
		await exit(0)
	else:
		print(f"\nUnknown server {inp}")
		print(f"Target Object: {target}")

		return await get_target_server(c)

@c.event
async def on_ready():
	print(f"Logged in as: {c.user}")
	await get_target_server(c)

async def attack_server(server, c):
	print(f"Wiping server: {server.id}")

	for channel in server.channels:
		if( str(channel.type) == "text" ):
			try:
				await send_payload(channel, c)
			except:
				print(f"Unable to wipe channel: {channel}")
				pass


async def send_payload(channel, c):
	print(f"Removing messages from channel: {channel}")
	messages = await channel.history(limit=9999).flatten()

	async for m in messages:
		try:
			if( m.author == c.user ):
				print(f"Deleting message: {m}")
		except:
			pass


c.run(authToken, bot=False)
