import asyncio
import discord
import discord.ext.commands
from datetime import datetime, timedelta, timezone
from time import mktime
from discord.ext import commands, tasks
import os 
from array import array
from pathlib import Path

#Initialise backup of existing server. create txt files if they don't exist
global server_backup_names
global server_backup_rdates
global server_backup_embed
global server_description
global backup_string
global server_context_path
global server_description_path

server_bn_path = f'{root}/{save_folder_Path}/backup_server_status_names.txt'
server_rbd_path = f'{root}/{save_folder_Path}/backup_server_rdates.txt'
server_ebe_path = f'{root}/{save_folder_Path}/backup_server_embed.txt'
server_id_path = f'{root}/{save_folder_Path}/backup_server_id.txt'
server_context_path = f'{root}/{save_folder_Path}/backup_server_context.txt'
server_description_path = f'{root}/{save_folder_Path}/backup_server_description.txt'

isExist = os.path.exists(server_bn_path)
if not isExist:
    create_txt =open(server_bn_path, "w")
    create_txt.close()
isExist = os.path.exists(server_rbd_path)
if not isExist:
    create_txt =open(server_rbd_path, "w")
    create_txt.close()
isExist = os.path.exists(server_ebe_path)
if not isExist:
    create_txt =open(server_ebe_path, "w")
    create_txt.close()
isExist = os.path.exists(server_id_path)
if not isExist:
    create_txt =open(server_id_path, "w")
    create_txt.close()
isExist = os.path.exists(server_context_path)
if not isExist:
    create_txt =open(server_context_path, "w")
    create_txt.close()

isExist = os.path.exists(server_description_path)
if not isExist:
    create_txt =open(server_description_path, "w")
    create_txt.close()

#Initialise date formats
long_date = "<t:D>" #<t: epoch :D>
relative_time = "<t:R>" #<t: epoch :R>
short_time = "<t:t>" #<t: epoch :t>

#initialise images
global server_image_url
server_image_url = "https://cdn.discordapp.com/attachments/553335312047144992/1070375467376447498/Serveur_Waven.jpg"

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
    global server_update_running
    server_update_running = 0
    bot_start = 0
    if os.stat(server_context_path).st_size != 0:
        server_update_running = 1
        await asyncio.sleep(server_sleeptime)
        server_message_update.start(command_channel)
    else:
        bot_start = 1

    #Initialise server names and dates variables
    global tmp_save
    tmp_save = ""
    global server_status_names_save
    global server_R_date_save
    global server_backup_E_save
    global server_id
    global server_description
    global server_description_path

    if os.stat(server_bn_path).st_size == 0:
        server_status_names_save = []
    else:
        backup_string = open(server_bn_path, 'r')
        server_status_names_save = backup_string.read()
        server_status_names_save = server_status_names_save.split(',')
        backup_string.close()

    if os.stat(server_rbd_path).st_size == 0:
        server_R_date_save = []
    else:
        backup_string = open(server_rbd_path, 'r')
        server_R_date_save = backup_string.read()
        server_R_date_save = server_R_date_save.split(',')
        backup_string.close()

    if os.stat(server_ebe_path).st_size == 0:
        server_backup_E_save = []
    else:
        backup_string = open(server_ebe_path, 'r')
        server_backup_E_save = backup_string.read()
        server_backup_E_save = server_backup_E_save.split(',')
        backup_string.close()

    if os.stat(server_id_path).st_size == 0:
        server_id = []
    else:
        backup_string = open(server_id_path, 'r')
        server_id = backup_string.read()
        server_id = server_id.split(',')
        backup_string.close()

    if os.stat(server_description_path).st_size == 0:
        server_description = []
    else:
        backup_string = open(server_description_path, 'r')
        server_description = backup_string.read()
        server_description = server_description.split(',')
        backup_string.close()

# Starting server date setting command
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

