from pyfbsdk import *

from pyfbsdk_additions import *
import os

def GetMotionBuilderInstallationDirectory() :
    applicationPath = FBSystem().ApplicationPath
    return applicationPath[0:applicationPath.index('bin')]

def previewSnake(control, event):
    loadFiles()
    
    rightFoot = FBFindModelByLabelName("BVH:RightFoot")
    leftArm = FBFindModelByLabelName("BVH:LeftArm")
    rightArm = FBFindModelByLabelName("BVH:RightArm")
    rightFoot.Parent = None
    rightArm.Parent = None
    leftArm.Parent = None

def addJointToCharacter ( characterObject, slot, jointName ):
    myJoint = FBFindModelByLabelName(jointName)
    if myJoint:
        proplist = characterObject.PropertyList.Find(slot + "Link")
        proplist.append (myJoint)

def CleanModel(objects_to_clean, node):
    objects_to_clean.append(node)
    for child in node.Children:
        CleanModel(objects_to_clean, child)

def ValueChange(control,event):
    print int(control.Value)
    scenePlayer.Goto(FBTime(0, 0, 0, int(control.Value), 0))

def Transaction(control,event):
    print "Transaction, is begin: ", event.IsBeginTransaction
    if(event.IsBeginTransaction==False):
        print int(control.Value)
        scenePlayer.Goto(FBTime(0, 0, 0, int(control.Value), 0))
#        if(control.Value>.5):
#            i=0
#            while(i<(((control.Value)-.5)*100)):
#                  lPlayer = FBPlayerControl()
#                  lPlayer.StepForward()
#                  i+=1
#        elif(control.Value<.5):
#            i=0
#            while(i>(((control.Value)-.5)*100)):
#                  lPlayer = FBPlayerControl()
#                  lPlayer.StepBackward()
#                  i-=1
#        control.Value=.5

def playScene(control, event):
    scenePlayer.Play()
def moveLeg(control, event):
   # leg= FBFindModelByLabelName("BVH:LeftLeg").LongName
   #print leg
    global bvhList
    for comp in FBSystem().Scene.Components:
        #print comp.LongName
        if (comp.LongName == "BVH:LeftLeg"):
            comp.Selected = True
            comp.Translation = FBVector3d(10, 10, 10)
        else:
            comp.Selected = False
def restartResponse(control, event):
    scenePlayer.GotoStart()

def loadAllScene(control,event):
    global FBXFilenames
    FBXFilenames = []
    loadFiles()

def nextFrameRespone(control,event):
    scenePlayer.StepForward()

def prevFrameRespone(control,event):
    scenePlayer.StepBackward()

def createButton(text, color):
    newButton = FBButton()
    newButton.Caption = text
    newButton.Style = FBButtonStyle.kFBPushButton
    newButton.Justify = FBTextJustify.kFBTextJustifyCenter
    newButton.Look = FBButtonLook.kFBLookColorChange
    if color != None:
        newButton.SetStateColor(FBButtonState.kFBButtonState0, color)
    return newButton

def selBone(control, event):
    global modelList
    global boneIndex
    for node in skelList:
        node.Selected = False
    modelList[0][control.ItemIndex].Selected = True
    boneIndex = control.ItemIndex

def renameClick(control, event):
    global modelList
    modelList[0][boneIndex].Name = textEnter.Text
    populateList(modelList[0])

def stopScene(control, event):
    scenePlayer.Stop()

def addModel(control, event):
    global app, bvhCharacter
    fbxName = fbxPopup()
    app.FileMerge(fbxName, False)
    fbxCharacter = FBSystem().Scene.Characters[len(FBSystem().Scene.Characters) - 1]

    print 'Number of characters in scene = ', (len(FBSystem().Scene.Characters))

    fbxCharacter.InputCharacter = bvhCharacter
    fbxCharacter.InputType = FBCharacterInputType.kFBCharacterInputCharacter
    fbxCharacter.ActiveInput = True

def populateList(skeleton):
    global bvhList
    bvhList.Items.removeAll()
    for node in skeleton:
        bvhList.Items.append(node.Name)
    bvhList.Selected(boneIndex, True)
    
