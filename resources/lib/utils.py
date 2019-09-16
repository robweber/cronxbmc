import xbmc
import xbmcgui
import xbmcaddon
    
__addon_id__= 'service.cronxbmc'
__Addon = xbmcaddon.Addon()

def addon_id():
    return __Addon.getAddonInfo('id')

def data_dir():
    return __Addon.getAddonInfo('profile')

def addon_dir():
    return __Addon.getAddonInfo('path')

def log(message,loglevel=xbmc.LOGNOTICE):
    xbmc.log(encode(__addon_id__ + "-" + __Addon.getAddonInfo('version') + " : " + message),level=loglevel)

def showNotification(title,message):
    xbmcgui.Dialog().notification(encode(getString(30000)),encode(message),time=4000,icon=xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/images/icon.png"),sound=False)

def setSetting(name,value):
    __Addon.setSetting(name,value)

def getSetting(name):
    return __Addon.getSetting(name)

def getString(string_id):
    return __Addon.getLocalizedString(string_id)

def getRegionalTimestamp(date_time,dateformat=['dateshort']):
    result = ''
    
    for aFormat in dateformat:
        result = result + ("%s " % date_time.strftime(xbmc.getRegion(aFormat)))
        
    return result.strip()

def encode(string):
    result = ''

    try:
        result = string.encode('UTF-8','replace')
    except UnicodeDecodeError:
        result = 'Unicode Error'
    
    return result
