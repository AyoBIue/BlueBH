import requests
import discord
from datetime import datetime, timedelta
from discord.ext import commands
import os
import asyncio

BKey = os.environ.get("KEY")

def GrabThumbnail(rank):
  if rank.startswith('Diamond'):
    return 'https://cdn.discordapp.com/attachments/676799653844353025/796587901101801562/Avatar_Diamond_1.png'
  elif rank.startswith('Platinum'):
    return 'https://cdn.discordapp.com/attachments/676799653844353025/796587899575205888/Avatar_Platinum_1.png'
  elif rank.startswith('Gold'):
    return 'https://cdn.discordapp.com/attachments/676799653844353025/796587898152419368/Avatar_Gold_1.png'
  elif rank.startswith('Silver'):
    return 'https://cdn.discordapp.com/attachments/676799653844353025/796587896681267200/Avatar_Participation_1.png'
  else:
    return 'https://cdn.discordapp.com/attachments/676799653844353025/796587896681267200/Avatar_Participation_1.png'

def FindPlayer(args, x):
  Name = None
  Level = None
  Region = None
  Clan = None

  Elo = None
  Tier = None
  Games = None
  Url = None
  Rank = None
  ID = None

  TeamName = None
  V2Rating = None
  V2Games = None
  V2Tier = None
  V2Rank = None


  link = requests.get(f'https://api.brawlhalla.com/rankings/1v1/all/1?name={args}&api_key={BKey}')
  if str(link.json()) == '[]':
    return False
  else:
    if type(link.json()) == list:
      try:
        ID = link.json()[x]['brawlhalla_id']
        Name = link.json()[x]['name']
        Region = link.json()[x]['region']
        Tier = link.json()[x]['tier']
        Rank = link.json()[x]['rank']
        Url = GrabThumbnail(Tier)
        Peak = link.json()[x]['peak_rating']
        Now = link.json()[x]['rating']
        Elo = f'{Now} / {Peak}'

        Wins = link.json()[x]['wins']
        Max = link.json()[x]['games']
        Max = int(Max) - int(Wins)

        Games = f'{Wins} - {Max}'

        clan = requests.get(f'https://api.brawlhalla.com/player/{ID}/stats?api_key={BKey}')
        ClanJson = clan.json()
        Level = ClanJson['level']
        Clan = ClanJson['clan']['clan_name']
      except KeyError:
        print("Key Error")
        Clan = 'Could not find a clan.'
      except IndexError:
        print("Index Error")

      try:
        v2 = requests.get(f'https://api.brawlhalla.com/player/{ID}/ranked?api_key={BKey}')
        v2 = v2.json()
        v2 = v2['2v2'][0]
        TeamName = v2['teamname']
        V2Rank = v2['global_rank']
        V2Tier = v2['tier']
        V2Losses = int(v2['games']) - int(v2['wins'])
        V2Wins = int(v2['wins'])
        V2Games = f'{V2Wins} - {V2Losses}'
        V20Rate = v2['rating']
        V20Peak = v2['peak_rating']

        V2Rating = f'{V20Rate} / {V20Peak}'
      except KeyError:
        pass
      except IndexError:
        pass

      Main = {
        'name': Name,
        'level': Level,
        'region': Region,
        'clan': Clan,
        'elo': Elo,
        'tier': Tier,
        'games': Games,
        'url': Url,
        'rank': Rank,
        'teamname': TeamName,
        'v2rating': V2Rating,
        'v2games': V2Games,
        'v2tier': V2Tier,
        'v2rank': V2Rank

      }

      return Main
    else:
      return False

