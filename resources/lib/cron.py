import time
import xbmc
import xbmcvfs
import xml.dom.minidom
import datetime
from croniter import croniter
import utils as utils

class CronJob:
    def __init__(self):
        self.id = -1
        self.name = ""
        self.command = ""
        self.expression = []
        self.show_notification = "false"
        self.addon = None

class CronManager:
    CRONFILE = 'special://profile/addon_data/service.cronxbmc/cron.xml'
    jobs = list()
    last_read = time.time()
    
    def __init__(self):
        self.jobs = self._readCronFile()
    
    def addJob(self,job):

        try:
            #verify the cron expression here, throws ValueError if wrong
            croniter(job.expression)
        except:
            #didn't work
            raise ValueError('Wrong expression')

        #set the addon id if there isn't one
        if(job.addon == None):
            job.addon = utils.addon_id()
        
        self._refreshJobs()

        if(job.id >= 0):
            raise ValueError('job.id should be -1')
        else:
            # check if expression and command already exist no need to define it twice
            if self._exist(job):
                xbmc.executebuiltin('Notification(Job Already exist, doing nothing)')
                xbmc.log('[service.cronxbmc] Job already exist, doing nothing', xbmc.LOGWARNING)
                return job.id
            #calcul the new job.id
            job.id = self._getLastId()+1
            #add a new job
            self.jobs.append(job)
        
        #write the file
        self._writeCronFile()
        return job.id

    def updateJob(self,job):
        try:
            #verify the cron expression here, throws ValueError if wrong
            croniter(job.expression)
        except:
            raise ValueError('Wrong expression')

        #set the addon id if there isn't one
        if(job.addon == None):
            job.addon = utils.addon_id()

        self._refreshJobs()

        if(job.id >= 0):
            #replace existing job
            indices = [i for i, x in enumerate(self.jobs) if x.id == str(job.id)]
            self.jobs[indices[0]] = job
        else:
            raise ValueError('Must provide target job.id')

        #write the file
        self._writeCronFile()
        return job.id


    
    #check if another addon has already defined exactly the same job but with another id/name
    def _exist(self,job):
        lJobs = self.getJobs(True)
        if any(c.command == job.command and c.expression == job.expression for c in lJobs):
            return True
        return False

    def _getLastId(self):
        lJobs = self.getJobs(True)
        nbRows = len(lJobs)
        if nbRows > 0:
            return int(lJobs[nbRows-1].id)
        else:
            return 0

    def deleteJob(self,jId):
        
        #delete the job with this id
        removeJob = self.jobs[jId]
        
        self.jobs.remove(removeJob)
        
        self._writeCronFile()
    
    def getJobs(self,show_all=False):
        self._refreshJobs()
 
        if(show_all != 'true'):
            #filter on currently loaded addon
            result = list(filter(lambda x: x.addon == utils.addon_id(),self.jobs))
        else:
            result = self.jobs
        
        return result
    
    def nextRun(self,cronJob):
        #create a cron expression
        cron_exp = croniter(cronJob.expression,datetime.datetime.fromtimestamp(time.time()))

        #compare now with next date
        nextRun = cron_exp.get_next(float)
        cronDiff = nextRun - time.time()
        hours = int((cronDiff / 60) / 60)
        minutes = int(cronDiff / 60 - hours * 60)

        #we always have at least one minute
        if minutes == 0:
            minutes = 1

        result = str(hours) + " h " + str(minutes) + " m"

        if hours == 0:
            result = str(minutes) + " m"
        elif hours > 36:
            #just show the date instead
            result = datetime.datetime.fromtimestamp(nextRun).strftime('%m/%d %I:%M%p')
        elif hours > 24:
            days = int(hours / 24)
            hours = hours - days * 24
            result = str(days) + " d " + str(hours) + " h " + str(minutes) + " m"
        
        return result
    
    def _refreshJobs(self):
        
        #check if we should read in a new files list
        stat_file = xbmcvfs.Stat(xbmc.translatePath(self.CRONFILE))
        
        if(stat_file.st_mtime() > self.last_read):
            xbmc.log("File update, loading new jobs",xbmc.LOGDEBUG)
            #update the file
            self.jobs = self._readCronFile();
            self.last_read = time.time()
    
    def _readCronFile(self):
        if(not xbmcvfs.exists(xbmc.translatePath('special://profile/addon_data/service.cronxbmc/'))):
            xbmcvfs.mkdir(xbmc.translatePath('special://profile/addon_data/service.cronxbmc/'))

        adv_jobs = []
        try:
            doc = xml.dom.minidom.parse(xbmc.translatePath(self.CRONFILE))
            
            for node in doc.getElementsByTagName("job"):
                tempJob = CronJob()
                tempJob.name = str(node.getAttribute("name"))
                tempJob.id = str(node.getAttribute("id"))
                tempJob.command = str(node.getAttribute("command"))
                tempJob.expression = str(node.getAttribute("expression"))
                tempJob.show_notification = str(node.getAttribute("show_notification"))

                #catch for older cron.xml files
                if(node.getAttribute('addon') != ''):
                    tempJob.addon = str(node.getAttribute('addon'))
                else:
                    tempJob.addon = utils.__addon_id__
                
                xbmc.log('[service.cronxbmc]'+tempJob.name + " " + tempJob.expression + " loaded",xbmc.LOGDEBUG)
                adv_jobs.append(tempJob)

        except IOError:
            #the file doesn't exist, return empty array
            doc = xml.dom.minidom.Document()
            rootNode = doc.createElement("cron")
            doc.appendChild(rootNode)
            #write the file
            f = xbmcvfs.File(xbmc.translatePath(self.CRONFILE),"w")
            doc.writexml(f,"   ")
            f.close()
            

        return adv_jobs
    
    def _writeCronFile(self):
        
        #write the cron file in full
        try:
            doc = xml.dom.minidom.Document()
            rootNode = doc.createElement("cron")
            doc.appendChild(rootNode)
            
            for aJob in self.jobs:
                
                #create the child
                newChild = doc.createElement("job")
                newChild.setAttribute("name",aJob.name)
                newChild.setAttribute("id",str(aJob.id))
                newChild.setAttribute("expression",aJob.expression)
                newChild.setAttribute("command",aJob.command)
                newChild.setAttribute("show_notification",aJob.show_notification)
                newChild.setAttribute("addon",aJob.addon)
                
                rootNode.appendChild(newChild)

            #write the file
            f = xbmcvfs.File(xbmc.translatePath(self.CRONFILE),"w")
            doc.writexml(f,"   ","    ","\r\n")
            f.close()
                                        
        except IOError:
            xbmc.log("error writing cron file",xbmc.LOGERROR)

