******************************************************************************************
** THIS ADDON IS UNFINISHED **

The intended features of the plugin part of this addon have not been finished. You will need to manually configure your own cron expressions in the cron.xml file that will be created in the addon_data directory of your user profile. The file should have the following layout:

<cron>
 <job name="Job Name" command="XBMC_Command()" expression="* * * * *" show_notification="true/false" />
</cron>
*********************************************************************************************

Cron Xbmc

This addon consists of a plugin and a service that will let you schedule various XBMC functions to be run on timers of your choosing. Functions to run can basically be anything from the list of built in XBMC functions (http://wiki.xbmc.org/index.php?title=List_of_built-in_functions). Examples include: 

Rebooting
Restart XBMC
Take a Screenshot
Run another Addon or Script
Play Media
Refresh RSS
Send a Notification
Set XBMC Volume
Update Music/Video Libraries

Additionally you can specify your timer to display an XBMC notification when they run. 


Using Cron:

A Cron expression is made up for 5 parts (see below). Read up on cro(http://en.wikipedia.org/wiki/Cron) for more information on how to create these expressions.

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


