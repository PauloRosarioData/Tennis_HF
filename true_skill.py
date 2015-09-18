# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 18:39:56 2015

@author: paulorosario
"""
from __future__ import print_function
import pandas as pd
import numpy as np
import datetime
import trueskill

print ("hello")

all_data = pd.read_csv('tennisdatabase.csv')
all_data = all_data.sort(['date'], ascending=[0])
all_data = all_data.reindex(index = np.arange(1, len(all_data) + 1))
all_data['winner_elo'] = 0
all_data['loser_elo'] = 0
all_data['winner_XP'] = 0.0
all_data['loser_XP'] = 0.0
all_data['winner_games'] = 0
all_data['loser_games'] = 0

print ("goodbye")

#creates a database of players

playerdatabase = pd.DataFrame()
list_winners = pd.pivot_table(all_data,index=["winner_name"],values=["tourney_id"],aggfunc=np.count_nonzero)
list_losers =  pd.pivot_table(all_data,index=["loser_name"],values=["tourney_id"],aggfunc=np.count_nonzero)
firstloss =  pd.pivot_table(all_data,index=["loser_name"],values=["date"],aggfunc=np.min)
firstwin =  pd.pivot_table(all_data,index=["winner_name"],values=["date"],aggfunc=np.min)
playerdatabase = pd.concat([list_winners, list_losers, firstloss, firstwin], axis=1)
playerdatabase['NumberOfGames'] = 0
playerdatabase['name']=playerdatabase.index
playerdatabase['mu'] = 0
playerdatabase['sigma'] = 0

mudatabase = playerdatabase
sigmadatabase = playerdatabase

print (3)


# The objects we pass to AdjustPlayers can be anything with skill and
# rank attributes.  We'll create a simple Player class that has
# nothing else.

class Player(object):
  pass

# Create the players.  Assign each of them the default skill.  
# sets a default skill (mu) and sigma


print (4)

pd = playerdatabase[["name", 'NumberOfGames',]].values

for i in xrange(0, len(pd)-1):
    pd[i][0] = Player()
    pd[i][0].skill = (25.0, 25.0/3.0)

print ("before the loop")



#creates a list of individual winners and losers
ir = all_data[["winner_name", "loser_name", 'winner_XP', 'loser_XP', 'winner_elo', 'loser_elo', 'winner_games', 'loser_games']].values


#for i in xrange(0, len(all_data)-1):
for i in xrange(0, len(all_data)-1):
    w = ir[i][0]
    l = ir[i][1]


    wilocation = playerdatabase.index.get_loc(w)
    llocation = playerdatabase.index.get_loc(l)

    #sets the winner and loser, the lowest score wins. The numbers dont matter.
    try:
        pd[wilocation][0].rank =1
        pd[llocation][0].rank =2
    except AttributeError:
        continue

    if i%5000 == 0:
        print ("loop 1")
        print (datetime.datetime.utcnow())


    #gets the adjusted rating for both players
    trueskill.AdjustPlayers([pd[wilocation][0], pd[llocation][0]])

    if i%5000 == 0:
        print ("loop2")
        print (datetime.datetime.utcnow())



    #updates the mu in the database
    playerdatabase.ix[w, 'mu'] = pd[wilocation][0].skill[0]
    playerdatabase.ix[l, 'mu'] = pd[llocation][0].skill[0]

    #updates the sigmain the database
    playerdatabase.ix[w, 'sigma'] = pd[wilocation][0].skill[1]
    playerdatabase.ix[l, 'sigma'] = pd[llocation][0].skill[1]


    if i%5000 == 0:
        print ("loop8")
        print (datetime.datetime.utcnow())

    if i%5000 == 0:
        print ("loop10")
        print (datetime.datetime.utcnow())

    if i%500==0:
        print (i/(len(all_data)-1.0))

    if i%5000==0:
        mudatabase = mudatabase.sort(['mu'], ascending=[1])
        sigmadatabase = sigmadatabase.sort(['mu'], ascending=[1])
        mudatabase.to_csv('ATPmu.csv')
        sigmadatabase.to_csv('ATPsigma.csv')
        #EXPORT IR TO CSV!!!
        print ("backup")





mudatabase = mudatabase.sort(['mu'], ascending=[1])
sigmadatabase = sigmadatabase.sort(['mu'], ascending=[1])
mudatabase.to_csv('ATPmu.csv')
sigmadatabase.to_csv('ATPsigma.csv')
#EXPORT IR TO CSV!!!
print ("backup")
#EXPORT IR TO CSV!!!
print ("alibaba")
