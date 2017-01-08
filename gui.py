import xbmcgui,xbmcplugin
import sys
import urlparse
from resources.lib.cron import CronManager, CronJob
import resources.lib.utils as utils


class CronGUI:
    params = {}
    context_url = "%s?%s"
    plugin_url = 'Xbmc.RunPlugin(%s?%s)' 
    cron = None

    def __init__(self,params):
        self.params = params
        self.cron = CronManager()

    def _createJob(self):
        newJob = CronJob()
        
        #get the name, command, expression and notification setting
        name = xbmcgui.Dialog().input(heading="Job Name")

        if(name == ""):
            return
        else:
            newJob.name = name

        command = xbmcgui.Dialog().input(heading="Kodi Command")

        if(command == ""):
            return
        else:
            newJob.command = command

        expression = xbmcgui.Dialog().input("Cron Expression","0 0 * * *")

        if(expression == ""):
            return
        else:
            newJob.expression = expression

        newJob.show_notification = xbmcgui.Dialog().yesno('Show Notification', "Show a notification when this task runs?")

        self.cron.addJob(newJob)

    def run(self):
        command = int(self.params['command'])
        window = int(self.params['window'])
        
        if(command == 1):
            #we want to create a job
            self._createJob()
            xbmc.executebuiltin('Container.Refresh')
        elif(command == 2):
            jobs = self.cron.getJobs()
            aJob = jobs[int(self.params['job'])]
            confirm = xbmcgui.Dialog().yesno("Delete","Delete job " + aJob.name)

            if(confirm):
                #delete the job
                self.cron.deleteJob(aJob.id)
                xbmc.executebuiltin('Container.Refresh')

        jobs = self.cron.getJobs()
        if(window == 0):
            #create the default window
            if(len(jobs) == 0):
                #there aren't any jobs, just list "add" as an option
                addItem = xbmcgui.ListItem(utils.getString(30001))
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.context_url % (sys.argv[0],'command=1&window=0'),listitem=addItem,isFolder=False)
            else:
                for j in jobs:
                    #list each job
                    cronItem = xbmcgui.ListItem(j.name + " - Next Run: " + self.cron.nextRun(j))
                    cronItem.addContextMenuItems([("Details",self.plugin_url % (sys.argv[0],'command=0&window=1&job=' + str(j.id))),("Delete",self.plugin_url % (sys.argv[0],'command=2&window=0&job=' + str(j.id)))])
                    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.context_url % (sys.argv[0],'command=0&window=1&job=' + str(j.id)),listitem=cronItem,isFolder=True)
        elif(window == 1):
            #list the details of this job
            aJob = jobs[int(self.params['job'])]
            utils.log(aJob.name)
            command = xbmcgui.ListItem(aJob.command)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.context_url % (sys.argv[0],'command=0&window=1&job=' + str(aJob.id)),listitem=command,isFolder=False)

            expression = xbmcgui.ListItem(aJob.expression)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.context_url % (sys.argv[0],'command=0&window=1&job=' + str(aJob.id)),listitem=expression,isFolder=False)

            showNotification = 'No'
            if(aJob.show_notification == 'true'):
                showNotification = 'Yes'

            notification = xbmcgui.ListItem('Notification: ' + showNotification)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.context_url % (sys.argv[0],'command=0&window=1&job=' + str(aJob.id)),listitem=notification,isFolder=False)

        xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
                    
#helper function to the get the incoming params
def get_params():
    param = {}
    try:
        for i in sys.argv:
            args = i
            if(args.startswith('?')):
                args = args[1:]
            param.update(dict(urlparse.parse_qsl(args)))
    except:
        pass
    return param

params = get_params()

if(not params.has_key('window')):
    params['window'] = 0

if(not params.has_key('command')):
    params['command'] = 0

CronGUI(params).run()

#xbmcgui.Dialog().ok(utils.getString(30000),"No GUI at this time")

    


