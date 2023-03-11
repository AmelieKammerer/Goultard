import asyncio
import discord
import discord.ext.commands
from datetime import datetime, timedelta, timezone
from time import mktime
from discord.ext import commands, tasks
import os 
from array import array
from pathlib import Path

#Initialise backup of existing quests. create txt files if they don't exist
global quest_backup_names
global quest_backup_rdates
global quest_backup_embed
global quest_frequence
global backup_string
global quest_context_path
global quest_frequence_path

quest_bn_path = f'{root}/{save_folder_Path}/backup_quests_names.txt'
quest_rbd_path = f'{root}/{save_folder_Path}/backup_quests_rdates.txt'
quest_ebe_path = f'{root}/{save_folder_Path}/backup_quest_embed.txt'
quest_id_path = f'{root}/{save_folder_Path}/backup_quests_id.txt'
quest_context_path = f'{root}/{save_folder_Path}/backup_quest_context.txt'
quest_frequence_path = f'{root}/{save_folder_Path}/backup_quest_frequence.txt'

isExist = os.path.exists(quest_bn_path)
if not isExist:
    create_txt =open(quest_bn_path, "w", encoding="utf-8")
    create_txt.close()
isExist = os.path.exists(quest_rbd_path)
if not isExist:
    create_txt =open(quest_rbd_path, "w", encoding="utf-8")
    create_txt.close()
isExist = os.path.exists(quest_ebe_path)
if not isExist:
    create_txt =open(quest_ebe_path, "w", encoding="utf-8")
    create_txt.close()
isExist = os.path.exists(quest_id_path)
if not isExist:
    create_txt =open(quest_id_path, "w", encoding="utf-8")
    create_txt.close()
isExist = os.path.exists(quest_context_path)
if not isExist:
    create_txt =open(quest_context_path, "w", encoding="utf-8")
    create_txt.close()

isExist = os.path.exists(quest_frequence_path)
if not isExist:
    create_txt =open(quest_frequence_path, "w", encoding="utf-8")
    create_txt.close()

#Initialise date formats
long_date = "<t:D>" #<t: epoch :D>
relative_time = "<t:R>" #<t: epoch :R>
short_time = "<t:t>" #<t: epoch :t>

#initialise images
global quest_dimage_url
global quest_himage_url
quest_dimage_url = "https://cdn.discordapp.com/attachments/1066006061154312263/1068132244960596030/iop_quotidienne.jpg"
quest_himage_url = "https://cdn.discordapp.com/attachments/1066006061154312263/1068132244683763762/xelor_hebdomadaire.jpg"

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
    global quest_update_running
    quest_update_running = 0
    bot_start = 0
    if os.stat(quest_context_path).st_size != 0:
        quest_update_running = 1
        await asyncio.sleep(quest_sleeptime)
        quest_message_update.start(command_channel)
    else:
        bot_start = 1

    #Initialise quest names and dates variables
    global tmp_save
    tmp_save = ""
    global quest_name_save
    global quest_R_date_save
    global quest_backup_E_save
    global quest_id
    global quest_frequence
    global quest_frequence_path

    if os.stat(quest_bn_path).st_size == 0:
        quest_name_save = []
    else:
        backup_string = open(quest_bn_path, 'r', encoding="utf-8")
        quest_name_save = backup_string.read()
        quest_name_save = quest_name_save.split(',')
        backup_string.close()

    if os.stat(quest_rbd_path).st_size == 0:
        quest_R_date_save = []
    else:
        backup_string = open(quest_rbd_path, 'r', encoding="utf-8")
        quest_R_date_save = backup_string.read()
        quest_R_date_save = quest_R_date_save.split(',')
        backup_string.close()

    if os.stat(quest_ebe_path).st_size == 0:
        quest_backup_E_save = []
    else:
        backup_string = open(quest_ebe_path, 'r', encoding="utf-8")
        quest_backup_E_save = backup_string.read()
        quest_backup_E_save = quest_backup_E_save.split(',')
        backup_string.close()

    if os.stat(quest_id_path).st_size == 0:
        quest_id = []
    else:
        backup_string = open(quest_id_path, 'r', encoding="utf-8")
        quest_id = backup_string.read()
        quest_id = quest_id.split(',')
        backup_string.close()

    if os.stat(quest_frequence_path).st_size == 0:
        quest_frequence = []
    else:
        backup_string = open(quest_frequence_path, 'r', encoding="utf-8")
        quest_frequence = backup_string.read()
        quest_frequence = quest_frequence.split(',')
        backup_string.close()

