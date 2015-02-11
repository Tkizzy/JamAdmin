#JamAdmin V 0.1

import logging
#from kivy.logger import Logger
#Logger.setLevel(logging.ERROR)

from kivy.core.text import LabelBase
LabelBase.register(name="HelveticaNeue",  
                   fn_regular="HelveticaNeueThn.ttf")
from kivy.app import App
from kivy.uix.listview import ListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown


from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from os.path import join
import telParse
import time

class JamAdmin(App):

	print ">Class JamApp"



	def setStore(self):
		self.data_dir = App().user_data_dir
		self.store = JsonStore(join(self.data_dir, 'storage.json'))

	def clearStore(self):
		self.store.clear()
		print ">>Function clearStore"


	def saveCreds(self,namer,passer):
		print ">>Function saveCreds ...."
		#self.data_dir = App().user_data_dir
		#self.store = JsonStore(join(self.data_dir, 'storage.json'))
		#savedCred = self.store.get('credentials')
		self.store.clear()
		#print "saved????",savedCred
		#savedCred.clear()
		self.store.put('credentials',username=namer,password = passer)
		print "saved User: "+str(namer)+", password: "+str(passer)
		print self.store
		#self.store.clear()



	def checkCreds(self):
		print ">>Function checkCreds"

		#self.data_dir = App().user_data_dir
		#global self.store
		#self.store = JsonStore(join(self.data_dir, 'storage.json'))
		
		print ">>checkCreds > exists? ",self.store.exists('credentials')


		try:
		    print ">>checkCreds >> trying JSON self.store get"
		    savedCred = self.store.get('credentials')
		    savedUser = savedCred['username']
		    savedPass = savedCred['password']
		except:
		    print "couldn't get credentials, creating default values"
		    savedUser = "noUsernameEntered"
		    savedPass = "noPasswordEntered"

		if (str(savedUser) == "noUsernameEntered" and str(savedPass) == "noPasswordEntered"):
		    print ">>checkCreds >> DEFAULT VALUES IF STATEMENT"
		elif str(savedUser) == "noUsernameEnteredX":
			print "Not default from Cred check, but default from loadList savecredss"
		else:
		    print ">>checkCreds >> NOT DEFAULT VALUES!! (correct creds????)"
		    #prepView(savedUser,savedPass)
		#return ">>checkCreds >> return : CHECK FOR EXISTING?????? RETURNED>...."
		return savedUser,savedPass


	def loadList(self,namer,passer):
		print "loading list...rewrite undo history :("
		#newTel=telParse.telnetLogin(self.username.text,self.password.text)
		newTel = telParse.telnetLogin(namer,passer)
		
		print newTel
		if newTel == "Success":
			stringy = telParse.ParseList()
			#self.saveCreds(self.username.text,self.password.text)
			self.saveCreds(namer,passer)

			print "successful telnet parse"
		elif newTel == "Failure":
			print "elif newtel failure"
			self.saveCreds("noUsernameEntered","noPasswordEntered")
			#stringy = {1:"TelNet",2:"Failure",3:"Or",4:"Incorrect credentials",5:"Try Again in a moment."}
			stringy = ["","","","TelNet failure","or (more likely)"," incorrect credentials.","","Try again in a moment."]

			telParse.quitTelnet()

		return stringy



	def launchLogic(self):
		print ">>Function LAUNCH LOGIC"

		#self.data_dir = App().user_data_dir
		self.store = JsonStore(join(self.data_dir, 'storage.json'))
		self.credentialsExist = self.store.exists('credentials')
		print ">> launchLogic > creds exist? ",self.credentialsExist

		if self.credentialsExist:
			launchCreds = self.store.get('credentials')
			launchCredUser = launchCreds['username']
			launchCredPass = launchCreds['password']

			if launchCredUser == "noUsernameEntered" or launchCredPass == "noPasswordEntered":
				print ">>launchLogic >  credentials exist as invalidly entered"
				self.validCredentials = False
			else:
				print ">>launchLogic >  Valid Creds exist. Will get list on load next."
				self.validCredentials = True
			return launchCredUser,launchCredPass
		else:
			print "NO CREDENTIALS FOUNDD!!!!"
			self.validCredentials = False

	def makeListView(self,stringyList):
		
		stringyLister = stringyList
		print "TYPE: ",type(stringyLister)
		

		if type(stringyLister) is dict:
			print "dict"
			madeList = ListView(item_strings=[str(key)+": "+str(stringyList[key]) for key in stringyList.keys()],font="Times")
		
		elif type(stringyLister) is list:
			emptyList = ["...","..."]
			#stringyList = emptyList.append(stringyLister)
			print "list"
			madeList = ListView(item_strings = stringyList,font_name="HelveticaNeue",padding=10)
			print madeList
		else:
			print "else"
			madeList = ListView(item_strings = stringyList)
		
		return madeList


	def actionButton(self,evt=None):
		print "hi"
		
		stringy = self.loadList(self.username.text,self.password.text)

		#stringy = telParse.ParseList()
		#stringy = {1:"New",2:"List",3:"Loaded",4:self.x}
		self.new_list_view = self.makeListView(stringy)

		#ListView(item_strings=[str(key)+": "+str(stringy[key]) for key in stringy.keys()],font="Times")
		
		print "children: ",self.list_view.children[0]

		try:
			self.listViewBlock.clear_widgets()
		except:
			print "excepting normal widget clear for some reason...ckearing by child index?"
			self.listViewBlock.remove_widget(self.listViewBlock.children[1])

		#self.
		print "removed?"
		selfList = self.list_view
		self.x+=1

		self.listViewBlock.add_widget(self.new_list_view,index=0)
		print "added?"

	def textControl(self,evt=None):
		print "text stuf...."
		self.actionButton()
		pass

	def kickPlayer(self,evt=None):
		pass
		print "fake kick"
		#self.outerMost.add_widget(self.popup)
		self.popupContent.clear_widgets()
		self.popupContent.add_widget(self.kickPopupReasonInput)
		
		self.popupBottom.clear_widgets()
		
		self.popupBottom.add_widget(self.kickPopupButton)
		self.popupBottom.add_widget(self.cancelCommitButton)
		
		self.popupContent.add_widget(self.popupBottom)
		
		self.popup.open()
		#kickText = self.

	def banPlayer(self,instance,evt=None):
		print "fake ban"
		self.popupContent.clear_widgets()
		self.popupContent.add_widget(self.banPopupReasonInput)
		self.popupBottom.clear_widgets()
		
		self.popupBottom.add_widget(self.banPopupButton)
		self.popupBottom.add_widget(self.cancelCommitButton)
		
		self.popupContent.add_widget(self.popupBottom)
		self.popup.open()

	def kickCommit(self,evt = None):
		print "kick commit.."
		print "should kick slot",self.kickSlotInput.text,"reason: ",self.kickPopupReasonInput.text
		telParse.kickPlayer(self.kickSlotInput.text,self.kickPopupReasonInput.text)
		self.popup.dismiss()

	def banCommit(self,evt = None):
		print "ban Commit:"
		print "Banning slot",self.banSlotInput.text,", reason: ",self.banPopupReasonInput.text
		
		telParse.banPlayer(self.banSlotInput.text,self.banPopupReasonInput.text)
		self.popup.dismiss()

	def on_text(self,instance,value):
		print "ON TEXT,,,,"
		print('The widget', instance, 'have:', value)

	def on_focus(self,instance,evt=None):
		print "Focus happening"
		if instance.text=="":
			print "empty, filling out"
			instance.text="slot"
		elif instance.text =="slot" or instance.text == "kick slot #" or instance.text== "ban slot #" or instance.text == "info slot #":
			instance.text=""

	def cred_focus(self,instance,evt=None):
		print "credential focus"
		if instance.text=="noUsernameEntered":
			instance.text=""
		elif instance.text == "noPasswordEntered":
			instance.text = ""
		elif instance.text =="" and instance.password == False:
			instance.text = str(self.credChecker[0])
		elif instance.text =="" and instance.password ==True:
			instance.text = str(self.credChecker[1])

	def formatInfo(self,name,connections,string):
		print "FORMATING:"
		print string
		print len(string)
		if len(string)<30:
			print "no aliases small string"
			noAliasArray = ["No","Aliases."]
			return noAliasArray
		else:
			try:
				deAliased = string.split("aliases:")
				deEnded = deAliased[1].strip()
				divided = deEnded.split(",")
			except:
				divided = ["String","Parse","Error","Or Invalid","Input"]
			print divided
			print "~~~~~~~ DIVIDED^"

			return divided

	def parseConnections(self,string):
		split = string.split(": connections is ")
		print split
		name = split[0].strip()
		print name
		connectionCount = split[1].strip()
		print connectionCount

		return name,connectionCount

	def getPlayerInfo(self,playerSlot):
		print "getting Con and Alias..."
		playerSlot = self.playerInfoText.text
		playerAlias = telParse.getAlias(playerSlot)
		playerConnections = telParse.getConnections(playerSlot)
		print playerConnections	
		conParse = self.parseConnections(playerConnections)
		name = conParse[0]
		connections = conParse[1]

		formattedAliasList = self.formatInfo(name,connections,playerAlias)

		#self.playerInfoLabel.text = str(formattedAliasList)

		return playerSlot,connections,formattedAliasList,name
			

	def layoutPlayerInfo(self,evt=None):
		
		playerSlot = self.playerInfoText.text
		
		#set other fields to correspond to this one...
		self.kickSlotInput.text = playerSlot
		self.banSlotInput.text = playerSlot
		#EnD

		playerInfo = self.getPlayerInfo(playerSlot)
		aliasList = playerInfo[2]
		ourSlot = playerInfo[0]#str(playerSlot)
		ourName = playerInfo[3]
		connections = playerInfo[1]
		print ourSlot
		ourSlotA = str(ourSlot+":")
		print ourSlotA
		lengthConString = len(str("|".ljust(2)+"Connections: "+str(connections)+"|".rjust(2)))
		print "length of top: ",lengthConString
		
		nameLineJustLength = (lengthConString - (len(ourName)+2))/2
		nameSlotLineJustLength = (lengthConString -(len(playerSlot)+2))/2
		akalengthCalc = (lengthConString - len("|_____ AKA: _____|"))/2

		aliasList.insert(0,str("|_____".ljust(akalengthCalc)+"AKA"+"_____|".rjust(akalengthCalc)))

		aliasList.insert(0,str("|".ljust(3)+"Connections: "+str(connections)+"|".rjust(3)))
		
		
		
		aliasList.insert(0,str("|".ljust(nameLineJustLength)+ourName+"|".rjust(nameLineJustLength)))
		aliasList.insert(0,str("|".ljust(nameSlotLineJustLength)+str(playerSlot)+"|".rjust(nameSlotLineJustLength)))

		print aliasList
		print "^^^"

		try:
			self.listViewBlock.remove_widget(self.playerDetailListView)
		except:
			print "No list view to remove?"
		self.playerDetailListView = self.makeListView(aliasList)
		self.listViewBlock.add_widget(self.playerDetailListView,index=0)







	'''
	def on_focus(instance, value):
		if value:
			print('User focused', instance)
		else:
			print('User defocused', instance)
	'''

	def updateListOnOpen(self):
		print ">> Function updateList"
		print "..."#self.layoutFields

	def build(self):
		self.icon = 'JamAdminIconA.icns'
		self.setStore()
		b=BoxLayout()
		print ">>Function Build"
		#self.data_dir = App().user_data_dir
		#store = JsonStore(join(self.data_dir, 'storage.json'))
		print "exists ",self.store.exists('credentials') 
		#self.store.clear()
		print "exists ",self.store.exists('credentials') 
		try:
			print self.store.get('credentials')
		except:
			pass

		self.outerMost = GridLayout(cols=0)

		self.layoutFields = BoxLayout()
		self.outerMost.add_widget(self.layoutFields)
		self.layoutFields.cols = 2
		self.x = 0
		
		#kick UI

		stringy = {1:"List",2:"Not",3:"Loaded"}
		#list_view = ListView(item_strings=[str(key)+": "+str(stringy[key]) for key in stringy.keys()],font="Times")
		kickRow = BoxLayout(padding= 1)
		self.kickSlotInput = TextInput(disabled_foreground_color =(.32,.70,.22,1),cursor_color = [.32,.70,.22,1],multiline=False,text="kick slot #",on_text_validate = self.kickPlayer)#,on_focus=self.on_focus("hi"))#,on_text_validate=self.kickPlayer)
		self.kickSlotInput.bind(focus=self.on_focus)#elf.on_focus)
		kickSlotButton = Button(text = "Kick this slot")
		kickSlotButton.bind(on_press = self.kickPlayer)
		kickRow.add_widget(self.kickSlotInput)
		kickRow.add_widget(kickSlotButton)

		#end KICK

		

		#ban UI

		banRow = BoxLayout(padding=1)
		self.banSlotInput = TextInput(multiline=False,text = "ban slot #",on_text_validate = self.banPlayer)#,focus=self.on_focus)
		self.banSlotInput.bind(focus=self.on_focus)
		banSlotButton = Button(text="Ban this Slot")
		banSlotButton.bind(on_press = self.banPlayer)
		banRow.add_widget(self.banSlotInput)
		banRow.add_widget(banSlotButton)


		#POPUP
		self.popupContent = StackLayout()
		self.popupContent.rows = 2
		#popup bottom
		self.popupBottom = BoxLayout()
		self.popupBottom.cols = 2
		#popup - kick
		self.kickPopupReasonInput = TextInput(text="reason",multiline=False,on_text_validate=self.kickCommit)
		self.kickPopupButton = Button(text="submit",on_press=self.kickCommit)
		#popup - ban
		self.banPopupReasonInput = TextInput(text="reason",multiline=False,on_text_validate=self.banCommit)
		self.banPopupButton = Button(text="submit",on_press=self.banCommit)
		#popup - shared
		self.popup = Popup(title='Enter a Reason',size_hint=(None, None),size=(200,200),auto_dismiss=False)#,content=TextInput(text='reason'))
		self.popup.add_widget(self.popupContent)
		self.cancelCommitButton = Button(text="Cancel",on_press=self.popup.dismiss)

		#Credential UI
		self.credChecker = self.checkCreds()
		self.username = TextInput(checkPlease = "user",focus=False,font_name="HelveticaNeue",font_size=16,write_tab = True,multiline=False,valign="bottom",padding = 1,text = str(self.credChecker[0]) )
		self.username.bind(focus=self.cred_focus)
		self.password = TextInput(checkPlease = "pass",focus=False,write_tab = False,password=True,multiline=False,padding=10,text = str(self.credChecker[1]))
		self.password.bind(on_text_validate=self.textControl,focus = self.cred_focus)
		usernameLabel = Label(text="Username: ",valign='top')
		userAndPass = BoxLayout(Padding = 10,write_tab = False)
		userAndPass.add_widget(self.username)
		userAndPass.add_widget(self.password)
		#cred labels
		userAndPassLabels = BoxLayout(padding= 50,halign="right")
		userAndPassLabels.add_widget(usernameLabel)
		userAndPassLabels.add_widget(Label(text='Password'))
		blankLabels = BoxLayout()

		getListButton = Button(text='Get List Button')
		getListButton.bind(on_press=self.actionButton)

		print ">> Build >> Launching launchLogic()"

		self.launchLogic()
		print ">> Build >> End launchLogic()"
		
		if self.validCredentials == True:
			self.list_view = self.makeListView(self.loadList(self.username.text,self.password.text))
		elif self.validCredentials == False:
			welcomeString = ["","","Welcome","Please enter your","username and password","to the right.","The last correctly","Loaded credentials will","be saved to auto log you in","the next time you","start the app.","Enjoy."]
			self.list_view = self.makeListView(welcomeString)#ListView(item_strings=[str(key)+": "+str(stringy[key]) for key in stringy.keys()],font="Times")
		
		self.playerDetailListView = ListView()
		self.listViewBlock = BoxLayout(padding = 30)
		self.listViewBlock.add_widget(self.list_view,index=1)
		self.layoutFields.add_widget(self.listViewBlock)
		textFieldA=BoxLayout(padding=12)

		#remove then add list view to be used for updating example...
		#self.layoutFields.remove_widget(self.list_view)
		#self.layoutFields.add_widget(self.list_view)

		#getListButton = Button(text='Get List Button')
		#getListButton.bind(state=self.updateList)

		playerInfoButton = Button(text="Get Info",on_press = self.layoutPlayerInfo)
		self.playerInfoLabel  = Label(text="")
		self.playerInfoText = TextInput(valign="center",padding = 1,on_text_validate=self.layoutPlayerInfo,multiline=False,text="info slot #")
		self.playerInfoText.bind(focus = self.on_focus)
		self.playerInfoControls = BoxLayout()
		self.playerInfoControls.add_widget(self.playerInfoText)
		self.playerInfoControls.add_widget(playerInfoButton)



		rightSidde = BoxLayout(padding = 15,orientation='vertical')
		rightSidde.add_widget(blankLabels)
		rightSidde.add_widget(userAndPassLabels)
		rightSidde.add_widget(userAndPass)
		rightSidde.add_widget(getListButton)
		rightSidde.add_widget(BoxLayout(padding=12))
		rightSidde.add_widget(BoxLayout(padding=12))
		rightSidde.add_widget(BoxLayout(padding=12))
		rightSidde.add_widget(BoxLayout(padding=12))
		rightSidde.add_widget(BoxLayout(padding=12))
		
		rightSidde.add_widget(BoxLayout(padding=12))
		rightSidde.add_widget(BoxLayout(padding=12))
		rightSidde.add_widget(self.playerInfoLabel)
		rightSidde.add_widget(self.playerInfoControls)
		rightSidde.add_widget(BoxLayout(padding=12))
		rightSidde.add_widget(kickRow)
		rightSidde.add_widget(BoxLayout(padding=12))
		rightSidde.add_widget(banRow)
		rightSidde.add_widget(BoxLayout(padding=12))
		
		self.layoutFields.add_widget(rightSidde)

		

		return self.layoutFields

	def allClear(self):
		print ">>>> ALL CLEAR <<<<"
		#re.compile('[^0-9]')
		self.data_dir = App().user_data_dir
		self.store = JsonStore(join(self.data_dir, 'storage.json'))
		print self.store['credentials']
		print self.store.exists('credentials')
		#self.store.clear()
		print self.store.exists('credentials')
		print "erasing self.store? credentials exist?",self.store.exists('credentials')
		#self.store.clear()
		print self.store.exists('credentials')
		#self.clearStore()
		#print self.store['credentials']


'''
class FloatInput(TextInput):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)
'''




if __name__ == "__main__":
	#JamApp().checkCreds()
	#JamApp().launchLogic()
	JamAdmin().run()
	JamAdmin().updateListOnOpen()
	JamAdmin().allClear()




