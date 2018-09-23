import discord
import time
import asyncio
import random
import json
from discord.ext import commands

TOKEN = 'NDkyODg5NDY3OTYzNTcyMjI0.Doc-rQ.FknvclFQ0EKTLWqIjeLxauvbfrU'

client = commands.Bot(command_prefix='!')
client.remove_command('help')

HelpCommand ="""
```css
<---Timer Commands--->
You can set the timer by useing this function: !timer 5
It will ping you after it is done!```
"""


@client.event
async def on_ready():
    print("Ready")
    await client.change_presence(game=discord.Game(name=f"over {len(set(client.get_all_members()))} Users - !help", type=3))

@client.event
async def on_command_error(error, ctx):
    channel = ctx.message.channel
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name='Incorrect Command!', value='There was an error! Please type ``!help``\n You can use!', inline=True)
        await client.send_message(channel, embed=embed)
    if isinstance(error, commands.NoPrivateMessage):
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name='Unknown Error', value='```We beilive that you do not let random people text you!\nPlease enable your PM messages so you can see this amazing\nMessage!```', inline=True)
        await client.say(embed=embed)

print("Loaded Kick")
@client.command(pass_context=True)
async def kick(ctx, user: discord.Member = None):
	#Function: !kick @User:
	author = ctx.message.author
	server = ctx.message.server
	if ctx.message.author.server_permissions.kick_members:
		if user is None:
			embed = discord.Embed(color=0xff00f0)
			embed.add_field(name=":interrobang: Unknown User!", value='Please specify a user for me to kick.')
			await client.say(embed=embed)
			#Sends the embed to the channel were they did not specify a user for me to kick!
		else:
			await client.kick(user)
			#Will kick the user from the server!
			embed = discord.Embed(color=0xff00f0)
			embed.add_field(name="Kicked by:", value=f"{author}", inline=False)
			embed.add_field(name="Server in:", value=f"{server.name}", inline=True)
			embed.set_footer(text="Member has been kicked.")
			await client.say(embed=embed)
	else:
		embed = discord.Embed(color=0x2700ff)
		embed.add_field(name="Missing Perms:", value="You need a permission for this command: ``Kick_Members``", inline=False)
		await client.send_message(author, embed=embed)
		embed = discord.Embed(color=0xff00f0)
		embed.add_field(name="Missing Perms:", value="You need a permission for this command: ``Kick_Members``", inline=False)
		await client.say(embed=embed)

print("Loaded Ban")
@client.command(pass_context=True)
async def ban(ctx, user: discord.Member = None):
	#Function: !kick @User:
	author = ctx.message.author
	server = ctx.message.server
	if ctx.message.author.server_permissions.ban_members:
		if user is None:
			embed = discord.Embed(color=0xff00f0)
			embed.add_field(name=":interrobang: Unknown User!", value="Please specify a user you want me to ban.", inline=False)
			await client.say(embed=embed)
		else:
			await client.ban(user)
			#Will ban the user from the server!
			embed = discord.Embed(color=0xff00f0)
			embed.add_field(name="Banned by:", value=f"{author}", inline=False)
			embed.add_field(name="Server in:", value=f"{server.name}", inline=True)
			embed.set_footer(text="Member has been banned.")
			await client.say(embed=embed)
	else:
		embed = discord.Embed(color=0xff00f0)
		embed.add_field(name="Missing Perms:", value="You need a permission for this command: ``Ban_Members``", inline=False)
		await client.send_message(author, embed=embed)
		embed = discord.Embed(color=0xff00f0)
		embed.add_field(name="Missing Perms:", value="You need a permission for this command: ``Ban_Members``", inline=False)
		await client.say(embed=embed)

print("Loaded Ping")
@client.command(pass_context=True)
async def ping(ctx):
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await client.send_typing(channel)
        t2 = time.perf_counter()
        embed=discord.Embed(title=":hourglass_flowing_sand: | My ping is:", description='**Latency: {}ms**'.format(round((t2-t1)*1000)), color=0xff00f0)
        await client.say(embed=embed)

