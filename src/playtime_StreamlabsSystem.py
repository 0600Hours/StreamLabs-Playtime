#---------------------------------------
# Script Import Libraries
#---------------------------------------
import json
import os
import codecs

#---------------------------------------
# Script Information
#---------------------------------------
ScriptName = "Steam Playtime"
Website = "https://www.twitter.com/0600Hours"
Description = "Retrieve playtime for a given game on Steam"
Creator = "0600Hours"
Version = "1.0.0"

#---------------------------------------
# Script Variables
#---------------------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
# Script Classes
#---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""
    #The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile=None):
        if SettingsFile and os.path.isfile(SettingsFile):
            with codecs.open(SettingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no settings file is found
            self.CommandName = "!playtime"
            self.Response = "An error has occurred while loading settings."
            self.TimeUnit = ""
            self.Cooldown = 30
            self.GameName = ""
            self.GameID = ""
            self.SteamID = ""
            self.SteamAPIKey = ""

    # Reload settings on save through UI
    def Reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')

    def Save(self, settingsfile):
        """ Save settings contained within the .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__,
                                                                encoding='utf-8',
                                                                ensure_ascii=False)))
        except ValueError:
            Parent.Log(ScriptName, "Failed to save settings to file.")

#---------------------------------------
# Script Functions
#---------------------------------------
def find_game(response, id):
    game_list = json.loads(response["response"])["response"]["games"]
    for game in game_list:
        if str(game["appid"]) == id:
            return game
    return {}    

def build_response(game_info):
    if game_info == {}:
        return "An error has occured while processing game info."
    else:
        time = game_info["playtime_forever"]
        time_message = ""
        if (ScriptSettings.TimeUnit == "Minutes"):
            time_message = "{0} minutes"
        elif (ScriptSettings.TimeUnit == "Hours"):
            time = time / 60
            time_message = "{0} hours"
        elif (ScriptSettings.TimeUnit == "Days"):
            time = time / 60 / 24
            time_message = "{0} days"
		
        time_message = time_message.format(time)
        if (time == 1):
            time_message = time_message[:-1]

        return ScriptSettings.Response.format(channel_name=Parent.GetChannelName(), time_played=time_message, game_name=ScriptSettings.GameName)

#---------------------------------------
# Chatbot Basic Functions
#---------------------------------------
def Init():
    # Load settings from file and verify
    global ScriptSettings
    ScriptSettings = Settings(SettingsFile)

    return

def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.CommandName and not Parent.IsOnCooldown(ScriptName,ScriptSettings.CommandName):
		url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={0}&steamid={1}".format(ScriptSettings.SteamAPIKey, ScriptSettings.SteamID)
		response = json.loads(Parent.GetRequest(url, {}))
		if (response["status"] == 200):
			game_info = find_game(response, ScriptSettings.GameID)
			Parent.SendStreamMessage(build_response(game_info))
		else:
			Parent.Log(ScriptName, "Error while fetching game\nurl: {0}\nstatus: {1}\nerror: {2}".format(url, response["status"], response["error"]))
			Parent.SendStreamMessage("An error occured while fetching game info.")

		Parent.AddCooldown(ScriptName, ScriptSettings.CommandName, ScriptSettings.Cooldown)
    return

def Tick():
    return

#---------------------------------------
# Chatbot ReadMe Function
#---------------------------------------
def OpenReadMe():
    os.startfile(os.path.join(os.path.dirname(__file__), "README.txt"))