# server command
@bot.event
async def make_server(ctx, server_status_names:str, description:str, R_date:str, modifying:int, ID = ID):
    global server_sleeptime
    global server_status_names_save
    global server_R_date_save
    global server_backup_E_save
    global server_id
    global server_description
    global server_description_path
    global tmp_save
    global bot_start
    global server_update_running
    global server_description
    if modifying == 1:
        if server_status_names_save == []:
            server_status_names_save.append(server_status_names)
            server_R_date_save.append(R_date)
            server_backup_E_save.append(server_status_names)
            server_description.append(description)

    if modifying == 0:
        bot_start = 1
        #check if an server already exist with the same name
        if ctx.channel.id != command_channel:
                await ctx.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')
                return
        else:
            backup_string = open(server_bn_path, 'r')
            ifserver_status_names_save = backup_string.read()
            ifserver_status_names_save = ifserver_status_names_save.split(',')
            backup_string.close()
            if (server_status_names) in ifserver_status_names_save and modifying == 0:
                await ctx.send(f'Un statu de serveur existe déjà à ce nom, veuillez choisir un autre nom')
                return
            else:
                #save server_status_names and date to be able to save them later in a txt file
                server_status_names_save.append(server_status_names)
                server_R_date_save.append(R_date)
                server_backup_E_save.append(server_status_names)
                server_description.append(description)

    #calculate server date reset
    Title = server_status_names
    R_date = datetime.strptime(R_date, '%d-%m-%Y %H:%M')
    server_status_names = discord.Embed(title=Title, description = description)
    await timezones(server_status_names, R_date)
    separator = relative_time.find(":")

    daily_reset = R_date.strftime('%H:%M')
    daily_reset = datetime.strptime(daily_reset, '%H:%M')

    if ((((daily_reset.hour - datetime.now().hour) * 60) + (daily_reset.minute - datetime.now().minute))) > 0:
        daily_reset = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year} {daily_reset.hour}:{daily_reset.minute}'
    else:
        daily_reset = f'{datetime.now().day + 1}-{datetime.now().month}-{datetime.now().year} {daily_reset.hour}:{daily_reset.minute}'
    daily_reset = datetime.strptime(daily_reset, '%d-%m-%Y %H:%M')
    await start_date(daily_reset.astimezone(central_europe).strftime('%d-%m-%Y %H:%M'))
    server_status_names.add_field(name= "Temps restant avant le reboot du serveur :", value= f'{relative_time[:(separator+1)]}{tmp_save}{relative_time[(separator):]}', inline=False)   

    #server Image
    server_status_names.set_image(url= server_image_url)
    
    if bot_start !=0:
        if modifying == 0:
            channel = bot.get_channel(server_channel)
            if ctx.channel.id == command_channel:

                server_id.append(str((await channel.send(embed=server_status_names)).id))
                await ctx.channel.send(f'Votre quête {Title} à bien été créé dans le salon {bot.get_channel(server_channel)}')
                
                #update txt files to save actual server datas
                openqbn = open(server_bn_path, "w+")
                openqbn.seek(0)
                openqbn.truncate()
                openqbn.write(','.join(server_status_names_save))
                openqbn.close()

                openqrbd = open(server_rbd_path, "w+")
                openqrbd.seek(0)
                openqrbd.truncate()
                openqrbd.write(','.join(server_R_date_save))
                openqrbd.close()

                openqebe = open(server_ebe_path, "w+")
                openqebe.seek(0)
                openqebe.truncate()
                openqebe.write(','.join(server_backup_E_save))
                openqebe.close()

                openqeid = open(server_id_path, "w+")
                openqeid.seek(0)
                openqeid.truncate()
                openqeid.write(','.join(server_id))
                openqeid.close()

                openqefd = open(server_description_path, "w+")
                openqefd.seek(0)
                openqefd.truncate()
                openqefd.write(','.join(server_description))
                openqefd.close()

                if os.stat(server_context_path).st_size == 0:
                    openqc = open(server_context_path, "w+")
                    openqc.seek(0)
                    openqc.truncate()
                    openqc.write(str(ctx))
                    openqc.close()

                if server_update_running == 0:
                    if server_hrefresh == 0:
                        server_sleeptime = (((60*server_mrefresh)+0) - (datetime.now().second))
                    if server_mrefresh == 0:
                        server_sleeptime = (((3600*server_hrefresh)) - (datetime.now().hour))
                    if (server_hrefresh > 0) and (server_mrefresh > 0):
                        server_sleeptime = (((60*server_mrefresh)) - (datetime.now().second)) + (((3600*server_hrefresh)) - (datetime.now().hour))
                    await asyncio.sleep(server_sleeptime)
                    server_message_update.start(ctx)
                    server_update_running = 1
            else:
                await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')
                
        else:
            channel = bot.get_channel(server_channel)
            message = await channel.fetch_message(ID)
            await message.edit(embed = server_status_names)
            
    else:
        channel = bot.get_channel(server_channel)
        message = await channel.fetch_message(ID)
        await message.edit(embed = server_status_names)