# Starting quest date setting command
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

# quest command
@bot.event
async def make_quest(ctx, quest_name:str, R_date:str, frequence:str, modifying:int, ID = ID):
    global quest_sleeptime
    global quest_name_save
    global quest_R_date_save
    global quest_backup_E_save
    global quest_id
    global quest_frequence
    global quest_frequence_path
    global tmp_save
    global bot_start
    global quest_update_running
    global quest_frequence
    if modifying == 1:
        if quest_name_save == []:
            quest_name_save.append(quest_name)
            quest_R_date_save.append(R_date)
            quest_backup_E_save.append(quest_name)
            quest_frequence.append(frequence)

    if modifying == 0:
        bot_start = 1
        #check if an quest already exist with the same name
        if ctx.channel.id != command_channel:
                await ctx.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')
                return
        else:
            backup_string = open(quest_bn_path, 'r', encoding="utf-8")
            ifquest_name_save = backup_string.read()
            ifquest_name_save = ifquest_name_save.split(',')
            backup_string.close()
            if (quest_name) in ifquest_name_save and modifying == 0:
                await ctx.send(f'Une quête à ce nom existe déjà, veuillez choisir un autre nom')
                return
            else:
                #save quest_name and date to be able to save them later in a txt file
                quest_name_save.append(quest_name)
                quest_R_date_save.append(R_date)
                quest_backup_E_save.append(quest_name)
                quest_frequence.append(frequence)

    #calculate quest date reset
    Title = quest_name
    R_date = datetime.strptime(R_date, '%d-%m-%Y %H:%M')
    quest_name = discord.Embed(title=Title, description="La quête est disponible jusqu'au:")
    await timezones(quest_name, R_date)
    separator = relative_time.find(":")
    await start_date(R_date.astimezone(central_europe).strftime('%d-%m-%Y %H:%M'))
    quest_name.add_field(name= "Temps restant avant la fin de la quête:", value= f'{relative_time[:(separator+1)]}{tmp_save}{relative_time[(separator):]}', inline=False)   

    #quest Images
    if frequence == "daily":
        quest_name.set_image(url= quest_dimage_url)
    if frequence == "hebdo":
        quest_name.set_image(url= quest_himage_url)

    if bot_start !=0:
        if modifying == 0:
            channel = bot.get_channel(quest_channel)
            if ctx.channel.id == command_channel:

                quest_id.append(str((await channel.send(embed=quest_name)).id))
                await ctx.channel.send(f'Votre quête {Title} à bien été créé dans le salon {bot.get_channel(quest_channel)}')
                
                #update txt files to save actual quests datas
                openqbn = open(quest_bn_path, "w+", encoding="utf-8")
                openqbn.seek(0)
                openqbn.truncate()
                openqbn.write(','.join(quest_name_save))
                openqbn.close()

                openqrbd = open(quest_rbd_path, "w+", encoding="utf-8")
                openqrbd.seek(0)
                openqrbd.truncate()
                openqrbd.write(','.join(quest_R_date_save))
                openqrbd.close()

                openqebe = open(quest_ebe_path, "w+", encoding="utf-8")
                openqebe.seek(0)
                openqebe.truncate()
                openqebe.write(','.join(quest_backup_E_save))
                openqebe.close()

                openqeid = open(quest_id_path, "w+", encoding="utf-8")
                openqeid.seek(0)
                openqeid.truncate()
                openqeid.write(','.join(quest_id))
                openqeid.close()

                openqefd = open(quest_frequence_path, "w+", encoding="utf-8")
                openqefd.seek(0)
                openqefd.truncate()
                openqefd.write(','.join(quest_frequence))
                openqefd.close()

                if os.stat(quest_context_path).st_size == 0:
                    openqc = open(quest_context_path, "w+", encoding="utf-8")
                    openqc.seek(0)
                    openqc.truncate()
                    openqc.write(str(ctx))
                    openqc.close()

                if quest_update_running == 0:
                    if quest_hrefresh == 0:
                        quest_sleeptime = (((60*quest_mrefresh)+0) - (datetime.now().second))
                    if quest_mrefresh == 0:
                        quest_sleeptime = (((3600*quest_hrefresh)) - (datetime.now().hour))
                    if (quest_hrefresh > 0) and (quest_mrefresh > 0):
                        quest_sleeptime = (((60*quest_mrefresh)) - (datetime.now().second)) + (((3600*quest_hrefresh)) - (datetime.now().hour))
                    await asyncio.sleep(quest_sleeptime)
                    quest_message_update.start(ctx)
                    quest_update_running = 1
            else:
                await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')
                
        else:
            channel = bot.get_channel(quest_channel)
            message = await channel.fetch_message(ID)
            await message.edit(embed = quest_name)
            
    else:
        channel = bot.get_channel(quest_channel)
        message = await channel.fetch_message(ID)
        await message.edit(embed = quest_name)

