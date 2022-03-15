import discord
from discord.ext import commands
from Utils.util import prettify,create_list
from random import randint
import random
import os

class Game:

    @staticmethod
    def roll():
        return randint(1, 6)

    @staticmethod
    def flip():
        coin = ["head", "tail"]
        selected = coin[randint(0,1)]
        return selected
    
    @staticmethod
    def givelane():
        lane=["top","jungle","mid","adc","support"]
        selected=lane[randint(0,len(lane)-1)]
        return selected


class Hungman:
    def __init__(self, word=None):
        
        self.word = word
        self.run = True
        
        self.word_meta = []
        self.stages = {}
        self.wrong_letters = []

        self.win = False

    def change_letter(self, letter):
        any_letter = 0
        for l in self.word_meta:
            if l[0] == letter.lower():
                l[1] = True
                any_letter += 1

        if not any_letter:
            self.wrong_letters.append(letter)

    def get_curr_word(self):
        res = "".join([l[0] if l[1] else "_" for l in self.word_meta])
        return res

    def get_curr_hung_stat(self):
        lenght = len(self.wrong_letters)
        return self.stages.get("stage"+str(lenght), "")

    def get_wrong_list(self):
        return "WRONG LIST: " + ",  ".join(self.wrong_letters)

    def check_meta(self):
        return all([i[1] for i in self.word_meta])

    def check_game_finished(self):
        if self.check_meta():
            self.win = True
            self.run = False

        if len(self.wrong_letters) > 6:
            self.run = False

    def init(self):
        
        # Init hungman pattern
        folder_loc = "Data/hungsman_stages/"
        for text_file in [f for f in os.listdir(folder_loc) if f.endswith(".txt")]:
            text_file_name = text_file[:-4]
            with open(folder_loc+text_file, "r") as txt_file:
                self.stages[text_file_name] = txt_file.read()

        # Init word meta
        for letter in self.word:
            self.word_meta.append([letter,False])

    @staticmethod
    def check_letter(letter):
        return len(letter) == 1 and letter.isalpha()

class Fun(commands.Cog,name="Fun Commands"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(description="Repeat something as many times as you want ")
    async def repeat(self, ctx, times : int, content="repeating"):
        for _ in range(times):
            await ctx.send(prettify(content))

    @commands.command(description="Play various games")
    async def game(self, ctx, game_type : str):

        methods = [method for method in dir(Game) if not method.startswith("__") and not method.endswith("_")]
        
        if game_type.lower() == "show":
            await ctx.send("Game List:")
            for method in methods:
                await ctx.send("- "+method)
        else:
            if game_type.lower() in methods:
                method = getattr(Game, game_type.lower())
                result = method()
                await ctx.send(prettify(result))
            else:
                await ctx.send(prettify(f"There is no game such that {game_type} "))

    @commands.command(description="Buy someone a beer")
    async def beer(self, ctx, user: discord.Member = None,  reason: commands.clean_content = ""):
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"{ctx.author.name}: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot {ctx.author.name}, but I don't think it will respond to you :/")

        beer_offer = f"{user.name}, you got a 🍺 from {ctx.author.name}"
        beer_offer = beer_offer + f"\n\nReason: {reason}" if reason else beer_offer
        await ctx.send(prettify(beer_offer))

    @commands.command(description="Press F to pay respect")
    async def f(self,ctx, *, text: commands.clean_content = None):
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for {text} " if text else ""
        await ctx.send(prettify(f"{ctx.author.name} has paid their respect {reason}{random.choice(hearts)}"))
    
    @commands.command(description="Create a list")
    async def createlist(self,ctx,title : str,*args):
        await ctx.send(create_list(title,args))
    
    @commands.command(description="Request a new password")
    async def password(self, ctx, nbytes: int = 18):
        alphabet="abcdefghijklmnoprstuvyzxwABCDEFGHIJKLMNOPRSTUVYZXW"
        numbers="0123456789"
        indicators=alphabet+numbers
        pswrd=""
        for _ in range(nbytes):
            pswrd+=indicators[randint(0,len(indicators)-1)]
        user = await self.bot.fetch_user(ctx.message.author.id)
        await user.send(prettify("You new password: "+pswrd))
        await ctx.send(prettify(f"Hey {ctx.message.author.display_name} I send you a private message about your password request."))
    
    @commands.command(description="Guess the number.")
    async def guess(self,ctx):
        computer = random.randint(1, 10)
        await ctx.send(prettify('Guess my number'))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        msg = await self.bot.wait_for("message", check=check)

        if int(msg.content) == computer:
            await ctx.send(prettify("Correct"))
        else:
            await ctx.send(prettify(f"Nope it was {computer}"))
    
    @commands.command(description="Play Hangman With Bot")
    async def hungman(self, ctx):
        
        if ctx.channel.name != "game":
            await ctx.send(prettify("You run this command only in 'GAME' channel"))
            return
        
        a = Hungman("kaplan")
        a.init()

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        await ctx.send(prettify("Welcome to Hungman"))

        while a.run:
            await ctx.send(prettify("letter >> "))
            msg = await self.bot.wait_for("message", check=check)
            letter = msg.content

            if not a.check_letter(letter):
                await ctx.send(prettify(f"Input must be character. (WRONG: {letter})"))
                continue

            a.change_letter(letter)
            a.check_game_finished()
            if a.run:
                await ctx.send(prettify(a.get_curr_word()))
                await ctx.send(prettify(a.get_curr_hung_stat()))
                await ctx.send(prettify(a.get_wrong_list()))

        if a.win:
            await ctx.send(prettify("You win the game"))
        else:
            await ctx.send(prettify("You lose the game"))

def setup(bot):
    bot.add_cog(Fun(bot))