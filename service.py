import time
import xbmc
import xml.dom.minidom
import datetime
import os
from resources.lib.croniter import croniter
import resources.lib.utils as utils

class CronJob:
    def __init__( self):
        self.name = ""
        self.command = ""
        self.expression = []
        self.show_notification = "false"
        
class CronXbmc:
    last_check = -1
    
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
                cron_jobs = self.readCronFile()

                for command in cron_jobs:
                    #create a cron expression for this command
                    cron_exp = croniter(command.expression,datetime.datetime.fromtimestamp(now - 60))
                    
                    runTime = cron_exp.get_next(float);
                    #if this command should run then run it
                    if(runTime <= now):
                        self.runJob(command)
                        utils.log(command.name + " will run again on " + datetime.datetime.fromtimestamp(cron_exp.get_next(float)).strftime('%m-%d-%Y %H:%M'))
                
            if(monitor.waitForAbort(10)):
                break;

    def runJob(self,cronJob,override_notification = False):
        utils.log("running command " + cronJob.name)

        if(cronJob.show_notification == "true" or override_notification):
            #show a notification that this command is running
            utils.showNotification("Cron", cronJob.name + " is executing")

        #run the command                    
        xbmc.executebuiltin(cronJob.command)
        
    def readCronFile(self):
        if(not os.path.exists(xbmc.translatePath(utils.data_dir()))):
            os.makedirs(xbmc.translatePath(utils.data_dir()))

        adv_jobs = []
        try:
            doc = xml.dom.minidom.parse(xbmc.translatePath(utils.data_dir() + "cron.xml"))
            for node in doc.getElementsByTagName("job"):
                tempJob = CronJob()
                tempJob.name = str(node.getAttribute("name"))
                tempJob.command = str(node.getAttribute("command"))
                tempJob.expression = str(node.getAttribute("expression"))
                tempJob.show_notification = str(node.getAttribute("show_notification"))
                tempJob.id = str(len(adv_jobs))
                adv_jobs.append(tempJob)

        except IOError:
            #the file doesn't exist, return empty array
            doc = xml.dom.minidom.Document()
            rootNode = doc.createElement("cron")
            doc.appendChild(rootNode)
            #write the file
            f = open(xbmc.translatePath(utils.data_dir() + "cron.xml"),"w")
            doc.writexml(f,"   ")
            f.close()
            

        return adv_jobs
    
    def deleteJob(self,iID):
        doc = xml.dom.minidom.parse(xbmc.translatePath(utils.data_dir() + "cron.xml"))
        rootNode = doc.getElementsByTagName("cron")[0]
        oldJob = rootNode.getElementsByTagName("job")[iID]
        rootNode.removeChild(oldJob)
        f = open(xbmc.translatePath(utils.data_dir() + "cron.xml"),"w")
        doc.writexml(f,"   ")
        f.close()
        
    def writeCronFile(self,job,overwrite=-1):
        #read in the cron file
        try:
            doc = xml.dom.minidom.parse(xbmc.translatePath(utils.data_dir() + "cron.xml"))
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
            f = open(xbmc.translatePath(utils.data_dir() + "cron.xml"),"w")
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
        
#run the program
utils.log("Cron for Kodi service starting....")
CronXbmc().runProgram()