#modify existing quest messages
@bot.event
async def modify_quest(ctx):
    global quest_ebe_path
    global quest_bn_path
    global quest_rbd_path
    global modifying
    global quest_rdates
    global quest_frequence
    global quest_frequence_path
    global quest_embed_names
    global quest_embed_id
    modifying = 1

    if os.stat(quest_rbd_path).st_size != 0:
        openqrbd = open(quest_rbd_path, "r", encoding="utf-8")
        quest_rdates = openqrbd.read()
        openqrbd.close()
        quest_rdates = quest_rdates.split(',')

        openqebe = open(quest_ebe_path, "r", encoding="utf-8")
        quest_embed_names = openqebe.read()
        openqebe.close()
        quest_embed_names = quest_embed_names.split(',')

        openqeid = open(quest_id_path, "r", encoding="utf-8")
        quest_embed_id = openqeid.read()
        openqeid.close()
        quest_embed_id = quest_embed_id.split(',')

        openqf = open(quest_frequence_path, "r", encoding="utf-8")
        quest_frequence = openqf.read()
        openqf.close()
        quest_frequence = quest_frequence.split(',')

        for i in range(len(quest_embed_names)):
            await make_quest(ctx, quest_embed_names[i], quest_rdates[i], quest_frequence[i], modifying, quest_embed_id[i])
            

# quest reboot
@bot.event
async def reboot_quest(for_length:int, for_quest_rdates:list, quest_f:list):
    print("reboot_quest est appelé")
    global quest_rdates
    global quest_R_date_save
    global quest_rbd_path
    length = for_length
    quest_rdates = for_quest_rdates

    i_count =[]
    i_dates =[]
    
    for i in range(length):
        date = quest_rdates[i]
        date = datetime.strptime(date, '%d-%m-%Y %H:%M')

        #count number of messages to reboot and save dates
        if (date - datetime.now()).total_seconds() <= 0:
            i_count.append(i)
            i_dates.append(date)

    for i in range(len(i_count)):
        openqrbd = open(quest_rbd_path, "r+", encoding="utf-8")
        quest_rdates = openqrbd.read()
        quest_rdates = quest_rdates.split(',')
        
        date_calcul = datetime.strptime(quest_rdates[i], '%d-%m-%Y %H:%M')
        if quest_f[i_count[i]] == "daily":
            date_calcul = date_calcul + timedelta(hours=24)
        if quest_f[i_count[i]] == "hebdo":
            date_calcul = date_calcul + timedelta(hours=7*24)
        date_calcul = f'{date_calcul.day}-{date_calcul.month}-{date_calcul.year} {date_calcul.hour}:{date_calcul.minute}'
        quest_rdates[i_count[i]] = date_calcul

        openqrbd.seek(0)
        openqrbd.truncate()
        openqrbd.write(','.join(quest_rdates))
        openqrbd.close()

        quest_R_date_save = quest_rdates

