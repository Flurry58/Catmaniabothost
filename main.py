import discord
from discord.ext import commands
from discord.utils import get
from replit import db
import mysql.connector
import os

mydb = mysql.connector.connect(
  host="sql103.epizy.com ",
  user="epiz_28407868",
  password="5P8RMUURN3Ps",
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE level_database")


client = commands.Bot(command_prefix='&')


@client.event
async def on_ready():
    print("Bot is on")

@client.command()
async def enable_leveling(ctx):
  sender_id = str(ctx.author)
  mydb[sender_id] = 0
  await ctx.send("You are now in the leveling database.")
  

@client.command()
async def testlevelsystem(ctx):
  role = discord.utils.get(ctx.guild.roles, name='Bot Developer')
  if role in ctx.author.roles:
    pass
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def afk_on(ctx):

  member = ctx.author
  role_members = discord.utils.get(ctx.guild.roles, name='Members')
  role_muted = discord.utils.get(ctx.guild.roles, name='AFK')
  await member.remove_roles(role_members)
  await member.add_roles(role_muted)
  await ctx.send("You are now labeled as AFK. To disable it type afk_off")
  

@client.command(pass_context=True)
async def afk_off(ctx):
  member = ctx.author
  role_members = discord.utils.get(ctx.guild.roles, name='Members')
  role_muted = discord.utils.get(ctx.guild.roles, name='AFK')
  await member.remove_roles(role_muted)
  await member.add_roles(role_members)
  await ctx.send("You are not afk anymore!")
  

@client.command(pass_context=True)
async def mute(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name='Admin')
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

@client.command(pass_context=True)
async def unmute(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name='Admin')
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

@client.command(pass_context=True)
async def warn(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name='Admin')
  if role in ctx.author.roles:
    await member.send("You are doing somethng you are not supposed to do. This is a warning to stop")
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  role = discord.utils.get(ctx.guild.roles, name='Admin')
  if role in ctx.author.roles:
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked.')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)



@client.event
async def on_member_join(member: discord.Member):
  mydb[member] = "";
  print(f'{member} has joined a server.')
  await ctx.send(f'Welcome to the server {member}')
    


@client.event
async def on_member_remove(member: discord.Member):
  print(f'{member} has left a server.')


config = os.environ['TOKEN']
client.run(config)

