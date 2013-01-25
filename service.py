import time
import xbmc
import xbmcaddon
import xml.dom.minidom
import datetime
import os
from resources.lib.croniter import croniter

class CronJob:
    def __init__( self):
        self.name = ""
        self.command = ""
        self.expression = []
        self.show_notification = "false"
        
class CronXbmc:
    addon_id = "service.cronxbmc"
    Addon = xbmcaddon.Addon(addon_id)
    datadir = Addon.getAddonInfo('profile')
    addondir = Addon.getAddonInfo('path')
    sleep_time = 10
    last_check = -1
    
    def runProgram(self):
        #run until XBMC quits
        while(not xbmc.abortRequested):

            structTime = time.localtime()
            now = time.time()
            
            #only do all this if we are in a new minute
            if(structTime[4] != self.last_check):
                self.last_check = structTime[4]

                #get a list of all the cron jobs
                cron_jobs = self.readCronFile()

                for command in cron_jobs:
                    #create a cron expression for this command
                    cron_exp = croniter(command.expression,datetime.datetime.fromtimestamp(now - 60))
                    self.nextRun(command)
                    runTime = cron_exp.get_next(float);
                    #if this command should run then run it
                    if(runTime <= now):
                        self.runJob(command)
                        self.log(command.name + " will run again on " + datetime.datetime.fromtimestamp(cron_exp.get_next(float)).strftime('%m-%d-%Y %H:%M'))

            #get as close to the top of each minute as we can
            self.sleep_time = 10 - (time.time() % 60 % 10)
            if(int(self.sleep_time) == 0):
                self.sleep_time = 10
                
            time.sleep(self.sleep_time)

    def runJob(self,cronJob,override_notification = False):
        self.log("running command " + cronJob.name)

        if(cronJob.show_notification == "true" or override_notification):
            #show a notification that this command is running
            xbmc.executebuiltin("Notification(Cron XBMC," + cronJob.name + " is executing,2000," + xbmc.translatePath(self.addondir + "/icon.png") + ")")

        #run the command                    
        xbmc.executebuiltin(cronJob.command)
        
    def readCronFile(self):
        if(not os.path.exists(xbmc.translatePath(self.datadir))):
            os.makedirs(xbmc.translatePath(self.datadir))

        adv_jobs = []
        try:
            doc = xml.dom.minidom.parse(xbmc.translatePath(self.datadir + "cron.xml"))

            for node in doc.getElementsByTagName("job"):
                tempJob = CronJob()
                tempJob.name = str(node.getAttribute("name"))
                tempJob.command = str(node.getAttribute("command"))
                tempJob.expression = str(node.getAttribute("expression"))
                tempJob.show_notification = str(node.getAttribute("show_notification"))
                
                adv_jobs.append(tempJob)

        except IOError:
            #the file doesn't exist, return empty array
            doc = xml.dom.minidom.Document()
            rootNode = doc.createElement("cron")
            doc.appendChild(rootNode)
            #write the file
            f = open(xbmc.translatePath(self.datadir + "cron.xml"),"w")
            doc.writexml(f,"   ")
            f.close()
            

        return adv_jobs
    def deleteJob(self,iID):
        doc = xml.dom.minidom.parse(xbmc.translatePath(self.datadir + "cron.xml"))
        rootNode = doc.getElementsByTagName("cron")[0]
        oldJob = rootNode.getElementsByTagName("job")[iID]
        rootNode.removeChild(oldJob)
        f = open(xbmc.translatePath(self.datadir + "cron.xml"),"w")
        doc.writexml(f,"   ")
        f.close()
    def writeCronFile(self,job,overwrite=-1):
        #read in the cron file
        try:
            doc = xml.dom.minidom.parse(xbmc.translatePath(self.datadir + "cron.xml"))
            rootNode = doc.getElementsByTagName("cron")[0]
            
            #create the child
            newChild = doc.createElement("job")
            newChild.setAttribute("name",job.name)
            newChild.setAttribute("expression",job.expression)
            newChild.setAttribute("command",job.command)
            newChild.setAttribute("show_notification",job.show_notification)
        
            if overwrite >= 0:
                #we are modifying an existing job
                oldJob = rootNode.getElementsByTagName("job")[overwrite]
                rootNode.replaceChild(newChild,oldJob)

            else:
                #we are writing a new job
                rootNode.appendChild(newChild)

            #write the file
            f = open(xbmc.translatePath(self.datadir + "cron.xml"),"w")
            doc.writexml(f,"   ")
            f.close()
                                        
        except IOError:
            self.log("error writing cron file")

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
        
    
    def log(self,message):
        xbmc.log('service.cronxbmc: ' + message)

