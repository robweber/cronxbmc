import xbmcgui
import xbmcaddon
import traceback
from cron import CronManager, CronJob
from operator import itemgetter

# Skin ID's
# Main Control
NAME_EDIT_BOX      = 51
COMMAND_EDIT_BOX   = 52
TIME_EDIT_BTN      = 57
NOTIFICATION_RADIO = 54
ADDJOB_BUTTON      = 55
CLEAR_BUTTON       = 56
STATUS_LABEL       = 100

# Modify Control
MODIFY_GRP_BTNS    = 76
MODIFY_SUBMIT_BTN  = 70
MODIFY_CANCEL_BTN  = 71


TEXT_INPUTS = (NAME_EDIT_BOX, COMMAND_EDIT_BOX, TIME_EDIT_BTN)
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

SkinName = "Default"
MainWindowXML = "script-cron-main.xml"
SelectDialogXML = 'script-cron-DialogContextMenu.xml'
CronMakerXML = 'script-cron-StringBuilder.xml'

__addon_id__ = "service.cronxbmc"
__Addon__ = xbmcaddon.Addon(__addon_id__)
__cwd__        = __Addon__.getAddonInfo('path')

class WindowGUI:
  def __init__( self, cwd ):
    __cwd__ = cwd
    ui = MainWindow( MainWindowXML , cwd, SkinName)
    ui.doModal()
    del ui

