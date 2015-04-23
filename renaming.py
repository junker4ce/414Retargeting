from pyfbsdk import *

from pyfbsdk_additions import *
import os

#Define the function to create the character to characterize the model to
def addJointsToCharacter(control, event):
	global skelList, characterize
	allNodes = FBSystem().Scene.Components
	lCharacter = FBCharacter("newChar")
	#for each joint in the predetrmined joint array add the joint
    for item in characterize:
		for lComponent in allNodes:
			if lComponent.Name == item:
				myJoint = lComponent
				myJoint.Selected = True
				property = lCharacter.PropertyList.Find(item + "Link")
				property.append (myJoint)
				print property.Name
				print item
				print lCharacter.Name
	lCharacter.SetCharacterizeOn(True)

#Function definition for creating a button in the UI
def createButton(text, color):
    newButton = FBButton()
    newButton.Caption = text
    newButton.Style = FBButtonStyle.kFBPushButton
    newButton.Justify = FBTextJustify.kFBTextJustifyCenter
    newButton.Look = FBButtonLook.kFBLookColorChange
    if color != None:
        newButton.SetStateColor(FBButtonState.kFBButtonState0, color)
    return newButton

#Function definition for retriving the installation path 
def GetMotionBuilderInstallationDirectory() :
    applicationPath = FBSystem().ApplicationPath
    return applicationPath[0:applicationPath.index('bin')]

#Define the function to create the file selection popup
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

#Define the function to load in the FBX character
def loadFile():
    from pyfbsdk import FBFilePopup, FBFilePopupStyle, FBMessageBox
    global FBXFilenames, bvhCharacter, app, BVHFilename
    #Create the application
    app = FBApplication()
    app.FileNew()

    #POP UP FOR FBX FILE(automatic redirect to tutorial folder)
    fbxName = fbxPopup()
    app.FileOpen(fbxName, False)
    #Get all nodes in the scene (will filter out skeleton's joints)
    allNodes = FBSystem().Scene.Components        
    global skelList
    for lComponent in allNodes:
        #Create array of nodes that are skeleton joints
        if lComponent and lComponent.ClassName() == "FBModelSkeleton":
            print lComponent.Name
            skelList.append (lComponent)

#Define the function to set the dropdown menus
def populateLists(skeleton):
    global fbxList, characterizeList
    #Remove all items from the dropdown menus
    fbxList.Items.removeAll()
    characterizeList.Items.removeAll()
    #Fill in menu of model joints
    for node in skeleton:
        fbxList.Items.append(node.Name)
    #Fill in menu of characterize values
    for bone in characterize:
    	characterizeList.Items.append(bone)
    #Rehighlight the currently selected bone
    fbxList.Selected(boneIndex, True)
    characterizeList.Selected(charIndex, True)

#Define the function of the rename button
def renameClick(control, event):
    global modelList, characterizeList
    #Rename the bone in the skeleton
    skelList[boneIndex].Name = characterize[charIndex]
    #Repopulate the list displayed to the user
    populateLists(skelList)

#Define the function of the save button
def saveResponse(control, event):
    # Save the file using a dialog box.
    saveDialog = FBFilePopup()
    saveDialog.Style = FBFilePopupStyle.kFBFilePopupSave
    saveDialog.Filter = '*'
    saveDialog.Caption = 'Save the Current FBX'
    # Set the path to the current user's My Documents.
    saveDialog.Path = os.path.expanduser('~') + '\Documents'
    saveDialog.FileName = 'Characterized.fbx'

    #Save the file
    if saveDialog.Execute():
        app.FileSave(saveDialog.FullFilename)

#Define the function of selecting an item from the character's joints list
def selBone(control, event):
    global modelList
    global boneIndex
    #Make sure all joints in skeleton are deselected
    for node in skelList:
        node.Selected = False
    #Highlight the selected bone on screen
    skelList[control.ItemIndex].Selected = True
    #Save the current selection
    boneIndex = control.ItemIndex

#Define the function of selecting an item from the characterize list
def selChar(control, event):
	global charIndex
    #Save the current selection
	charIndex = control.ItemIndex

FBXFilenames = []
skelList = []
boneIndex = 0
charIndex = 0

#Array of the names of the required skeleton nodes
characterize = ["Hips", "LeftUpLeg", "LeftLeg", "LeftFoot", "RightUpLeg", "RightLeg", "RightFoot",
				 "Spine", "LeftArm", "LeftForeArm", "LeftHand", "RightArm", "RightForeArm", "RightHand", "Head"]

loadFile()

#Initalize the size and region for the application interface
tool = FBCreateUniqueTool("Renamer")
tool.StartSizeX = 500
tool.StartSizeY = 75

x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
h = FBAddRegionParam(0,FBAttachType.kFBAttachBottom,"")
tool.AddRegion("main","main", x, y, w, h)

#Get the current renderer
renderer = FBSystem().Scene.Renderer
viewOptions = renderer.GetViewingOptions()

#Set current picking mode to X-ray to highlight bones
viewOptions.PickingMode = FBPickingMode.kFBPickingModeXRay
renderer.SetViewingOptions(viewOptions)

#Set up the dropdown menu for the list of joints in the model
global fbxList
fbxList = FBList()
fbxList.Style = FBListStyle.kFBDropDownList
fbxList.ReadOnly = False
fbxList.OnChange.Add(selBone)

#Set up the dropdown menu for predefined MotionBuilder required joints
global characterizeList
characterizeList = FBList()
characterizeList.Style = FBListStyle.kFBDropDownList
characterizeList.ReadOnly = False
characterizeList.OnChange.Add(selChar)

#Place the values into the dropdown menues and highight the first item
populateLists(skelList)
skelList[0].Selected = True

#Create and add functionality to Rename Bone Button
renameBone = createButton("Rename Bone", None)
renameBone.OnClick.Add(renameClick)

#Create and add functionality to Save Button
saveFBX = createButton("Save", None)
saveFBX.OnClick.Add(saveResponse)

#Create and add functionality to Characterize Button
characterizeButton = createButton("Characterize", None)
characterizeButton.OnClick.Add(addJointsToCharacter)

#Add the Dropdown menus and buttons to the UI
hbox = FBHBoxLayout( FBAttachType.kFBAttachLeft )
hbox.AddRelative(fbxList, 2.0)
hbox.AddRelative(characterizeList, 2.0)
hbox.AddRelative(renameBone, 1.0)
hbox.AddRelative(characterizeButton, 1.0)
hbox.AddRelative(saveFBX, 1.0)

#Attach the box to the window of the program
window = FBVBoxLayout(FBAttachType.kFBAttachTop)
tool.SetControl("main", window)
window.AddRelative(hbox, 1.0)

#Display the application
ShowTool(tool)