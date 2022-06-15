import requests
import json
import time
from urllib.request import urlopen
from urllib.request import Request
import urllib
import xml.etree.ElementTree as ET
import csv
import profile
import plotly.plotly as py
import plotly.graph_objs as go


# All function calls
def main():
    steam_key = 'B1A67A938E1F9E6BFFE3CEA16E5F6079'
    filename = 'games.txt'
    idList = steamGetIDs(steam_key)                             # format: a list of ids
    topGames = readTopGames(filename)                           # format: dict[AppID] = Game
    ignRatings = getRatingsIGN(topGames)
    gamesdict = steamGetGames(idList, steam_key, topGames)      # format: dict[SteamProfileID] = AppID, game, playtime
    playtime = averagePlayTimePerGame(gamesdict, topGames)
    readydict = joinAvgScore(playtime,ignRatings)
    graphPlotly(readydict)

# This function uses the Steam API to create a group of profiles to scrape game information from. The API returns in
# XML. The function uses ElementTree to parse the XML and then returns a list of the profile IDs.
def steamGetIDs(steam_key):
    request_url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=' + steam_key + \
                  '&steamid=76561198023414915&relationship=friend&format=xml'

    response = urlopen(request_url)
    userList = response.read()
    userList = userList.decode("utf8")
    userList = str(userList)

    # print(userList)

    root = ET.fromstring(userList)
    steamid_list = []

    for i in range (0, 396):
        steamid = root[0][i][0].text
        steamid_list.append(steamid)

    print("Done with ID scrape, total IDs:", len(steamid_list))
    return(steamid_list)


# This function reads games and their corresponding Steam IDs from a tab-delimited file into a dictionary.
def readTopGames(filename):
    readgames = {}
    with open(filename, 'r', newline='') as input_file:
        game_reader = csv.DictReader(input_file, delimiter='\t')

        for row in game_reader:
            readgames[row['AppID']] = row['Game']

    print("Top games read, total: ", len(readgames))
    return(readgames)

# This function calls the IGN API (through Mashape) and searches for the games in the dict returned from the previous
# function, then parses the returned JSON to get the score for each game. The function returns a dictionary of games
# and ratings.
def getRatingsIGN(topGames):
    ratingList = {}
    for game in topGames:
        request_url = 'https://videogamesrating.p.mashape.com/get.php?count=1&game=' + topGames[game].replace(' ', '+')
        req = Request(request_url)
        req.add_header("X-Mashape-Key", "5qRM6p89aJmshODnN0iC8R3uI4s1p1Zrrsjjsn3drmIOO8PTjT")
        ignList = urlopen(req)
        ignList = str(ignList.read().decode("utf8"))

        newList = ignList.replace("[", "")
        newNew = newList.replace("]","")
        ignList = newNew

        ignList = json.loads(ignList)
        ratingList[topGames[game]] = ignList['score']

    print("Ratings completed, total:", len(ratingList), ratingList)
    return(ratingList)

# This function calls the Steam API with each ID gathered from a previous step, and looks at all the games that profile
# owns. The function only looks at profiles that are public, and only looks at games that are in the previously gotten
# list and games that have playtime. The function returns a dictionary of profile IDs with game information (AppID,
# name, and playtime)
def steamGetGames(steamIDList,steam_key,topgames):
    user_games_dict = {}
    for id in steamIDList:
        request_url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + steam_key + \
                      '&steamid='+ id +'&include_appinfo=1&format=xml'

        response = urlopen(request_url)
        gamesList = response.read()
        gamesList = gamesList.decode("utf8")
        gamesList = str(gamesList)

        root = ET.fromstring(gamesList)

        gameStats = []

        if root.getchildren():
            number = root[0].text
            number = int(number)


            for game in range(0, number):
                gameID = root[1][game][0].text
                gameName = root[1][game][1].text
                gameTime = root[1][game][2].text
                gameTime = int(gameTime)
                if gameID is not None and gameTime is not 0 and gameID in topgames:
                    gameStats.append((gameID, gameName, gameTime))
        if gameStats:
            user_games_dict[id] = gameStats
            print(gameStats, len(user_games_dict))

        time.sleep(5)

    #print(user_games_dict)
    print("Profiles gotten, total:", len(user_games_dict))
    return(user_games_dict)