def addTailResponse(control, event):
    hipRef = FBFindModelByLabelName('BVH:Hips')
    tail = FBModelSkeleton('BVH:Tail')
    tail.Parent = hipRef
    tail.Show = True
    tail.Translation = FBVector3d(0, 0, -5)
    tail.Scaling = FBVector3d(0.5,0.5,0.5)
    hipRef2 = FBFindModelByLabelName('BVH:Tail')
    tail2 = FBModelSkeleton('BVH:Tail2')
    tail2.Parent = hipRef2
    tail2.Translation = FBVector3d(0, 1, -7)

modelList = []
skelList = []
boneIndex = 0
scenePlayer = FBPlayerControl()
FBXFilenames = []
bvhCharacter = None
app = None




lBipedMap = (('Reference', 'BVH:reference'),
        ('Hips','BVH:Hips'),
        ('Tail', 'BVH:Tail'),
        ( 'LeftUpLeg', 'BVH:LeftUpLeg' ),
        ( 'LeftLeg', 'BVH:LeftLeg' ),
        ( 'LeftFoot', 'BVH:LeftFoot'),
        ( 'RightUpLeg', 'BVH:RightUpLeg'),
        ( 'RightLeg', 'BVH:RightLeg'),
        ( 'RightFoot', 'BVH:RightFoot'),
        ( 'Spine', 'BVH:Spine'),
        ( 'LeftArm', 'BVH:LeftArm'),
        ( 'LeftForeArm', 'BVH:LeftForeArm'),
        ( 'LeftHand', 'BVH:LeftHand'),
        ( 'RightArm', 'BVH:RightArm'),
        ( 'RightForeArm', 'BVH:RightForeArm'),
        ( 'RightHand', 'BVH:RightHand'),
        ( 'Head', 'BVH:Head'),
        ( 'Neck', 'BVH:Neck'))


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

def loadBVH():
    lFp = FBFilePopup()
    lFp.Caption = "Select a BVH File to be Retargeted"
    lFp.Style = FBFilePopupStyle.kFBFilePopupOpen

    lFp.Filter = "*"

    # Set the default path.
    lFp.Path = r"C:\Users"
    # Get the GUI to show.
    lRes = lFp.Execute()
    # If we select files, show them, otherwise indicate that the selection was canceled
    if lRes:
        return lFp.Path + "/" + lFp.FileName
    else:
        FBMessageBox( "Invalid selection", "Selection canceled", "OK", None, None )


def loadFiles():
    from pyfbsdk import FBFilePopup, FBFilePopupStyle, FBMessageBox

    global FBXFilenames, bvhCharacter, app, BVHFilename

    app = FBApplication()
    app.FileNew()

    system = FBSystem()
    scene = system.Scene
    #POP UP FOR BVH FILE

    if (FBXFilenames == []):
        BVHFilename = loadBVH()
    #POP UP FOR FBX FILE(automatic redirect to tutorial folder)
    fbxName = fbxPopup()

    app.FileOpen(fbxName, False)

    fbxCharacter = app.CurrentCharacter
    print fbxCharacter
    print 'Number of characters in scene = ', (len(FBSystem().Scene.Characters))

    app.FileImport(BVHFilename, False)
    bvhCharacter = FBCharacter("MJ")

    for ( pslot, pjointname ) in lBipedMap:
        addJointToCharacter(bvhCharacter, pslot, pjointname)
    bvhCharacter.SetCharacterizeOn(True)
    bvhCharacter.CreateControlRig(True)
    
    controlRefName = FBFindModelByLabelName('BVH:reference')
    controlRefName.Translation = FBVector3d(0.0, 0.0, 0.0) 
    controlRefName.Scaling = FBVector3d(6.5, 6.5, 6.5) 
    
    fbxCharacter.InputCharacter = bvhCharacter
    fbxCharacter.InputType = FBCharacterInputType.kFBCharacterInputCharacter
    fbxCharacter.ActiveInput = True

    global skelList
    for enum in FBBodyNodeId.values:
        lBodyNodeId = FBBodyNodeId.values[enum]
        model = fbxCharacter.GetModel(lBodyNodeId)
        if (model != None):
             if model.ClassName() == 'FBModelSkeleton':
                skelList.append(model)