class ControlObject:
  def __init__(self, aType, aObjId, aControlId, aParent, defOptions={}):
    self.objectId = aObjId
    self.controlId = aControlId
    self.type = aType
    self.parent = aParent
    self.options = defOptions
    self.reset()
        
  def reset(self):
    if 'label' in self.options:
      self.setLabel(self.options['label'])
    if 'text' in self.options:
      self.setText(self.options['text'])
    if 'selected' in self.options:
      self.setSelected(self.options['selected'])
    if 'visible' in self.options:
      self.setVisible(self.options['visible'])
      
    if self.type == 'list':
      self.listReset()
    elif 'spincontrol' == self.type:
      self.initSpinControl()
    elif 'selectcontrol' == self.type:
      self.initSelectControl()
      
    ''' Keep Last '''  
    if 'onLoad' in self.options:
      self.options['onLoad'](self)
      
  def initSelectControl(self):
    self.options['selectCurList'] = []
    selcAddControl = self.parent.addMyControl('button', self.options['selectadd'], {
      'onClick':self.selectControlChange,
    })
    selcDelControl = self.parent.addMyControl('button', self.options['selectdel'], {
      'onClick':self.selectControlChange,
    })
    self.options['listcontrol'] = self.parent.addMyControl('list', self.options['selectlist'])
    self.options['ealabel'] = self.parent.addMyControl('label', self.options['selectlabel'])
    
  def selectControlChange(self, control):
    spnObj = self.options['spinControl']
    curSelected = spnObj.options['spinlist'][spnObj.options['spinCurPos']]
    existsAtIndex = -1
    for i in range(0,len(self.options['selectCurList'])):
      if self.options['selectCurList'][i] == curSelected:
        existsAtIndex = i
        break
        
    if control.controlId == self.options['selectadd']:
      if existsAtIndex < 0:
        self.options['selectCurList'].append(curSelected)
        self.options['selectCurList'] = sorted(self.options['selectCurList'], key=itemgetter('value')) 
    else:
      if existsAtIndex >= 0:
        self.options['selectCurList'].pop(existsAtIndex)
    
    self.options['listcontrol'].reset()
    for i in self.options['selectCurList']:
      listitem = xbmcgui.ListItem( label=i['name']) 
      self.options['listcontrol'].addListItem(listitem)
    
    if 'updatedcb' in self.options:
      try:
        self.options['updatedcb'](self)
      except:
        traceback.print_exc()
        
    #self.options['spinLabel'].setLabel(self.options['spinlist'][self.options['spinCurPos']]['name'])
  def setSelectControlList(self, list):
    saveList = []
    spnObj = self.options['spinControl']
    spnList = spnObj.options['spinlist']
    
    for i in list:
      for b in spnList:
        if i == b['value']:
          saveList.append(b)
          break
    self.options['selectCurList'] = saveList
    self.options['listcontrol'].reset()      
    for i in self.options['selectCurList']:
      listitem = xbmcgui.ListItem( label=i['name']) 
      self.options['listcontrol'].addListItem(listitem)
    
  def initSpinControl(self):
    self.options['spinCurPos'] = 0
    for i in self.options['spinlist']:
      if 'value' not in i:
        i['value'] = i['name']
      elif 'name' not in i:
        i['name'] = i['value']
      i['name'] = str(i['name'])      
    self.options['spinListSize'] = len(self.options['spinlist'])
    lblControl = self.parent.addMyControl('label', self.options['spinlabel'])
    self.options['spinLabel'] = lblControl
    self.options['spinLabel'].setLabel(self.options['spinlist'][self.options['spinCurPos']]['name'])
    spinUpControl = self.parent.addMyControl('button', self.options['spinup'], {
      'onClick':self.spinControlChange,
    })
    spinDwnControl = self.parent.addMyControl('button', self.options['spindown'], {
      'onClick':self.spinControlChange,
    })
    
  def spinControlChange(self, control):
    if control.controlId == self.options['spinup']:
      self.options['spinCurPos'] += 1
      if self.options['spinCurPos'] >= self.options['spinListSize']:
        self.options['spinCurPos'] = 0
    else:
      self.options['spinCurPos'] -= 1
      if self.options['spinCurPos'] < 0:
        self.options['spinCurPos'] = self.options['spinListSize'] - 1
    self.options['spinLabel'].setLabel(self.options['spinlist'][self.options['spinCurPos']]['name'])
    
    if 'updatedcb' in self.options:
      try:
        self.options['updatedcb'](self)
      except:
        traceback.print_exc()
        
  def setSpinControlValue(self,value):
    for i in range(0,len(self.options['spinlist'])):
      if self.options['spinlist'][i]['value'] == int(value):
        self.options['spinCurPos'] = i
        break
    self.options['spinLabel'].setLabel(self.options['spinlist'][self.options['spinCurPos']]['name'])    
    
  
  def listReset(self):
    try:
      self.parent.getControl( self.controlId ).reset()
      return True
    except:
      traceback.print_exc()
    return False
      
  def setVisible(self, setting):
    try:
      self.parent.getControl( self.controlId ).setVisible( setting )
      return True
    except:
      traceback.print_exc()
      return False
      
  def setText(self, setting):
    try:
      self.parent.getControl( self.controlId ).setText( setting )
      return True
    except:
      traceback.print_exc()
      return False
      
  def getDefaultOption(self, setting):
    if setting in self.options:
      return self.options[setting]
    else:
      return ''
  
  def setSelected(self, setting):  
    try:
      self.parent.getControl( self.controlId ).setSelected( setting )
      return True
    except:
      traceback.print_exc()
      return False
      
  def setLabel(self, setting):
    try:
      self.parent.getControl( self.controlId ).setLabel( setting )
      return True
    except:
      traceback.print_exc()
      return False
      
  def addListItem(self, listitem):
    try:
      self.parent.getControl( self.controlId ).addItem( listitem )
      return True
    except:
      traceback.print_exc()
      return False
      
  def getCurListItem(self):
    try:
      return self.parent.getControl( self.controlId ).getSelectedItem()
    except:
      traceback.print_exc()
      return False
      
  def getObjectId(self):
    return self.objectId
    
  def getControlId(self):
    return self.controlId
    
  def click(self):
    if 'onClick' in self.options:
      try:
        self.options['onClick'](self)
      except:
        traceback.print_exc()
    
    if 'updatedcb' in self.options:
      try:
        self.options['updatedcb'](self)
      except:
        traceback.print_exc()
  
  def setOption(self, setting, value):
    try:
      self.options[setting] = value
      return True
    except:
      traceback.print_exc()
      return False
    
  
  def getValue(self):
    if self.type == 'label':
      return self.parent.getControl( self.controlId ).getLabel()
    elif self.type == 'editbox':
      return self.parent.getControl( self.controlId ).getText()
    elif self.type == 'button':
      return self.parent.getControl( self.controlId ).getLabel()
    elif self.type == 'radio':
      return self.parent.getControl( self.controlId ).isSelected()