#This function calculates the average playtime for each game and returns a dict with the game and average.
def averagePlayTimePerGame(gamestats, topgames):
    playtimeAverage = {}

    halflife = []
    halflife2 = []
    darksouls = []
    portal = []
    portal2 = []
    masseffect2 = []
    thewitcher3 = []
    dishonored = []
    grandtheftauto = []
    skyrim = []
    kerbal = []
    bioshock = []
    civ = []
    left4dead2 = []
    csgo = []
    fallout4 = []
    terraria = []
    bioshockinfinite = []
    fez = []
    falloutnv = []

    for entry in gamestats:
        for game in gamestats[entry]:
            if game[1] == "Half-Life":
                halflife.append(game[2])
            if game[1] == "Half-Life 2":
                halflife2.append(game[2])
            if game[1] == "Dark Souls: Prepare to Die Edition":
                darksouls.append(game[2])
            if game[1] == "Portal":
                portal.append(game[2])
            if game[1] == "Portal 2":
                portal2.append(game[2])
            if game[1] == "Mass Effect 2":
                masseffect2.append(game[2])
            if game[1] == "The Witcher 3: Wild Hunt":
                thewitcher3.append(game[2])
            if game[1] == "Dishonored":
                dishonored.append(game[2])
            if game[1] == "Grand Theft Auto V":
                grandtheftauto.append(game[2])
            if game[1] == "The Elder Scrolls V: Skyrim":
                skyrim.append(game[2])
            if game[1] == "Kerbal Space Program":
                kerbal.append(game[2])
            if game[1] == "BioShock":
                bioshock.append(game[2])
            if game[1] == "Sid Meier's Civilization V":
                civ.append(game[2])
            if game[1] == "Left 4 Dead 2":
                left4dead2.append(game[2])
            if game[1] == "Counter-Strike: Global Offensive":
                csgo.append(game[2])
            if game[1] == "Fallout 4":
                fallout4.append(game[2])
            if game[1] == "Terraria":
                terraria.append(game[2])
            if game[1] == "BioShock Infinite":
                bioshockinfinite.append(game[2])
            if game[1] == "FEZ":
                fez.append(game[2])
            if game[1] == "Fallout: New Vegas":
                falloutnv.append(game[2])

    playtimeAverage['Half-Life'] = (sum(halflife)/len(halflife))
    playtimeAverage['Half-Life 2'] = (sum(halflife2)/len(halflife2))
    playtimeAverage['Dark Souls: Prepare to Die Edition'] = (sum(darksouls)/len(darksouls))
    playtimeAverage['Portal'] = (sum(darksouls)/len(darksouls))
    playtimeAverage['Portal 2'] = (sum(portal2)/len(portal2))
    playtimeAverage['Mass Effect 2'] = (sum(masseffect2)/len(masseffect2))
    playtimeAverage['The Witcher 3: Wild Hunt'] = (sum(thewitcher3)/len(thewitcher3))
    playtimeAverage['Dishonored'] = sum(dishonored)/len(darksouls)
    playtimeAverage['Grand Theft Auto V'] = sum(grandtheftauto)/len(grandtheftauto)
    playtimeAverage['The Elder Scrolls V: Skyrim'] = sum(skyrim)/len(skyrim)
    playtimeAverage['Kerbal Space Program'] = sum(kerbal)/len(kerbal)
    playtimeAverage['BioShock'] = sum(bioshock)/len(bioshock)
    playtimeAverage['Sid Meiers Civilization V'] = sum(civ)/len(civ)
    playtimeAverage['Left 4 Dead 2'] = sum(left4dead2)/len(left4dead2)
    playtimeAverage['Counter-Strike: Global Offensive'] = sum(csgo)/len(csgo)
    playtimeAverage['Fallout 4'] = sum(fallout4)/len(fallout4)
    playtimeAverage['Terraria'] = sum(terraria)/len(terraria)
    playtimeAverage['BioShock Infinite'] = sum(bioshockinfinite)/len(bioshockinfinite)
    playtimeAverage['FEZ'] = sum(fez)/len(fez)
    playtimeAverage['Fallout: New Vegas'] = sum(falloutnv)/len(falloutnv)

    for game in playtimeAverage:
        playtimeAverage[game] = round(playtimeAverage[game], 1)

    print("Averages calculated, total:", len(playtimeAverage))
    return(playtimeAverage)

#This function creates one dictionary out of two, from the dict containing the ratings and the dict containing
# the scores.
def joinAvgScore(playtimeAverage, ratings):
    joined = {}
    for game in ratings:
        if game in playtimeAverage:
            joined[game] = (ratings[game], playtimeAverage[game])

    return(joined)

# This function formats the dict from the previous function so Plotly can use the information and form a scatter plot.
def graphPlotly(scores):
    print(scores)
    xaxis = []
    yaxis = []
    for game in scores:
        print(scores[game])
        xaxis.append(scores[game][0])
        yaxis.append(scores[game][1])

    print(xaxis, yaxis)
    trace = go.Scatter(
        x = xaxis,
        y = yaxis,
        mode = 'markers'
    )

    data = [trace]
    plot_url = py.plot(data, filename='timeAndScores')

if __name__=='__main__':
    main()