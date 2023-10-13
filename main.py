import hikari
import lightbulb
import datetime
import pytz
import gspread
import random
import asyncio
import miru

bot = lightbulb.BotApp(token="#####", default_enabled_guilds=(997911326141714465))

#Google sheet stuff
sa = gspread.service_account(filename="cult-bot-document-0309ae29bae7.json")
sh = sa.open("CultBotDiscord")
wks = sh.worksheet("Discord Data")

@bot.command()
@lightbulb.command('summon', '@everyone 5 time')
@lightbulb.implements(lightbulb.SlashCommand)
async def summon(ctx):
    await ctx.respond("I'll start summoning everyone!")
    await bot.rest.create_message(ctx.channel_id,hikari.File(r"C:\Users\satap\PycharmProjects\BK BOT NEW\Summon.webp"))
    for i in range(5):
        await bot.rest.create_message(ctx.channel_id, "@everyone")

@bot.command()
@lightbulb.command('countdown', 'Group for time command')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def time_group(ctx):
    pass

@time_group.child
@lightbulb.command('five', '5 minute countdown')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    await ctx.respond("Timer for 5 minute⌛ start!")
    await bot.rest.create_message(ctx.channel_id,"https://upload.wikimedia.org/wikipedia/commons/7/7a/Alarm_Clock_GIF_Animation_High_Res.gif")
    for i in range(5 * 60):
        await asyncio.sleep(1) #5 min
        if i % 60 == 0 and i != 0:
            await ctx.respond(str(int(i/60)) + " minute⌛ has passed!")
    await ctx.respond("Timer ended!")

@time_group.child
@lightbulb.command('ten', '10 minute countdown')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    await ctx.respond("Timer for 10 minute⌛ start!")
    await bot.rest.create_message(ctx.channel_id,"https://upload.wikimedia.org/wikipedia/commons/7/7a/Alarm_Clock_GIF_Animation_High_Res.gif")
    for i in range(10*60):
        await asyncio.sleep(1)
        if i % 60 == 0 and i != 0:
            await ctx.respond(str(int(i/60)) + " minute⌛ has passed!")
    await ctx.respond("Timer ended!")

@time_group.child
@lightbulb.command('thirty', '30 minute countdown')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    await ctx.respond("Timer for 30 minute⌛ start!")
    await bot.rest.create_message(ctx.channel_id,"https://upload.wikimedia.org/wikipedia/commons/7/7a/Alarm_Clock_GIF_Animation_High_Res.gif")
    for i in range(30*60):
        await asyncio.sleep(1) #30 min
        if i % 300 == 0 and i != 0:
            await ctx.respond(str(int(i/300)) + " minute⌛ has passed!")
    await ctx.respond("Timer ended!")

@bot.command()
@lightbulb.command('timezone', 'Check everyone timezone')
@lightbulb.implements(lightbulb.SlashCommand)
async def timezone(ctx):
    dt_today = datetime.datetime.today()
    dt_Thailand = dt_today.astimezone(pytz.timezone('Asia/Bangkok'))
    dt_UK = dt_today.astimezone(pytz.timezone('Europe/London'))
    dt_Spain = dt_today.astimezone(pytz.timezone('Europe/Madrid'))
    Thailand,UK,Spain = (dt_Thailand.strftime('%H:%M')),(dt_UK.strftime('%H:%M')),(dt_Spain.strftime('%H:%M'))
    await ctx.respond("Thailand time right now is "+Thailand+" 🕑."
                      "\n""UK time right now is "+UK+" 🕑.\n"
                      "Spain time right now is  "+Spain+" 🕑.")

def cell_Update():
    global current_cell,author_message_cell, author_name_cell, cell_position
    current_cell, author_message_cell,author_name_cell,cell_position = 2, {}, {}, {}
    while wks.acell("C"+str(current_cell)).value != None:
        print(current_cell)
        cell_position[int(wks.acell("C" + str(current_cell)).value)] = current_cell
        author_message_cell[int(wks.acell("C" + str(current_cell)).value)] = "B" + str(current_cell)
        author_name_cell[int(wks.acell("C" + str(current_cell)).value)] = "A" + str(current_cell)
        current_cell = current_cell + 1