class CommonWindow( xbmcgui.WindowXMLDialog ):
  def __init__( self, *args, **kwargs ):
    self.cronxbmc = CronManager()
    self.updated = {}
    self.glblObjs = []
    self.id2ObjMap = {}
    self.resettable = []
    self.controlInputs = []

  def addResettable(self, cntrl):
    self.resettable.append(cntrl.getObjectId())
    
  def resetControls(self, control=None):
    for i in self.resettable:
      self.glblObjs[i].reset()
      
  def onFocus( self, controlId ):
    pass
    
  def onAction( self, action ):
    if ( action.getId() in CANCEL_DIALOG):
      self.close()
    
  def onClick( self, controlId ):
    print 'click'
    control = self.findControl(controlId)
    
    if(not isinstance(control,(bool))):
        control.click()
    
  def addAsInput(self, control, validator=None):
    self.controlInputs.append({'objId' : control.getObjectId(), 'validator' : validator})
    
  def getInputVals(self):
    retDict = {}
    for i in self.controlInputs:
      valFunc = i['validator']
      control = self.glblObjs[i['objId']]
      inputVal = control.getValue()
      if valFunc is not None:
        valid = valFunc(inputVal, control)
        tmp = {}
        if valid:
          tmp =  {'inputVal' : inputVal, 'valid' : True}
        else:
          tmp =  {'valid' : False}
        retDict[control.getControlId()] = tmp
      else:
        tmp =  {'inputVal' : inputVal, 'valid' : True}
        retDict[control.getControlId()] = tmp
    print retDict
    return retDict
        
  
  def noneEmpty(self, testString, control):
    if (len(testString) > 0):
      if testString != control.getDefaultOption('label'):
        return True
    return False
    
  def findControl(self, controlId):
    try:
      return self.glblObjs[self.id2ObjMap[controlId]]
    except:
      traceback.print_exc()
      return False
    
  def addMyControl(self, type, controlId, defOptions={}, existingControl=False):
    objId = -1
    if existingControl:
      objId = defOptions.getId()
      cntrlObj = defOptions
    else:
      objId = len(self.glblObjs)
      cntrlObj = ControlObject(type, objId, controlId, self, defOptions)
      self.glblObjs.append(cntrlObj)
    
    self.id2ObjMap[controlId] = objId
    return cntrlObj
    
  def openSelectDialog(self, title, list):
    dia = SelectDialog(SelectDialogXML , __cwd__, SkinName, {
      'items':list,
    })
    dia.doModal()
    ret = dia.getSelectedVal()
    del dia
    return ret
  