#modify existing server messages
@bot.event
async def modify_server(ctx):
    global server_ebe_path
    global server_bn_path
    global server_rbd_path
    global modifying
    global server_rdates
    global server_description
    global server_description_path
    global server_embed_names
    global server_embed_id
    modifying = 1

    if os.stat(server_rbd_path).st_size != 0:
        openqrbd = open(server_rbd_path, "r")
        server_rdates = openqrbd.read()
        openqrbd.close()
        server_rdates = server_rdates.split(',')

        openqebe = open(server_ebe_path, "r")
        server_embed_names = openqebe.read()
        openqebe.close()
        server_embed_names = server_embed_names.split(',')

        openqeid = open(server_id_path, "r")
        server_embed_id = openqeid.read()
        openqeid.close()
        server_embed_id = server_embed_id.split(',')

        openqf = open(server_description_path, "r")
        server_description = openqf.read()
        openqf.close()
        server_description = server_description.split(',')

        for i in range(len(server_embed_names)):
            await make_server(ctx, server_embed_names[i], server_rdates[i], server_description[i], modifying, server_embed_id[i])

# server delete
@bot.event
async def delete_server(for_length:int, for_server_edates):
    print("delete_server est appelé")
    global server_R_date_save
    global server_status_names_save
    global server_backup_E_save
    global server_description
    global server_ebe_path
    global server_bn_path
    global server_rbd_path
    global server_rdates
    global server_description
    global server_description_path
    global server_embed_names
    global server_embed_id
    length = for_length
    server_edates = for_server_edates

    i_count =[]
    openeeid = open(server_id_path, "r+")
    server_embed_id = openeeid.read()
    server_embed_id = server_embed_id.split(',')
    openeeid.close()
    
    for i in range(length):
        date = server_edates[i]
        date = datetime.strptime(date, '%d-%m-%Y %H:%M')

        if (date - datetime.now()).total_seconds() <= 0:
             #delete message
            channel = bot.get_channel(server_channel)
            delete_message = await channel.fetch_message(server_embed_id[i])
            await delete_message.delete()
            i_count.append(i)

    for i in range(len(i_count)):
        openesbd = open(server_rbd_path, "r+")
        server_rdates = openesbd.read()
        server_rdates = server_rdates.split(',')
        del server_rdates[i_count[i]]
        if length == 1:
            server_rdates = []
        openesbd.seek(0)
        openesbd.truncate()
        openesbd.write(','.join(server_rdates))
        openesbd.close()

        openeebn = open(server_bn_path, "r+")
        server_name_save = openeebn.read()
        server_name_save = server_name_save.split(',')
        del server_name_save[i_count[i]]
        if length == 1:
            server_name_save = []
        openeebn.seek(0)
        openeebn.truncate()
        openeebn.write(','.join(server_name_save))
        openeebn.close()

        openeebe = open(server_ebe_path, "r+")
        server_embed_names = openeebe.read()
        server_embed_names = server_embed_names.split(',')
        del server_embed_names[i_count[i]]
        if length == 1:
            server_embed_names = []
        openeebe.seek(0)
        openeebe.truncate()
        openeebe.write(','.join(server_embed_names))
        openeebe.close()

        openbd = open(server_description_path, "r+")
        del server_description[i_count[i]]
        if length == 1:
            server_description = []
        openbd.seek(0)
        openbd.truncate()
        openbd.write(','.join(server_description))
        openbd.close()

        server_R_date_save = server_rdates
        server_status_names_save = server_name_save
        server_backup_E_save = server_embed_names
        server_description = server_description
            
# server reboot
@bot.event
async def reboot_server(for_length:int, for_server_rdates:list, server_f:list):
    print("reboot_server est appelé")
    global server_rdates
    global server_R_date_save
    global server_rbd_path
    length = for_length
    server_rdates = for_server_rdates

    i_count =[]
    i_dates =[]
    
    for i in range(length):
        date = server_rdates[i]
        date = datetime.strptime(date, '%d-%m-%Y %H:%M')

        #count number of messages to reboot and save dates
        if (date - datetime.now()).total_seconds() <= 0:
            i_count.append(i)
            i_dates.append(date)

    for i in range(len(i_count)):
        openqrbd = open(server_rbd_path, "r+")
        server_rdates = openqrbd.read()
        server_rdates = server_rdates.split(',')
        
        date_calcul = date_calcul + timedelta(hours=7*24)
        date_calcul = f'{date_calcul.day}-{date_calcul.month}-{date_calcul.year} {date_calcul.hour}:{date_calcul.minute}'
        server_rdates[i_count[i]] = date_calcul

        openqrbd.seek(0)
        openqrbd.truncate()
        openqrbd.write(','.join(server_rdates))
        openqrbd.close()

        server_R_date_save = server_rdates