@client.command(pass_context=True)
async def mute(ctx, user: discord.Member = None):
	server = ctx.message.server
	if ctx.message.author.server_permissions.mute_members:
		if user is None:
			embed = discord.Embed(color=0xff00f0)
			embed.add_field(name=":interrobang: Unknown User!", value="Please specify a user you want me to mute!", inline=True)
			await client.say(embed=embed)
		else:
			mutedrole = discord.utils.get(ctx.message.server.roles, name="Muted")
			await client.add_roles(user, mutedrole)
			embed = discord.Embed(color=0xff00f0)
			embed.add_field(name="Muted user:", value=f"You have muted **{user}**", inline=False)
			await client.say(embed=embed)
	else:
		embed = discord.Embed(color=0xff00f0)
		embed.add_field(name="Missing Perms!", value="You are missing permissions: ``Mute_Members``", inline=False)
		await client.say(embed=embed)

@client.command(pass_context=True)
async def unmute(ctx, user: discord.Member = None):
	server = ctx.message.server
	if ctx.message.author.server_permissions.mute_members:
		if user is None:
			embed = discord.Embed(color=0xff00f0)
			embed.add_field(name=":interrobang: Unknown User!", value="Please specify a user you want me to unmute!", inline=True)
			await client.say(embed=embed)
		else:
			mutedrole = discord.utils.get(ctx.message.server.roles, name="Muted")
			await client.remove_roles(user, mutedrole)
			embed = discord.Embed(color=0xff00f0)
			embed.add_field(name="Unmuted user:", value=f"You have unmuted **{user}**", inline=False)
			await client.say(embed=embed)
	else:
		embed = discord.Embed(color=0xff00f0)
		embed.add_field(name="Missing Perms!", value="You are missing permissions: ``Mute_Members``", inline=False)
		await client.say(embed=embed)




print("Loaded Timer")
@client.command(pass_context=True)
async def timer(ctx, time=None):
    if time is None:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name=':interrobang: **Error**', value='Oops! Please define the seconds you want me to set for you!', inline=False)
        embed.set_footer(text='Please set a timer >timer <amount>')
        await client.say(embed=embed)
    channel = ctx.message.channel
    author = ctx.message.author
    message = []
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name=':stopwatch: Timer!:', value='Timer set for **{}** seconds'.format(int(time), inline=True))
    embed.set_footer(text='Timer:')
    await client.say(embed=embed)
    await asyncio.sleep(int(time))
    msg=await client.say('{}'.format(author.mention))
    await client.delete_message(msg)
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name=':stopwatch: Timer Up:', value='Timer is up **{}**'.format(author.name), inline=True)
    embed.set_footer(text='Timer:')
    await client.say(embed=embed)

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    server = ctx.message.server
    embed = discord.Embed(color=0xff00f0)
    embed.set_author(name="KreamyBot Help Manual")
    embed.add_field(name=":moneybag: ***___Economy:___***", value="**!daily** Get some daily Coins \n **!work** Get some working Coins \n **!bal** See all your current Coins", inline=False)
    embed.add_field(name=":tools: ***__Moderation:__***", value="**!kick @user** Kicks the user you mentioned \n **!ban @user** Bans the user you mentioned \n **!mute @user** Muted the user you have mentioned \n **!unmute @user** Unmutes the user you mentioned \n **!clear 5** Clears the amount of messages you said to clear Limit: *2-100* \n **!nick @user Awesome Scauce** Changes the mentioned user to the nickname you set", inline=True)
    embed.add_field(name=":tada: ***__Fun:__***", value="**!avatar** Will show your avatar only \n **!avatar @user** Will show that users  \n **!memes** Will show you a random meme!", inline=False)
    embed.add_field(name=":books: ***__Infos:__***", value="**!botinfo** Will give you the bots info \n **!userinfo @user** Will show that users info \n **!serverinfo** Shows the servers info \n **!membercount** Shows the servers membercount", inline=True)
    embed.add_field(name=":warning: ***__Administration:__***", value="**!crole <name>** Will create a role with <name> you set \n **!drole <name>** Will delete the role you have said \n **!setup** Will create everything for the bot if you havent got it yet", inline=False)
    embed.add_field(name=":candy: ***__Other Economy:__***", value="**!candy** Will show you your candy balance \n **!eat** You will gain candy points", inline=False)
    embed.add_field(name=":heavy_plus_sign: ***__Math:__***", value="**!add <num> <num>** Adds the numbers \n **!sub <num> <num>** Subtracts the numbers \n **!mul <num> <num>** Multiplies the numbers together \n **!div <num> <num>** Divides the numbers", inline=True)
    embed.add_field(name=":ping_pong: ***__Others:__***", value="**!timer <seconds>** Will set a timer and ping you \n **!ping** Will shows the bots ping \n **!invite** Will send you a Private Message and will send you the link", inline=False)
    await client.send_message(author, embed=embed)
    embed = discord.Embed(color=0xff00f0)
    embed.set_author(name="We have sent a PM containing the help message")
    await client.say(embed=embed)