loadFiles()
scenePlayer.SetTransportFps(FBTimeMode.kFBTimeMode60Frames)

#UI WINDOW CREATION
tool = FBCreateUniqueTool("Retargeter")
tool.StartSizeX = 600
tool.StartSizeY = 200

x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
h = FBAddRegionParam(0,FBAttachType.kFBAttachBottom,"")
tool.AddRegion("main","main", x, y, w, h)

red = FBColor(0.8, 0.0, 0.1)
green = FBColor(0.1, 0.8, 0.0)

PlayButton = createButton("Play Scene", green)
PlayButton.OnClick.Add(playScene)

StopButton = createButton("Stop Scene", red)
StopButton.OnClick.Add(stopScene)

loadAll = createButton("Choose New Files", None)
loadAll.OnClick.Add(loadAllScene)

snakeButton = createButton ("Snake", None)
snakeButton.OnClick.Add(previewSnake)

MoveLef = createButton("Move Leg", None)
MoveLef.OnClick.Add(moveLeg)

nextFrame = createButton("Next Frame", None)
nextFrame.OnClick.Add(nextFrameRespone)

prevFrame = createButton("Prev Frame", None)
prevFrame.OnClick.Add(prevFrameRespone)

restartScene = createButton("Restart Scene", None)
restartScene.OnClick.Add(restartResponse)

addFBX = createButton("Add Model", None)
addFBX.OnClick.Add(addModel)

addTail = createButton("Add Tail", None)
addTail.OnClick.Add(addTailResponse)

global bvhList
bvhList = FBList()
bvhList.Style = FBListStyle.kFBDropDownList
populateList(skelList)
bvhList.ReadOnly = False
bvhList.OnChange.Add(selBone)

global textEnter
textEnter = FBEdit()
textEnter.Text = ""
skelList[0].Selected = True

renameBone = createButton("Rename Bone", None)
renameBone.OnClick.Add(renameClick)


hs = FBSlider()
hs.Orientation = FBOrientation.kFBHorizontal
hs.Caption ="frame slider"
hs.Min = scenePlayer.LoopStart.GetFrame()
hs.Max = scenePlayer.LoopStop.GetFrame()
#hs.SmallStep = 1
#hs.LargeStep = 1
hs.OnChange.Add(ValueChange)
hs.OnTransaction.Add(Transaction)
hs.Value = 0
#vbox.Add(hs, 30, height=5)

#Assembling the UI
hbox1 = FBHBoxLayout( FBAttachType.kFBAttachLeft )
hbox1.AddRelative(prevFrame, 1.0)
hbox1.AddRelative(PlayButton, 1.0)
hbox1.AddRelative(StopButton, 1.0)
hbox1.AddRelative(nextFrame, 1.0)
hbox1.AddRelative(MoveLef,1.0)

hbox2 = FBHBoxLayout( FBAttachType.kFBAttachLeft )
hbox2.AddRelative(bvhList, 2.0)
hbox2.AddRelative(textEnter, 2.0)
hbox2.AddRelative(renameBone, 1.0)

hbox3 = FBHBoxLayout( FBAttachType.kFBAttachLeft )
hbox3.AddRelative(addFBX, 2.0)
hbox3.AddRelative(loadAll, 1.0)
hbox3.AddRelative(snakeButton, 1.0)
hbox3.AddRelative(addTail,1.0)

window = FBVBoxLayout(FBAttachType.kFBAttachTop)
tool.SetControl("main", window)

window.AddRelative(hs, 1.0)
window.AddRelative(hbox1, 1.0)
window.AddRelative(hbox2, 1.0)
window.AddRelative(hbox3, 1.0)

#container = FBVisualContainer()

#window.AddRelative(container, 3.0)

ShowTool(tool)