@bot.command()
async def serverdelete(ctx, name:str):

        global server_ebe_path
        global server_bn_path
        global server_rbd_path
        global server_rdates
        global server_rdates
        global server_embed_names
        global server_embed_id
        global server_status_names_save
        global server_R_date_save
        global server_backup_E_save
        global server_id
        global server_description
        global server_description_path

        if os.stat(server_rbd_path).st_size != 0:
            openqrbd = open(server_rbd_path, "r")
            server_rdates = openqrbd.read()
            openqrbd.close()
            server_rdates = server_rdates.split(',')

            openqebe = open(server_ebe_path, "r")
            server_embed_names = openqebe.read()
            openqebe.close()
            server_embed_names = server_embed_names.split(',')

            openqeid = open(server_id_path, "r")
            server_embed_id = openqeid.read()
            openqeid.close()
            server_embed_id = server_embed_id.split(',')

            openqf = open(server_description_path, "r")
            server_description = openqf.read()
            openqf.close()
            server_description = server_description.split(',')

        if ctx.channel.id == command_channel:
            #search for name in embed names
            openqebe = open(server_ebe_path, "r+")
            server_embed_names = openqebe.read()
            server_embed_names = server_embed_names.split(',')
            if name in server_embed_names:
                channel = bot.get_channel(server_channel)
                i = server_embed_names.index(name)
                delete_message = await channel.fetch_message(server_embed_id[i])
                await delete_message.delete()
                openqebe.close()

                openqrbd = open(server_rbd_path, "r+")
                server_rdates = openqrbd.read()
                server_rdates = server_rdates.split(',')
                del server_rdates[i]
                openqrbd.seek(0)
                openqrbd.truncate()
                openqrbd.write(','.join(server_rdates))
                openqrbd.close()

                openeebn = open(server_bn_path, "r+")
                server_status_names_save = openeebn.read()
                server_status_names_save = server_status_names_save.split(',')
                del server_status_names_save[i]
                openeebn.seek(0)
                openeebn.truncate()
                openeebn.write(','.join(server_status_names_save))
                openeebn.close()

                openqebe = open(server_ebe_path, "r+")
                server_embed_names = openqebe.read()
                server_embed_names = server_embed_names.split(',')
                del server_embed_names[i]
                openqebe.seek(0)
                openqebe.truncate()
                openqebe.write(','.join(server_embed_names))
                openqebe.close()

                openqeid = open(server_id_path, "r+")
                del server_embed_id[i]
                openqeid.seek(0)
                openqeid.truncate()
                openqeid.write(','.join(server_embed_id))
                openqeid.close()

                openqf = open(server_description_path, "r+")
                del server_description[i]
                openqf.seek(0)
                openqf.truncate()
                openqf.write(','.join(server_description))
                openqf.close()

                server_R_date_save = server_rdates
                server_backup_E_save = server_embed_names
                server_id = server_embed_id

                await ctx.channel.send(f'Le statu de serveur {name} a bien été supprimé.')
            else:
                await ctx.channel.send(f'Aucun statu de serveur n\'existe à ce nom.')
        else:
            await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')


#Beggins server statu creation
@bot.command()
async def serverstatus(ctx, server_status_names:str, jour:str, heure:str,):
    print("allo?")
    if ctx.channel.id == command_channel:
        global modifying
        modifying = 0
        description = "hebdo"
        Semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        semaine = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        actual_day = datetime.now().strftime("%A")
        actual_day = week.index(actual_day)

        if (jour in Semaine) or (jour in semaine):
            if jour in Semaine:
                index = Semaine.index(jour)
            if jour in semaine:
                index = semaine.index(jour)
            if (jour in Semaine) or (jour in semaine):
                index = index-actual_day
                if index < 0:
                    index = index+7

                heure = datetime.strptime(heure, '%H:%M')
                R_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year} {heure.hour}:{heure.minute}'
                R_date = datetime.strptime(R_date, '%d-%m-%Y %H:%M')
                R_date = R_date + timedelta(days=index)
                R_date = f'{R_date.day}-{R_date.month}-{R_date.year} {R_date.hour}:{R_date.minute}'
                await make_server(ctx, server_status_names, R_date, description, modifying)
            else:
                await ctx.send(f'Désolé, le jour indiqué doit être un nom de jour de la semaine. Tapez !help dans {bot.get_channel(command_channel)} pour plus d\'informations')
    else:
        await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')

@tasks.loop(seconds = server_sleeptime_loop)
async def server_message_update(ctx):
    # reboot server messages
    global server_ebe_path
    global server_bn_path
    global server_rbd_path
    global server_hrefresh 
    global server_mrefresh
    global server_update_running

    print("Starting server update")
    await modify_server(ctx)

    # Delete ended server messages
    global server_ebe_path
    global server_bn_path
    global server_sbd_path
    global server_ebd_path
    if os.stat(server_ebd_path).st_size != 0:
        openeebd = open(server_ebd_path, "r+")
        server_edates = openeebd.read()
        server_edates = server_edates.split(',')
        openeebd.close()
        length = len(server_edates)
        await delete_server(length, server_edates)

    