class CronService:
    last_check = -1
    manager = None
    
    def __init__(self):
        self.manager = CronManager()
    
    def runProgram(self):
        monitor = xbmc.Monitor()
        
        #run until abort requested
        while(True):

            structTime = time.localtime()
            now = time.time()
            #only do all this if we are in a new minute
            if(structTime[4] != self.last_check):
                self.last_check = structTime[4]

                #get a list of all the cron jobs
                cron_jobs = self.manager.getJobs()

                for command in cron_jobs:
                    #create a cron expression for this command
                    cron_exp = croniter(command.expression,datetime.datetime.fromtimestamp(now - 60))
                    
                    runTime = cron_exp.get_next(float);
                    #if this command should run then run it
                    if(runTime <= now):
                        self.runJob(command)
                        xbmc.log(command.name + " will run again on " + datetime.datetime.fromtimestamp(cron_exp.get_next(float)).strftime('%m-%d-%Y %H:%M'))
                
            if(monitor.waitForAbort(10)):
                break;

    def runJob(self,cronJob,override_notification = False):
        xbmc.log("running command " + cronJob.name + " for addon " + cronJob.addon)

        if(cronJob.show_notification == "true" or override_notification):
            #show a notification that this command is running
            utils.showNotification("Cron", cronJob.name + " is executing")

        #run the command                    
        xbmc.executebuiltin(cronJob.command)