@client.event
async def on_member_join(member):
	server = member.server
	channels = [
            "welcome-goodbye",
            "welcome",
            "welcome-and-goodbye",
            "welcome-good_bye",
        ]
	channel = discord.utils.get(server.channels, name=channels)
	embed = discord.Embed(color=0xff00f0)
	embed.add_field(name=f":wave: Welcome {member}", value=f"You have joined {server}, enjoy your stay!", inline=False)
	embed.set_image(url="https://cdn.discordapp.com/attachments/492889926900252695/493233175267639328/Welcome2.jpg")
	await client.send_message(channel, embed=embed)
	await client.change_presence(game=discord.Game(name=f"over {len(set(client.get_all_members()))} Users - !help", type=3))

@client.event
async def on_member_remove(member):
    server = member.server
    channel = discord.utils.get(server.channels, name="welcome-goodbye")
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name=f":wave: {member}", value=f"{member} has sady left us :(", inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/492889926900252695/493237009364549652/Goodbye.jpg")
    await client.send_message(channel, embed=embed)
    await client.change_presence(game=discord.Game(name=f"over {len(set(client.get_all_members()))} Users - !help", type=3))

@client.command(pass_context=True)
async def setup(ctx):
    if ctx.message.author.server_permissions.administrator:
        server = ctx.message.server
        await client.create_channel(server=server, name="welcome-goodbye")
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name="Information:", value="I have added a channel to your server! Please make sure you check the permissions!", inline=False)
        await client.say(embed=embed)
    else:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name=':interrobang: **Error**', value='Oops! You cant use this command. Permission Required: ``Administrator``', inline=False)
        await self.client.say(embed=embed)
    

@client.command(pass_context=True)
async def crole(ctx, *, role):
    if ctx.message.author.server_permissions.manage_roles:
        server = ctx.message.server
        author = ctx.message.author
        await client.create_role(server=server, name=role)
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name='Creation!', value=f"**{role}** Has been created!", inline=False)
        embed.add_field(name='Author:', value=f"**{author}**", inline=True)
        embed.add_field(name="Info:", value="Please make sure the perms are for you and your server!", inline=False)
        await client.say(embed=embed)
    else:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name=':interrobang: **Error**', value='Oops! You cant use this command. Permission Required: ``Manage_Roles``', inline=False)
        await self.client.say(embed=embed)
        


@client.command(pass_context=True)
async def drole(ctx, *, name):
    if ctx.message.author.server_permissions.manage_roles:
        author = ctx.message.author
        server = ctx.message.server
        role = discord.utils.get(ctx.message.server.roles, name=name)
        await client.delete_role(server=server, role=role)
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name='Deletion!', value=f"**{name}** Has been deleted!", inline=False)
        embed.add_field(name='Author:', value=f"**{author}**", inline=True)
        await client.say(embed=embed)
    else:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name=':interrobang: **Error**', value='Oops! You cant use this command. Permission Required: ``Manage_Roles``', inline=False)
        await self.client.say(embed=embed)
    
        
    
    

@client.command(pass_context=True)
async def work(ctx):
    with open("coins.json", "r") as f:
       	coins = json.load(f)
    author = ctx.message.author
    coinsc = random.randint(1, 700)
    if not ctx.message.server.id in coins:
       	coins[ctx.message.server.id] = {}
    if not author.id in coins[ctx.message.server.id]:
        coins[ctx.message.server.id][author.id] = 0
    coins[ctx.message.server.id][author.id] += coinsc
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name="Work!", value=f"You have worked all day! You deserve :moneybag: ``{coinsc}`` as a prize!", inline=False)
    embed.set_footer(text="Enjoy!")
    await client.say(embed=embed)
    with open("coins.json", "w") as f:
        json.dump(coins, f, indent=4)

