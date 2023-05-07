import discord
import discord.ext.commands
from discord.utils import get
import emojis
import os 

# Initialise variables
global roles_backup
roles_backup = ([],[],"")

roles_backup_path = f'{root}/{save_folder_Path}/backup_roles.txt'
isExist = os.path.exists(roles_backup_path)
if not isExist:
    create_txt =open(roles_backup_path, "w", encoding="utf-8")
    create_txt.close()

# Role file loading
@bot.event
async def on_ready():
    global roles_save
    global server_emojis
    roles_save = ([],[],[],[])
    server_emojis = []

    if os.stat(roles_backup_path).st_size != 0:
        roles_string = open(roles_backup_path, 'r', encoding="utf-8")
        roles_save = roles_string.read()
        roles_save = roles_save.replace(", ",",")
        roles_save = roles_save.replace("],[","]|[")
        roles_save = roles_save.replace("(","")
        roles_save = roles_save.replace(")","")
        roles_save = roles_save.replace("[","")
        roles_save = roles_save.replace("]","")
        roles_save = roles_save.replace("'","")
        roles_save = roles_save.split('|')
        roles_save = (roles_save[0].split(','),roles_save[1].split(','),[roles_save[2]],[roles_save[3]])
        roles_string.close()

    
    for emote in bot.emojis:
        server_emojis.append(emote)
    if roles_save != ([],[],[],[]):
        await role_message(roles_save)


# Make/modify role message
@bot.event
async def role_message(save):
    global roles_save
    channel = bot.get_channel(role_channel)

    roles_m = discord.Embed(title="Liste des rôles", description="")
    for i in range(len(roles_save[0])):
        roles_m.add_field(name= f'{emojis.encode(roles_save[1][i])}   {roles_save[0][i]}', value = "", inline=False)
    if save[3] == []:
        save[3].append(str((await channel.send(embed=roles_m)).id))
        message = await channel.fetch_message(save[3][0])
        await message.add_reaction(emojis.encode(roles_save[1][0]))

    if save[2] == []:
        save[2].append(roles_m)
    else:
        save[2][0] = roles_m
    
        message = await channel.fetch_message(save[3][0])
        await message.edit(embed = save[2][0])
        for y in range(len(save[1])):
            await message.add_reaction(emojis.encode(roles_save[1][y]))
    roles_save = save

# Add role to a member
@bot.event
async def on_raw_reaction_add(reaction):
    global roles_save

    print(reaction)
    channel = bot.get_channel(role_channel)
    message = await channel.fetch_message(roles_save[3][0])

    if reaction.message_id != message.id:
        return
    else:
        if (emojis.decode(reaction.emoji.name)) in roles_save[1]:
            index = roles_save[1].index(emojis.decode(reaction.emoji.name))
            member = reaction.member
            role = discord.utils.get(reaction.member.guild.roles, name = roles_save[0][index])
            await member.add_roles(role)

#Remove role to a member
@bot.event
async def on_raw_reaction_remove(reaction):
    global roles_save

    print(reaction)

    channel = bot.get_channel(role_channel)
    message = await channel.fetch_message(roles_save[3][0])

    if reaction.message_id != message.id:
        return
    else:
        if (emojis.decode(reaction.emoji.name)) in roles_save[1]:
            index = roles_save[1].index(emojis.decode(reaction.emoji.name))
            guild = discord.utils.find(lambda g : g.id == reaction.guild_id, bot.guilds)
            member = discord.utils.find(lambda m : m.id == reaction.user_id, guild.members)
            role = discord.utils.get(guild.roles, name = roles_save[0][index])
            await member.remove_roles(role)

# Create a new role
@bot.command()
async def role(ctx, name = None, emote = None):
    global roles_save
    global server_emojis

    if ctx.channel.id == command_channel:
        if not name or not emote:
            await ctx.channel.send(f'Désolé, vous devez donner un nom et un emoji au rôle que vous créez.')
        else:
            if emojis.count(emote) == 1 or emote in server_emojis:
                if name in roles_save[0] or emote in roles_save[1]:
                    if name in roles_save[0]:
                        await ctx.channel.send(f'Désolé, un rôle existe déjà à ce nom.')
                    if emote in roles_save[1]:
                        await ctx.channel.send(f'Désolé, cet emoji est déjà associé à un rôle.')
                else:
                    roles_save[0].append(name)
                    if emojis.count(emote) == 1:
                        roles_save[1].append(emojis.decode(emote))
                    if emote in server_emojis:
                        roles_save[1].append(emote)
                    await ctx.guild.create_role(name = name, mentionable = True)

                    #update txt files to save actual roles datas
                    openbr = open(roles_backup_path, "w+", encoding="utf-8")
                    openbr.seek(0)
                    openbr.truncate()
                    openbr.write(str(roles_save))
                    openbr.close()

                    await role_message(roles_save)
                    await ctx.channel.send(f'Le rôle {name} a bien été créé associé à l\'emoji {emote}.')
            else:
                await ctx.channel.send(f'Désolé, l\'emoji saisi n\'est pas valide.')
    else:
        await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')

#suprimme un role
@bot.command()
async def roledelete(ctx, name):
    global roles_save
    
    if ctx.channel.id == command_channel:
        if not name:
            await ctx.channel.send(f'Désolé, vous devez nommer le rôle que vous voulez supprimer.')

        if name in roles_save[0]:
            index = roles_save[0].index(name)
            del roles_save[0][index]
            channel = bot.get_channel(role_channel)
            print(roles_save[3][0])
            message = await channel.fetch_message(roles_save[3][0])
            await message.clear_reaction(emojis.encode(roles_save[1][index]))
            del roles_save[1][index]

            #update txt files to save actual roles datas
            openbr = open(roles_backup_path, "w+", encoding="utf-8")
            openbr.seek(0)
            openbr.truncate()
            openbr.write(str(roles_save))
            openbr.close()
            
            await role_message(roles_save)
            await ctx.channel.send(f'Le rôle {name} a bien été supprimé.')
        else:
            await ctx.channel.send(f'Désolé, aucun rôle n\'existe à ce nom.')
    else:
        await ctx.channel.send(f'Désolé, vous devez utiliser cette commande dans le salon {bot.get_channel(command_channel)}')