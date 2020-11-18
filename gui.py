import xbmc,xbmcgui,xbmcplugin
import sys
from urllib.parse import parse_qsl
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
        name = xbmcgui.Dialog().input(heading=utils.getString(30002))

        if(name == ""):
            return
        else:
            newJob.name = name

        command = xbmcgui.Dialog().input(heading=utils.getString(30003))

        if(command == ""):
            return
        else:
            newJob.command = command

        expression = xbmcgui.Dialog().input(utils.getString(30004),"0 0 * * *")

        if(expression == ""):
            return
        else:
            newJob.expression = expression

        if(xbmcgui.Dialog().yesno(utils.getString(30005), utils.getString(30010))):
            newJob.show_notification = "true"
        else:
            newJob.show_notification = "false"

        if(not self.cron.addJob(newJob)):
            xbmcgui.Dialog().ok(utils.getString(30000),'Job not added, cron expression error')

    def run(self):
        command = int(self.params['command'])
        window = int(self.params['window'])
        
        if(command == 1):
            #we want to create a job
            self._createJob()
        elif(command == 2):
            #delete command
            aJob = self.cron.getJob(int(self.params['job']))
            confirm = xbmcgui.Dialog().yesno(utils.getString(30007),utils.getString(30009) + " " + aJob.name)

            if(confirm):
                #delete the job
                self.cron.deleteJob(aJob.id)
        elif(command == 3):
            #update the name
            aJob = self.cron.getJob(int(self.params['job']))

            aJob.name = xbmcgui.Dialog().input(utils.getString(30006) + " " + utils.getString(30002),aJob.name)
            self.cron.addJob(aJob)
        elif(command == 4):
            #udpate the command
            aJob = self.cron.getJob(int(self.params['job']))

            aJob.command = xbmcgui.Dialog().input(utils.getString(30006) + " " + utils.getString(30003),aJob.command)
            self.cron.addJob(aJob)
            
        elif(command == 5):
            #update the expression
            aJob = self.cron.getJob(int(self.params['job']))

            aJob.expression = xbmcgui.Dialog().input(utils.getString(30006) + " " + utils.getString(30004),aJob.expression)

            if(not self.cron.addJob(aJob)):
                xbmcgui.Dialog().ok(utils.getString(30000),'Job not added, cron expression error')

        elif(command == 6):
            #update the notification setting
            aJob = self.cron.getJob(int(self.params['job']))

            if(xbmcgui.Dialog().yesno(utils.getString(30005), utils.getString(30010))):
                aJob.show_notification = "true"
            else:
                aJob.show_notification = "false"
                
            self.cron.addJob(aJob)
            
        if(command != 0):
            #always refresh after command
            xbmc.executebuiltin('Container.Refresh')

        jobs = self.cron.getJobs(utils.getSetting('show_all'))
        if(window == 0):
            #create the default window
            addItem = xbmcgui.ListItem(utils.getString(30001))
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.context_url % (sys.argv[0],'command=1&window=0'),listitem=addItem,isFolder=False)
           
            for j in jobs:
                #list each job
                cronItem = xbmcgui.ListItem(j.name + " - " + utils.getString(30011) + ": " + self.cron.nextRun(j))
                cronItem.addContextMenuItems([(utils.getString(30008),self.plugin_url % (sys.argv[0],'command=0&window=1&job=' + str(j.id))),(utils.getString(30007),self.plugin_url % (sys.argv[0],'command=2&window=0&job=' + str(j.id)))])
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.context_url % (sys.argv[0],'command=0&window=1&job=' + str(j.id)),listitem=cronItem,isFolder=True)
        elif(window == 1):
            #list the details of this job
            aJob = self.cron.getJob(int(self.params['job']))

            name = xbmcgui.ListItem(utils.getString(30002) + ": " + aJob.name)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.context_url % (sys.argv[0],'command=3&window=1&job=' + str(aJob.id)),listitem=name,isFolder=False)
           
            command = xbmcgui.ListItem(utils.getString(30003) + ": " + aJob.command)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.context_url % (sys.argv[0],'command=4&window=1&job=' + str(aJob.id)),listitem=command,isFolder=False)

            expression = xbmcgui.ListItem(utils.getString(30004) + ": " + aJob.expression)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.context_url % (sys.argv[0],'command=5&window=1&job=' + str(aJob.id)),listitem=expression,isFolder=False)

            showNotification = 'No'
            if(aJob.show_notification == 'true'):
                showNotification = 'Yes'

            notification = xbmcgui.ListItem(utils.getString(30005) + ": " + showNotification)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.context_url % (sys.argv[0],'command=6&window=1&job=' + str(aJob.id)),listitem=notification,isFolder=False)

        xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
                    
#helper function to the get the incoming params
def get_params():
    param = {}
    try:
        for i in sys.argv:
            args = i
            if(args.startswith('?')):
                args = args[1:]
            param.update(dict(parse_qsl(args)))
    except:
        pass
    return param

params = get_params()

if(not 'window' in params):
    params['window'] = 0

if(not 'command' in params):
    params['command'] = 0

CronGUI(params).run()

#xbmcgui.Dialog().ok(utils.getString(30000),"No GUI at this time")

    


