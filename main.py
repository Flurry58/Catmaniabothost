import discord
import requests
import keepalive
import aiosqlite
from discord.ext import commands
from discord.utils import get
import json
import os
import sqlite3
from itertools import islice

#from monkeylearn import MonkeyLearn
#ml = MonkeyLearn('a84d30868cfcc851f5ac5f21d48b2f64786518df')
#model_id = 'cl_pi3C7JiL'
client = commands.Bot(command_prefix='&')
client2 = discord.Client()
memberlist = []
updatefunc = False

def isPower (x, y):
     
    # The only power of 1
    # is 1 itself
    if (x == 1):
        return (y == 1)
         
    # Repeatedly compute
    # power of x
    pow = 1
    while (pow < y):
        pow = pow * x
 
    # Check if power of x
    # becomes y
    return (pow == y)
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 
@client.event
async def on_ready():
    print("Bot is on")

@client.event
async def on_member_join(member):
  sender_id = str(ctx.author)
  #db[sender_id] = 0
  member = ctx.author
  role_members = discord.utils.get(ctx.guild.roles, name='Level 1')
  with open('users.json', 'r') as f:
    users = json.load(f)
    await update_data(users, member)

    with open('users.json', 'w') as f:
      json.dump(users, f)


  await member.add_roles(role_members)
  await member.create_dm()
  await member.dm_channel.send(f'Hi {member.name}, welcome to my Discord server!')


@client.command()
async def clear_data(ctx):
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    realms = sqlite3.connect('realm.db')
    curs = realms.cursor()
    curs.execute('DROP table realms')
    curs.execute('CREATE TABLE realms(name, realm_name)')
    realms.commit()
    await ctx.send("Database cleared")
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)
@client.command()
async def view_realms(ctx):
  realms = sqlite3.connect('realm.db')
  curs = realms.cursor()
  curs.execute("SELECT realm_name FROM realms")
  rows = curs.fetchall()
  realms.commit()
  realms = sqlite3.connect('realm.db')
  curs = realms.cursor()
  curs.execute("SELECT name FROM realms")
  names = curs.fetchall()
  realms.commit()
  realmlist = []
  namelist = []
  for row in rows:
    string = str(row)
    without = string.translate({ord('('): None})
    with2 = without.translate({ord(')'): None})
    realmlist.append(str(with2))
  for row in names:
    string = str(row)
    without = string.translate({ord('('): None})
    with2 = without.translate({ord(')'): None})
    with2 = with2.translate({ord(','): None})
    with2 = with2.translate({ord("'"): None})
    print(with2)
    namelist.append(str(with2))
  amount = len(realmlist)
  if amount == 0:
    embed = discord.Embed(title="No applications found", color=0xff00f6) 
    await ctx.send(embed=embed)
    return
  else:
    for idx, word in enumerate(realmlist):
      splitlist = realmlist[idx].split(",")
      del splitlist[0]
      del splitlist[4]
      print(splitlist)
      new = splitlist[3].translate({ord("'"): None})
      splitlist[3] = new
      present = "Realm Name: (" + splitlist[0] + ") OP's: (" + splitlist[1] + ") Time Active So Far: (" + splitlist[2] + ") Staying Active?: (" + splitlist[3] + ")"
      embed = discord.Embed(title=namelist[idx], description=present, color=0xff00f6) 
      await ctx.send(embed=embed)

  
@client.command(pass_context=True)
async def application(ctx):
  name = ctx.author
  await name.create_dm()
  await name.dm_channel.send(f'Please type the realm name you want to advertise:')
  def check(msg):
        return msg.author == ctx.author and msg.channel == name.dm_channel
  msg = await client.wait_for("message", check=check)
  realm_name = str(msg.content)
  await name.create_dm()
  await name.dm_channel.send("Please type a list of the OP's of the realm seperated by (;):")
  msg = await client.wait_for("message", check=check)
  op_list = str(msg.content)
  await name.create_dm()
  await name.dm_channel.send("How long has this realm been active for?:")
  msg = await client.wait_for("message", check=check)
  active_long = str(msg.content)
  await name.create_dm()
  await name.dm_channel.send("Is this realm going to be active?:")
  msg = await client.wait_for("message", check=check)
  active = str(msg.content)
  namestr = str(ctx.author)
  questions = [",", realm_name, ",", op_list, ",", active_long, ",", active]
  questions = listToString(questions)
  realms = sqlite3.connect('realm.db')
  curs = realms.cursor()
  curs.execute('insert into realms values (?,?)', (namestr, questions))
  realms.commit()
  await name.dm_channel.send("Request sent to database!")