class MainWindow( CommonWindow ):

  def onInit( self ):
    ''' Job Name '''
    cntrl = self.addMyControl('editbox', NAME_EDIT_BOX, {'text':''})
    self.addResettable(cntrl)
    self.addAsInput(cntrl, self.noneEmpty)
    
    ''' Command To Run '''
    cntrl = self.addMyControl('editbox', COMMAND_EDIT_BOX, {'text':''})
    self.addResettable(cntrl)
    self.addAsInput(cntrl, self.noneEmpty)
    
    ''' Cron Expression '''
    cntrl = self.addMyControl('button', TIME_EDIT_BTN, {
      'label' : 'Enter Cron Time',
      'onClick' : self.expMakerWindow,
    })
    self.addResettable(cntrl)
    self.addAsInput(cntrl, self.noneEmpty)
    
    ''' Show Notification '''
    cntrl = self.addMyControl('radio', NOTIFICATION_RADIO, {'selected' : True})
    self.addResettable(cntrl)
    self.addAsInput(cntrl)
    
    ''' Job List '''
    cntrl = self.addMyControl('list', 120, {
      'onLoad'  : self.fillCronTab,
      'onClick' : self.deleteOrModifyJob,
    })
    self.addResettable(cntrl)
    
    ''' Add Job '''
    cntrl = self.addMyControl('button', ADDJOB_BUTTON, {
      'onClick' : self.addNewJob,
    })
    
    ''' Clear Inputs '''
    cntrl = self.addMyControl('button', CLEAR_BUTTON, {
      'onClick' : self.resetControls,
    })
    
    ''' Modify Group '''
    cntrl = self.addMyControl('group', MODIFY_GRP_BTNS, {
      'visible' : False,
    })
    self.addResettable(cntrl)
    
    ''' Submit Modified '''
    cntrl = self.addMyControl('group', MODIFY_SUBMIT_BTN, {
      'onClick' : self.addNewJob,
    })
    
    ''' Cancel Modify '''
    cntrl = self.addMyControl('group', MODIFY_CANCEL_BTN, {
      'onClick' : self.resetControls,
    })
    
  def fillCronTab(self, control):
    cron_jobs = self.cronxbmc.getJobs()
    for i in cron_jobs:
      try:
        title = i.name
        nextTime = self.cronxbmc.nextRun(i)
        listitem = xbmcgui.ListItem( label=title, label2=nextTime) 
        listitem.setProperty( "command", i.command )
        listitem.setProperty( "cronExpre", i.expression )
        listitem.setProperty( "notification", i.show_notification )
        listitem.setProperty( "iID", str(i.id) )
        control.addListItem(listitem)
      except:
        traceback.print_exc()
  
  def expMakerWindow(self, control):
    dia = CronExpre(CronMakerXML , __cwd__, SkinName)
    cronStr = control.getValue()
    if len(cronStr) > 0:
      dia.setCronString(cronStr)
    dia.doModal()
    cronStr = dia.getCronString()
    if len(cronStr) > 0:
      control.setLabel(cronStr)
    del dia
    pass
    
  def deleteOrModifyJob(self, control):
    dia = self.openSelectDialog("Delete or Modify Job", ['Modify Job', 'Delete Job'])
    curListItem = control.getCurListItem()
    if dia == 0:
      ''' Modify Job '''
      for i in self.controlInputs:
        inpControl = self.glblObjs[i['objId']]
        
        if inpControl.getControlId() == NAME_EDIT_BOX:
          inpControl.setText(curListItem.getLabel())
          
        elif inpControl.getControlId() == COMMAND_EDIT_BOX:
          inpControl.setText(curListItem.getProperty( "command" ))
          
        elif inpControl.getControlId() == TIME_EDIT_BTN:
          inpControl.setLabel(curListItem.getProperty( "cronExpre" ))
          
        elif inpControl.getControlId() == NOTIFICATION_RADIO:
          if curListItem.getProperty( "notification" ) == "True":
            inpControl.setSelected(True)
          else:
            inpControl.setSelected(False)
      mdControl = self.findControl(MODIFY_SUBMIT_BTN)
      mdControl.setOption('jobId',curListItem.getProperty( "iID" ))
      mdControl = self.findControl(MODIFY_GRP_BTNS)
      mdControl.setVisible(True)
        
    elif dia == 1:
      ''' Delete Job '''
      self.cronxbmc.deleteJob(int(curListItem.getProperty( "iID" )))
      self.resetControls()
      pass
    
  def addNewJob(self, control):
    addJob = True
    newJob = CronJob()
    gotControlInputs = self.getInputVals()
    for inpK in gotControlInputs:
      if not gotControlInputs[inpK]['valid']:
        addJob = False
        break
      if inpK == NAME_EDIT_BOX:
        newJob.name = gotControlInputs[inpK]['inputVal']
      elif inpK == COMMAND_EDIT_BOX:
        newJob.command = gotControlInputs[inpK]['inputVal']
      elif inpK == TIME_EDIT_BTN:
        newJob.expression = gotControlInputs[inpK]['inputVal']
      elif inpK == NOTIFICATION_RADIO:
        if gotControlInputs[inpK]['inputVal']:
          newJob.show_notification = "True"
        else:
          newJob.show_notification = "False"
    if addJob:
      jobId = control.getDefaultOption('jobId')
      self.cronxbmc.addJob(newJob)
      self.resetControls()
    else:
      dialog = xbmcgui.Dialog()
      dialog.ok("ERROR", "Please fill out all fields to add a new job.")
    pass

