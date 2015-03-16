from pyfbsdk import *
from pyfbsdk_additions import *
import os

def GetMotionBuilderInstallationDirectory() :
    applicationPath = FBSystem().ApplicationPath
    return applicationPath[0:applicationPath.index('bin')]
    
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
    print control.Value
    
def Transaction(control,event):
    print "Transaction, is begin: ", event.IsBeginTransaction
    if(event.IsBeginTransaction==False):
        print control.Value
        if(control.Value>.5):
            i=0
            while(i<(((control.Value)-.5)*100)):
                  lPlayer = FBPlayerControl()
                  lPlayer.StepForward()
                  i+=1
        elif(control.Value<.5):
            i=0
            while(i>(((control.Value)-.5)*100)):
                  lPlayer = FBPlayerControl()
                  lPlayer.StepBackward()
                  i-=1
        control.Value=.5
            
def playScene(control, event)   :
    FBPlayerControl().SetTransportFps(FBTimeMode.kFBTimeMode60Frames)
    lPlayer = FBPlayerControl()
    
    lPlayer.Play()
def restartResponse(control, event):
    FBPlayerControl().SetTransportFps(FBTimeMode.kFBTimeMode60Frames)
    lPlayer = FBPlayerControl()
    lPlayer.GotoStart()
    
def loadAllScene(control,event):
    loadFiles()

def nextFrameRespone(control,event):
    FBPlayerControl().SetTransportFps(FBTimeMode.kFBTimeMode60Frames)
    lPlayer = FBPlayerControl()
    lPlayer.StepForward()

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
    global skelList
    global index
    for node in skelList:
        node.Selected = False
    skelList[control.ItemIndex].Selected = True
    index = control.ItemIndex
    
def renameClick(control, event):
    skelList[boneIndex].Name = textEnter.Text

def stopScene(control, event):
    playback = FBPlayerControl()
    playback.Stop()

skelList = []
boneIndex = 0
    
lBipedMap = (('Reference', 'BVH:reference'),
        ('Hips','BVH:Hips'),
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
            

def loadFiles():
    from pyfbsdk import FBFilePopup, FBFilePopupStyle, FBMessageBox 
    app = FBApplication()
    app.FileNew()

    system = FBSystem()
    scene = system.Scene
    #POP UP FOR BVH FILE
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
        BVHFilename = lFp.Path + "/" + lFp.FileName
    else:
        FBMessageBox( "Invalid selection", "Selection canceled", "OK", None, None )
    
    #POP UP FOR FBX FILE(automatic redirect to tutorial folder)
    lFp2 = FBFilePopup()
    lFp2.Caption = "Select an FBX File for the Retargeting"
    lFp2.Style = FBFilePopupStyle.kFBFilePopupOpen
    
    lFp2.Filter = "*"
    
    # Set the default path.
    lFp2.Path = GetMotionBuilderInstallationDirectory()+"Tutorials"
    # Get the GUI to show.
    lRes = lFp2.Execute()
    # If we select files, show them, otherwise indicate that the selection was canceled
    if lRes:
        FBXFilename = lFp2.Path + "/" + lFp2.FileName
    else:
        FBMessageBox( "Invalid selection", "Selection canceled", "OK", None, None )
    # Cleanup.
    del( lFp2, lRes, FBFilePopup, FBFilePopupStyle, FBMessageBox )
     
    app.FileOpen(FBXFilename, False)
    fbxCharacter = FBApplication().CurrentCharacter
    
    
    app.FileImport(BVHFilename, False)
    bvhCharacter = FBCharacter("MJ")
    
    for ( pslot, pjointname ) in lBipedMap:
        addJointToCharacter(bvhCharacter, pslot, pjointname)
    bvhCharacter.SetCharacterizeOn(True)
    bvhCharacter.CreateControlRig(True)
    
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

#UI WINDOW CREATION
tool = FBCreateUniqueTool("Retargeter")
tool.StartSizeX = 400
tool.StartSizeY = 400

x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
h = FBAddRegionParam(0,FBAttachType.kFBAttachBottom,"")
tool.AddRegion("main","main", x, y, w, h)

vbox = FBVBoxLayout( FBAttachType.kFBAttachTop )
tool.SetControl("main",vbox)

red = FBColor(0.8, 0.0, 0.1)
green = FBColor(0.1, 0.8, 0.0)

PlayButton = createButton("Play Scene", green)
vbox.Add(PlayButton,50)
PlayButton.OnClick.Add(playScene)

StopButton = createButton("Stop Scene", red)
vbox.Add(StopButton,50)
StopButton.OnClick.Add(stopScene)

loadAll = createButton("Choose New Files", None)
vbox.Add(loadAll,50)
loadAll.OnClick.Add(loadAllScene)

nextFrame = createButton("Next Frame", None)
vbox.Add(nextFrame,50)
nextFrame.OnClick.Add(nextFrameRespone)

restartScene = createButton("Restart Scene", None)
vbox.Add(restartScene,50)
restartScene.OnClick.Add(restartResponse)

hbox = FBHBoxLayout( FBAttachType.kFBAttachLeft )

bvhList = FBList()
bvhList.Style = FBListStyle.kFBDropDownList
for node in skelList:
    bvhList.Items.append(node.Name)
bvhList.ReadOnly = False
bvhList.OnChange.Add(selBone)
hbox.AddRelative(bvhList, 2.0)

global textEnter
textEnter = FBEdit()
textEnter.Text = ""
hbox.AddRelative(textEnter, 2.0)
skelList[0].Selected = True

renameBone = createButton("Rename Bone", None)
renameBone.OnClick.Add(renameClick)
hbox.AddRelative(renameBone, 1.0)


hs = FBSlider()    
hs.Orientation = FBOrientation.kFBHorizontal  
hs.Caption ="frame slider"
hs.Style = FBButtonStyle.kFB2States
hs.Look = FBButtonLook.kFBLookColorChange
hs.Justify = FBTextJustify.kFBTextJustifyCenter
hs.SmallStep = 10
hs.LargeStep = 10 
hs.OnChange.Add(ValueChange)
hs.OnTransaction.Add(Transaction)
vbox.Add(hs, 30, height=5)

vbox.Add(hbox, 50)


container = FBVisualContainer()

vbox.AddRelative(container, 3.0)

ShowTool(tool)