@bot.listen(hikari.GuildMessageCreateEvent)
async def message_count(event):
    if event.is_bot == False:
        try:
            wks.update(author_message_cell[event.author_id], int(wks.acell(author_message_cell[event.author_id]).value) + 1)
        except:
            wks.update("A" + str(current_cell), str(event.author))
            wks.update("B" + str(current_cell), 1)
            wks.update("C"+str(current_cell),str(event.author_id))
            await asyncio.sleep(5)
            cell_Update()
        if (int(wks.acell("B" + str(cell_position[event.author_id])).value) % 100) == 0:
            await bot.rest.create_message(event.channel_id,
                                          str(wks.acell(author_name_cell[event.author_id]).value)+ " has reach a new milestone of **"
                                          + str(wks.acell(author_message_cell[event.author_id]).value) + "** messages sent!")

@bot.command()
@lightbulb.command('messagecount', 'Check everyone amounts of messages sent')
@lightbulb.implements(lightbulb.SlashCommand)
async def message_count(ctx):
    setence1, setence2, NameArray, MessageCountArray,PercentageArray,MessageCount1,MessageCount2  = [],[],[],[],[],"",""
    await ctx.respond("Current messages count are...")
    for i in range(current_cell - 2):
        NameArray.append("A"+str(i+2))
        MessageCountArray.append("B"+str(i+2))
        PercentageArray.append("D"+str(i+2))
        setence1.append([str(str(wks.acell(NameArray[i]).value) + " has sent **" + str(wks.acell(MessageCountArray[i]).value) + "** messages!")])
        setence2.append([str(str(wks.acell(NameArray[i]).value) + " has contributed to **" + str(wks.acell(PercentageArray[i]).value) + "** of messages sent!")])
        MessageCount1 = (MessageCount1 + str(*setence1[i]) + "\n")
        MessageCount2 = (MessageCount2 + str(*setence2[i]) + "\n")
    await ctx.respond(str(MessageCount1))
    await ctx.respond(str(MessageCount2))
    await ctx.respond("With a total of **" + str(wks.acell("G2").value) + "** messages sent overall in this server!")

@bot.command()
@lightbulb.option("max", "Will roll a dice from 1 to input number")
@lightbulb.command('roll', 'Roll a dice!')
@lightbulb.implements(lightbulb.SlashCommand)
async def dice_roll(ctx: lightbulb.SlashContext) -> None:
    try:
        await ctx.respond("You rolled a 🎲**" + str(random.randint(1, int(ctx.options.max))) + "**!")
    except:
        await ctx.respond("You rolled a 🎲**" + str(random.randint(1,6)) + "**!")

@bot.command()
@lightbulb.command('bkquote', 'I will read out the holy words of BK!')
@lightbulb.implements(lightbulb.SlashCommand)
async def BK_quote(ctx):
    await ctx.respond("I will rehearse the wise word of our cult leader!")
    await ctx.respond(hikari.File(r"C:\Users\satap\PycharmProjects\BK BOT NEW\sermon.jpg"))
    await ctx.respond(str(wks.acell("I"+str(random.randint(2, 9))).value))

@bot.command()
@lightbulb.option("question", "What question you want to ask the cult bot?")
@lightbulb.command('askcultbot', 'Ask cult bot a question and it will answer!')
@lightbulb.implements(lightbulb.SlashCommand)
async def dice_roll(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(
        "Question : " + str(ctx.options.question)
        + "\n" + "Answer : " + str(wks.acell("F" + str(random.randint(2, 23))).value)
                     )

@bot.command()
@lightbulb.command('insult', 'I will read out the holy words of BK!')
@lightbulb.implements(lightbulb.SlashCommand)
async def Insult_Message(ctx):
    await ctx.respond(str(wks.acell("E"+str(random.randint(2, 101))).value))

Card_DictionaryVisible = {2: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\2_of_clubs.png",
                          3: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\3_of_clubs.png",
                          4: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\4_of_clubs.png",
                          5: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\5_of_clubs.png",
                          6: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\6_of_clubs.png",
                          7: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\7_of_clubs.png",
                          8: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\8_of_clubs.png",
                          9: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\9_of_clubs.png",
                          10: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\10_of_clubs.png",
                          11: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\jack_of_clubs.png",
                          12: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\queen_of_clubs.png",
                          13: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\king_of_clubs.png",
                          14: r"C:\Users\satap\PycharmProjects\BK BOT NEW\PNG-cards-1.3\ace_of_clubs.png"}
Card_DictionaryInvisible = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10 ,11:10 ,12:10 ,13:10 ,14:11}