@client.command()
async def suggest(ctx, *, message):
  channel = discord.utils.get(ctx.guild.text_channels, name="『suggestions』")
  await channel.send(message)
  
@client.command(pass_context=True, help="enable afk role")
async def afk_on(ctx):
  author = ctx.author
  role = discord.utils.get(ctx.guild.roles, name='AFK')
  await author.add_roles(role)
  
  await ctx.send("You are now labeled as AFK. To disable it type afk_off")

@client.command()
async def say(ctx, *, message):
  await ctx.send(message)

  
@client.command(pass_context=True, help="disable afk role")
async def afk_off(ctx):
  member = ctx.author
  role_members = discord.utils.get(ctx.guild.roles, name='Members')
  role_muted = discord.utils.get(ctx.guild.roles, name='AFK')
  await member.remove_roles(role_muted)
  await member.add_roles(role_members)
  await ctx.send("You are not afk anymore!")
  
@client.command(pass_context = True)
async def add_role(ctx, *, role_add):
  user = ctx.author
  if "[!]" in role_add:
    embed = discord.Embed(title="Permission Denied.", description="You can't add an administrator role to yourself", color=0xff00f6) 
    await ctx.send(embed=embed)
  else:
    try:
      role_get = discord.utils.get(ctx.guild.roles, name=str(role_add))
      await user.add_roles(role_get)
      await ctx.send(f"Role added to {user}")
    except AttributeError:
      await ctx.send("That role doesn't exist!")

@client.command()
async def commands(ctx):
  member_command_list = "add_role (role), afk_off, afk_on, say [](make the bot say something), application, suggest"
  admin_command_list = "mute [@user], unmute[@user], deletechannel [channel name], warn [@user] [message to send], clearwarnings[@user], checkwarnings[@user], ban[@user], kick[@user], clear_data (clears realm application database), view_realms (view realm application database)"
  embed = discord.Embed(title="Info", description="Note if a word is in brackets you don't have to write the brackets in the command", color=0xff00f6) 
  await ctx.send(embed=embed)
  embed = discord.Embed(title="Member Commands", description=member_command_list, color=0xff00f6) 
  await ctx.send(embed=embed)
  embed = discord.Embed(title="Admin Commands", description=admin_command_list, color=0xff00f6) 
  await ctx.send(embed=embed)
  

@client.command(pass_context=True, help="mute a server member so they can't send messages")
async def mute(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    role_members = discord.utils.get(ctx.guild.roles, name='Members')
    role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role_members)
    await member.add_roles(role_muted)
    await ctx.send("User Was Muted")
    print(f'{member} was muted')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)

@client.command(name='deletechannel', help='delete a channel with the specified name')
async def deletechannel(ctx, channel_name):
   # check if the channel exists
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
   # if the channel exists
    if existing_channel is not None:
      await existing_channel.delete()
   # if the channel does not exist, inform the user
    else:
      await ctx.send(f'No channel named, "{channel_name}", was found')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def unmute(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    role_members = discord.utils.get(ctx.guild.roles, name='Members')
    role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role_muted)
    await member.add_roles(role_members)
    await ctx.send("User Was Unmuted")
    print(f'{member} was unmuted')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)

@client.command()
async def warn(ctx, member: discord.Member, *, reason):
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    with open('warnings.json', 'r') as f:
      users = json.load(f)
      await update_warning(users, str(ctx.author))
      if updatefunc == False:
        await add_warnings(users, str(ctx.author), reason)
        with open('warnings.json', 'w') as f:
          json.dump(users, f)
    await member.create_dm()
    await member.dm_channel.send(f'This is a warning for {reason} sent by {ctx.author}')
    await ctx.send("Warning sent!")
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)
		
