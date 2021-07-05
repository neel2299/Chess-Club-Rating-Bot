import discord
import os
from replit import db
import requests 
import re
from webser import webser
import pandas as pd
def wrong_user(username):
  URL="https://api.chess.com/pub/player/"+username+"/stats"
  r = requests.get(URL) 
  conten=r.content.decode('utf-8')
  if conten=='':
    return 1
  if 1:
    pattern = re.compile(r' not found.')
    matches = pattern.finditer(conten)
    for match in matches:
      return 1
  return 0
      

def rating_finder(rat_type,user):
  URL="https://api.chess.com/pub/player/"+user+"/stats"
  r = requests.get(URL) 
  conten=r.content.decode('utf-8')
  if rat_type == 'tactics':
    pattern = re.compile(r'"tactics":{"h')
    matches = pattern.finditer(conten)
    for match in matches:
      x=match.span()[1]+18
      if(conten[x+3]==','):
        return conten[x:x+3]
      return(conten[x:x+4])
  if rat_type == 'rapid':
    pattern = re.compile(r'chess_rapid')
    matches = pattern.finditer(conten)
    for match in matches:
      x=match.span()[1]+20
      if(conten[x+3]==','):
        return conten[x:x+3]
      return(conten[x:x+4])
  if rat_type == 'blitz':
    pattern = re.compile(r'chess_blitz')
    matches = pattern.finditer(conten)
    for match in matches:
      x=match.span()[1]+20
      if(conten[x+3]==','):
        return conten[x:x+3]
      return(conten[x:x+4])
  if rat_type == 'bullet':
    pattern = re.compile(r'chess_bullet')
    matches = pattern.finditer(conten)
    for match in matches:
      x=match.span()[1]+20
      if(conten[x+3]==','):
        return conten[x:x+3]
      return(conten[x:x+4])
  return '0'

def update_members(username):
  if(wrong_user(username)==1):
    return 0
  if "members" in db.keys():
    members = db["members"]
    members.append(username)
    db["members"] = members
  else:
    db["members"] = [username]
  return 1


def delete_members(username):
  members = db["members"]
  if username in members:
    index=members.index(username)
    del members[index]
    db["members"] = members



def show_data(members,parameter):
  dic = {}
  for member in members:
    dic[member]=[int(rating_finder(parameter, member))]
  df = pd.DataFrame(dic)
  df.loc['Rank'] = df.loc[0].rank(ascending=False,method='min')
  df.sort_values(0, inplace = True, axis=1,ascending=False) 
  df=df.rename(index={0: "Rating"})
  dictd=df.to_dict()
  x="Rank"
  y="Name"
  z="Rating"
  msg=""
  msg=msg+f"{x:{20}} {y:{20}} {z:{20}}"+"\n"
  for key in dictd.keys():
    x=str(int(dictd[key]["Rating"]))
    y=str(int(dictd[key]["Rank"]))
    msg=msg+f"{y:{20}} {key:{20}} {x:{4}}"+"\n"
  return msg



def show_data1(members,parameter):
  dic = {}
  for member in members:
    dic[member]=int(rating_finder(parameter, member))
  rat_list = sorted(dic.values(),reverse=True)
  bigdic = {}
  for i in rat_list:
    for k in dic.keys():
        if dic[k] == i:
            bigdic[k] = dic[k]
            break

  k=1
  msg=''
  for i in bigdic:
    msg=msg+str(k)+2*"\t"+i#+"\t"+str(bigdic[i])+"\n"
    if(20-len(str(i))>0):
      msg=msg+(20-len(str(i)))*' '
    k=k+1
    msg=msg+str(bigdic[i])+"\n"
  return msg


members_starter=['vedantttt','ID_15','pawn_222','neelk22','XREVERBX']
client=discord.Client()


@client.event
async def on_ready():
  print('Hi there, this is{0.user}'.format(client) )
@client.event
async def on_message(message):
  if message.author==client.user:
    return
  msg = message.content
  if msg.startswith('$show'):
    parameter = msg.split("$show ",1)[1]
    members_all=db["members"]+members_starter
    if parameter=='rapid' or parameter=='blitz' or parameter=='bullet' or parameter=='tactics':
      out_msg = show_data(members_all, parameter)
      await message.channel.send(out_msg)
    else:
      await message.channel.send('Check command')
  if msg.startswith("$add"):
    username = msg.split("$add ",1)[1]
    members_all=db["members"]+members_starter
    if username not in members_all:
      x=update_members(username)
      if(x==1):
        await message.channel.send("New username added.")
      elif(x==0):
        await message.channel.send("Check your username.")
    else:
      await message.channel.send("Username already added.")
  if msg.startswith("$remove"):
    username = msg.split("$remove ",1)[1]
    delete_members(username)
    await message.channel.send("Username removed.")
webser()
client.run(os.getenv('TOKEN'))