@client.command(pass_context=True)
async def bal(ctx):
    with open("coins.json", "r") as f:
        coins = json.load(f)
    author = ctx.message.author
    if not author.id in coins[ctx.message.server.id]:
        coins[ctx.message.server.id][author.id] = 0
    coinss = coins[ctx.message.server.id][author.id]
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name="Balance!", value=f"You have :moneybag: ``{coinss}`` in your bank account!", inline=False)
    embed.set_footer(text="More money commands! type: !help")
    await client.say(embed=embed)

@client.command(pass_context=True)
async def daily(ctx):
    with open("coins.json", "r") as f:
       	coins = json.load(f)
    author = ctx.message.author
    coinsc = random.randint(1, 700)
    if not ctx.message.server.id in coins:
       	coins[ctx.message.server.id] = {}
    if not author.id in coins[ctx.message.server.id]:
        coins[ctx.message.server.id][author.id] = 0
    coins[ctx.message.server.id][author.id] += coinsc
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name="Daily!", value=f"+ :moneybag: ``{coinsc}``", inline=False)
    embed.set_footer(text="Enjoy your money!")
    await client.say(embed=embed)
    with open("coins.json", "w") as f:
        json.dump(coins, f, indent=4)


@client.command(pass_context=True)
async def clear(ctx, amount=None):
    if ctx.message.author.server_permissions.manage_messages:
        if amount is None:
            embed = discord.Embed(color=0xff00f0)
            embed.add_field(name=':interrobang: **Error**', value='Oops! Please define the amount of messages you want me to delete!', inline=False)
            embed.set_footer(text='You need permission to continue if you dont have!')
            await client.say(embed=embed)
        else:
            channel = ctx.message.channel
            author = ctx.message.author
            messages = []
            async for message in client.logs_from(channel, limit=int(amount)):
                messages.append(message)
            await client.delete_messages(messages)
            embed = discord.Embed(color=0xff00f0)
            embed.set_author(name='Clear - Information')
            embed.add_field(name='Amount:', value='**I have deleted {} messages**'.format(amount), inline=False)
            embed.add_field(name='Author:', value='**{}**'.format(author.name), inline=False)
            msg = await client.say(embed=embed)
            await asyncio.sleep(5)
            await client.delete_message(msg)
    else:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name=':interrobang: **Error**', value='Oops! You cant use this command. Permission Required: ``Manage Messages``', inline=False)
        embed.set_footer(text='You cant use this command!')
        await self.client.say(embed=embed)

@client.command(pass_context=True)
async def nick(ctx, member:discord.User=None, *, newnick=None):
    author = ctx.message.author
    if ctx.message.author.server_permissions.manage_nicknames:
        if member is None:
            embed = discord.Embed(color=0xff00f0)
            embed.add_field(name=':interrobang: **Error**', value='Oops! Please define the user you want me to change the nickname of!', inline=False)
            embed.set_footer(text='You need permission to continue if you dont have!')
            await client.say(embed=embed)
        else:
            await client.change_nickname(member, newnick)
            embed = discord.Embed(color=0xff00f0)
            embed.set_author(name='{} Nickname has been changed.'.format(member.name))
            embed.add_field(name='Changed:', value='You have changed the nickname to: **{}**'.format(newnick), inline=True)
            await client.say(embed=embed)
    else:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name=':interrobang: **Error**', value='Oops! You cant use this command. Permission Required: ``Manage Nicknames``', inline=False)
        embed.set_footer(text='You cant use this command!')
        await client.say(embed=embed)

@client.command(pass_context=True)
async def avatar(ctx, user: discord.Member = None):
    author = ctx.message.author
    if user is None:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name='Your avatar!', value=f'**{author}**s avatar!', inline=True)
        embed.set_image(url=author.avatar_url)
        embed.set_footer(text='Your avatar! Reminder: You can say: !avatar <user> for there profile picture!')
        await client.say(embed=embed)
    else:    
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name='You asked for an avatar!', value=f'**{user}**s avatar!', inline=True)
        embed.set_image(url=user.avatar_url)
        embed.set_footer(text='The avatar!')
        await client.say(embed=embed)