class BlackJackView(miru.View):
    @miru.button(label="Draw", emoji=chr(128220), style=hikari.ButtonStyle.PRIMARY)
    async def Draw_button(self, button: miru.Button, ctx: miru.Context) -> None:
        global CardNo, AceInHand
        Draws = (random.randint(2, 14))
        CardsVisible.append(str(Card_DictionaryVisible[Draws]))
        CardsInvisible.append(int(Card_DictionaryInvisible[Draws]))
        BlackJackTotalInvisible[0] = int(BlackJackTotalInvisible[0])+int(CardsInvisible[CardNo])
        if CardsInvisible[CardNo] == 11:
            AceInHand = True
            if int(BlackJackTotalInvisible[0]) > 21:
                BlackJackTotalInvisible[0] = int(BlackJackTotalInvisible[0]) - 10
                AceInHand = False
        if int(BlackJackTotalInvisible[0]) > 21 and AceInHand == True:
            BlackJackTotalInvisible[0] = int(BlackJackTotalInvisible[0]) - 10
            AceInHand = False
        await bot.rest.create_message(ctx.channel_id, hikari.File(CardsVisible[CardNo]))
        if AceInHand:
            await bot.rest.create_message(ctx.channel_id, "Your total : **" + str(BlackJackTotalInvisible[0]) + "** or **" + str(int(BlackJackTotalInvisible[0]) - 10) + "**")
        else:
            await bot.rest.create_message(ctx.channel_id, "Your total : **" + str(BlackJackTotalInvisible[0]) + "**")

        if int(BlackJackTotalInvisible[0]) > 21:
            await bot.rest.create_message(ctx.channel_id,"Your total exceed **21**, cult bot win!")
            self.stop()
        elif int(BlackJackTotalInvisible[0]) == 21:
            await bot.rest.create_message(ctx.channel_id, "Your total is **21**, you win!")
            self.stop()
        CardNo = CardNo + 1

    @miru.button(label="Pass", emoji=chr(128220), style=hikari.ButtonStyle.PRIMARY)
    async def Pass_button(self, button: miru.Button, ctx: miru.Context) -> None:
        await ctx.respond("You pass!")
        for i in range(2):
            CultBotDraws,CultBotCardNo = random.randint(2, 14), 0
            CultBotCardsVisible.append(str(Card_DictionaryVisible[CultBotDraws]))
            CultBotCardsInvisible.append(int(Card_DictionaryInvisible[CultBotDraws]))
            CultBotCardNo = CultBotCardNo + 1
        if 11 in CultBotCardsInvisible:
            CultbotAceInHand = True
        else:
            CultbotAceInHand = False
        CultBotBlackJackTotalInvisible.append(str(CultBotCardsInvisible[0] + CultBotCardsInvisible[1]))
        await bot.rest.create_message(ctx.channel_id, hikari.File(CultBotCardsVisible[0]))
        await bot.rest.create_message(ctx.channel_id, hikari.File(CultBotCardsVisible[1]))
        if CultbotAceInHand == True and int(CultBotBlackJackTotalInvisible[0]) != 21:
            await bot.rest.create_message(ctx.channel_id, "Cult bot total : **" + str(CultBotBlackJackTotalInvisible[0]) + "** or **" + str(int(CultBotBlackJackTotalInvisible[0]) - 10) + "**")
        else:
            await bot.rest.create_message(ctx.channel_id,"Cult bot total : **" + str(CultBotBlackJackTotalInvisible[0]) + "**")
        while True:
            if int(CultBotBlackJackTotalInvisible[0]) > 21:
                await bot.rest.create_message(ctx.channel_id, "Cult bot total exceed **21**, you win!")
                self.stop()
                break
            elif int(CultBotBlackJackTotalInvisible[0]) > int(BlackJackTotalInvisible[0]):
                await bot.rest.create_message(ctx.channel_id, "Cult  total closer to **21**, Cult bot win!")
                self.stop()
                break
            CultBotAceInHand = False
            CultBotDraws = random.randint(2, 14)
            CultBotCardsVisible.append(str(Card_DictionaryVisible[CultBotDraws]))
            CultBotCardsInvisible.append(int(Card_DictionaryInvisible[CultBotDraws]))
            CultBotCardNo = CultBotCardNo + 1
            CultBotBlackJackTotalInvisible[0] = int(CultBotBlackJackTotalInvisible[0])+int(CultBotCardsInvisible[CultBotCardNo])
            await bot.rest.create_message(ctx.channel_id, hikari.File(CultBotCardsVisible[CultBotCardNo]))
            if CultBotCardsInvisible[CultBotCardNo] == 11:
                CultBotAceInHand = True
                if int(CultBotBlackJackTotalInvisible[0]) > 21:
                    CultBotBlackJackTotalInvisible[0] = int(CultBotBlackJackTotalInvisible[0]) - 10
                    CultBotAceInHand = False
            if int(CultBotBlackJackTotalInvisible[0]) > 21 and CultBotAceInHand == True:
                CultBotBlackJackTotalInvisible[0] = int(CultBotBlackJackTotalInvisible[0]) - 10
                CultBotAceInHand = False
            if CultbotAceInHand == True and int(CultBotBlackJackTotalInvisible[0]) != 21:
                await bot.rest.create_message(ctx.channel_id, "Cult bot total : **" + str(CultBotBlackJackTotalInvisible[0]) + "** or **" + str(int(CultBotBlackJackTotalInvisible[0]) - 10) + "**")
            else:
                await bot.rest.create_message(ctx.channel_id,"Cult bot total : **" + str(CultBotBlackJackTotalInvisible[0]) + "**")

    @miru.button(emoji=chr(9209), style=hikari.ButtonStyle.DANGER, row=2)
    async def Stop_button(self, button: miru.Button, ctx: miru.Context):
        await ctx.respond("Game ended!")
        self.stop()

