import asyncio
import discord
import discord.ext.commands
from datetime import datetime, timedelta, timezone
from time import mktime
from discord.ext import commands, tasks
import os 
from array import array
from pathlib import Path

# event/event/server_statue refresh time values
global event_sleeptime
global event_hrefresh 
global event_mrefresh
global event_loop_sleeptime
event_hrefresh = 1 # value in hour (int)
event_mrefresh = 0 # value in min (int)
event_loop_sleeptime = (event_hrefresh*3600) + (event_mrefresh*60)

if event_hrefresh == 0:
    event_sleeptime = (((60*event_mrefresh)-1) - (datetime.now().second))
if event_mrefresh == 0:
    event_sleeptime = (((3600*event_hrefresh)-60) - (datetime.now().hour))
if (event_hrefresh > 0) and (event_mrefresh > 0):
    event_sleeptime = (((60*event_mrefresh)-1) - (datetime.now().second)) + (((3600*event_hrefresh)-60) - (datetime.now().hour))

#Initialise backup of existing events. create txt files if they don't exist
global event_backup_names
global event_backup_sdates
global event_backup_embed
global backup_string
global event_context_path

event_bn_path = f'{root}/{save_folder_Path}/backup_events_names.txt'
event_sbd_path = f'{root}/{save_folder_Path}/backup_events_sdates.txt'
event_ebd_path = f'{root}/{save_folder_Path}/backup_events_edates.txt'
event_ebe_path = f'{root}/{save_folder_Path}/backup_event_embed.txt'
event_id_path = f'{root}/{save_folder_Path}/backup_events_id.txt'
event_context_path = f'{root}/{save_folder_Path}/backup_event_context.txt'

isExist = os.path.exists(event_bn_path)
if not isExist:
    create_txt =open(event_bn_path, "w", encoding="utf-8")
    create_txt.close()
isExist = os.path.exists(event_sbd_path)
if not isExist:
    create_txt =open(event_sbd_path, "w", encoding="utf-8")
    create_txt.close()
isExist = os.path.exists(event_ebd_path)
if not isExist:
    create_txt =open(event_ebd_path, "w", encoding="utf-8")
    create_txt.close()
isExist = os.path.exists(event_ebe_path)
if not isExist:
    create_txt =open(event_ebe_path, "w", encoding="utf-8")
    create_txt.close()
isExist = os.path.exists(event_id_path)
if not isExist:
    create_txt =open(event_id_path, "w", encoding="utf-8")
    create_txt.close()
isExist = os.path.exists(event_context_path)
if not isExist:
    create_txt =open(event_context_path, "w", encoding="utf-8")
    create_txt.close()

#Initialise date formats
long_date = "<t:D>" #<t: epoch :D>
relative_time = "<t:R>" #<t: epoch :R>
short_time = "<t:t>" #<t: epoch :t>

#initialise images
global event_image_url
event_image_url = "https://cdn.discordapp.com/attachments/553335312047144992/1066350484039925810/1273135.png"

# Initialise modifying and ID variable
global modifying
global ID
modifying = 0
ID = "ID"

# Set timezone
pacific = timezone(timedelta(hours=-8))
central_europe = timezone(timedelta(hours=1))
asia = timezone(timedelta(hours=8))

#Global context
global Context

