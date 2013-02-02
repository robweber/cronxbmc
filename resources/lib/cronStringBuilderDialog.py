import sys
import os
import xbmc
import xbmcgui
import traceback
from service import CronXbmc, CronJob
from operator import itemgetter

# Action ID's
ACTION_MOVE_LEFT             = 1
ACTION_MOVE_RIGHT            = 2
ACTION_MOVE_UP               = 3
ACTION_MOVE_DOWN             = 4
ACTION_PAGE_UP               = 5
ACTION_PAGE_DOWN             = 6
ACTION_SELECT_ITEM           = 7
ACTION_MOUSE_LEFT_CLICK      = 100
ACTION_MOUSE_RIGHT_CLICK     = 101
ACTION_MOUSE_MIDDLE_CLICK    = 102
ACTION_MOUSE_DOUBLE_CLICK    = 103
ACTION_MOUSE_WHEEL_UP        = 104
ACTION_MOUSE_WHEEL_DOWN      = 105
CANCEL_DIALOG = ( 9, 10, 92, 216, 247, 257, 275, 61467, 61448, )
CLICK_GROUP   = (ACTION_SELECT_ITEM, ACTION_MOUSE_LEFT_CLICK, ACTION_MOUSE_RIGHT_CLICK, ACTION_MOUSE_DOUBLE_CLICK)
KEYB_NAV = (ACTION_MOVE_LEFT, ACTION_MOVE_RIGHT, ACTION_MOVE_UP, ACTION_MOVE_DOWN, ACTION_PAGE_UP, ACTION_PAGE_DOWN, ACTION_MOUSE_WHEEL_UP, ACTION_MOUSE_WHEEL_DOWN)