@bot.command()
@lightbulb.command('blackjack', 'Cult bot will play blackjack with you!')
@lightbulb.implements(lightbulb.SlashCommand)
async def buttons(ctx):
    await ctx.respond("Cult bot will play blackjack with you!")
    global CardsVisible,CardsInvisible,CardNo,BlackJackTotalInvisible,CultBotCardsInvisible,CultBotCardsVisible,CultBotDraws,CultBotBlackJackTotalInvisible,BlackJackTable,AceInHand
    CardsVisible = []
    CardsInvisible = []
    CardNo = 0
    BlackJackTotalInvisible = []
    CultBotCardsInvisible = []
    CultBotCardsVisible = []
    CultBotDraws = 0
    CultBotBlackJackTotalInvisible = []
    AceInHand = False
    for i in range(2):
        Draws = (random.randint(2, 14))
        CardsVisible.append(str(Card_DictionaryVisible[Draws]))
        CardsInvisible.append(int(Card_DictionaryInvisible[Draws]))
        CardNo = CardNo + 1
    if 11 in CardsInvisible:
        AceInHand = True
    BlackJackTotalInvisible.append(str(CardsInvisible[0]+CardsInvisible[1]))
    BlackJackTable = BlackJackView(timeout=60)
    await bot.rest.create_message(ctx.channel_id, hikari.File(CardsVisible[0]))
    await bot.rest.create_message(ctx.channel_id, hikari.File(CardsVisible[1]))
    if AceInHand == True and int(BlackJackTotalInvisible[0]) != 21:
        CultBotResponse = await bot.rest.create_message(ctx.channel_id,"Your total : **"+str(BlackJackTotalInvisible[0])+"** or **"+str(int(BlackJackTotalInvisible[0])-10)+"**" ,components=BlackJackTable.build())
    else:
        CultBotResponse = await bot.rest.create_message(ctx.channel_id, "Your total : **" +str(BlackJackTotalInvisible[0]) + "**"  ,components=BlackJackTable.build())
    if int(BlackJackTotalInvisible[0]) == 21:
        await bot.rest.create_message(ctx.channel_id, "Your total is **21**, you win!")
        BlackJackTable.stop()
    BlackJackTable.start(CultBotResponse)


cell_Update()
miru.load(bot)
bot.run()
