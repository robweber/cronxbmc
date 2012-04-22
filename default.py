import xbmc
from service import CronXbmc

#run the program
xbmc.log("Cron XBMC service starting....")
CronXbmc().runProgram()
