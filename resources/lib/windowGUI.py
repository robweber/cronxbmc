import sys
import os
import xbmc
import xbmcgui
import xbmcaddon
import traceback
from service import CronXbmc, CronJob
from resources.lib.cronStringBuilderDialog import cronBuildGUI

__addon_id__ = "service.cronxbmc"
__Addon__ = xbmcaddon.Addon(__addon_id__)
__cwd__        = __Addon__.getAddonInfo('path')

# Skin ID's
# Main Control
NAME_EDIT_BOX      = 51
COMMAND_EDIT_BOX   = 52
TIME_EDIT_BOX      = 53
CRON_TIME_BUTTON   = 57
NOTIFICATION_RADIO = 54
ADDJOB_BUTTON      = 55
CLEAR_BUTTON       = 56
MAIN_CONTROL       = 60
STATUS_LABEL       = 100
CRON_LIST          = 120
SCROLL_BAR         = 121

# Modify Control
MODIFY_CONTROL            = 61
MODIFY_NAME_EDIT_BOX      = 63
MODIFY_COMMAND_EDIT_BOX   = 64
MODIFY_TIME_EDIT_BOX      = 65
MODIFY_NOTIFICATION_RADIO = 66
MODIFY_SUBMIT_BUTTON      = 67
MODIFY_DELETE_BUTTON      = 68
MODIFY_ID_LABEL           = 69

TEXT_INPUTS = (NAME_EDIT_BOX, COMMAND_EDIT_BOX, TIME_EDIT_BOX, MODIFY_NAME_EDIT_BOX, MODIFY_COMMAND_EDIT_BOX, MODIFY_TIME_EDIT_BOX)
# Action ID's
CANCEL_DIALOG      = ( 9, 10, 92, 216, 247, 257, 275, 61467, 61448, )
ACTION_SELECT_ITEM           = 7
ACTION_MOUSE_LEFT_CLICK      = 100
ACTION_MOUSE_RIGHT_CLICK     = 101
ACTION_MOUSE_MIDDLE_CLICK    = 102
ACTION_MOUSE_DOUBLE_CLICK    = 103
ACTION_MOUSE_WHEEL_UP        = 104
ACTION_MOUSE_WHEEL_DOWN      = 105
ACTION_MOUSE_DRAG            = 106
ACTION_MOUSE_MOVE            = 107
ACTION_MOUSE_END             = 109

