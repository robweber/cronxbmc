## Cron for Kodi

This addon consists of a plugin and a service that will let you schedule various Kodi functions to be run on timers of your choosing. Functions to run can basically be anything from the list of built in Kodi functions (http://kodi.wiki/view/List_of_built-in_functions). Examples include: 

* Rebooting
* Restart Kodi
* Take a Screenshot
* Run another Addon or Script
* Play Media
* Refresh RSS
* Send a Notification
* Set Volume
* Update Music/Video Libraries

Additionally you can specify your timer to display a notification when they run. 


### Running the addon

You can run the addon directly to bring up a GUI. The __Add Job__ option will let you create a job, setting its name, command, and cron schedule. Clicking on an existing job will allow you to edit it's properties. Finally bringing up the context menu on a selected job will let you delete it. 

By default the GUI will only show cron jobs created within the GUI. To edit jobs created anywhere on the system you can toggle the "show all" setting before loading the script. 

### Using as import in another addon

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

#add a job
job = CronJob()
job.name = "name"
job.command = "Shutdown"
job.expression = "0 0 * * *"
job.show_notification = "false"

jobId = manager.addJob(job)

#delete the previously defined job
manager.deleteJob(jobId)

```
### Important Note 
Now job Id did not change, you can keep it for reusing later (delete or update)  
Now If you try to add a job than have same expression and command than another addon have added before, it did not add again, it's ressources-consumming to add same cron  
It can avoid to fill cron file with same cron if addon caller have bad implementation of addingJob at each launch

### Manually Editing the cron.xml file

If you need to you can bypass the GUI and write the cron.xml file yourself, or via a script.  

The file should have the following layout:

```xml 
<cron>
 <job id="job id" name="Job Name" command="Kodi_Command()" expression="* * * * *" show_notification="true/false" />
</cron>
```

Using Cron:

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


