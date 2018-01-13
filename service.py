import resources.lib.utils as utils
from resources.lib.cron import CronService

#run the program
xbmc.log("Cron for Kodi service starting....",xbmc.LOGINFO)
CronService().runProgram()
