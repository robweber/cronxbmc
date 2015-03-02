
import xbmcaddon
from resources.lib.windowGUI import WindowGUI

__addon_id__ = "service.cronxbmc"
__Addon__ = xbmcaddon.Addon(__addon_id__)
__cwd__        = __Addon__.getAddonInfo('path')

def updateJobs():
    ui = WindowGUI( __cwd__)
    del ui

updateJobs()

    