@client.command(pass_context=True)
async def gamble(ctx, amount: int):
    with open("coins.json", "r") as f:
        coins = json.load(f)
    choices = random.randint(0, 1)
    amountt = coins[ctx.message.server.id][ctx.message.author.id]
    if coins[ctx.message.server.id][ctx.message.author.id] <= 1:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name="Wrong!", value=f"You dont have enough! Required: ``2``. Your balance: ``{amountt}``.", inline=False)
        await client.say(embed=embed)
        return
    if amount > coins[ctx.message.server.id][ctx.message.author.id]:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name="Not Enough!", value="You don't have sufficiant coins.", inline=False)
        await client.say(embed=embed)
        return
    if amount <= 0:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name="Not Enough", value="You cannot gamble anything less then ``0``!", inline=False)
        await client.say(embed=embed)
        return
    if choices == 0:
        coins[ctx.message.server.id][ctx.message.author.id] += amount * 2
        won = amount * 2
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name="You won!", value=f"You won! You won ``{won}``.", inline=False)
        await client.say(embed=embed)
    else:
        coins[ctx.message.server.id][ctx.message.author.id] -= amount
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name="You lost", value=f"You lost! Taken ``{amount}`` from your balance.", inline=False)
        await client.say(embed=embed)
    with open("coins.json", "w") as f:
        json.dump(coins, f, indent=4)

@client.command()
async def cc():
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name="Economy", value=":white_medium_small_square: Gamble", inline=False)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Here's what I could find.", color=0xff00f0)
    embed.set_author(name="Server info")
    embed.add_field(name="**Name**", value=ctx.message.server.name, inline=True)
    embed.add_field(name="**ID**", value=ctx.message.server.id, inline=False)
    embed.add_field(name="**Roles**", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="**Members**", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def userinfo(ctx, user: discord.Member = None):
    if user is None:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name=':interrobang: **Error**', value='Oops! Please specify a user for me to give info about!', inline=False)
        await client.say(embed=embed)
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x36393E)
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name="**Users Name Is:**", value="{}".format(user.name), inline=False)
    embed.add_field(name="**Highest Role Is:**", value="{}".format(user.top_role), inline=False)
    embed.add_field(name="**Users ID Is:**", value="{}".format(user.id), inline=False)
    embed.add_field(name="**Users Nickname Is:**", value="{}".format(user.nick), inline=False)
    embed.add_field(name="**Users Status Is:**", value="{}".format(user.status), inline=False)
    embed.add_field(name="**Users Game Is:**", value="{}".format(user.game), inline=False)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def membercount(ctx):
    server = ctx.message.server
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name=f"**__{server}'s Membercount:__**", value=len(ctx.message.server.members))
    await client.say(embed=embed)

@client.command(pass_context=True)
async def botinfo(ctx):
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await client.send_typing(channel)
    t2 = time.perf_counter()
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name="***__Ping:__***", value="**Latency: {}ms**".format(round((t2-t1)*1000)), inline=True)
    embed.add_field(name="***__Members Hosting:__***", value=f"**{len(set(client.get_all_members()))}**", inline=False)
    await client.say(embed=embed)

@client.command(aliases = ["8ball"])
async def eight_ball():
    responses = [
        "Sorry its a **No**",
        "Maybe some time later, I can't figure it out!",
        "Maybe, to hard to tell!",
        "You have a 50% chance!",
        "Indeed."
    ]
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name=":8ball: 8ball :8ball:", value=(random.choice(responses)), inline=False)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def eat(ctx):
    with open("candy.json", "r") as f:
       	candy = json.load(f)
    author = ctx.message.author
    candys = random.randint(1, 700)
    if not ctx.message.server.id in candy:
       	candy[ctx.message.server.id] = {}
    if not author.id in candy[ctx.message.server.id]:
        candy[ctx.message.server.id][author.id] = 0
    candy[ctx.message.server.id][author.id] += candys
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name="Food, Candy!", value=f"You have worked all day! You deserve :candy: ``{candys}`` as a prize!", inline=False)
    embed.set_footer(text="Enjoy!")
    await client.say(embed=embed)
    with open("candy.json", "w") as f:
        json.dump(candy, f, indent=4)

