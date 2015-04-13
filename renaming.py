from pyfbsdk import *

from pyfbsdk_additions import *
import os

def addJointsToCharacter(control, event):
	global skelList, characterize
	allNodes = FBSystem().Scene.Components
	lCharacter = FBCharacter("newChar")
	for item in characterize:
		for lComponent in allNodes:
			if lComponent.Name == item:
				myJoint = lComponent
			
		#myJoint =  FBFindModelByLabelName(item)
				myJoint.Selected = True
				property = lCharacter.PropertyList.Find(item + "Link")
				property.append (myJoint)
				print property.Name
				print item
				print lCharacter.Name
	lCharacter.SetCharacterizeOn(True)

def createButton(text, color):
    newButton = FBButton()
    newButton.Caption = text
    newButton.Style = FBButtonStyle.kFBPushButton
    newButton.Justify = FBTextJustify.kFBTextJustifyCenter
    newButton.Look = FBButtonLook.kFBLookColorChange
    if color != None:
        newButton.SetStateColor(FBButtonState.kFBButtonState0, color)
    return newButton

def GetMotionBuilderInstallationDirectory() :
    applicationPath = FBSystem().ApplicationPath
    return applicationPath[0:applicationPath.index('bin')]

def fbxPopup():
    from pyfbsdk import FBFilePopup, FBFilePopupStyle, FBMessageBox

    lFp2 = FBFilePopup()
    fbxName = None
    lFp2.Caption = "Select an FBX File for the Retargeting"
    lFp2.Style = FBFilePopupStyle.kFBFilePopupOpen

    lFp2.Filter = "*"

    # Set the default path.
    lFp2.Path = GetMotionBuilderInstallationDirectory()+"Tutorials"
    # Get the GUI to show.
    lRes = lFp2.Execute()
    # If we select files, show them, otherwise indicate that the selection was canceled
    if lRes:
        fbxName = lFp2.Path + "/" + lFp2.FileName
    else:
        FBMessageBox( "Invalid selection", "Selection canceled", "OK", None, None )
    # Cleanup.
    del( lFp2, lRes, FBFilePopup, FBFilePopupStyle, FBMessageBox )
    return fbxName

def loadFiles():
    from pyfbsdk import FBFilePopup, FBFilePopupStyle, FBMessageBox

    global FBXFilenames, bvhCharacter, app, BVHFilename

    app = FBApplication()
    app.FileNew()

    system = FBSystem()
    scene = system.Scene
    #POP UP FOR BVH FILE

    #POP UP FOR FBX FILE(automatic redirect to tutorial folder)
    fbxName = fbxPopup()

    app.FileOpen(fbxName, False)

    allNodes = FBSystem().Scene.Components
        

    global skelList
    for lComponent in allNodes:
        #print lComponent.Name
        if lComponent and lComponent.ClassName() == "FBModelSkeleton":
            print lComponent.Name
            skelList.append (lComponent)

def populateLists(skeleton):
    global fbxList, characterizeList
    fbxList.Items.removeAll()
    characterizeList.Items.removeAll()
    for node in skeleton:
        fbxList.Items.append(node.Name)
    for bone in characterize:
    	characterizeList.Items.append(bone)
    fbxList.Selected(boneIndex, True)

def renameClick(control, event):
    global modelList, characterizeList
    skelList[boneIndex].Name = characterize[charIndex]
    populateLists(skelList)

def saveResponse(control, event):
    # Save the file using a dialog box.
    saveDialog = FBFilePopup()
    saveDialog.Style = FBFilePopupStyle.kFBFilePopupSave
    saveDialog.Filter = '*'

    saveDialog.Caption = 'Save the Current FBX'
    # Set the path to the current user's My Documents.
    saveDialog.Path = os.path.expanduser('~') + '\Documents'
    saveDialog.FileName = 'Characterized.fbx'

    if saveDialog.Execute():
        app.FileSave(saveDialog.FullFilename)

def selBone(control, event):
    global modelList
    global boneIndex
    for node in skelList:
        node.Selected = False
    skelList[control.ItemIndex].Selected = True
    boneIndex = control.ItemIndex

def selChar(control, event):
	global charIndex
	charIndex = control.ItemIndex

FBXFilenames = []
skelList = []
boneIndex = 0
charIndex = 0

characterize = ["Hips", "LeftUpLeg", "LeftLeg", "LeftFoot", "RightUpLeg", "RightLeg", "RightFoot",
				 "Spine", "LeftArm", "LeftForeArm", "LeftHand", "RightArm", "RightForeArm", "RightHand", "Head"]

loadFiles()

tool = FBCreateUniqueTool("Renamer")
tool.StartSizeX = 500
tool.StartSizeY = 75

x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
h = FBAddRegionParam(0,FBAttachType.kFBAttachBottom,"")
tool.AddRegion("main","main", x, y, w, h)

renderer = FBSystem().Scene.Renderer
viewOptions = renderer.GetViewingOptions()

#Set current picking mode
viewOptions.PickingMode = FBPickingMode.kFBPickingModeXRay
renderer.SetViewingOptions(viewOptions)

global fbxList
fbxList = FBList()
fbxList.Style = FBListStyle.kFBDropDownList
fbxList.ReadOnly = False
fbxList.OnChange.Add(selBone)

global characterizeList
characterizeList = FBList()
characterizeList.Style = FBListStyle.kFBDropDownList
characterizeList.ReadOnly = False
characterizeList.OnChange.Add(selChar)

populateLists(skelList)

global textEnter
textEnter = FBEdit()
textEnter.Text = ""
skelList[0].Selected = True

renameBone = createButton("Rename Bone", None)
renameBone.OnClick.Add(renameClick)

saveFBX = createButton("Save", None)
saveFBX.OnClick.Add(saveResponse)

characterizeButton = createButton("Characterize", None)
characterizeButton.OnClick.Add(addJointsToCharacter)

hbox2 = FBHBoxLayout( FBAttachType.kFBAttachLeft )
hbox2.AddRelative(fbxList, 2.0)
hbox2.AddRelative(characterizeList, 2.0)
hbox2.AddRelative(renameBone, 1.0)
hbox2.AddRelative(characterizeButton, 1.0)
hbox2.AddRelative(saveFBX, 1.0)

window = FBVBoxLayout(FBAttachType.kFBAttachTop)
tool.SetControl("main", window)

window.AddRelative(hbox2, 1.0)

ShowTool(tool)