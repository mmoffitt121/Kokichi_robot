import random
from datetime import datetime
import time

import asyncio

from discord.ext.commands import Bot
import discord  # python -m pip install discord.py

# <editor-fold desc = "global variables">
BOT_PREFIX = ("kokichi.", "kok.", "kokichi ", "kok ")
TOKEN = "NzIyODk1NjI0NTg0MDM2Mzcy.Xu_ofg.fDQyPDl1kn5YOqQ20eLNQs43yfk"

bot = Bot(command_prefix=BOT_PREFIX)

class RunTime:
    hangman_running = False
    hangman_input = ""

    timer_running = False


# </editor-fold desc = "global variables">

# <editor-fold desc = "discord functions">

# -=-=-
# Timer
# -=-=-

@bot.command(name="timer")
async def kokichi_timer(ctx, *args):  # Command that sets a timer for an inputted number of seconds
    if not RunTime.timer_running:
        if args:
            if args[0].isnumeric():
                RunTime.timer_running = True
                input_seconds = args[0]

                command_name = "kokichi_timer for " + str(input_seconds) + " seconds."
                print_command(command_name, ctx.message.author.name, ctx.message.author.id, ctx.message.author.display_name)

                start_time = time.time()
                input_seconds = float(input_seconds)

                bar_color = 0xff00ff
                embed = discord.Embed(title="Timer", color=bar_color)  # Sets initial time, creates embed
                embed.add_field(name="Time:", value=int(start_time + input_seconds - time.time()), inline=False)
                timer_message = await ctx.send(embed=embed)

                next_second = int(time.time()) + 1
                while time.time() < start_time + input_seconds:  # Edits embed to show current time
                    current_time = time.time()
                    if int(current_time) == int(next_second):
                        next_second += 1

                        new_embed = discord.Embed(title="Timer", color=bar_color)
                        new_embed.add_field(name="Time:", value=int(start_time + input_seconds - time.time()), inline=False)
                        await timer_message.edit(embed=new_embed)

                await ctx.send("Time is up!")
                RunTime.timer_running = False
            else:
                await ctx.send("Enter a number. Bitch.")

        else:
            await ctx.send("To use this command, please specify the number of seconds.")
    else:
        await ctx.send("Wait your fucking turn, someone else has already started a timer.")

# -=-=-
# Bank
# -=-=-

# incomplete

# -=-=-=-
# Hangman
# -=-=-=-

@bot.command(name="hangman")
async def kokichi_hangman(ctx, *args):
    if not RunTime.hangman_running:
        RunTime.hangman_running = True
        users = []

        urldict = get_urldict()
        strikes = 0

        character = "K"
        word = random.choice(get_words())

        available = "[ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z ]"
        guessed = "= " * len(word)
        guessed = list(guessed)
        for i in range(len(word)):
            if word[i].upper() == "|":
                guessed[i * 2] = "|"
        guessed = "".join(guessed)

        while True:  # Each loop iteration is one round of gameplay
            # output block =-=-=-=-
            if strikes > 5:
                await kokichi_hangman_printwinnerloser(ctx, False, word, urldict, character)
                break
            if not "=" in guessed:
                await kokichi_hangman_printwinnerloser(ctx, True, word, urldict, character)
                break
            await kokichi_hangman_printgame(ctx, urldict, character, strikes, available, guessed)
            # /output block =-=-=-=-

            # Computes gameplay
            while True:
                if RunTime.hangman_input:
                    guess = RunTime.hangman_input
                    RunTime.hangman_input = ""
                    if guess in available:
                        available = available.replace(guess, "-")
                        if guess in word.upper():
                            guessed = list(guessed)
                            for i in range(len(word)):
                                if word[i].upper() == guess:
                                    guessed[i*2] = guess
                            guessed = "".join(guessed)
                        else:
                            strikes += 1
                        break
                    else:
                        await ctx.send("You've already guessed " + guess + "!")
                await asyncio.sleep(1)
        RunTime.hangman_running = False