@client.command(pass_context=True)
async def candy(ctx):
    with open("candy.json", "r") as f:
        candy = json.load(f)
    author = ctx.message.author
    if not author.id in candy[ctx.message.server.id]:
        candy[ctx.message.server.id][author.id] = 0
    candys = candy[ctx.message.server.id][author.id]
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name="Balance!", value=f"You have :candy: ``{candys}`` in your bank account!", inline=False)
    embed.set_footer(text="More candy commands! type: !help")
    await client.say(embed=embed)

@client.command(pass_context=True)
async def cdaily(ctx):
    with open("candy.json", "r") as f:
       	candy = json.load(f)
    author = ctx.message.author
    candys = random.randint(1, 700)
    if not ctx.message.server.id in candy:
       	candy[ctx.message.server.id] = {}
    if not author.id in candy[ctx.message.server.id]:
        candy[ctx.message.server.id][author.id] = 0
    candy[ctx.message.server.id][author.id] += coinsc
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name="Daily!", value=f"+ :candy: ``{candys}``", inline=False)
    embed.set_footer(text="Enjoy your candy!")
    await client.say(embed=embed)
    with open("candy.json", "w") as f:
        json.dump(candy, f, indent=4)

@client.command()
async def memes():
    memes = [
        "Memes! https://media.giphy.com/media/rsf33kKU6WdA4/giphy.gif",
        "Memes! https://media.giphy.com/media/puOukoEvH4uAw/giphy.gif",
        "Memes! https://media.giphy.com/media/h30Uk86LypXpe/giphy.gif",
        "Memes! https://media.giphy.com/media/d3mlE7uhX8KFgEmY/giphy.gif",
        "Memes! https://media.giphy.com/media/9t6xpYZ9npJmM/giphy.gif",
        "Memes! https://media.giphy.com/media/ZJqPtMjmHbNN6/giphy.gif",
        "Memes! https://media.giphy.com/media/dEdmW17JnZhiU/giphy.gif",
        "Memes! https://media.giphy.com/media/l4Jz3a8jO92crUlWM/giphy.gif",
        "Memes! https://media.giphy.com/media/xL7PDV9frcudO/giphy.gif",
        "Memes! https://media.giphy.com/media/ehc19YLR4Ptbq/giphy.gif",
        "Memes! https://media.giphy.com/media/3oKIPBxpm5tHqcL1Ic/giphy.gif",
        "Memes! https://media.giphy.com/media/xs5rDcfmb8Ms8/giphy.gif",
        "Memes! https://media.giphy.com/media/xT0BKiaM2VGJ553P9K/giphy.gif",
        "Memes! https://media.giphy.com/media/a0Lgc1JvbfS4o/giphy.gif",
        "Memes! https://media.giphy.com/media/l4FGnnlIQslHkOPaU/giphy.gif",
        "Memes! https://media.giphy.com/media/3o6fISqUj1AOxgYwsU/giphy.gif",
        "Memes! https://media.giphy.com/media/T5Jw0y7zrmZzO/giphy.gif"
    ]
    await client.say((random.choice(memes)))


@client.command()
async def add(left : int, right : int):
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name='Math Equations!', value='**{} + {} = {}**'.format(left, right, left + right), inline=True)
    await client.say(embed=embed)

@client.command()
async def sub(left : int, right : int):
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name='Math Equations!', value='**{} - {} = {}**'.format(left, right, left - right), inline=True)
    await client.say(embed=embed)

@client.command()
async def mul(left : int, right : int):
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name='Math Equations!', value='**{} x {} = {}**'.format(left, right, left * right), inline=True)
    await client.say(embed=embed)

@client.command()
async def div(left : int, right : int):
    embed = discord.Embed(color=0xff00f0)
    embed.add_field(name='Math Equations!', value='**{} / {} = {}**'.format(left, right, left / right), inline=True)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def invite(ctx):
    author = ctx.message.author
    embed = discord.Embed(color=0xff00f0)
    embed.title = "***__Here__***"
    embed.url = "https://discordapp.com/api/oauth2/authorize?client_id=492889467963572224&permissions=8&scope=bot"
    embed.add_field(name="Invite", value="The bot invite has administrator perms on there! Please change if you would like.", inline=False)
    await client.send_message(author, embed=embed)
    await client.say(f"{author.mention} Please check your Private Messages!")
        



    
    
    











client.run(TOKEN)
