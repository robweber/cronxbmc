from resources.lib.cron_utils import utils
from resources.lib.cron import CronService

# run the program
utils.log("Cron for Kodi service starting....")
CronService().runProgram()