#Check if the bot is ready to work
@bot.event
async def on_ready():
    global bot_start
    global event_update_running
    event_update_running = 0
    bot_start = 0
    if os.stat(event_context_path).st_size != 0:
        event_update_running = 1
        await asyncio.sleep(quest_sleeptime)
        event_message_update.start(command_channel)
    else:
        bot_start = 1

    #Initialise Event names and dates variables
    global tmp_save
    tmp_save = ""
    global event_name_save
    global event_S_date_save
    global event_E_date_save
    global event_backup_E_save
    global event_id

    if os.stat(event_bn_path).st_size == 0:
        event_name_save = []
    else:
        backup_string = open(event_bn_path, 'r', encoding="utf-8")
        event_name_save = backup_string.read()
        event_name_save = event_name_save.split(',')
        backup_string.close()

    if os.stat(event_sbd_path).st_size == 0:
        event_S_date_save = []
    else:
        backup_string = open(event_sbd_path, 'r', encoding="utf-8")
        event_S_date_save = backup_string.read()
        event_S_date_save = event_S_date_save.split(',')
        backup_string.close()

    if os.stat(event_ebd_path).st_size == 0:
        event_E_date_save = []
    else:
        backup_string = open(event_ebd_path, 'r', encoding="utf-8")
        event_E_date_save = backup_string.read()
        event_E_date_save = event_E_date_save.split(',')
        backup_string.close()

    if os.stat(event_ebe_path).st_size == 0:
        event_backup_E_save = []
    else:
        backup_string = open(event_ebe_path, 'r', encoding="utf-8")
        event_backup_E_save = backup_string.read()
        event_backup_E_save = event_backup_E_save.split(',')
        backup_string.close()

    if os.stat(event_id_path).st_size == 0:
        event_id = []
    else:
        backup_string = open(event_id_path, 'r', encoding="utf-8")
        event_id = backup_string.read()
        event_id = event_id.split(',')
        backup_string.close()
        
    print('The bot is ready!')

# Starting event date setting command
@bot.event
async def start_date(date:str):
    global tmp_save
    tmp_save = datetime.strptime(date, '%d-%m-%Y %H:%M').timetuple()
    tmp_save = int(mktime(tmp_save))
    
#Make the message with timezones epoch dates
@bot.event
async def timezones(embed:discord.Embed ,date:str):
    global tmp_save
    separator = long_date.find(":")
    #NA timezone
    await start_date(date.astimezone(pacific).strftime('%d-%m-%Y %H:%M'))
    tmp_save = f'{long_date[:(separator+1)]}{tmp_save}{long_date[(separator):]}'
    embed.add_field(name= ":earth_americas:・NA", value= tmp_save + "\n" + " ", inline=False)

    #CE timezone
    await start_date(date.astimezone(central_europe).strftime('%d-%m-%Y %H:%M'))
    tmp_save = f'{long_date[:(separator+1)]}{tmp_save}{long_date[(separator):]}'
    embed.add_field(name=":earth_africa:・EU", value= tmp_save + "\n" + " ", inline=False)
                
    #A timezone
    await start_date(date.astimezone(asia).strftime('%d-%m-%Y %H:%M'))
    tmp_save = f'{long_date[:(separator+1)]}{tmp_save}{long_date[(separator):]}'
    embed.add_field(name=":earth_asia:・ASIA", value= tmp_save + "\n" + " ", inline=False)

