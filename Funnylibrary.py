import requests 
import re
rat_type='rapid'
user='neelk22'
def rating_finder(rat_type,user):
  URL="https://api.chess.com/pub/player/"+user+"/stats"
  r = requests.get(URL) 
  conten=r.content.decode('utf-8')
  if rat_type == 'rapid':
    pattern = re.compile(r'chess_rapid')
    matches = pattern.finditer(conten)
    for match in matches:
      x=match.span()[1]+20
      return(conten[x:x+4])
  if rat_type == 'blitz':
    pattern = re.compile(r'chess_blitz')
    matches = pattern.finditer(conten)
    for match in matches:
      x=match.span()[1]+20
      return(conten[x:x+4])
  if rat_type == 'bullet':
    pattern = re.compile(r'chess_bullet')
    matches = pattern.finditer(conten)
    for match in matches:
      x=match.span()[1]+20
      return(conten[x:x+4])
  return '0'



  
