import asyncio
import discord
import discord.ext.commands
from datetime import datetime, timedelta, timezone
from time import mktime
from discord.ext import commands, tasks
import os 
from array import array
from pathlib import Path

#Récupère les noms et id des salons discords du serveur
global channels_names
global channels_id
channels_names = []
channels_id = []

#Initialise backup of existing events. create txt files if they don't exist
alert_bn_path = f'{root}/{save_folder_Path}/backup_alert_names.txt'
alert_bd_path = f'{root}/{save_folder_Path}/backup_alert_descriptions.txt'
alert_bc_path = f'{root}/{save_folder_Path}/backup_alert_channels.txt'
alert_bi_path = f'{root}/{save_folder_Path}/backup_alert_id.txt'

isExist = os.path.exists(alert_bn_path)
if not isExist:
    create_txt =open(alert_bn_path, "w", encoding="utf-8")
    create_txt.close()
isExist = os.path.exists(alert_bd_path)
if not isExist:
    create_txt =open(alert_bd_path, "w", encoding="utf-8")
    create_txt.close()
isExist = os.path.exists(alert_bc_path)
if not isExist:
    create_txt =open(alert_bc_path, "w", encoding="utf-8")
    create_txt.close()
isExist = os.path.exists(alert_bi_path)
if not isExist:
    create_txt =open(alert_bi_path, "w", encoding="utf-8")
    create_txt.close()


@bot.event
async def on_ready():
    #Récupère les noms et id des salons textuels du serveur
    for guild in bot.guilds:
        for channel in guild.text_channels:
            channels_names.append(channel.name)
            channels_id.append(channel.id)

    # Initialise ou charge les sauvegardes
    global alert_backup_names
    global alert_backup_descriptions
    global alert_backup_channels
    global alert_backup_id

    if os.stat(alert_bn_path).st_size == 0:
        alert_backup_names = []
    else:
        backup_string = open(alert_bn_path, 'r', encoding="utf-8")
        alert_backup_names = backup_string.read()
        alert_backup_names = alert_backup_names.split(',')
        backup_string.close()

    if os.stat(alert_bd_path).st_size == 0:
        alert_backup_descriptions = []
    else:
        backup_string = open(alert_bd_path, 'r', encoding="utf-8")
        alert_backup_descriptions = backup_string.read()
        alert_backup_descriptions = alert_backup_descriptions.split(',')
        backup_string.close()

    if os.stat(alert_bc_path).st_size == 0:
        alert_backup_channels = []
    else:
        backup_string = open(alert_bc_path, 'r', encoding="utf-8")
        alert_backup_channels = backup_string.read()
        alert_backup_channels = alert_backup_channels.split(',')
        backup_string.close()

    if os.stat(alert_bi_path).st_size == 0:
        alert_backup_id = []
    else:
        backup_string = open(alert_bi_path, 'r', encoding="utf-8")
        alert_backup_id = backup_string.read()
        alert_backup_id = alert_backup_id.split(',')
        backup_string.close()

@bot.event
async def on_message(message):
    global alert_backup_names
    global alert_backup_descriptions
    global alert_backup_channels
    global alert_backup_id

    openebn = open(alert_bn_path, "w+", encoding="utf-8")
    openebn.seek(0)
    alert_list = openebn.read()
    alert_list = alert_list.split(',')
    openebn.close()
    if alert_list != ['']:
        if message.channel.name in alert_backup_channels and message.author.bot == False:
            index = alert_backup_channels.index(message.channel.name)
            channel_index = channels_id.index(message.channel.id)
            salon = bot.get_channel(channels_id[channel_index])
            delete_message = await salon.fetch_message(alert_backup_id[index])
            await delete_message.delete()

            openebi = open(alert_bi_path, 'w+', encoding="utf-8")
            alert_backup_id = openebi.read()
            alert_backup_id = alert_backup_id.split(',')
            alert_backup_id[index] = (str((await salon.send(alert_backup_descriptions[index])).id))
            openebi.seek(0)
            openebi.truncate()
            openebi.write(','.join(alert_backup_id))
            openebi.close()

    await bot.process_commands(message)

