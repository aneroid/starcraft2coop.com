#!/usr/bin/env python

import os
import mpyq
import time
import json
from s2protocol import versions

replayFolder = r"K:\SC2Coop Resources\Replay Data Summarizer\test"
playerName = "Aommaster"

replayList = [f for f in os.listdir(replayFolder) if f.endswith('.SC2Replay')]
totalFiles= len(replayList)

parsedData = ["Date Played\tMap\tCommander\tLevel\tAlly Commander\tAlly Level\tGame Type\tResult\tGame Length"]
coopMaps = ["Chain of Ascension","Cradle of Death","Dead of Night","Lock & Load","Malwarfare","Miner Evacuation","Mist Opportunities","Oblivion Express","Part and Parcel","Rifts to Korhal","Scythe of Amon","Temple of the Past","The Vermillion Problem","Void Launch","Void Thrashing"]
count = 0
for replayFile in replayList:
    replay= replayFolder + os.sep + replayFile
    datePlayed= time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(replay)))
    
    try:
        archive = mpyq.MPQArchive(replay)
    except:
        continue
    contents = archive.header['user_data_header']['content']
    header = versions.latest().decode_replay_header(contents)
    baseBuild = header['m_version']['m_baseBuild']
    gameLoops = header['m_elapsedGameLoops']
    gameTime = gameLoops/16
    protocol = versions.build(baseBuild)

    contents = archive.read_file("replay.initData")
    initData = protocol.decode_replay_initdata(contents)

    p1Commander = initData["m_syncLobbyState"]["m_lobbyState"]["m_slots"][0]["m_commander"]
    p1Level = initData["m_syncLobbyState"]["m_lobbyState"]["m_slots"][0]["m_commanderMasteryLevel"]
    p2Commander = initData["m_syncLobbyState"]["m_lobbyState"]["m_slots"][1]["m_commander"]
    p2Level = initData["m_syncLobbyState"]["m_lobbyState"]["m_slots"][1]["m_commanderMasteryLevel"]

    mutatorGame = initData["m_syncLobbyState"]["m_gameDescription"]["m_hasExtensionMod"]
    if mutatorGame == 1:
        mutatorGame = "Mutators"
    else:
        mutatorGame = "Standard"
    
    contents = archive.read_file("replay.details")
    details = protocol.decode_replay_details(contents)

    mapName = details["m_title"]

    if mapName not in coopMaps:
        continue

    if details["m_playerList"][0]["m_name"] == playerName:
        result = details["m_playerList"][0]["m_result"]
        myCommander = p1Commander
        myLevel = p1Level
        otherCommander = p2Commander
        otherLevel = p2Level
    else:
        result = details["m_playerList"][1]["m_result"]
        myCommander = p2Commander
        myLevel = p2Level
        otherCommander = p1Commander
        otherLevel = p1Level

    if result == 1:
        result = "Win"
    else:
        result = "Lose"

    parsedData.append(datePlayed + "\t" + mapName + "\t" + myCommander + "\t" + str(myLevel) + "\t" + otherCommander + "\t" + str(otherLevel) + "\t" +mutatorGame + "\t" + result + "\t" + str(gameTime))
with open('output.txt', 'w') as f:
    for item in parsedData:
        f.write("%s\n" % item)
