import xbmc
import xbmcgui
import xbmcaddon
from resources.lib.windowGUI import WindowGUI
from service import CronXbmc, CronJob

__addon_id__ = "service.cronxbmc"
__Addon__ = xbmcaddon.Addon(__addon_id__)
__cwd__        = __Addon__.getAddonInfo('path')

def updateJobs():
    ui = WindowGUI( __cwd__)
    del ui
    

def runJob(jobNum):
    #get the current jobs
    cron_jobs = CronXbmc().readCronFile()

    selected = cron_jobs[jobNum]
    CronXbmc().runJob(selected,True)

updateJobs()

    