class CronExpre( CommonWindow ):
  def __init__( self, *args, **kwargs ):
    self.cronxbmc = CronManager()
    self.updated = {}
    self.glblObjs = []
    self.id2ObjMap = {}
    self.resettable = []
    self.controlInputs = []
    self.mainCronString = "* * * * *"
    self.origCronString = ""
    
  def everyToggleSetup(self, group, controlId):
    evryCntrl = self.addMyControl('radio', controlId, {
      'cronString':'*',
      'updatedcb' : self.updatedGroup,
      'mainGroup' : group
    })
    
    return evryCntrl
  
  def nToggleSetup(self, group, nToggle, spinGrp, spinUp, spinDwn, spinLbl, spinList ):  
    nCntrl = self.addMyControl('radio', nToggle, {
      'cronString':'*/1',
      'updatedcb'   : self.updatedGroup,
      'mainGroup' : group
    })
    spnCntrl = self.addMyControl('spincontrol', spinGrp, {
      'spinup'   :spinUp,
      'spindown' :spinDwn,
      'spinlabel':spinLbl,
      'updatedcb':self.updatedGroup,
      'main':nCntrl,
      'spinlist' :spinList,
    })
    nCntrl.setOption('spincontrol', spnCntrl)
    return nCntrl
    
  def eachToggleSetup(self, group, eaToggle, spinGrp, spinUp, spinDwn, spinLbl, eaGrp, eaLbl, eaAdd, eaDel, eaList, spinList ):
    eaCntrl = self.addMyControl('radio', eaToggle, {
      'cronString'  :'',
      'updatedcb'   : self.updatedGroup,
      'mainGroup' : group
    })
    spnCntrl = self.addMyControl('spincontrol', spinGrp, {
      'spinup'   : spinUp,
      'spindown' : spinDwn,
      'spinlabel': spinLbl,
      'spinlist' : spinList
    })
    eaListCntrl = self.addMyControl('selectcontrol', eaGrp, {
      'selectlabel' : eaLbl,
      'selectadd'   : eaAdd,
      'selectdel'   : eaDel,
      'selectlist'  : eaList,
      'spinControl' : spnCntrl,
      'updatedcb'   : self.updatedGroup,
      'main'        : eaCntrl,
    })
    eaCntrl.setOption('selectcontrol', eaListCntrl)
    return eaCntrl
    
  def onInit( self ):
    mainGroups = []
    self.addMyControl('label', 1001)
    ''' Minute Group '''
    grpCntrl = self.addMyControl('radiogroup', 2000, {'cronStringIndex':0})
    ''' Every Min '''
    evryCntrl = self.everyToggleSetup(grpCntrl, 2100)
    ''' N Min '''
    nCntrl = self.nToggleSetup(grpCntrl, 2200, 2210, 2215, 2214, 2216, [
      {'value' : 1},{'value' : 2},{'value' : 3},{'value' : 4},{'value' : 5},{'value' : 6},{'value' : 7},{'value' : 8},{'value' : 9},{'value' : 10},
      {'value' : 11},{'value' : 12},{'value' : 13},{'value' : 14},{'value' : 15},{'value' : 16},{'value' : 17},{'value' : 18},{'value' : 19},{'value' : 20},
      {'value' : 21},{'value' : 22},{'value' : 23},{'value' : 24},{'value' : 25},{'value' : 26},{'value' : 27},{'value' : 28},{'value' : 29},{'value' : 30},
      {'value' : 31},{'value' : 32},{'value' : 33},{'value' : 34},{'value' : 35},{'value' : 36},{'value' : 37},{'value' : 38},{'value' : 39},{'value' : 40},
      {'value' : 41},{'value' : 42},{'value' : 43},{'value' : 44},{'value' : 45},{'value' : 46},{'value' : 47},{'value' : 48},{'value' : 49},{'value' : 50},
      {'value' : 51},{'value' : 52},{'value' : 53},{'value' : 54},{'value' : 55},{'value' : 56},{'value' : 57},{'value' : 58},{'value' : 59},
    ])    
    ''' Each Min '''
    eaCntrl = self.eachToggleSetup(grpCntrl, 2300, 2310, 2315, 2314, 2316, 2319, 2301, 2320, 2321, 2330, [
      {'value' : 0},{'value' : 1},{'value' : 2},{'value' : 3},{'value' : 4},{'value' : 5},{'value' : 6},{'value' : 7},{'value' : 8},{'value' : 9},{'value' : 10},
      {'value' : 11},{'value' : 12},{'value' : 13},{'value' : 14},{'value' : 15},{'value' : 16},{'value' : 17},{'value' : 18},{'value' : 19},{'value' : 20},
      {'value' : 21},{'value' : 22},{'value' : 23},{'value' : 24},{'value' : 25},{'value' : 26},{'value' : 27},{'value' : 28},{'value' : 29},{'value' : 30},
      {'value' : 31},{'value' : 32},{'value' : 33},{'value' : 34},{'value' : 35},{'value' : 36},{'value' : 37},{'value' : 38},{'value' : 39},{'value' : 40},
      {'value' : 41},{'value' : 42},{'value' : 43},{'value' : 44},{'value' : 45},{'value' : 46},{'value' : 47},{'value' : 48},{'value' : 49},{'value' : 50},
      {'value' : 51},{'value' : 52},{'value' : 53},{'value' : 54},{'value' : 55},{'value' : 56},{'value' : 57},{'value' : 58},{'value' : 59},
    ])
    self.toggleGroupSetup(grpCntrl, [evryCntrl, nCntrl, eaCntrl])
    mainGroups.append(grpCntrl)
    
    ''' Hour Group '''
    grpCntrl = self.addMyControl('radiogroup', 3000, {'cronStringIndex':1})
    evryCntrl = self.everyToggleSetup(grpCntrl, 3100)
    nCntrl = self.nToggleSetup(grpCntrl, 3200, 3210, 3215, 3214, 3216, [
      {'value' : 1},{'value' : 2},{'value' : 3},{'value' : 4},{'value' : 5},{'value' : 6},{'value' : 7},{'value' : 8},{'value' : 9},{'value' : 10},
      {'value' : 11},{'value' : 12},{'value' : 13},{'value' : 14},{'value' : 15},{'value' : 16},{'value' : 17},{'value' : 18},{'value' : 19},{'value' : 20},
      {'value' : 21},{'value' : 22},{'value' : 23},
    ])
    eaCntrl = self.eachToggleSetup(grpCntrl, 3300, 3310, 3315, 3314, 3316, 3319, 3301, 3320, 3321, 3330, [
      {'value' : 0, 'name' : '12AM'},{'value' : 1, 'name' : '1AM'},{'value' : 2, 'name' : '2AM'},{'value' : 3, 'name' : '3AM'},{'value' : 4, 'name' : '4AM'},{'value' : 5, 'name' : '5AM'},{'value' : 6, 'name' : '6AM'},{'value' : 7, 'name' : '7AM'},{'value' : 8, 'name' : '8AM'},{'value' : 9, 'name' : '9AM'},{'value' : 10, 'name' : '10AM'},
      {'value' : 11, 'name' : '11AM'},{'value' : 12, 'name' : 'Noon'},{'value' : 13, 'name' : '1PM'},{'value' : 14, 'name' : '2PM'},{'value' : 15, 'name' : '3PM'},{'value' : 16, 'name' : '4PM'},{'value' : 17, 'name' : '5PM'},{'value' : 18, 'name' : '6PM'},{'value' : 19, 'name' : '7PM'},{'value' : 20, 'name' : '8PM'},
      {'value' : 21, 'name' : '9PM'},{'value' : 22, 'name' : '10PM'},{'value' : 23, 'name' : '11PM'},
    ])
    self.toggleGroupSetup(grpCntrl, [evryCntrl, nCntrl, eaCntrl])
    mainGroups.append(grpCntrl)
    
    ''' Day Group '''
    grpCntrl = self.addMyControl('radiogroup', 4000, {'cronStringIndex':2})
    evryCntrl = self.everyToggleSetup(grpCntrl, 4100)
    eaCntrl = self.eachToggleSetup(grpCntrl, 4300, 4310, 4315, 4314, 4316, 4319, 4301, 4320, 4321, 4330, [
      {'value' : 1},{'value' : 2},{'value' : 3},{'value' : 4},{'value' : 5},{'value' : 6},{'value' : 7},{'value' : 8},{'value' : 9},{'value' : 10},
      {'value' : 11},{'value' : 12},{'value' : 13},{'value' : 14},{'value' : 15},{'value' : 16},{'value' : 17},{'value' : 18},{'value' : 19},{'value' : 20},
      {'value' : 21},{'value' : 22},{'value' : 23},{'value' : 24},{'value' : 25},{'value' : 26},{'value' : 27},{'value' : 28},{'value' : 29},{'value' : 30},{'value' : 31},
    ])
    self.toggleGroupSetup(grpCntrl, [evryCntrl, eaCntrl])
    mainGroups.append(grpCntrl)
    
    ''' Month Group '''
    grpCntrl = self.addMyControl('radiogroup', 5000, {'cronStringIndex':3})
    evryCntrl = self.everyToggleSetup(grpCntrl, 5100)
    eaCntrl = self.eachToggleSetup(grpCntrl, 5300, 5310, 5315, 5314, 5316, 5319, 5301, 5320, 5321, 5330, [
      {'value' : 1, 'name' : 'January'},{'value' : 2, 'name' : 'February'},{'value' : 3, 'name' : 'March'},{'value' : 4, 'name' : 'April'},{'value' : 5, 'name' : 'May'},{'value' : 6, 'name' : 'June'},
      {'value' : 7, 'name' : 'July'},{'value' : 8, 'name' : 'August'},{'value' : 9, 'name' : 'September'},{'value' : 10, 'name' : 'October'},{'value' : 11, 'name' : 'November'},{'value' : 12, 'name' : 'December'},
    ])
    self.toggleGroupSetup(grpCntrl, [evryCntrl, eaCntrl])
    mainGroups.append(grpCntrl)
    
    ''' Day of Week Group '''
    grpCntrl = self.addMyControl('radiogroup', 5000, {'cronStringIndex':4})
    evryCntrl = self.everyToggleSetup(grpCntrl, 6100)
    eaCntrl = self.eachToggleSetup(grpCntrl, 6300, 6310, 6315, 6314, 6316, 6319, 6301, 6320, 6321, 6330, [
      {'value' : 0, 'name' : 'Sunday'}, {'value' : 1, 'name' : 'Monday'},{'value' : 2, 'name' : 'Tuesday'},{'value' : 3, 'name' : 'Wednesday'},{'value' : 4, 'name' : 'Thursday'},{'value' : 5, 'name' : 'Friday'},{'value' : 6, 'name' : 'Saturday'},
    ])
    self.toggleGroupSetup(grpCntrl, [evryCntrl, eaCntrl])
    mainGroups.append(grpCntrl)
    
    self.addMyControl('button', 1080, {
      'onClick' : self.save,
    })
    self.addMyControl('button', 1090, {
      'onClick' : self.save,
    })
    
    self.setInitial(mainGroups)
  def setCronString(self, cronStr):
    self.origCronString = cronStr
    
  def getCronString(self):
    return self.mainCronString
  
  def save(self, controlId):
    ''' Save Button '''
    if controlId == 1080:
      pass
    ''' Dont Save Button '''
    if controlId == 1090:
      self.mainCronString = self.origCronString
    self.close()
    pass
    
  def setInitial(self, groups):
    #self.mainCronString = "* * * * *"
    #self.origCronString = ''
    cronString = self.origCronString
    sections = cronString.split()
    if len(sections) != 5:
      ''' Invalid CronString '''
      cronString = '* * * * *'
      sections = cronString.split()
    for n in [2,3,4]:
      if sections[n].startswith('*/'):
        divisor = int(sections[n][2:len(sections[n])])
        curTog = groups[n].options['toggles'][len(groups[n].options['toggles'])-1]
        selectCntrl = curTog.options['selectcontrol']
        spnObj = selectCntrl.options['spinControl']
        spnList = spnObj.options['spinlist']
        tmp = []
        for b in spnList:
          if (b['value'] % divisor) == 0:
            tmp.append(str(b['value']))
        listStr = ",".join(tmp)
        sections[n] = listStr
    for i in groups:
      strIndex = i.options['cronStringIndex']
      if sections[strIndex] == '*':
        i.options['toggles'][0].setSelected(True)
      elif sections[strIndex].startswith('*/'):
        curTog = i.options['toggles'][1]
        curTog.setSelected(True)
        spinCntrl = curTog.options['spincontrol']
        spinCntrl.setSpinControlValue(sections[strIndex][2:len(sections[strIndex])])
        curTog.options['cronString'] = sections[strIndex]
        self.updatedGroup(spinCntrl)
      else:
        curTog = i.options['toggles'][len(i.options['toggles'])-1]
        curTog.setSelected(True)
        tmp = sections[strIndex].split(',')
        val = []
        for n in tmp:
          if '-' in n:
            tmp2 = n.split('-')
            val.extend(range(int(tmp2[0]),int(tmp2[1])+1))
          else:
            val.append(int(n))
        val.sort()
        selectCntrl = curTog.options['selectcontrol']
        selectCntrl.setSelectControlList(val)
        curTog.options['cronString'] = sections[strIndex]
        self.updatedGroup(selectCntrl)
        
  def toggleGroupSetup(self, mainGrp, toggles):
    mainGrp.setOption('toggles', toggles)
    for i in toggles:
      i.setOption('onClick', self.toggleControl)
      
  def toggleControl(self, control):
    mainGrpToggles = control.options['mainGroup'].options['toggles']
    for i in mainGrpToggles:
      if i.controlId != control.controlId:
        i.setSelected(False)
    control.setSelected(True)
    
  def updatedGroup(self,control):
    if 'main' in control.options:
      cronString = ''
      if 'selectcontrol' == control.type:
        cronString = self.listToRangedStr(control.options['selectCurList'])
        control.options['ealabel'].setLabel(cronString)
      elif 'spincontrol' == control.type:
        cronString = "*/" + str(control.options['spinlist'][control.options['spinCurPos']]['value'])
      control = control.options['main']
      control.setOption('cronString', cronString)
      
    cronString = control.options['cronString']
    if len(cronString) > 0:
      strIndex = control.options['mainGroup'].options['cronStringIndex']
      sections = self.mainCronString.split()
      sections[strIndex] = cronString
      cronString = ' '.join(sections)
      self.mainCronString = cronString
      self.findControl(1001).setLabel(self.mainCronString)
    
  def listToRangedStr(self, list):
      lasti = -1
      cronAr = []
      tmpAr = []
      for i in list:
        if (int(i['value']) == (lasti + 1)):
          tmpAr.append(str(i['value']))
        else:
          if (len(tmpAr) > 0):
            delimit = ","
            if (len(tmpAr) > 2):
              tmpAr = [tmpAr[0], tmpAr[len(tmpAr)-1]]
              delimit = "-"
            cronAr.append(delimit.join(tmpAr))
          tmpAr = []
          tmpAr.append(str(i['value']))
        lasti = int(i['value'])
      if (len(tmpAr) > 0):
        delimit = ","
        if (len(tmpAr) > 2):
          tmpAr = [tmpAr[0], tmpAr[len(tmpAr)-1]]
          delimit = "-"
        cronAr.append(delimit.join(tmpAr))
      cronStrin = ""
      if (len(cronAr) > 0):
        cronStrin = ",".join(cronAr)
      return cronStrin
      
class SelectDialog( xbmcgui.WindowXMLDialog ):
  def __init__( self, *args, **kwargs):
    defSize = {}
    defSize.update(args[3])
    self.options = defSize
    self.selectedVal = -1

  def onInit( self ):
    self.getControl( 999 ).setHeight(25+(50*len(self.options['items'])))
    control = ControlObject('list', 0, 996, self)
    for i in range(0,len(self.options['items'])):
      print self.options['items'][i]
      listitem = xbmcgui.ListItem( label=self.options['items'][i]) 
      listitem.setProperty( "return", str(i) )
      control.addListItem(listitem)
    
  def onClick( self, controlId ):
    if controlId == 996:
      selectedItem = self.getControl( controlId ).getSelectedItem()
      self.selectedVal = int(selectedItem.getProperty( "return" ))
      self.close()
    
  def getSelectedVal(self):
    return self.selectedVal
    
  def onAction( self, action ):
    if ( action.getId() in CANCEL_DIALOG):
      self.close()
            