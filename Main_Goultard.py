import asyncio
import discord
import discord.ext.commands
from datetime import datetime, timedelta, timezone
from time import mktime
from discord.ext import commands, tasks
import os 
from array import array
from pathlib import Path
import sys

##initialise variables to avoid errors when executing others python scripts

#Event variables
global event_name_save
event_name_save = []
global event_S_date_save
event_S_date_save = []
global event_E_date_save
event_E_date_save = []
global event_backup_E_save
event_backup_E_save = []
global event_id
event_id = []
global event_update_running
event_update_running = 0

#Quest variables
global quest_name_save
quest_name_save = []
global quest_R_date_save
quest_R_date_save = []
global quest_backup_E_save
quest_backup_E_save = []
global quest_id
quest_id = []
global quest_frequence
quest_frequence = []
global quest_frequence_path
quest_frequence_path = []
global quest_update_running
quest_update_running = 0

#Server Status variables
global server_status_names_save
server_status_names_save = []
global server_R_date_save
server_R_date_save = []
global server_backup_E_save
server_backup_E_save = []
global server_id
server_id = []
global server_frequence
server_frequence = []
global server_frequence_path
server_frequence_path = []
global server_update_running
server_update_running = 0

#Get root path then check if folder exists or not. Create it if it doesn't exist
root = Path(__file__).parent
root = str(root).replace(os.path.sep, '/')
save_folder_Path = "data_saves"
isExist = os.path.exists(save_folder_Path)

if isExist == False:
    os.makedirs(save_folder_Path)

#Permet à l'exécutable de trouver l'emplacement depuis lequel il est executé
if getattr(sys, 'frozen', False):
    root = os.path.abspath(".")

#Initialize Intents
intents = discord.Intents().all()
intents.members = True

# Initialize bot and command prefix
bot = commands.Bot(command_prefix='!', intents = intents, help_command=None)

# Define channels
command_channel=1065256294673547434
event_channel=1065257019449294929
quest_channel=1067816640508604457
server_channel=1070293896787144765
role_channel=1084073482503065610

# Clear quest channel command
@bot.command()
async def clear(ctx, number:int):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=number)
        print("!clear has done its task")
    else:
        await ctx.channel.send(f'Désolé, vous devez être administrateur·trice pour utiliser cette commande.')

