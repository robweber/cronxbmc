# Cron for Kodi
![Kodi Version](https://img.shields.io/endpoint?url=https%3A%2F%2Fweberjr.com%2Fkodi-shield%2Fversion%2Frobweber%2Fcronxbmc%2Fmatrix%2Ftrue%2Ftrue)
[![Build Status](https://img.shields.io/travis/com/robweber/cronxbmc/matrix)](https://travis-ci.com/github/robweber/cronxbmc)
[![License](https://img.shields.io/github/license/robweber/cronxbmc)](https://github.com/robweber/cronxbmc/blob/master/LICENSE.txt)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

This addon consists of a plugin and a service that will let you schedule various Kodi functions to be run on timers of your choosing. Functions to run can basically be anything from the list of [built in](http://kodi.wiki/view/List_of_built-in_functions) Kodi functions or any [JSON-RPC methods](https://kodi.wiki/view/JSON-RPC_API/v12). Examples include:

* Rebooting
* Restart Kodi
* Take a Screenshot
* Run another Addon or Script
* Play Media
* Refresh RSS
* Send a Notification
* Set Volume
* Update Music/Video Libraries
* Playing specific video or audio file

Additionally you can specify your timer to display a notification when they run.


## Running the addon

You can run the addon directly to bring up a GUI. The __Add Job__ option will let you create a job, setting its name, type, command, and cron schedule. Clicking on an existing job will allow you to edit it's properties. Bringing up the context menu on a selected job will let you delete it. All of the job attributes are pretty self-explanatory, with the exception of the Run If Skipped option. This is meant to ensure a job is run if it's run time is skipped due to Kodi not being on at that time. This is similar to the ```@reboot``` attribute in some cron daemons. At startup any skipped jobs where this is set to "true" will be executed.

By default the GUI will only show cron jobs created within the GUI. To edit jobs created anywhere on the system you can toggle the "show all" setting before loading the script.

## Using as import in another addon

If you want to schedule something as part of your own addon you can import the CronManager class as an Kodi addon module. This will only load jobs created by your specific addon. To do this first add the following to your addon.xml file:

```xml
<import addon="service.cronxbmc" version="Current.Version.Number" />
```

From within your addon import the required classes and modify jobs using the following example:


```python
from cron import CronManager,CronJob

manager = CronManager()

#get jobs
jobs = manager.getJobs()

#get a specific job with a known id
job = manager.getJob(id)

#delete a job
manager.deleteJob(job.id)

#add a job
job = CronJob()
job.name = "name"
job.command_type = "json"  # this is set to "built-in" by default
job.command = '{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.Clean", "params": {"showdialogs": true, "content": "movies"}}'
job.expression = "0 0 * * *"
job.show_notification = "false"

manager.addJob(job) #call this to create new or update an existing job

```

Do not attempt to assign a job ID manually. For a new job leave the ID as is, for a current job just call ```manager.addJob()``` and the id will be used to update the correct entry. Refresh jobs ```jobs = manager.getJobs()``` will pull in any new jobs that may have been added via other methods.


## Manually Editing the cron.xml file

If you need to you can bypass the GUI and write the cron.xml file yourself, or via a script.  

The file should have the following layout:

```xml
<cron>
 <job name="Job Name" command_type="built-in" command="Kodi_Command()" expression="* * * * *" show_notification="true/false" id="5" run_if_skipped="false" last_run="0" />
</cron>
```

If editing the file directly make sure you set a job id that is different than any other in the file (typically just a higher integer than any other job). Also note that the ```last_run``` value will be automatically updated as the program executes. Make sure you don't touch this value if updating the file.

## Using Cron

A Cron expression is made up for 5 parts (see below). Read up on cron(http://en.wikipedia.org/wiki/Cron) for more information on how to create these expressions.

    .--------------- minute (0 - 59)
    |   .------------ hour (0 - 23)
    |   |   .--------- day of month (1 - 31)
    |   |   |   .------ month (1 - 12) or Jan, Feb ... Dec
    |   |   |   |  .---- day of week (0 - 6) or Sun(0 or 7), Mon(1) ... Sat(6)
    V   V   V   V  V
    *   *   *   *  *
Example:
	0 */5 ** 1-5 - runs every five hours Monday - Friday
	0,15,30,45 0,15-18 * * * - runs every quarter hour during midnight hour and 3pm-6pm
