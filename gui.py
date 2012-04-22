import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from service import CronXbmc, CronJob

__addon_id__ = "service.cronxbmc"
__Addon__ = xbmcaddon.Addon(__addon_id__)
    
def updateJobs():
    #read in the xml file
    cronxbmc = CronXbmc()
    cron_jobs = cronxbmc.readCronFile()
    
    array_count = 0
    for job in cron_jobs:
        itemListing = xbmcgui.ListItem(job.name,cronxbmc.nextRun(job))
        rp = "XBMC.RunPlugin(%s?mode=%s)"
        xbmc.log(rp % (sys.argv[0],1000))
        itemListing.addContextMenuItems([("Edit Job",rp % (sys.argv[0],1000)),("Delete Job",rp %(sys.argv[0],1001)),("Create Job", rp % (sys.argv[0],1002))],replaceItems=True)
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=sys.argv[0] + "?mode=1003&job=" + str(array_count),listitem=itemListing,isFolder=False)
        array_count = array_count + 1
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)


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
    


