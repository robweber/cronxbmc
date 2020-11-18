import resources.lib.utils as utils
from resources.lib.cron import CronService

# run the program
utils.log("Cron for Kodi service starting....")
CronService().runProgram()
