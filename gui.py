import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from resources.lib.windowGUI import windowGUI
from service import CronXbmc, CronJob

__addon_id__ = "service.cronxbmc"
__Addon__ = xbmcaddon.Addon(__addon_id__)
__cwd__        = __Addon__.getAddonInfo('path')

def updateJobs():
    #print __cwd__
    xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
    ui = windowGUI( "script-cron-main.xml" , __cwd__, "Default")
    ui.doModal()
    del ui
    

def runJob(jobNum):
    #get the current jobs
    cron_jobs = CronXbmc().readCronFile()

    selected = cron_jobs[jobNum]
    CronXbmc().runJob(selected,True)

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                    params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                    splitparams={}
                    splitparams=pairsofparams[i].split('=')
                    if (len(splitparams))==2:
                            param[splitparams[0]]=splitparams[1]

    return param

mode = 0
params = get_params()

try:
    mode = int(params['mode'])
except:
    pass

if mode == 0:
    updateJobs()
elif mode == 1003:
    runJob(int(params['job']))
    