class Brawlhalla(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def rank(self, ctx, *, args=None):
    x = 0
    if not args:
      await ctx.send("Please provide a username.")
    else:
      Value = FindPlayer(args, 0)
      if Value:
        Name = Value['name']
        Level = Value['level']
        Region = Value['region']
        Clan = Value['clan']

        Elo = Value['elo']
        Tier = Value['tier']
        Games = Value['games']
        Url = Value['url']
        Rank = Value['rank']

        TeamName = Value['teamname']
        V2Rank = Value['v2rank']
        V2Games = Value['v2games']
        V2Tier = Value['v2tier']
        V2Rating = Value['v2rating']

        embed = discord.Embed(
          title = 'Player Information',
          colour = ctx.author.color,
          timestamp = datetime.now()
        )
        embed.add_field(name='Name', value=f'{Name}')
        embed.add_field(name='Level', value=f'{Level}')
        embed.add_field(name='Clan', value=f'{Clan}')
        embed.add_field(name='Region', value=f'{Region}', inline=False)
        embed.add_field(name='1v1 Information', value=f'**Tier:** {Tier}\n**Elo:** {Elo}\n**Games:** {Games}\n**Global Rank:** {Rank}')
        if not TeamName:
          embed.add_field(name='2v2 Information', value='**Not 2v2 information found..**')
        else:
          embed.add_field(name='2v2 Information', value=f'**Team Name:** {TeamName}\n**Elo:** {V2Rating}\n**Games:** {V2Games}\n**Global Rank:** {V2Rank}')
        embed.set_thumbnail(url=ctx.guild.icon_url)

        lol = await ctx.send(embed=embed)
        await lol.add_reaction('➡️')

        while True:
          def check(reaction, user):
            return user == ctx.author and str(reaction.emoji)
          try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
          except asyncio.TimeoutError:
            try:
              await lol.delete()
              return
            except:
              return
          else:
            await lol.clear_reactions()
            if str(reaction) == '⬅️':
              if x == 0:
                pass
              else:
                x -= 1
                Value = FindPlayer(args, x)
                if not Value:
                  pass
                else:
                  Name = Value['name']
                  Region = Value['region']

                  Tier = Value['tier']
                  Elo = Value['elo']
                  Games = Value['games']
                  Rank = Value['rank']
                  Url = Value['url']

                  TeamName = Value['teamname']
                  V2Rank = Value['v2rank']
                  V2Games = Value['v2games']
                  V2Tier = Value['v2tier']
                  V2Rating = Value['v2rating']

                  embed = discord.Embed(
                    title = 'Player Information',
                    colour = ctx.author.color,
                    timestamp = datetime.now()
                  )
                  embed.add_field(name='Name', value=f'{Name}')
                  embed.add_field(name='Level', value=f'{Level}')
                  embed.add_field(name='Region', value=f'{Region}')
                  embed.add_field(name='Clan', value=f'{Clan}')
                  embed.add_field(name='1v1 Information', value=f'**Tier:** {Tier}\n**Elo:** {Elo}\n**Games:** {Games}\n**Global Rank:** {Rank}')
                  if not TeamName:
                    embed.add_field(name='2v2 Information', value='**Not 2v2 information found..**')
                  else:
                    embed.add_field(name='2v2 Information', value=f'**Team Name:** {TeamName}\n**Elo:** {V2Rating}\n**Games:** {V2Games}\n**Global Rank:** {V2Rank}')
                  embed.set_thumbnail(url=ctx.guild.icon_url)

                  await lol.edit(embed=embed)

                  await asyncio.sleep(1)
            elif str(reaction) == '➡️':
              if (x + 1) >= len(Value):
                pass
              else:
                x += 1
                Value = FindPlayer(args, x)
                if not Value:
                  pass
                else:
                  Name = Value['name']
                  Region = Value['region']

                  Tier = Value['tier']
                  Elo = Value['elo']
                  Games = Value['games']
                  Rank = Value['rank']
                  Url = Value['url']

                  TeamName = Value['teamname']
                  V2Rank = Value['v2rank']
                  V2Games = Value['v2games']
                  V2Tier = Value['v2tier']
                  V2Rating = Value['v2rating']

                  embed = discord.Embed(
                    title = 'Player Information',
                    colour = ctx.author.color,
                    timestamp = datetime.now()
                  )
                  embed.add_field(name='Name', value=f'{Name}')
                  embed.add_field(name='Level', value=f'{Level}')
                  embed.add_field(name='Region', value=f'{Region}')
                  embed.add_field(name='Clan', value=f'{Clan}')
                  embed.add_field(name='1v1 Information', value=f'**Tier:** {Tier}\n**Elo:** {Elo}\n**Games:** {Games}\n**Global Rank:** {Rank}')
                  if not TeamName:
                    embed.add_field(name='2v2 Information', value='**Not 2v2 information found..**')
                  else:
                    embed.add_field(name='2v2 Information', value=f'**Team Name:** {TeamName}\n**Elo:** {V2Rating}\n**Games:** {V2Games}\n**Global Rank:** {V2Rank}')
                  embed.set_thumbnail(url=ctx.guild.icon_url)

                  await lol.edit(embed=embed)

                  await asyncio.sleep(1)
            else:
              pass


            if x >= 1:
              await lol.add_reaction('⬅️')
            if (x + 1) <= len(Value):
              await lol.add_reaction('➡️')

def setup(bot):
  bot.add_cog(Brawlhalla(bot))