# Event command
@bot.event
async def make_event(ctx, Event_name:str, S_date:str, E_date:str, modifying:int, ID = ID):
    global event_sleeptime
    global event_name_save
    global event_S_date_save
    global event_E_date_save
    global event_backup_E_save
    global event_id
    global tmp_save
    global bot_start
    global event_update_running

    if modifying == 1:
        if event_name_save == []:
            event_name_save.append(Event_name)
            event_S_date_save.append(S_date)
            event_E_date_save.append(E_date)
            event_backup_E_save.append(Event_name)

    if modifying == 0:
        bot_start = 1

        #check if an event already exist with the same name
        if ctx.channel.id != command_channel:
                await ctx.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')
                return
        else:
            if (Event_name) in event_name_save and modifying == 0:
                await ctx.send(f'Un évènement à ce nom existe déjà, veuillez choisir un autre nom')
                return
            else:
                #save Event_name and date to be able to save them later in a txt file
                event_name_save.append(Event_name)
                event_S_date_save.append(S_date)
                event_E_date_save.append(E_date)
                event_backup_E_save.append(Event_name)

    #calculate time_until_event
    is_positive_time_until_event = datetime.strptime(S_date, '%d-%m-%Y %H:%M') - datetime.now()
    Title = Event_name
    if is_positive_time_until_event.total_seconds() > 0:
        time_until_event = datetime.strptime(S_date, '%d-%m-%Y %H:%M') - datetime.now()
        S_date = datetime.strptime(S_date, '%d-%m-%Y %H:%M')
        Event_name = discord.Embed(title=Title, description="L'évènement aura lieu le :")
        await timezones(Event_name, S_date)
        separator = relative_time.find(":")
        await start_date(S_date.astimezone(central_europe).strftime('%d-%m-%Y %H:%M'))
        Event_name.add_field(name= "Temps restant:", value= f'{relative_time[:(separator+1)]}{tmp_save}{relative_time[(separator):]}', inline=False)   

    else:
        time_until_event = datetime.strptime(E_date, '%d-%m-%Y %H:%M') - datetime.now()
        E_date = datetime.strptime(E_date, '%d-%m-%Y %H:%M')
        Event_name = discord.Embed(title=Title, description="L'évènement se termine le :")
        await timezones(Event_name, E_date)
        separator = relative_time.find(":")
        await start_date(E_date.astimezone(central_europe).strftime('%d-%m-%Y %H:%M'))
        Event_name.add_field(name= "Fin de l'évènement:", value= f'{relative_time[:(separator+1)]}{tmp_save}{relative_time[(separator):]}', inline=False)   

    #Event Image
    Event_name.set_image(url= event_image_url)

    if bot_start !=0:
        if modifying == 0:
            channel = bot.get_channel(event_channel)
            if ctx.channel.id == command_channel:

                event_id.append(str((await channel.send(embed=Event_name)).id))
                await ctx.channel.send(f'Votre évènement {Title} à bien été créé dans le salon {bot.get_channel(event_channel)}')
                
                #update txt files to save actual events datas
                openebn = open(event_bn_path, "w+", encoding="utf-8")
                openebn.seek(0)
                openebn.truncate()
                openebn.write(','.join(event_name_save))
                openebn.close()

                openesbd = open(event_sbd_path, "w+", encoding="utf-8")
                openesbd.seek(0)
                openesbd.truncate()
                openesbd.write(','.join(event_S_date_save))
                openesbd.close()

                openeebd = open(event_ebd_path, "w+", encoding="utf-8")
                openeebd.seek(0)
                openeebd.truncate()
                openeebd.write(','.join(event_E_date_save))
                openeebd.close()

                openeebe = open(event_ebe_path, "w+", encoding="utf-8")
                openeebe.seek(0)
                openeebe.truncate()
                openeebe.write(','.join(event_backup_E_save))
                openeebe.close()

                openeeid = open(event_id_path, "w+", encoding="utf-8")
                openeeid.seek(0)
                openeeid.truncate()
                openeeid.write(','.join(event_id))
                openeeid.close()

                if os.stat(event_context_path).st_size == 0:
                    openec = open(event_context_path, "w+", encoding="utf-8")
                    openec.seek(0)
                    openec.truncate()
                    openec.write(str(ctx))
                    openec.close()

                if event_update_running == 0:
                    if quest_hrefresh == 0:
                        quest_sleeptime = (((60*quest_mrefresh)+0) - (datetime.now().second))
                    if quest_mrefresh == 0:
                        quest_sleeptime = (((3600*quest_hrefresh)) - (datetime.now().hour))
                    if (quest_hrefresh > 0) and (quest_mrefresh > 0):
                        quest_sleeptime = (((60*quest_mrefresh)) - (datetime.now().second)) + (((3600*quest_hrefresh)) - (datetime.now().hour))
                    await asyncio.sleep(quest_sleeptime)
                    event_message_update.start(ctx)
                    event_update_running = 1
            else:
                await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')
                
        else:
            channel = bot.get_channel(event_channel)
            message = await channel.fetch_message(ID)
            await message.edit(embed = Event_name)
            
    else:
        channel = bot.get_channel(event_channel)
        message = await channel.fetch_message(ID)
        await message.edit(embed = Event_name)

