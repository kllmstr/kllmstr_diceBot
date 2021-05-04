import discord
from discord.ext.commands import Bot
import random
import os

from dotenv import load_dotenv

load_dotenv()
bot = Bot(command_prefix='!')
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(name='server')
async def fetchServerInfo(context):
    guild = context.guild

    await context.send(f'Server Name: {guild.name}')
    await context.send(f'Server Size: {len(guild.members)}')
    await context.send(f'Server Name: {guild.owner.display_name}')

@bot.command(name='commands')
async def commandList(ctx):
    await ctx.channel.send('Liste des commandes : \n'
                           '!roll => Lance des dés classiques \n'
                           '!rollsw => Lance des dés spéciaux liés au JDR star wars l\'ére de la rébélion')

@bot.command(name='reponds')
async def hello(ctx, *, user: discord.Member = None):
    if user:
        for i in range(0,10):
            await ctx.send(f"VIENS ICI TT DE SUITE, {user.mention}")
    else:
        await ctx.send('Désignes quelq\'un fils de p*te !')

@bot.command(name='roll', help='Lance des dés classiques d6 d8 d12 d100 etc\ne.g. !roll 5d20 lance 5 dés à 20 faces, donne le résultat de chaque dé ainsi que leur somme')
async def classicalRoll(ctx, arg, *gargs):
    err = False
    errMessage = ''

    if 'd' in arg:
        args = arg.split('d')
        number = args[0]
        dice = args[1]

        if number != '' or dice != '':
            number = int(number) if number != '' else 1
            dice = int(dice)
            result = 0
            results = []
            for i in range(0, number):
                rslt = random.randint(1, dice) if len(gargs) == 0 else random.randint(1, dice)+int(gargs[0])
                results.append(rslt)
                result += rslt
    else:
        err = True
        errMessage = 'Erreur de syntaxe, veuillez réessayer'

    if err:
        await ctx.channel.send(errMessage)
    else:
        await ctx.channel.send(f'{ctx.author.mention} You rolled {results} ')

@bot.command(name='rollsw', help='utilisation !rollsw + nombre de dés et spécifier le dé e.g. !rollsw 1b 2n 3j\nb = dé bleu de fortune; n = dé noir d\'infortune; v = dé vert d\'aptitude; p = dé violet de difficulté; j = dé jaune de maitrise; r = dé rouge de défi; d = dé blanc de force/destin')
async def starwarsRoll(ctx, *args):
    fortune = []
    infortune = []
    aptitude = []
    difficulte = []
    maitrise = []
    defi = []
    destin = []

    args = list(args)

    succes = 0
    avantage = 0
    triomphe = 0
    ptNoir = 0
    ptBlanc = 0

    for arg in args:
        if 'b' in arg:
            arg = arg.split('b')[0] if arg.split('b')[0] != '' else 1
            for i in range(0, int(arg)):
                fortune.append(random.randint(1, 6))
        elif 'n' in arg:
            arg = arg.split('n')[0] if arg.split('n')[0] != '' else 1
            for i in range(0, int(arg)):
                infortune.append(random.randint(1, 6))
        elif 'v' in arg:
            arg = arg.split('v')[0] if arg.split('v')[0] != '' else 1
            for i in range(0, int(arg)):
                aptitude.append(random.randint(1, 8))
        elif 'p' in arg:
            arg = arg.split('p')[0] if arg.split('p')[0] != '' else 1
            for i in range(0, int(arg)):
                difficulte.append(random.randint(1, 8))
        elif 'j' in arg:
            arg = arg.split('j')[0] if arg.split('j')[0] != '' else 1
            for i in range(0, int(arg)):
                maitrise.append(random.randint(1, 12))
        elif 'r' in arg:
            arg = arg.split('r')[0] if arg.split('r')[0] != '' else 1
            for i in range(0, int(arg)):
                defi.append(random.randint(1, 12))
        elif 'd' in arg:
            arg = arg.split('d')[0] if arg.split('d')[0] != '' else 1
            for i in range(0, int(arg)):
                destin.append(random.randint(1, 12))

    for val in fortune:
        if val == 3:
            succes += 1
        elif val == 4:
            succes += 1
            avantage += 1
        elif val == 5:
            avantage += 2
        elif val == 6:
            avantage += 1

    for val in infortune:
        if val == 3 or val == 4:
            succes -= 1
        elif val == 5 or val == 6:
            avantage -= 1

    for val in aptitude:
        if val == 2 or val == 3:
            succes += 1
        elif val == 4:
            succes += 2
        elif val == 5 or val == 6:
            avantage += 1
        elif val == 7:
            succes += 1
            avantage += 1
        elif val == 8:
            avantage += 2

    for val in difficulte:
        if val == 2:
            succes -= 1
        elif val == 3:
            succes -= 2
        elif val == 4 or val == 5 or val == 6:
            avantage -= 1
        elif val == 7:
            avantage -= 2
        elif val == 8:
            succes -= 1
            avantage -= 1

    for val in maitrise:
        if val == 2 or val == 3:
            succes += 1
        elif val == 4 or val == 5:
            succes += 2
        elif val == 6:
            avantage += 1
        elif val == 7 or val == 8 or val == 9:
            succes += 1
            avantage += 1
        elif val == 10 or val == 11:
            avantage += 2
        elif val == 12:
            triomphe += 1

    for val in defi:
        if val == 2 or val == 3:
            succes -= 1
        elif val == 4 or val == 5:
            succes -= 2
        elif val == 6 or val == 7:
            avantage -= 1
        elif val == 8 or val == 9:
            succes -= 1
            avantage -= 1
        elif val == 10 or val == 11:
            avantage -= 2
        elif val == 12:
            triomphe -= 1

    for val in destin:
        if val == 1 or val == 2 or val == 3 or val == 4 or val == 5 or val == 6:
            ptNoir += 1
        elif val == 7:
            ptNoir += 2
        elif val == 8 or val == 9:
            ptBlanc += 1
        elif val == 10 or val == 11 or val == 12:
            ptBlanc += 2

    succesMsg = ''
    avantageMsg = ''
    triompheMsg = ''

    if succes > 0:
        succesMsg = f'Votre jet est réussi avec {succes} succès'
    elif succes < 0:
        succesMsg = f'Votre jet est raté avec {-succes} échect'
    else:
        succesMsg = 'Égalité, il ne se passe rien'


    if avantage >= 0:
        avantageMsg = f', {avantage} avantages'
    elif avantage < 0:
        avantageMsg = f', {-avantage} désavantages'

    if triomphe >= 0:
        triompheMsg = f'et {triomphe} triomphes'
    elif triomphe < 0:
        triompheMsg = f'et {-triomphe} désastres'

    if (len(destin) > 0):
        await ctx.channel.send(f'{ctx.author.mention} Ton jet a donné {ptNoir} points noirs et {ptBlanc} points blancs')
    else:
        await ctx.channel.send(f'{ctx.author.mention} {succesMsg} {avantageMsg} {triompheMsg} ')
                               # f'Succes:{succes} avantage:{avantage} triomphe:{triomphe} \n'
                           # f'fortune:{fortune} infortune:{infortune} aptitude:{aptitude} difficulte:{difficulte} maitrise:{maitrise} defi:{defi} destin:{destin}')


bot.run(TOKEN)