class cronBuildGUI( xbmcgui.WindowXMLDialog ):

    ''' Initialize Window Controls '''
    def controlSetup(self):
      minEvry = self.everyToggleSetup(2100)
      minNcntrl = self.nToggleSetup(2200, 2215, 2214, 2216, [
        {'value' : 1},{'value' : 2},{'value' : 3},{'value' : 4},{'value' : 5},{'value' : 6},{'value' : 7},{'value' : 8},{'value' : 9},{'value' : 10},
        {'value' : 11},{'value' : 12},{'value' : 13},{'value' : 14},{'value' : 15},{'value' : 16},{'value' : 17},{'value' : 18},{'value' : 19},{'value' : 20},
        {'value' : 21},{'value' : 22},{'value' : 23},{'value' : 24},{'value' : 25},{'value' : 26},{'value' : 27},{'value' : 28},{'value' : 29},{'value' : 30},
        {'value' : 31},{'value' : 32},{'value' : 33},{'value' : 34},{'value' : 35},{'value' : 36},{'value' : 37},{'value' : 38},{'value' : 39},{'value' : 40},
        {'value' : 41},{'value' : 42},{'value' : 43},{'value' : 44},{'value' : 45},{'value' : 46},{'value' : 47},{'value' : 48},{'value' : 49},{'value' : 50},
        {'value' : 51},{'value' : 52},{'value' : 53},{'value' : 54},{'value' : 55},{'value' : 56},{'value' : 57},{'value' : 58},{'value' : 59},
      ])
      minEAcntrl = self.eachToggleSetup(2300, 2315, 2314, 2316, 2320, 2321, 2330, 2301, [
        {'value' : 0},{'value' : 1},{'value' : 2},{'value' : 3},{'value' : 4},{'value' : 5},{'value' : 6},{'value' : 7},{'value' : 8},{'value' : 9},{'value' : 10},
        {'value' : 11},{'value' : 12},{'value' : 13},{'value' : 14},{'value' : 15},{'value' : 16},{'value' : 17},{'value' : 18},{'value' : 19},{'value' : 20},
        {'value' : 21},{'value' : 22},{'value' : 23},{'value' : 24},{'value' : 25},{'value' : 26},{'value' : 27},{'value' : 28},{'value' : 29},{'value' : 30},
        {'value' : 31},{'value' : 32},{'value' : 33},{'value' : 34},{'value' : 35},{'value' : 36},{'value' : 37},{'value' : 38},{'value' : 39},{'value' : 40},
        {'value' : 41},{'value' : 42},{'value' : 43},{'value' : 44},{'value' : 45},{'value' : 46},{'value' : 47},{'value' : 48},{'value' : 49},{'value' : 50},
        {'value' : 51},{'value' : 52},{'value' : 53},{'value' : 54},{'value' : 55},{'value' : 56},{'value' : 57},{'value' : 58},{'value' : 59},
      ])
      self.toggleSetup('min',[minEvry, minNcntrl, minEAcntrl])
      
      hrEvry = self.everyToggleSetup(3100)
      hrNcntrl = self.nToggleSetup(3200, 3215, 3214, 3216, [
        {'value' : 1},{'value' : 2},{'value' : 3},{'value' : 4},{'value' : 5},{'value' : 6},{'value' : 7},{'value' : 8},{'value' : 9},{'value' : 10},
        {'value' : 11},{'value' : 12},{'value' : 13},{'value' : 14},{'value' : 15},{'value' : 16},{'value' : 17},{'value' : 18},{'value' : 19},{'value' : 20},
        {'value' : 21},{'value' : 22},{'value' : 23},
      ])
      hrEAcntrl = self.eachToggleSetup(3300, 3315, 3314, 3316, 3320, 3321, 3330, 3301, [
        {'value' : 0, 'name' : '12AM'},{'value' : 1, 'name' : '1AM'},{'value' : 2, 'name' : '2AM'},{'value' : 3, 'name' : '3AM'},{'value' : 4, 'name' : '4AM'},{'value' : 5, 'name' : '5AM'},{'value' : 6, 'name' : '6AM'},{'value' : 7, 'name' : '7AM'},{'value' : 8, 'name' : '8AM'},{'value' : 9, 'name' : '9AM'},{'value' : 10, 'name' : '10AM'},
        {'value' : 11, 'name' : '11AM'},{'value' : 12, 'name' : 'Noon'},{'value' : 13, 'name' : '1PM'},{'value' : 14, 'name' : '2PM'},{'value' : 15, 'name' : '3PM'},{'value' : 16, 'name' : '4PM'},{'value' : 17, 'name' : '5PM'},{'value' : 18, 'name' : '6PM'},{'value' : 19, 'name' : '7PM'},{'value' : 20, 'name' : '8PM'},
        {'value' : 21, 'name' : '9PM'},{'value' : 22, 'name' : '10PM'},{'value' : 23, 'name' : '11PM'},
      ])
      self.toggleSetup('hour',[hrEvry, hrNcntrl, hrEAcntrl])
      
      dyEvry = self.everyToggleSetup(4100)
      dyEAcntrl = self.eachToggleSetup(4300, 4315, 4314, 4316, 4320, 4321, 4330, 4301, [
        {'value' : 1},{'value' : 2},{'value' : 3},{'value' : 4},{'value' : 5},{'value' : 6},{'value' : 7},{'value' : 8},{'value' : 9},{'value' : 10},
        {'value' : 11},{'value' : 12},{'value' : 13},{'value' : 14},{'value' : 15},{'value' : 16},{'value' : 17},{'value' : 18},{'value' : 19},{'value' : 20},
        {'value' : 21},{'value' : 22},{'value' : 23},{'value' : 24},{'value' : 25},{'value' : 26},{'value' : 27},{'value' : 28},{'value' : 29},{'value' : 30},{'value' : 31},
      ])
      self.toggleSetup('day',[dyEvry, dyEAcntrl])
      
      monEvry = self.everyToggleSetup(5100)
      monEAcntrl = self.eachToggleSetup(5300, 5315, 5314, 5316, 5320, 5321, 5330, 5301, [
        {'value' : 1, 'name' : 'January'},{'value' : 2, 'name' : 'February'},{'value' : 3, 'name' : 'March'},{'value' : 4, 'name' : 'April'},{'value' : 5, 'name' : 'May'},{'value' : 6, 'name' : 'June'},
        {'value' : 7, 'name' : 'July'},{'value' : 8, 'name' : 'August'},{'value' : 9, 'name' : 'September'},{'value' : 10, 'name' : 'October'},{'value' : 11, 'name' : 'November'},{'value' : 12, 'name' : 'December'},
      ])
      self.toggleSetup('month',[monEvry, monEAcntrl])
      
      wkEvry = self.everyToggleSetup(6100)
      wkEAcntrl = self.eachToggleSetup(6300, 6315, 6314, 6316, 6320, 6321, 6330, 6301, [
        {'value' : 0, 'name' : 'Sunday'}, {'value' : 1, 'name' : 'Monday'},{'value' : 2, 'name' : 'Tuesday'},{'value' : 3, 'name' : 'Wednesday'},{'value' : 4, 'name' : 'Thursday'},{'value' : 5, 'name' : 'Friday'},{'value' : 6, 'name' : 'Saturday'},
      ])
      self.toggleSetup('weekday',[wkEvry, wkEAcntrl])
      
      self.setOnClickListener(1080, {'action' : self.save}) # Save Button
      self.setOnClickListener(1090, {'action' : self.save}) # Dont Save Button
      
      ''' Maybe need to convert names(jan,feb,mar) to nums(1,2,3)? '''
      if 'cronString' in self.initOpts:
        self.cronString = self.initOpts['cronString']
        
      self.setInitial()
      pass
    def save(self, controlId):
      ''' Save Button '''
      if controlId == 1080:
        if 'saveLbl' in self.initOpts:
          self.parent.updated['cron'] = self.cronString
          self.parent.getControl( self.initOpts['saveLbl'] ).setLabel(self.cronString)
          self.close()
      ''' Dont Save Button '''
      if controlId == 1090:
        self.close()
      pass
      
    def setInitial(self):
      cronString = self.cronString
      sections = cronString.split()
      if len(sections) != 5:
        ''' Invalid CronString '''
        cronString = '* * * * *'
        sections = cronString.split()
      for i in range(0,len(sections)):
        interval = ''
        val = ''
        if '*/' in sections[i]:
          interval = 'evryN'
          val = sections[i][2:len(sections[i])]
          pass
        elif (',' in sections[i]) or ('-' in sections[i]) or (sections[i].isdigit()):
          interval = 'each'
          tmp = sections[i].split(',')
          val = []
          for n in tmp:
            if '-' in n:
              tmp2 = n.split('-')
              val.extend(range(int(tmp2[0]),int(tmp2[1])+1))
            else:
              val.append(int(n))
          pass
        else:
          interval = 'evry'
          val = '*'
          pass
        thisMainObj = {}
        if i == 0:
          thisMainObj = self.mainGroups['min']
        elif i == 1:
          thisMainObj = self.mainGroups['hour']
        elif i == 2:
          thisMainObj = self.mainGroups['day']
        elif i == 3:
          thisMainObj = self.mainGroups['month']
        elif i == 4:
          thisMainObj = self.mainGroups['weekday']
        for grp in thisMainObj:
          obj = self.objStore[grp]
          togButn = obj['toggleBtn']
          if interval == 'evry':
            if ('eaLBL' not in obj) and ('spinLabel' not in obj):
              self.getControl( togButn ).setSelected(True)
              break
          elif interval == 'evryN':
            if ('eaLBL' not in obj) and ('spinLabel' in obj):
              self.getControl( togButn ).setSelected(True)
              valList = obj['valList']
              curPos = 0
              for eachI in range(0,len(valList)):
                if val == str(valList[eachI]['value']):
                  curPos = eachI
                  break
              obj['listPos'] = curPos
              obj['spinLabel'].setLabel(str(val))
              obj['cronString'] = "*/" + str(val)
              break
          elif interval == 'each':
            if ('eaLBL' in obj):
              self.getControl( togButn ).setSelected(True)
              valList = obj['valList']
              tmpL = []
              for each in val:
                for eachA in valList:
                  if each == eachA['value']:
                    tmpL.append(eachA)
                    break
              for each in tmpL:
                listitem = xbmcgui.ListItem( label=each['name']) 
                listitem.setProperty( "value", str(each['value']) )
                obj['eaList'].addItem( listitem )
              cronString = self.listToRangedStr( tmpL )
              obj['eaLBL'].setLabel(cronString)
              obj['cronString'] = cronString
              break
          pass
      self.updateCronString()
    
    def toggleControl(self, obj, controlID):
      thisGrp = obj['toggles']
      for togObj in thisGrp:
        togButn = self.objStore[togObj]['toggleBtn']
        if togButn != controlID:
          self.getControl( togButn ).setSelected(False)
      if not self.getControl( controlID ).isSelected():
        self.getControl( controlID ).setSelected(True)

    def toggleSetup(self, type, toggles):
      tmp = {
        'type'    : type,
        'toggles' : toggles,
      }
      for i in toggles:
        self.objStore[i].update(tmp)
        obj = {
          'action'    : self.toggleControl,
          'glblObjID' : i,
        }
        self.setOnClickListener(self.objStore[i]['toggleBtn'], obj)
      self.mainGroups[type] = toggles
    
    def everyToggleSetup(self,toggleBtn):
      objId = len(self.objStore)
      tmp = {
        'cronString' : '*',
        'toggleBtn' : toggleBtn,
      }
      self.objStore.append(tmp)
      return objId
      
    def nToggleSetup(self, toggleBtn, spinControlUP, spinControlDWN, spinControlLBL, valList):
      objId = self.fauxSpinControl(spinControlUP, spinControlDWN, spinControlLBL, valList)
      obj = self.objStore[objId]
      tmp = {
        'cronString' : "*/" + str(obj['valList'][obj['listPos']]['value']),
        'toggleBtn' : toggleBtn,
      }
      obj.update(tmp)
      return objId
      
    def eachToggleSetup(self, toggleBtn, spinUP, spinDWN, spinLBL, eaAdd, eaDel, eaList, eaLBL, valList):
      objId = self.listSelection(spinUP, spinDWN, spinLBL, eaAdd, eaDel, eaList, eaLBL, valList)
      tmp = {
        'cronString' : '',
        'toggleBtn' : toggleBtn,
      }
      self.objStore[objId].update(tmp)
      return objId
      
    def listSelection(self, spinUP, spinDWN, spinLBL, eaAdd, eaDel, eaList, eaLBL, valList):
      spinObjId = self.fauxSpinControl(spinUP, spinDWN, spinLBL, valList)
      obj = {
        'action'    : self.listController,
        'glblObjID' : spinObjId,
      }
      tmpObj = {
        'eaAdd'    : self.getControl( eaAdd ),
        'eaDel'    : self.getControl( eaDel ),
        'eaAddId'  : eaAdd,
        'eaDelId'  : eaDel,
        'eaList'   : self.getControl( eaList ),
        'eaLBL'    : self.getControl( eaLBL ),
      }
      self.objStore[spinObjId].update(tmpObj)
      
      self.setOnClickListener(eaAdd, obj)
      self.setOnClickListener(eaDel, obj)
      return spinObjId
      
    def listController(self, obj, controlId):
      curSelected = obj['valList'][obj['listPos']]
      itemList = []
      currentExists = False
      
      for items in range(0, obj['eaList'].size() ):
        item = obj['eaList'].getListItem(items)
        if str(item.getProperty( "value" )) == str(curSelected['value']):
          currentExists = True
        else:
          itemList.append({'name' : item.getLabel(), 'value' : int(item.getProperty( "value" ))})
          
      if controlId == obj['eaAddId']:
        itemList.append(curSelected)
        if not currentExists:
          listitem = xbmcgui.ListItem( label=curSelected['name']) 
          listitem.setProperty( "value", str(curSelected['value']) )
          obj['eaList'].addItem( listitem )
      elif controlId == obj['eaDelId']:
        if currentExists:
          obj['eaList'].reset()
          for i in itemList:
            listitem = xbmcgui.ListItem( label=i['name']) 
            listitem.setProperty( "value", str(i['value']) )
            obj['eaList'].addItem( listitem )
      
      cronString = self.listToRangedStr( itemList )
      obj['eaLBL'].setLabel(cronString)
      obj['cronString'] = cronString

    def listToRangedStr(self, list):
      lasti = -1
      cronAr = []
      tmpAr = []
      sortedList = sorted(list, key=itemgetter('value')) 
      for i in sortedList:
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
    
    def fauxSpinControl(self, spinControlUP, spinControlDWN, spinControlLBL, valList):
      for i in valList:
        if 'value' not in i:
          i['value'] = i['name']
        elif 'name' not in i:
          i['name'] = i['value']
        i['name'] = str(i['name'])
      obj = {
        'action'    : self.spinWrapper,
        'glblObjID' : len(self.objStore),
      }
      glblObj = {
        'valList'   : valList,
        'spinLabel' : self.getControl( spinControlLBL ),
        'spinUP'    : self.getControl( spinControlUP ),
        'spinDWN'   : self.getControl( spinControlDWN ),
        'spinUPId'  : spinControlUP,
        'spinDWNId' : spinControlDWN,
        'listSize'  : len(valList),
        'listPos'   : 0,
      }
      self.objStore.append(glblObj)
      
      self.setOnClickListener(spinControlUP, obj)
      self.setOnClickListener(spinControlDWN, obj)
      
      glblObj['spinLabel'].setLabel(valList[glblObj['listPos']]['name'])
      return obj['glblObjID']
      
    def spinWrapper(self, obj, controlId):
      #obj['lastPos']
      if obj['spinUPId'] == controlId:
        obj['listPos'] += 1
        if obj['listPos'] >= obj['listSize']:
          obj['listPos'] = 0
      else:
        obj['listPos'] -= 1
        if obj['listPos'] < 0:
          obj['listPos'] = obj['listSize'] - 1
      obj['spinLabel'].setLabel(obj['valList'][obj['listPos']]['name'])
      if 'eaList' not in obj:
        obj['cronString'] = "*/" + str(obj['valList'][obj['listPos']]['value'])
      
    def updateCronString(self):
      mainDisplayLabel = 1001
      cronString = '* * * * *'
      sections = cronString.split()
      for i in self.mainGroups:
        thisCronStr = ''
        n = self.mainGroups[i]
        for o in n:
          thisGrp = self.objStore[o]
          if self.getControl( thisGrp['toggleBtn'] ).isSelected():
            thisCronStr = thisGrp['cronString']
            break
        if thisCronStr == '':
          thisCronStr = '*'
        if i == 'min':
          sections[0] = thisCronStr
        elif i == 'hour':
          sections[1] = thisCronStr
        elif i == 'day':
          sections[2] = thisCronStr
        elif i == 'month':
          sections[3] = thisCronStr
        elif i == 'weekday':
          sections[4] = thisCronStr
      cronString = ' '.join(sections)
      self.getControl( mainDisplayLabel ).setLabel(cronString)
      self.cronString = cronString
      
    def setOnClickListener(self, controlID, options={}):
      defClickObj = { 'action'   : ''}
      defClickObj.update(options)
      if controlID in self.clickListeners:
        #for i in self.clickListeners[controlID]:
        #  if defClickObj['priority'] <= i['priority']:
        #    defClickObj['priority'] = i['priority'] + 1
        self.clickListeners[controlID].append(defClickObj)
      else:
        self.clickListeners[controlID] = [defClickObj]
      pass
    
    def __init__( self, *args, **kwargs ):
      self.cronxbmc = CronXbmc()
      self.initOpts = {}
      self.focusedControlId = 0
      self.clickListeners = {}
      self.cronString = '* * * * *'
      self.objStore = []
      self.mainGroups = {}

    def onInit( self ):  
      self.controlSetup()
      
    def setStuff( self, parent, options=None ):
      self.parent = parent
      self.initOpts = options
      
    def onClick( self, controlId ):
      if controlId in self.clickListeners:
        ''' TODO:: Click Priorities '''
        for i in self.clickListeners[controlId]:
          if 'glblObjID' in i:
            i['action'](self.objStore[i['glblObjID']], controlId)
          else:
            i['action'](controlId)
        ## update Labels on every click
        self.updateCronString()
      pass

    def onFocus( self, controlId ):
      if self.focusedControlId != controlId:
        self.setFocus(self.getControl( controlId ))
        self.focusedControlId = controlId

    def onAction( self, action ):
      if ( action.getId() in CANCEL_DIALOG):
        self.close()
         