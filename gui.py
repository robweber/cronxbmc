
import xbmcaddon
from resources.lib.windowGUI import WindowGUI
from service import CronService,CronManager, CronJob

__addon_id__ = "service.cronxbmc"
__Addon__ = xbmcaddon.Addon(__addon_id__)
__cwd__        = __Addon__.getAddonInfo('path')

def updateJobs():
    ui = WindowGUI( __cwd__)
    del ui
    

def runJob(jobNum):
    #get the current jobs
    cron_jobs = CronManager().getJobs()

    selected = cron_jobs[jobNum]
    CronService().runJob(selected,True)

updateJobs()

    


