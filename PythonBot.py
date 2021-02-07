import discord
from discord.ext import commands
import random

app = commands.Bot(command_prefix='PBOT')

token = "ODA3ODU4MzU2OTczNzMxOTAw.YB-GuQ.7ox70ZbFzPpjU4IFg3RkdPpG-qc"
calcResult = 0

@app.event
async def on_ready():
    print("다음으로 로그인합니다 : ")
    print(app.user.name)
    print(app.user.id)
    print("==========")
    game = discord.Game("PBOT도움말을 이용하여 명령어를 알아내세요!")
    await app.change_presence(status=discord.Status.online, activity=game)

@app.command(pass_context=True)
async def randomNum(ctx, num1, num2):
    picked = random.randint(int(num1), int(num2))
    await ctx.send('뽑힌 숫자는 : '+str(picked))

@app.event
async def on_message(message):
    await app.process_commands(message)
    if message.content.startswith("PBOT1부터10"):
        for x in range(10):
            await message.channel.send(x+1)
    if message.content.startswith("PBOT계산"):
        global calcResult
        param = message.content.split()
        try:
            if param[1].startswith("더하기"):
                calcResult = int(param[2])+int(param[3])
                await message.channel.send("Result : "+str(calcResult))
            if param[1].startswith("빼기"):
                calcResult = int(param[2])-int(param[3])
                await message.channel.send("Result : "+str(calcResult))
            if param[1].startswith("곱하기"):
                calcResult = int(param[2])*int(param[3])
                await message.channel.send("Result : "+str(calcResult))
            if param[1].startswith("나누기"):
                calcResult = int(param[2])/int(param[3])
                await message.channel.send("Result : "+str(calcResult))
        except IndexError:
            await message.channel.send("무슨 숫자를 계산할지 알려주세요.")
        except ValueError:
            await message.channel.send("숫자로 넣어주세요.")
        except ZeroDivisionError:
            await message.channel.send("You can't divide with 0.")
    if message.content.startswith("PBOT도움말"):
        embed=discord.Embed(title="파이썬", description="제작자:개쟁", color=0x00ff56)
        embed.set_author(name="도움말", url="https://www.python.org/static/img/python-logo.png", icon_url="https://www.python.org/static/img/python-logo.png")
        embed.set_thumbnail(url="https://www.python.org/static/img/python-logo.png")
        embed.add_field(name="제작자의 유튜브", value="https://www.youtube.com/channel/UCD8T-_IFHHoO-JAvghn3rIg", inline=True)
        embed.add_field(name="제작자의 카페", value="https://cafe.naver.com/gaejaeng", inline=True)
        embed.add_field(name="명령어", value="https://cafe.naver.com/gaejaeng/2", inline=True)
        embed.set_footer(text="앞으로 더 많은 기능이 생길 예정이니 기다려달라구~")
        await message.channel.send(embed=embed)
        if message.content == "가위" or message.content == "바위" or message.content == "보":
            bot_response = random.randint(1, 3)
            if bot_response == 1:
                if message.content == "가위":
                    await message.channel.send("가위 비겼네요")
                elif message.content == "바위":
                    await message.channel.send("가위 제가 졌네요")
                elif message.content == "보":
                    await message.channel.send("가위 제가 이겼네요")
            elif bot_response == 2:
                if message.content == "가위":
                    await message.channel.send("바위 제가 이겼네요")
                elif message.content == "바위":
                    await message.channel.send("바위 비겼네요")
                elif message.content == "보":
                    await message.channel.send("바위 제가 졌네요")
            elif bot_response == 3:
                if message.content == "가위":
                    await message.channel.send("보 제가 졌네요")
                elif message.content == "바위":
                    await message.channel.send("보 제가 이겼네요")
                elif message.content == "보":
                    await message.channel.send("보 비겼네요")

@app.command(name="추방", pass_context=True)
async def _kick(ctx, *, user_name: discord.Member, reason=None):
    await user_name.kick(reason=reason)
    await ctx.send(str(user_name)+"을(를) 추방하였습니다.")
@commands.has_permissions(administrator=True)

@app.command(name="밴", pass_context=True)
async def _ban(ctx, *, user_name: discord.Member):
    await user_name.ban()
    await ctx.send(str(user_name)+"을(를) 영원히 매장시켰습니다.")
@commands.has_any_role("Commander")

@app.command(name="언밴", pass_context=True)
async def _unban(ctx, *, user_name):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = user_name.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention}을(를) 회생시켰습니다.")
            return

@app.command(name="참가", pass_context=True)
async def _join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("채널에 연결되지 않았습니다.")

@app.command(name="연결끊기")
async def _leave(ctx):
    await app.voice_clients[0].disconnect()

    @app.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("값이 없네요.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("값이 다릅니다.")
        else:
            embed = discord.Embed(title="오류!!", description="오류가 발생했습니다.", color=0xFF0000)
            embed.add_field(name="상세", value=f"```{error}```")
            await ctx.send(embed=embed)
app.run(token)