async def kokichi_hangman_printgame(ctx, urldict, character, strikes, available, guessed):  # Prints each round
    embed = discord.Embed(title="Kokichi's Hangman", color=0xff00ff)
    embed.set_image(url=urldict["HM" + character + str(strikes)])
    embed.add_field(name="Available Characters:", value=available, inline=False)
    embed.add_field(name="Word:", value=guessed, inline=False)
    await ctx.send(embed=embed)

async def kokichi_hangman_printwinnerloser(ctx, did_i_win, word, urldict, character):  # Prints victory or defeat
    if did_i_win:
        embed = discord.Embed(title="Victory!", color=0xff00ff)
        embed.set_image(url=urldict["HM" + character + "6"])
        embed.add_field(name="Word:", value=word.upper(), inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="You lost!", color=0xff00ff)
        embed.set_image(url=urldict["HM" + character + "6"])
        embed.add_field(name="Wow!", value="You must be a hardcore loser!", inline=False)
        embed.add_field(name="Word:", value=word.upper(), inline=False)
        await ctx.send(embed=embed)

# -=-=-
# Horny
# -=-=-

@bot.command(name="horny")  # Command that returns a random string for how horny the user is
async def kokichi_how_horny(ctx):
    command_name = "how_horny"
    print_command(command_name, ctx.message.author.name, ctx.message.author.id, ctx.message.author.display_name)

    possible_responses = [
        "You are horny.",
        "You are kind of horny.",
        "You are no longer horny.",
        "I have taken your horny."
    ]
    await ctx.send(random.choice(possible_responses))

# -=-=-=-=-=-=-=-
# Initialization
# -=-=-=-=-=-=-=-

@bot.event  # Command that prints to the console when the bot is online
async def on_ready():
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("Logged in as", bot.user.name)
    print("userID:", bot.user.id)
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

# -=-=-=-=-=-=-=-=-
# Message Analysis
# -=-=-=-=-=-=-=-=-

@bot.event
async def on_message(message):
    if RunTime.hangman_running:
        try:
            message.content.strip()[1]
        except:
            if str(message.content).strip().isalpha():
                RunTime.hangman_input = str(message.content).strip().upper()

    if str(message.author) == "Wolf#0649":  # Jeremy
        await message.add_reaction(":GayRats:596127670111305732")
    if str(message.author) == "protosapper#7808":  # Sean
        await message.add_reaction(":gotit:492091724781453313")
    if str(message.author) == "Pwnutbutter#8964":  # Jonathan
        await message.add_reaction(":Horny:667192911200518174")

    await bot.process_commands(message)

# </editor-fold desc = "discord functions">

# <editor-fold desc = "helper functions">

# -=-=-=-=-
# Datafiles
# -=-=-=-=-

def print_command(chosen_command, user_name, user_id, user_disp):  # The executed command is logged
    output = ("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n"
              "Time: [{}]\n"
              "Command Run: [{}]\n"
              "Name: [{}]\n"
              "UserID: [{}]\n"
              "Nickname: [{}]\n"
              .format(datetime.now(), chosen_command, user_name, user_id, user_disp))

    log = open("data/log.txt", "a")
    log.write(output)
    print(output)

def get_urldict():  # gets dictionary of image urls in folder
    with open("data/image_urls.dat", "r") as image_urls:
        urldict = {}
        for line in image_urls:
            urldict.update({line[0:4]: line[5:]})
        return urldict

def get_users():  # Returns a dictionary of userids and money taken from users.dat
    with open("data/users.dat", "r") as users_file:
        userdict = {}
        for line in users_file:
            i = line.find(",")
            print(i)
            userdict.update({line[:i]: line[i+1:].strip()})
        print(userdict)

def save_users(users):  # Gets a dictionary of users as input, saves in users.dat
    with open("data/users.dat", "w") as users_file:
        keys = users.keys()
        for i in keys:
            users_file.write(str(i) + "," + str(users[i]) + "\n")

def get_words():  # Gets wordlist from directory
    with open("data/word_list.dat", "r") as word_data:
        output_list = []
        char_list = []
        for line in word_data:
            for i in line.strip():
                if i.isalpha() or i == "|":
                    char_list.append(i)
            output_list.append("".join(char_list))
            char_list = []
        print(output_list)
        return output_list


# </editor-fold desc = "helper functions">

bot.run(TOKEN)
