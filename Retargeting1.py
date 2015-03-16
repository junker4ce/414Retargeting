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
    
##    FBPlayerControl().SetTransportFps(FBTimeMode.kFBTimeMode60Frames)
##    lPlayer = FBPlayerControl()
##    
##    lPlayer.

def stopScene(control, event):
    playback = FBPlayerControl()
    playback.Stop()
    
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
    GremlinCharacter = FBApplication().CurrentCharacter
    
    
    app.FileImport(BVHFilename, False)
    MJCharacter = FBCharacter("MJ")
    
    for ( pslot, pjointname ) in lBipedMap:
        addJointToCharacter(MJCharacter, pslot, pjointname)
    MJCharacter.SetCharacterizeOn(True)
    MJCharacter.CreateControlRig(True)
    
    GremlinCharacter.InputCharacter = MJCharacter
    GremlinCharacter.InputType = FBCharacterInputType.kFBCharacterInputCharacter
    GremlinCharacter.ActiveInput = True
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

PlayButton = FBButton()
PlayButton.Caption = "Play Scene"
PlayButton.Style = FBButtonStyle.kFB2States
PlayButton.Look = FBButtonLook.kFBLookColorChange
PlayButton.Justify = FBTextJustify.kFBTextJustifyCenter
PlayButton.SetStateColor(FBButtonState.kFBButtonState0,FBColor(0.1, 0.8, 0.0))
vbox.Add(PlayButton,50)
PlayButton.OnClick.Add(playScene)

StopButton = FBButton()
StopButton.Caption = "Stop Scene"
StopButton.Style = FBButtonStyle.kFB2States
StopButton.Look = FBButtonLook.kFBLookColorChange
StopButton.Justify = FBTextJustify.kFBTextJustifyCenter
StopButton.SetStateColor(FBButtonState.kFBButtonState0,FBColor(0.8, 0.0, 0.1))
vbox.Add(StopButton,50)
StopButton.OnClick.Add(stopScene)

loadAll = FBButton()
loadAll.Caption = "Choose New Files"
loadAll.Style = FBButtonStyle.kFB2States
loadAll.Look = FBButtonLook.kFBLookColorChange
loadAll.Justify = FBTextJustify.kFBTextJustifyCenter
loadAll.SetStateColor(FBButtonState.kFBButtonState0,FBColor(0.8, 0.0, 0.1))
vbox.Add(loadAll,50)
loadAll.OnClick.Add(loadAllScene)

nextFrame = FBButton()
nextFrame.Caption = "Next Frame"
nextFrame.Style = FBButtonStyle.kFB2States
nextFrame.Look = FBButtonLook.kFBLookColorChange
nextFrame.Justify = FBTextJustify.kFBTextJustifyCenter
nextFrame.SetStateColor(FBButtonState.kFBButtonState0,FBColor(0.8, 0.0, 0.1))
vbox.Add(nextFrame,50)
nextFrame.OnClick.Add(nextFrameRespone)

restartScene = FBButton()
restartScene.Caption = "Restart Scene"
restartScene.Style = FBButtonStyle.kFB2States
restartScene.Look = FBButtonLook.kFBLookColorChange
restartScene.Justify = FBTextJustify.kFBTextJustifyCenter
restartScene.SetStateColor(FBButtonState.kFBButtonState0,FBColor(0.8, 0.0, 0.1))
vbox.Add(restartScene,50)
restartScene.OnClick.Add(restartResponse)

container = FBVisualContainer()

vbox.AddRelative(container, 3.0)

ShowTool(tool)