#Crée une alerte
@bot.command()
async def alert(ctx, titre:str, description:str, salon:str):
    global alert_backup_names
    global alert_backup_descriptions
    global alert_backup_channels
    global alert_backup_id

    if ctx.channel.id == command_channel:
        if salon not in channels_names or titre in alert_backup_names:
            if salon not in channels_names:
                await ctx.channel.send(f'Aucun salon n\'existe à ce nom.')
            if titre in alert_backup_names:
                await ctx.channel.send(f'Une alerte existe déjà à ce nom.')
        else:
            iterateur = channels_names.index(salon)
            salon = bot.get_channel(channels_id[iterateur])

            #update txt files to save actual events datas
            alert_backup_names.append(titre)
            alert_backup_descriptions.append(description)
            alert_backup_channels.append(str(salon))
            alert_backup_id.append(str((await salon.send(description)).id))

            openebn = open(alert_bn_path, "w+", encoding="utf-8")
            openebn.seek(0)
            openebn.truncate()
            openebn.write(','.join(alert_backup_names))
            openebn.close()

            openebd = open(alert_bd_path, "w+", encoding="utf-8")
            openebd.seek(0)
            openebd.truncate()
            openebd.write(','.join(alert_backup_descriptions))
            openebd.close()

            openebc = open(alert_bc_path, "w+", encoding="utf-8")
            openebc.seek(0)
            openebc.truncate()
            openebc.write(','.join(alert_backup_channels))
            openebc.close()

            openebi = open(alert_bi_path, "w+", encoding="utf-8")
            openebi.seek(0)
            openebi.truncate()
            openebi.write(','.join(alert_backup_id))
            openebi.close()
        await ctx.channel.send(f'Votre alerte {titre} à bien été créé dans le salon {salon}')

    else:
        await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')

#Donne les informations liées aux alertes potentiellement en cours
@bot.command()
async def alertcheck(ctx):
    global alert_backup_names
    global alert_backup_descriptions
    global alert_backup_channels
    global alert_backup_id

    if ctx.channel.id == command_channel:
        if range(len(alert_backup_names)) == range(0, 0):
            alert_list = discord.Embed(title="Alertes", description="Il n'y a aucune alerte en cours.")
        else:
            alert_list = discord.Embed(title="Alertes", description="Liste des alertes en cours :")
            for i in range(len(alert_backup_names)):
                alert_list.add_field(name= alert_backup_names[i], value= f'Salon : {alert_backup_channels[i]} ; Description : {alert_backup_descriptions[i]}', inline=False) 
        await ctx.channel.send(embed=alert_list)
    else:
        await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')

#Supprime une alerte
@bot.command()
async def alertdelete(ctx, name:str):
    global alert_backup_names
    global alert_backup_descriptions
    global alert_backup_channels
    global alert_backup_id

    if ctx.channel.id == command_channel:
        if name not in alert_backup_names:
            await ctx.channel.send(f'Aucune alerte n\'existe à ce nom.')
        else:
            index = alert_backup_names.index(name)
            channel_index = channels_names.index(alert_backup_channels[index])
            salon = bot.get_channel(channels_id[channel_index])
            delete_message = await salon.fetch_message(alert_backup_id[index])
            await delete_message.delete()

            openbn = open(alert_bn_path, "r+", encoding="utf-8")
            alert_backup_names = openbn.read()
            alert_backup_names = alert_backup_names.split(',')
            del alert_backup_names[index]
            openbn.seek(0)
            openbn.truncate()
            openbn.write(','.join(alert_backup_names))
            openbn.close()

            openbd = open(alert_bd_path, "r+", encoding="utf-8")
            alert_backup_descriptions = openbd.read()
            alert_backup_descriptions = alert_backup_descriptions.split(',')
            del alert_backup_descriptions[index]
            openbd.seek(0)
            openbd.truncate()
            openbd.write(','.join(alert_backup_descriptions))
            openbd.close()

            openbc = open(alert_bc_path, "r+", encoding="utf-8")
            alert_backup_channels = openbc.read()
            alert_backup_channels = alert_backup_channels.split(',')
            del alert_backup_channels[index]
            openbc.seek(0)
            openbc.truncate()
            openbc.write(','.join(alert_backup_channels))
            openbc.close()

            openbi = open(alert_bi_path, "r+", encoding="utf-8")
            alert_backup_id = openbi.read()
            alert_backup_id = alert_backup_id.split(',')
            del alert_backup_id[index]
            openbi.seek(0)
            openbi.truncate()
            openbi.write(','.join(alert_backup_id))
            openbi.close()

            await ctx.channel.send(f'L\'alerte {name} a bien été supprimée.')

    else:
        await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')