async def add_warnings(users, auth, reason):
  users[f'{auth}']['warnings'] += 1
  reasons_list=users[f'{auth}']['reasons']
  reasons_list = reasons_list + str(reason) + ", "
  users[f'{auth}']['reasons'] = reasons_list
  if users[f'{auth}']['warnings'] == "5":
    user = await client.fetch_user(471332393870163969)
    await user.create_dm()
    await user.dm_channel.send(f'Alert! User {auth} now has 5 warnings! The reasons are {reasons_list}')

async def update_warning(users, auth):
  if not f'{auth}' in users:
        users[f'{auth}'] = {}
        users[f'{auth}']["warnings"] = 0
        users[f"{auth}"]["reasons"] = " "
        updatefunc = True

@client.command()
async def clearwarnings(ctx, member: discord.Member):
  auth = str(ctx.author)
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    with open('warnings.json', 'r') as f:
      users = json.load(f)
      await update_warning(users, str(ctx.author))
      if updatefunc == False:
        users[f'{auth}']['warnings'] = 0
        users[f'{auth}']['reasons'] = ""
        with open('warnings.json', 'w') as f:
          json.dump(users, f)
          await member.create_dm()
          await member.dm_channel.send('Your warnings have been cleared!')
          await ctx.send(f'Warnings cleared for {auth}')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)
		


@client.command()
async def checkwarnings(ctx, member: discord.Member):
    auth = str(ctx.author)
    with open('warnings.json', 'r') as f:
      users = json.load(f)
      await update_warning(users, str(ctx.author))
      if updatefunc == False:
        reasons_list=users[f'{auth}']['reasons']
        warningsnum = users[f'{auth}']['warnings']
        embed = discord.Embed(description=f'This member has {warningsnum} warnings for {reasons_list}',color = 0xf54242)
        await ctx.send(embed=embed)
      else:
        embed = discord.Embed(description=f'This member does not have any warnings yet.',color = 0xf54242)
        await ctx.send(embed=embed)

@client.command(pass_context=True)

async def ban(ctx, member: discord.Member, *,reason=None, membertoban):
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    await ban(membertoban)
    await ctx.send(f'User {membertoban} has been banned')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)
    
