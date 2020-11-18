import time
import xbmc
import xbmcvfs
import xml.dom.minidom
import datetime
from resources.lib.croniter import croniter
from . import utils as utils


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
    jobs = {}  # format {job_id:job_obj}
    last_read = time.time()

    def __init__(self):
        self.jobs = self._readCronFile()

    def addJob(self, job):

        try:
            # verify the cron expression here, throws ValueError if wrong
            croniter(job.expression)
        except:
            # didn't work
            return False

        # set the addon id if there isn't one
        if(job.addon is None):
            job.addon = utils.addon_id()

        self._refreshJobs()

        if(job.id >= 0):
            # replace existing job
            self.jobs[job.id] = job
        else:
            # set the job id
            job.id = self._nextId()

            # add a new job
            self.jobs[job.id] = job

        # write the file
        self._writeCronFile()

        return True

    def deleteJob(self, jId):
        self._refreshJobs()

        self.jobs.pop(jId)

        self._writeCronFile()

    def getJobs(self, show_all=False):
        self._refreshJobs()

        if(show_all != 'true'):
            # filter on currently loaded addon
            result = list(filter(lambda x: x.addon == utils.addon_id(), self.jobs.values()))
        else:
            result = self.jobs.values()

        return result

    def getJob(self, jId):
        self._refreshJobs()

        return self.jobs[jId]

    def nextRun(self, cronJob):
        # create a cron expression
        cron_exp = croniter(cronJob.expression, datetime.datetime.fromtimestamp(time.time()))

        # compare now with next date
        nextRun = cron_exp.get_next(float)
        cronDiff = nextRun - time.time()
        hours = int((cronDiff / 60) / 60)
        minutes = int(cronDiff / 60 - hours * 60)

        # we always have at least one minute
        if minutes == 0:
            minutes = 1

        result = str(hours) + " h " + str(minutes) + " m"

        if hours == 0:
            result = str(minutes) + " m"
        elif hours > 36:
            # just show the date instead
            result = utils.getRegionalTimestamp(datetime.datetime.fromtimestamp(nextRun), ['dateshort', 'time'])
        elif hours > 24:
            days = int(hours / 24)
            hours = hours - days * 24
            result = str(days) + " d " + str(hours) + " h " + str(minutes) + " m"

        return result

    def _nextId(self):
        result = 0

        # find the next largest id
        for k in self.jobs.keys():
            if(k >= result):
                result = k + 1

        return result

    def _refreshJobs(self):

        # check if we should read in a new files list
        stat_file = xbmcvfs.Stat(xbmc.translatePath(self.CRONFILE))

        if(stat_file.st_mtime() > self.last_read):
            utils.log("File update, loading new jobs")
            # update the file
            self.jobs = self._readCronFile()
            self.last_read = time.time()

    def _readCronFile(self):
        if(not xbmcvfs.exists(xbmc.translatePath('special://profile/addon_data/service.cronxbmc/'))):
            xbmcvfs.mkdir(xbmc.translatePath('special://profile/addon_data/service.cronxbmc/'))

        adv_jobs = {}
        try:
            doc = xml.dom.minidom.parse(xbmc.translatePath(self.CRONFILE))

            for node in doc.getElementsByTagName("job"):
                tempJob = CronJob()
                tempJob.name = str(node.getAttribute("name"))
                tempJob.command = str(node.getAttribute("command"))
                tempJob.expression = str(node.getAttribute("expression"))
                tempJob.show_notification = str(node.getAttribute("show_notification"))

                # catch for older cron.xml where no id was saved
                if(node.getAttribute('id') == ''):
                    tempJob.id = len(adv_jobs)
                else:
                    tempJob.id = int(node.getAttribute('id'))

                # catch for older cron.xml files
                if(node.getAttribute('addon') != ''):
                    tempJob.addon = str(node.getAttribute('addon'))
                else:
                    tempJob.addon = utils.__addon_id__

                utils.log(tempJob.name + " " + tempJob.expression + " loaded")
                adv_jobs[tempJob.id] = tempJob

        except IOError:
            # the file doesn't exist, return empty array
            doc = xml.dom.minidom.Document()
            rootNode = doc.createElement("cron")
            doc.appendChild(rootNode)
            # write the file
            f = xbmcvfs.File(xbmc.translatePath(self.CRONFILE), "w")
            doc.writexml(f, "   ")
            f.close()

        return adv_jobs

    def _writeCronFile(self):

        # write the cron file in full
        try:
            doc = xml.dom.minidom.Document()
            rootNode = doc.createElement("cron")
            doc.appendChild(rootNode)

            for aJob in self.jobs.values():

                # create the child
                newChild = doc.createElement("job")
                newChild.setAttribute('id', str(aJob.id))
                newChild.setAttribute("name", aJob.name)
                newChild.setAttribute("expression", aJob.expression)
                newChild.setAttribute("command", aJob.command)
                newChild.setAttribute("show_notification", aJob.show_notification)
                newChild.setAttribute("addon", aJob.addon)

                rootNode.appendChild(newChild)

            # write the file
            f = xbmcvfs.File(xbmc.translatePath(self.CRONFILE), "w")
            doc.writexml(f, "   ")
            f.close()

        except IOError:
            utils.log("error writing cron file", xbmc.LOGERROR)


class CronService:
    last_check = -1
    manager = None

    def __init__(self):
        self.manager = CronManager()

    def runProgram(self):
        monitor = xbmc.Monitor()

        # run until abort requested
        while(True):

            structTime = time.localtime()
            now = time.time()
            # only do all this if we are in a new minute
            if(structTime[4] != self.last_check):
                self.last_check = structTime[4]

                # get a list of all the cron jobs
                cron_jobs = self.manager.getJobs()

                for command in cron_jobs:
                    # create a cron expression for this command
                    cron_exp = croniter(command.expression, datetime.datetime.fromtimestamp(now - 60))

                    runTime = cron_exp.get_next(float)
                    # if this command should run then run it
                    if(runTime <= now):
                        self.runJob(command)
                        utils.log(command.name + " will run again on " + utils.getRegionalTimestamp(datetime.datetime.fromtimestamp(cron_exp.get_next(float)), ['dateshort', 'time']))

            # calculate the sleep time (next minute)
            currentSec = datetime.datetime.now()
            if(monitor.waitForAbort(60 - currentSec.second)):
                break

    def runJob(self, cronJob, override_notification=False):
        utils.log("running command " + cronJob.name + " for addon " + cronJob.addon)

        if(cronJob.show_notification == "true" or override_notification):
            # show a notification that this command is running
            utils.showNotification("Cron", cronJob.name + " is executing")

        # run the command
        xbmc.executebuiltin(cronJob.command)