#modify existing event messages
@bot.event
async def modify_event(ctx):
    global event_ebe_path
    global event_bn_path
    global event_sbd_path
    global event_ebd_path
    global modifying
    global event_sdates
    global event_edates
    global event_embed_names
    global event_embed_id
    modifying = 1

    if os.stat(event_ebd_path).st_size != 0:
        openesbd = open(event_sbd_path, "r", encoding="utf-8")
        event_sdates = openesbd.read()
        openesbd.close()
        event_sdates = event_sdates.split(',')

        openeebd = open(event_ebd_path, "r", encoding="utf-8")
        event_edates = openeebd.read()
        openeebd.close()
        event_edates = event_edates.split(',')

        openeebe = open(event_ebe_path, "r", encoding="utf-8")
        event_embed_names = openeebe.read()
        openeebe.close()
        event_embed_names = event_embed_names.split(',')

        openeeid = open(event_id_path, "r", encoding="utf-8")
        event_embed_id = openeeid.read()
        openeeid.close()
        event_embed_id = event_embed_id.split(',')

        for i in range(len(event_embed_names)):
            await make_event(ctx, event_embed_names[i], event_sdates[i], event_edates[i], modifying, event_embed_id[i])

# Event delete
@bot.event
async def delete_event(for_length:int, for_event_edates):
    print("delete_event est appelé")
    global event_ebe_path
    global event_bn_path
    global event_sbd_path
    global event_ebd_path
    global event_sdates
    global event_edates
    global event_embed_names
    global event_embed_id
    global event_name_save
    global event_S_date_save
    global event_E_date_save
    global event_backup_E_save
    global event_id
    length = for_length
    event_edates = for_event_edates

    i_count =[]
    openeeid = open(event_id_path, "r+", encoding="utf-8")
    event_embed_id = openeeid.read()
    event_embed_id = event_embed_id.split(',')
    openeeid.close()
    
    for i in range(length):
        date = event_edates[i]
        date = datetime.strptime(date, '%d-%m-%Y %H:%M')

        if (date - datetime.now()).total_seconds() <= 0:
             #delete message
            channel = bot.get_channel(event_channel)
            delete_message = await channel.fetch_message(event_embed_id[i])
            await delete_message.delete()
            i_count.append(i)

    for i in range(len(i_count)):
        openesbd = open(event_sbd_path, "r+", encoding="utf-8")
        event_sdates = openesbd.read()
        event_sdates = event_sdates.split(',')
        del event_sdates[i_count[i]]
        if length == 1:
            event_sdates = []
        openesbd.seek(0)
        openesbd.truncate()
        openesbd.write(','.join(event_sdates))
        openesbd.close()

        openeebn = open(event_bn_path, "r+", encoding="utf-8")
        event_name_save = openeebn.read()
        event_name_save = event_name_save.split(',')
        del event_name_save[i_count[i]]
        if length == 1:
            event_name_save = []
        openeebn.seek(0)
        openeebn.truncate()
        openeebn.write(','.join(event_name_save))
        openeebn.close()

        openeebe = open(event_ebe_path, "r+", encoding="utf-8")
        event_embed_names = openeebe.read()
        event_embed_names = event_embed_names.split(',')
        del event_embed_names[i_count[i]]
        if length == 1:
            event_embed_names = []
        openeebe.seek(0)
        openeebe.truncate()
        openeebe.write(','.join(event_embed_names))
        openeebe.close()

        openeebd = open(event_ebd_path, "r+", encoding="utf-8")
        del event_edates[i_count[i]]
        if length == 1:
            event_edates = []
        openeebd.seek(0)
        openeebd.truncate()
        openeebd.write(','.join(event_edates))
        openeebd.close()

        openeeid = open(event_id_path, "r+", encoding="utf-8")
        del event_embed_id[i_count[i]]
        if length == 1:
            event_embed_id = []
        openeeid.seek(0)
        openeeid.truncate()
        openeeid.write(','.join(event_embed_id))
        openeeid.close()

        event_S_date_save = event_sdates
        event_E_date_save = event_edates
        event_backup_E_save = event_embed_names
        event_id = event_embed_id