#Help command
@bot.command()
async def help(ctx):
    if ctx.channel.id == command_channel:
        embed = discord.Embed(title="Help", description="Voici la liste des commandes de ce bot:")
        embed.add_field(name="!event", value=f'Cette commande permet de créer votre évènement avec un nom\, une date de début et une date de fin. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant en mettant bien le nom et les dates entre **\" \"** : `!event \"Nom de l\'évènement\" \"jj-mm-aaa HH:MM\" \"jj-mm-aaa HH:MM\"`', inline=False)
        embed.add_field(name="!eventdelete", value=f'Cette commande permet de supprimer un évènement à partir de son nom. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant en mettant bien le nom entre **\" \"** : `!eventdelete \"Nom de l\'évènement\"`', inline=False)
        embed.add_field(name="!dailyquest", value=f'Cette commande permet de créer votre quête avec un nom\, et une heure indiquant quand elle doit s\'actualiser. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant en mettant bien le nom et l\'heure entre **\" \"** : `!dailyquest \"Nom de la quête\" \"HH:MM\"`', inline=False)
        embed.add_field(name="!hebdoquest", value=f'Cette commande permet de créer votre quête avec un nom\, un jour et une heure indiquant quand elle doit s\'actualiser. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant en mettant bien le nom, le jour et l\'heure entre **\" \"** : `!hebdoquest \"Nom de la quête\" \"Jour de la semaine\" \"HH:MM\"`', inline=False)
        embed.add_field(name="!questdelete", value=f'Cette commande permet de supprimer une quête à partir de son nom. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant en mettant bien le nom entre **\" \"** : `!questdelete \"Nom de la quête\"`', inline=False)
        #embed.add_field(name="!serverstatus", value=f'Cette commande permet de créer un statu de serveur avec un nom, un jour et une heure. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant en mettant bien le nom **\" \"** : `!serverstatus \"Nom du statu de serveur\" \"Jour de la semaine\" \"HH:MM\"`', inline=False)
        #embed.add_field(name="!serverdelete", value=f'Cette commande permet de supprimer un statu de serveur à partir de son nom. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant en mettant bien le nom **\" \"** : `!questdelete \"Nom du statu de serveur\"`', inline=False)
        embed.add_field(name="!alert", value=f'Cette commande permet de créer une alerte dans un salon. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant en mettant bien le nom, la description et le salon entre **\" \"** : `!alert \"Nom de l\'alerte\" \"Description de l\'alerte\" \"Salon de l\'alerte\"`', inline=False)
        embed.add_field(name="!alertcheck", value=f'Cette commande liste les alertes en cours. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant : `!alertcheck`', inline=False)        
        embed.add_field(name="!alertdelete", value=f'Cette commande permet de supprimer une alerte. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant en mettant bien le nom entre **\" \"** : `!alertdelete \"Nom de l\'alerte\" `', inline=False)                
        embed.add_field(name="!clear", value=f'Cette commande est utile si vous faites des tests. Elle vous permet d\'effacer un nombre choisi de messages. La commande doit être utilisée par un·e administrateur·trice comme dans l\'exemple suivant: `!clear nombre`', inline=False)
        embed.add_field(name="!role", value=f'Cette commande permet d\'ajouter un rôle au serveur. La commande doit être être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant: `!role "nom du rôle"`', inline=False)
        embed.add_field(name="!roledelete", value=f'Cette commande permet de supprimer un rôle du serveur. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant: `!roledelete "nom du rôle"`', inline=False)
        embed.add_field(name="!rolecheck", value=f'Cette commande permet liste les rôles du serveur. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant: `!rolecheck`', inline=False)
        embed.add_field(name="!addroles", value=f'Cette commande permet d\'ajouter un rôle à un membre du serveur. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant: `!addroles @nomdujoueur "liste du ou des rôles"`', inline=False)
        embed.add_field(name="!removeroles", value=f'Cette commande permet de retirer un rôle à un membre du serveur. La commande doit être tapée dans le salon ***{bot.get_channel(command_channel)}*** comme dans l\'exemple suivant: `!removeroles @nomdujoueur "liste du ou des rôles"`', inline=False)
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')

# quest/quest/server_statue refresh time values 
global quest_sleeptime
global quest_sleeptime_loop
global quest_hrefresh 
global quest_mrefresh
quest_sleeptime_loop = 60 # value in sec (int)
quest_mrefresh = 1# value in min (int)
quest_hrefresh = 0# value in hour (int)
if quest_hrefresh == 0:
    quest_sleeptime = (((60*quest_mrefresh)-2) - (datetime.now().second))
if quest_mrefresh == 0:
    quest_sleeptime = (((3600*quest_hrefresh)) - (datetime.now().hour))
if (quest_hrefresh > 0) and (quest_mrefresh > 0):
    quest_sleeptime = (((60*quest_mrefresh)-2) - (datetime.now().second)) + (((3600*quest_hrefresh)) - (datetime.now().hour))

server_sleeptime_loop = 60 # value in sec (int)
server_mrefresh = 1# value in min (int)
server_hrefresh = 0# value in hour (int)
if server_hrefresh == 0:
    server_sleeptime = (((60*server_mrefresh)-2) - (datetime.now().second))
if server_mrefresh == 0:
    server_sleeptime = (((3600*server_hrefresh)) - (datetime.now().hour))
if (server_hrefresh > 0) and (server_mrefresh > 0):
    server_sleeptime = (((60*server_mrefresh)-2) - (datetime.now().second)) + (((3600*server_hrefresh)) - (datetime.now().hour))


exec(open("Event_Goultard.py", encoding="utf-8").read())
exec(open("Quest_Goultard.py", encoding="utf-8").read())
exec(open("Alert_Goultard.py", encoding="utf-8").read())
exec(open("Role_Goultard.py", encoding="utf-8").read())

# Start bot
print("Bot is ready")
bot.run("MTA2NTI1NDcwNzIwMDc5NDY0NA.GSTip4.dLV_SGtiv7-wjEqb1l2fm36afZzhBgGnlWnPPM")