@bot.command()
async def questdelete(ctx, name:str):

        global quest_ebe_path
        global quest_bn_path
        global quest_rbd_path
        global quest_rdates
        global quest_rdates
        global quest_embed_names
        global quest_embed_id
        global quest_name_save
        global quest_R_date_save
        global quest_backup_E_save
        global quest_id
        global quest_frequence
        global quest_frequence_path

        if os.stat(quest_rbd_path).st_size != 0:
            openqrbd = open(quest_rbd_path, "r", encoding="utf-8")
            quest_rdates = openqrbd.read()
            openqrbd.close()
            quest_rdates = quest_rdates.split(',')

            openqebe = open(quest_ebe_path, "r", encoding="utf-8")
            quest_embed_names = openqebe.read()
            openqebe.close()
            quest_embed_names = quest_embed_names.split(',')

            openqeid = open(quest_id_path, "r", encoding="utf-8")
            quest_embed_id = openqeid.read()
            openqeid.close()
            quest_embed_id = quest_embed_id.split(',')

            openqf = open(quest_frequence_path, "r", encoding="utf-8")
            quest_frequence = openqf.read()
            openqf.close()
            quest_frequence = quest_frequence.split(',')

        if ctx.channel.id == command_channel:
            #search for name in embed names
            openqebe = open(quest_ebe_path, "r+", encoding="utf-8")
            quest_embed_names = openqebe.read()
            quest_embed_names = quest_embed_names.split(',')
            if name in quest_embed_names:
                channel = bot.get_channel(quest_channel)
                i = quest_embed_names.index(name)
                delete_message = await channel.fetch_message(quest_embed_id[i])
                await delete_message.delete()
                openqebe.close()

                openqrbd = open(quest_rbd_path, "r+", encoding="utf-8")
                quest_rdates = openqrbd.read()
                quest_rdates = quest_rdates.split(',')
                del quest_rdates[i]
                openqrbd.seek(0)
                openqrbd.truncate()
                openqrbd.write(','.join(quest_rdates))
                openqrbd.close()

                openeebn = open(quest_bn_path, "r+", encoding="utf-8")
                quest_name_save = openeebn.read()
                quest_name_save = quest_name_save.split(',')
                del quest_name_save[i]
                openeebn.seek(0)
                openeebn.truncate()
                openeebn.write(','.join(quest_name_save))
                openeebn.close()

                openqebe = open(quest_ebe_path, "r+", encoding="utf-8")
                quest_embed_names = openqebe.read()
                quest_embed_names = quest_embed_names.split(',')
                del quest_embed_names[i]
                openqebe.seek(0)
                openqebe.truncate()
                openqebe.write(','.join(quest_embed_names))
                openqebe.close()

                openqeid = open(quest_id_path, "r+", encoding="utf-8")
                del quest_embed_id[i]
                openqeid.seek(0)
                openqeid.truncate()
                openqeid.write(','.join(quest_embed_id))
                openqeid.close()

                openqf = open(quest_frequence_path, "r+", encoding="utf-8")
                del quest_frequence[i]
                openqf.seek(0)
                openqf.truncate()
                openqf.write(','.join(quest_frequence))
                openqf.close()

                quest_R_date_save = quest_rdates
                quest_backup_E_save = quest_embed_names
                quest_id = quest_embed_id

                await ctx.channel.send(f'La quête {name} a bien été supprimée.')
            else:
                await ctx.channel.send(f'Aucune quête n\'existe à ce nom.')
        else:
            await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')

#Beggins daily quest creation 
@bot.command()
async def dailyquest(ctx, quest_name:str, heure:str):
    if ctx.channel.id == command_channel:
        global modifying
        modifying = 0
        frequence = "daily"
        heure = datetime.strptime(heure, '%H:%M')
        R_date = f'{datetime.now().day}-{datetime.now().month}-{datetime.now().year} {heure.hour}:{heure.minute}'
        await make_quest(ctx, quest_name, R_date, frequence, modifying)
    else:
        await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')

#Beggins hebdo quest creation
@bot.command()
async def hebdoquest(ctx, quest_name:str, jour:str, heure:str,):
    if ctx.channel.id == command_channel:
        global modifying
        modifying = 0
        frequence = "hebdo"
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
                await make_quest(ctx, quest_name, R_date, frequence, modifying)
            else:
                await ctx.send(f'Désolé, le jour indiqué doit être un nom de jour de la semaine. Tapez !help dans {bot.get_channel(command_channel)} pour plus d\'informations')
    else:
        await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')

@tasks.loop(seconds = quest_sleeptime_loop)
async def quest_message_update(ctx):
    # reboot quest messages
    global quest_ebe_path
    global quest_bn_path
    global quest_rbd_path
    global quest_hrefresh 
    global quest_mrefresh
    global quest_update_running

    print("Starting quest update")

    if os.stat(quest_rbd_path).st_size != 0: #remplacer par r date
        openqrbd = open(quest_rbd_path, "r+", encoding="utf-8")
        quest_rdates = openqrbd.read()
        quest_rdates = quest_rdates.split(',')
        openqrbd.close()

        openqf = open(quest_frequence_path, "r+", encoding="utf-8")
        quest_f = openqf.read()
        quest_f = quest_f.split(',')
        openqf.close()

        length = len(quest_rdates)
        await reboot_quest(length, quest_rdates, quest_f)
    await modify_quest(ctx)