@client.command(pass_context=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked.')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)



#----------------------------------EVENTS----------------------------------
@client.event
async def on_member_join(member: discord.Member):
  role = discord.utils.get(member.guild.roles, name="Level 1")
  guild1 = str(message.guild.name)
  if guild1 == "Catgalactic Hangout/Support Server":
    spam_chat = client.get_channel(838864866876850228)
  elif guild1 == "sʞɹoMʎɯnᗡɓıᙠ⚠":
    spam_chat = client.get_channel(842544786506121247)
  await spam_chat.send(f'{member} welcome')
  with open('users.json', 'r') as f:
      users = json.load(f)
      await update_data(users, member)
      with open('users.json', 'w') as f:
        json.dump(users, f)
  await member.add_roles(role)

async def update_sentiment(users, auth):
  
@client.event
async def on_message(message):
  member = message.author
  auth = str(message.author)
  if auth not in memberlist:
    memberlist.append(auth)
    #db[auth] = 0
  
  mescon = str(message.content)
  mescon = mescon.lower()
  r = requests.post("https://api.deepai.org/api/sentiment-analysis",data={'text': mescon,},headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'})
  result = r.json()
  print(result)
  
  with open('sentiment.json', 'r') as f:
    users = json.load(f)
    await updata_sentiment(users, auth)
  data = [mescon]
  #result = ml.classifiers.classify(model_id, data)
  #print(result.body)
  bad_words = ["cunt", "bloody hell", "crikey", "choad", "wanker", "twat", "pussy", "nigga", "gay"]
  res = [ele for ele in bad_words if(ele in mescon)]
  result = bool(res)
  if result == True:
    await message.channel.send("You have said a swear word. It will now be deleted") 
    await message.delete()
  print(message.content)
  if message.author.bot == False:
    if isinstance(message.channel, discord.channel.DMChannel):
      return
    else:
      guild1 = str(message.guild.name)
      if guild1 == "Catgalactic Hangout/Support Server":
        with open('users.json', 'r') as f:
          users = json.load(f)
          await update_data(users, message.author)
          if updatefunc == False:
            await add_experience(users, message.author, 5)
            await level_up(users, message.author, message)
          with open('users.json', 'w') as f:
            json.dump(users, f)
      elif guild1 == "sʞɹoMʎɯnᗡɓıᙠ⚠":
        with open('users2.json', 'r') as f:
          users = json.load(f)
          await update_data(users, message.author)
          if updatefunc == False:
            await add_experience(users, message.author, 5)
            await level_up(users, message.author, message)
          with open('users2.json', 'w') as f:
            json.dump(users, f)
      elif guild1 == "M͎i͎n͎e͎c͎r͎a͎f͎t͎ H͎u͎b͎ H͎o͎t͎e͎l͎":
        with open('users3.json', 'r') as f:
          users = json.load(f)
          await update_data(users, message.author)
          if updatefunc == False:
            await add_experience(users, message.author, 5)
            await level_up(users, message.author, message)
          with open('users3.json', 'w') as f:
            json.dump(users, f)
      

  await client.process_commands(message)


@client.event
async def on_member_remove(member: discord.Member):
  print(f'{member} has left a server.')

async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1
        role = discord.utils.get(user.guild.roles, name="Level 1")
        previous = discord.utils.get(user.guild.roles, name="Level 1")
        await user.add_roles(role)
        updatefunc = True


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 5))
    guild1 = str(message.guild.name)
    if guild1 == "Catgalactic Hangout/Support Server":
      spam_chat = client.get_channel(836702503311638589)
      
    elif guild1 == "sʞɹoMʎɯnᗡɓıᙠ⚠":
      spam_chat = client.get_channel(842544786506121247)
    elif guild1 == "M͎i͎n͎e͎c͎r͎a͎f͎t͎ H͎u͎b͎ H͎o͎t͎e͎l͎":
      spam_chat = client.get_channel(834483739459059722)
    if lvl_start < lvl_end:
        await spam_chat.send(f'{user.mention} has leveled up to level {lvl_end}')
        if lvl_end == 1:
          role = discord.utils.get(user.guild.roles, name="Level 1")
          await user.add_roles(role)
        elif lvl_end == 2:
          previous = discord.utils.get(user.guild.roles, name="Level 1")
          role = discord.utils.get(user.guild.roles, name="Level 2")
          await user.remove_roles(previous)
          await user.add_roles(role)
        elif lvl_end == 3:
          previous = discord.utils.get(user.guild.roles, name="Level 2")
          await user.remove_roles(previous)
          role = discord.utils.get(user.guild.roles, name="Level 3")
          await user.add_roles(role)
        elif lvl_end == 4:
          previous = discord.utils.get(user.guild.roles, name="Level 3")
          await user.remove_roles(previous)
          role = discord.utils.get(user.guild.roles, name="Level 4")
          await user.add_roles(role)
        elif lvl_end == 5:
          previous = discord.utils.get(user.guild.roles, name="Level 4")
          await user.remove_roles(previous)
          role = discord.utils.get(user.guild.roles, name="Level 5")
          await user.add_roles(role)
        elif lvl_end == 6:
          previous = discord.utils.get(user.guild.roles, name="Level 5")
          await user.remove_roles(previous)
          role = discord.utils.get(user.guild.roles, name="Level 6")
          await user.add_roles(role)
        elif lvl_end == 7:
          previous = discord.utils.get(user.guild.roles, name="Level 6")
          await user.remove_roles(previous)
          role = discord.utils.get(user.guild.roles, name="Level 7")
          await user.add_roles(role)
        elif lvl_end == 8:
          previous = discord.utils.get(user.guild.roles, name="Level 7")
          await user.remove_roles(previous)
          role = discord.utils.get(user.guild.roles, name="Level 8")
          await user.add_roles(role)
        elif lvl_end == 9:
          previous = discord.utils.get(user.guild.roles, name="Level 8")
          await user.remove_roles(previous)
          role = discord.utils.get(user.guild.roles, name="Level 9")
          await user.add_roles(role)
        users[f'{user.id}']['level'] = lvl_end


config = os.environ['DISCORD_TOKEN']
keep_alive.keep_alive()
client.run(config)