@bot.command()
async def eventdelete(ctx, name:str):

        global event_ebe_path
        global event_bn_path
        global event_sbd_path
        global event_ebd_path
        global event_sdates
        global event_edates
        global event_embed_names
        global event_embed_id
        global event_name_save
        global event_S_date_save
        global event_E_date_save
        global event_backup_E_save
        global event_id

        if ctx.channel.id == command_channel:
            #search for name in embed names
            openeebe = open(event_ebe_path, "r+", encoding="utf-8")
            event_embed_names = openeebe.read()
            event_embed_names = event_embed_names.split(',')
            if name in event_embed_names:
                channel = bot.get_channel(event_channel)
                i = event_embed_names.index(name)
                delete_message = await channel.fetch_message(event_embed_id[i])
                await delete_message.delete()
                openeebe.close()

                openesbd = open(event_sbd_path, "r+", encoding="utf-8")
                event_sdates = openesbd.read()
                event_sdates = event_sdates.split(',')
                del event_sdates[i]
                openesbd.seek(0)
                openesbd.truncate()
                openesbd.write(','.join(event_sdates))
                openesbd.close()

                openeebn = open(event_bn_path, "r+", encoding="utf-8")
                event_name_save = openeebn.read()
                event_name_save = event_name_save.split(',')
                del event_name_save[i]
                openeebn.seek(0)
                openeebn.truncate()
                openeebn.write(','.join(event_name_save))
                openeebn.close()

                openeebe = open(event_ebe_path, "r+", encoding="utf-8")
                event_embed_names = openeebe.read()
                event_embed_names = event_embed_names.split(',')
                del event_embed_names[i]
                openeebe.seek(0)
                openeebe.truncate()
                openeebe.write(','.join(event_embed_names))
                openeebe.close()

                openeebd = open(event_ebd_path, "r+", encoding="utf-8")
                del event_edates[i]
                openeebd.seek(0)
                openeebd.truncate()
                openeebd.write(','.join(event_edates))
                openeebd.close()

                openeeid = open(event_id_path, "r+", encoding="utf-8")
                del event_embed_id[i]
                openeeid.seek(0)
                openeeid.truncate()
                openeeid.write(','.join(event_embed_id))
                openeeid.close()

                event_S_date_save = event_sdates
                event_E_date_save = event_edates
                event_backup_E_save = event_embed_names
                event_id = event_embed_id

                await ctx.channel.send(f'L\'évènement {name} a bien été supprimé.')
            else:
                await ctx.channel.send(f'Aucun évènement n\'existe à ce nom.')
        else:
            await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')

#Beggins event creation
@bot.command()
async def event(ctx, Event_name:str, S_date:str, E_date:str):
    global modifying
    modifying = 0
    await make_event(ctx, Event_name, S_date, E_date, modifying)

@tasks.loop(seconds = quest_sleeptime_loop)
async def event_message_update(ctx):
    # update existing event messages
    global event_sleeptime
    global event_hrefresh 
    global event_mrefresh
    print("Starting event update")
    await modify_event(ctx)

    # Delete ended event messages
    global event_ebe_path
    global event_bn_path
    global event_sbd_path
    global event_ebd_path
    if os.stat(event_ebd_path).st_size != 0:
        openeebd = open(event_ebd_path, "r+", encoding="utf-8")
        event_edates = openeebd.read()
        event_edates = event_edates.split(',')
        openeebd.close()
        length = len(event_edates)
        await delete_event(length, event_edates)