class windowGUI( xbmcgui.WindowXMLDialog ):
    
    def __init__( self, *args, **kwargs ):
      self.cronxbmc = CronXbmc()
      self.lastClickedControl  = 0
      self.modifyControlActive = False
      self.updated = {}
      pass

    def onInit( self ):  
      self.setup_all()

    def setup_all( self ):
      self.setInputsToDefault()
      self.getControl( MODIFY_CONTROL ).setVisible(False)
      self.getControl( CRON_LIST ).reset()
      
      try:
          cron_jobs = self.cronxbmc.readCronFile()
          try:
            iID = 0
            for i in cron_jobs:
              print iID
              title = i.name
              nextTime = self.cronxbmc.nextRun(i)
              listitem = xbmcgui.ListItem( label=title, label2=nextTime) 
              listitem.setProperty( "command", i.command )
              listitem.setProperty( "cronExpre", i.expression )
              listitem.setProperty( "notification", i.show_notification )
              listitem.setProperty( "iID", str(iID) )
              self.getControl( CRON_LIST ).addItem( listitem )
              iID = iID + 1
          except:
            traceback.print_exc()
          self.setFocus( self.getControl( CRON_LIST ) )
          self.getControl( CRON_LIST ).selectItem( 0 )
      except:
        pass
    
    def onClick( self, controlId ):
      self.lastClickedControl = controlId
      cntrl = self.getControl( controlId )
      if (controlId == NOTIFICATION_RADIO):
          cntrl.setSelected(not (cntrl.isSelected()))
      elif (controlId == ADDJOB_BUTTON):
          newJob = CronJob()
          newJob.name = self.getControl( NAME_EDIT_BOX ).getText()
          newJob.command = self.getControl( COMMAND_EDIT_BOX ).getText()
          #newJob.expression = self.getControl( TIME_EDIT_BOX ).getText()
          newJob.expression = self.getControl( CRON_TIME_BUTTON ).getLabel()
          newJob.show_notification = "True" if self.getControl( NOTIFICATION_RADIO ).isSelected() else "False"
          self.cronxbmc.writeCronFile(newJob)
          self.setInputsToDefault()
          self.setup_all()
      elif (controlId == CLEAR_BUTTON):
          self.setInputsToDefault()
      elif (controlId == CRON_LIST):
          selItem = cntrl.getSelectedItem()
          self.getControl( MODIFY_NAME_EDIT_BOX ).setText(selItem.getLabel())
          self.getControl( MODIFY_COMMAND_EDIT_BOX ).setText(selItem.getProperty( "command" ))
          self.getControl( MODIFY_TIME_EDIT_BOX ).setText(selItem.getProperty( "cronExpre" ))
          tmpNotR = False
          if selItem.getProperty( "notification" ) == "true":
            tmpNotR = True
          self.getControl( MODIFY_NOTIFICATION_RADIO ).setSelected(tmpNotR)
          self.getControl( MODIFY_ID_LABEL ).setLabel(selItem.getProperty( "iID" ))
          self.toggleModifyControl()
      elif (controlId == MODIFY_SUBMIT_BUTTON):
          modJob = CronJob()
          iID = int(self.getControl( MODIFY_ID_LABEL ).getLabel())
          modJob.name = self.getControl( MODIFY_NAME_EDIT_BOX ).getText()
          modJob.command = self.getControl( MODIFY_COMMAND_EDIT_BOX ).getText()
          modJob.expression = self.getControl( MODIFY_TIME_EDIT_BOX ).getText()
          modJob.show_notification = "True" if self.getControl( MODIFY_NOTIFICATION_RADIO ).isSelected() else "False"
          self.cronxbmc.writeCronFile(modJob,iID)
          self.toggleModifyControl()
      elif (controlId == MODIFY_DELETE_BUTTON):
          iID = int(self.getControl( MODIFY_ID_LABEL ).getLabel())
          self.cronxbmc.deleteJob(iID)
          self.toggleModifyControl()
      elif (controlId == CRON_TIME_BUTTON):
          ui = cronBuildGUI( "cronStringBuilder.xml" , __cwd__, "Default")
          obj = {'saveLbl' : 57}
          if 'cron' in self.updated:
            obj['cronString'] = self.updated['cron']
          ui.setStuff(self, obj)
          ui.doModal()
          del ui
          
    def setInputsToDefault(self):
        self.getControl( NAME_EDIT_BOX ).setText("")
        self.getControl( COMMAND_EDIT_BOX ).setText("")
        self.getControl( TIME_EDIT_BOX ).setText("")
        self.getControl( CRON_TIME_BUTTON ).setLabel("Enter Cron Time")
        self.getControl( NOTIFICATION_RADIO ).setSelected(True)
        self.updated = {}
        
    def onFocus( self, controlId ):
      self.controlId = controlId
          
    def toggleModifyControl(self):
      if (self.modifyControlActive):
        self.getControl( MODIFY_CONTROL ).setVisible(False)
        self.setFocus( self.getControl( CRON_LIST ) )
        self.modifyControlActive = False
        self.setup_all()
      else:
        self.getControl( MODIFY_CONTROL ).setVisible(True)
        self.setFocus( self.getControl( MODIFY_CONTROL ) )
        self.modifyControlActive = True
    
    def onAction( self, action ):
      try:
        if ( action.getId() in CANCEL_DIALOG):
          if (self.modifyControlActive):
            self.toggleModifyControl()
          elif (self.controlId in TEXT_INPUTS):
            pass
          else:
            self.close()
        elif (action.getId() in (ACTION_SELECT_ITEM, ACTION_MOUSE_LEFT_CLICK)):
          if (self.lastClickedControl == NOTIFICATION_RADIO):
            cntrl = self.getControl( NOTIFICATION_RADIO )
            cntrl.setSelected(not (cntrl.isSelected()))
          self.lastClickedControl = 0
      except:
        pass
      
    
