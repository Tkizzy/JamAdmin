import pexpect
from pexpect import *

debugA = False

#welcomeScreen = "type 'help' to have a list of available commands"
#listCommand = "!list"

def telnetLogin(namer,passer):
	myUserName = namer
	myPassword = passer
	welcomeScreen = "type 'help' to have a list of available commands"
	global child
	try:
		child = pexpect.spawn("telnet 64.94.100.200 30300")
		child.expect ("user id :")
		child.sendline(myUserName)
		child.expect("password",timeout = .5)
		child.sendline(myPassword)
		child.expect(welcomeScreen,timeout = .5)
	except:
		print "TELNET LOGIN ERROR, TIMEOUT!!!"
		child.close()
		return "Failure"
	print "Telnet Logged in"
	return "Success"

def turnChatOff():
	print "turning telnet game chat off"
	chatOffString = "/chat off" 
	child.sendline(chatOffString)
	child.expect("You won't see players' chat anymore")
	#turnChatOffData = (child.read_nonblocking(size=1000,timeout=100))
	#print ">>>"+str(turnChatOffData)

def quitTelnet():
	quitString = "/quit"
	try:
		child.sendline(quitString)
	except:
		pass
	child.close()
	print "TELNET QUITTED!!! YESSIR!"


print "\n\n"
if debugA==True:
	telnetLogin("NEEDSPASS")
	turnChatOff()

slotNumber = 6


print "\n\n"

def getConnections(slot):
	clientInfoString = "!clientinfo "+str(slot)+" connections"
	child.sendline(clientInfoString)
	child.expect(clientInfoString)
	
	try:
		clientInfoData = (child.read_nonblocking(size=1000,timeout=5))
	except:
		clientInfoData = "PlayerERROR: connections is 9999"

	print ">>>>>>>><><><><>CLIENT INFODATA:"
	print clientInfoData
	return clientInfoData

def getList():
	#prints out a single string of the list of players.
	listCommandString = "!list"
	child.sendline(listCommandString)
	child.expect(listCommandString)
	listData = (child.read_nonblocking(size=1000, timeout=100))
	#print listData
	return listData

def ParseList():
	playerListString =getList()# "mileu [20], jomaniz [21], gerazee [22], fazee [23], Rahil [3], CPU [2], Kilo [5], P GAY PRINCES [4], whj [6], Myzamir [9], BenyP [8], Dudson [10], meayyam [13], a rainbow pony [12], hehe [15], ryskelt [14], dogs [17], BLOODS [16], mike [19], Spraitas_LT [18]"
	#getList()
	deCommad = playerListString.split(",")
	print deCommad

	playerList = dict([])
	playerSlotArray = []

	for each in deCommad:
		
		#lastBracketIndex = each.rfind("]")
		#secondToLastBracketIndex = each.rfind("[")
		#firstBracket = each.split(secondToLastBracketIndex)
		#print firstBracket


		#print lastBracketIndex," ",secondToLastBracketIndex
		#print"..."
		if "]" in each:
			firstBracket = each.rsplit("]",1)
			secondBracket = firstBracket[0].rsplit(" [",1)
			print firstBracket
			print secondBracket
			playerName = str(secondBracket[0].strip())
			playerSlot = int(secondBracket[1])
			print secondBracket
			#slot = str(playerSlot.strip())
			#rrprint slot
			print playerName
			playerSlotArray.append(playerSlot)
			playerList[playerSlot]=playerName
			
			#toggled to avoid getting connections right now.
			#conn = getConnections(playerSlot)
			conn = str(playerName)+": connections is 696969"

			print conn
			playerConn=str(conn).strip(str(playerName+": connections is "))
			print playerConn
			#playerConnections = str(getConnections(playerSlot).strip(str(playerName+": connections is ")))
			
			#print playerConnections
			playerAliases= "sexy"#str(getAlias(playerSlot)).strip(playerName+" aliases:")
			print playerSlot,": ",playerName,"(Connections: ",playerConn," --> ",playerAliases
			#print getID(playerSlot)
			#print getGUID(playerSlot)

	#print playerList
	print "?"
	#print playerList
	return playerList

def getNumberOfPlayers():
	pass







def spank(spankSlot,reason):
	spankString = "!sp "+str(spankSlot)+" "+str(reason)
	child.sendline(spankString)
	child.expect(spankString)

def warn(slot,reason):
	warnString = "!w "+str(slot)+" "+str(reason)
	child.sendline(warnString)
	child.expect(warnString)
	warnData = (child.read_nonblocking(size=1000,timeout=100))
	print warnData

def warnClear(slot):
	warnClearString = "!wc "+str(slot)
	child.sendline(warnClearString)
	child.expect(warnClearString)
	warnClearData = (child.read_nonblocking(size=1000,timeout=100))
	print warnClearData

def getAlias(slot):
	getAliasString = "!alias "+str(slot)
	child.sendline(getAliasString)
	child.expect(getAliasString)
	try:
		getAliasData = child.read_nonblocking(size=1000,timeout=2)
	except:
		getAliasData = "No Alias or timed out."
	print getAliasData
	return getAliasData

def getID(slot):
	getIDString = "!clientinfo "+str(slot)+" id"
	child.sendline(getIDString)
	child.expect(getIDString)
	getIDData = child.read_nonblocking(size=1000,timeout=2)
	#print getAliasData
	return getIDData

def getGUID(slot):
	getGUIDString = "!clientinfo "+str(slot)+" guid"
	child.sendline(getGUIDString)
	child.expect(getGUIDString)
	getGUIDData = child.read_nonblocking(size=1000,timeout=2)
	#print getAliasData
	return getGUIDData


def maprotate():
	maprotateString = "!maprotate"
	child.sendline(maprotateString)

def banPlayer(slot,reason):
	banPlayerString = "!pb "+str(slot)+" "+str(reason)
	child.sendline(banPlayerString)
	child.expect(banPlayerString)
	banPlayerData = child.read_nonblocking(size=1000,timeout=35)
	print banPlayerData

def kickPlayer(slot,reason):
	kickPlayerString = "!k "+str(slot)+" "+str(reason)
	child.sendline(kickPlayerString)
	child.expect(kickPlayerString)
	kickPlayerData = child.read_nonblocking(size = 1000, timeout=5)
	print kickPlayerData
	return str(kickPlayerData)



#getList()
#ParseList()

#maprotate()
#warn(slotNumber,"Too cool for school")
#warnClear(slotNumber)
if debugA ==True:	
	getConnections(slotNumber)

	#getPlayers()
	getAlias(slotNumber)
#banPlayer(17,"WH NOOB")


#quitTelnet()
#child.close()



