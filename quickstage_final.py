# bl_info is data that blender will read to recognize that its an addon, also works as a decription.
bl_info = {
    "name" : "Quick Stage",
    "description" : "Quickly set up a stage for your renders",
    "author" : "Samuel C.A (KomandoKartoffel)",
    "blender" : (2,92,0),
    "location" : "View3D > Panel",
    "wiki_url" : "",
    "category" : "Tools",
}
# ======================================================
# Module imports


import bpy                  # Blender's API - through here, python is able to interact with Blender and vice versa.
from math import radians    # 3D object rotation in blender - python uses radians instead of degrees.


# ======================================================
# Below is a class that contains custom properties. Data types that are preconfigured to work with the Blender API.


class QSProps(bpy.types.PropertyGroup):
    bl_idname = "object.QSCusProp"          # Every class has a bl_idname and a bl_label
    bl_label = "Quick Stage custom props"   # bl_idname is a reference for blender, bl_label is for human - the display name of the classes.
    
    # A bool for spawning camera with lights or without. Bool will be displayed as toggleable check box.
    CamLitRig : bpy.props.BoolProperty(name = "Camera Light", description = "Make a light, attached to the selected camera", default = False)
    
    # An Enumerator is list that will be turned into a dropdown menu.
    # A list of selectable screen ratios.
    ScrRat : bpy.props.EnumProperty(
        name = "Screen Ratio",
        description = "Set camera ratio you want",
        items = [('Sqr', "1:1", "Square"),
                ('SDScr', "4:3", "SDTV"),
                ('HDScr', "16:9", "HDTV"),
                ('WideScr', "21:9", "Ultrawide")
        ]
        # Each item in "items" comes is this format: ('blender reference', 'dropdown menu display', 'item tooltip description')
    )
    
    # A list of selectable screen resolution.
    ScrReso : bpy.props.EnumProperty(
        name = "Render Resolution",
        description = "Quickly set the render resolution",
        items = [('res720', "720p", ""),
                ('res1080', "1080p", ""),
                ('res1440', "1440p", ""),
                ('res2160', "2160p", ""),
                ('res4320', "4320p", "")
        ]
    )
    
    # A list of light set that later can be made.
    MakeLight : bpy.props.EnumProperty(
        name = "Render Resolution",
        description = "Quickly set the render resolution",
        items = [('clmshll', "Clamshell", "Two middle lights, one above subject, one below subject."),
                ('fltlt', "Flat Light", "Two lights at equal power, position at the side of the camera."),
                ('kfh', "Key Fill & Highlight", "Two softlight, one on the left side, one on the right side with half strenght. A highlight lamp from above, aimed at the subject."),
                ('hghky', "High Key", "A 45 degree light at full strength at the left, a soft light at the side of subject, and a background fill light."),
                ('lprmlt', "Loop with Rim Light", "A 45 degree light at full strength at the left. A high powered lamp behind the subject."),
                ('hkk', "Hard Key with Kickers", "Two soft lights behind the subject, a single hard light at an angle towards subject."),
                ('bgr', "Badger", "Two soft lights behind the subject.")
                  
        ]
    )


# ======================================================
# Below is a group of classes that governs panel displays. Basically displayed menus.

     
# Render Setting panel. Will display to user, the enum list 
# of dropdown menu from the custom properties above.
# In this panel, user can select screen resolution and ratio.
class RendSet(bpy.types.Panel):
    bl_label = "Render Settings"
    bl_idname = "quickstage_PT_RendSet"
    bl_space_type = "VIEW_3D"               # Dictates which screen its displayed, here its 3D view
    bl_region_type = "UI"                   # Dictates which section of the screen its displayed in, here its the tab groups
    bl_category = "Quick Stage"             # Tab name
    bl_options = {'DEFAULT_CLOSED'}         # When displayed, panel will be by default in compact view
    
    # Each panel class has a draw function,
    # which will draw buttons, menus, etc.
    def draw(self, context):    
        
        # First, declare variables
        layout = self.layout                # layout is the panel's layout - displaying line per line.
        scene = context.scene               # scene is the current scene in context.
        QSData = scene.QSProp               # QSData is pointed to our custom properties pointer. (Under the hood, Blender is written in C/C++)
        
        layout.prop(QSData, "ScrRat")       # Make a dropdown menu, based on custom properties' ScrRat (screen ratio)
        layout.operator("object.scrrat")    # Make a button that execute a function-like class, that sets the screen ratio
        layout.prop(QSData, "ScrReso")      # same like layout.prop(QSData, "ScrRat"), but for screen resolution
        layout.operator("object.scrreso")   # same, another button for a function-like class, sets screen resolution


# Panel for making camera rigs.
# Users can choose, make a simple or complex rig, with or without light.
class CamRigPnl(bpy.types.Panel):
    bl_label = "Camera Quick Rig"
    bl_idname = "quickstage_PT_CamRig"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Quick Stage"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        QSData = scene.QSProp
        
        layout.prop(QSData, "CamLitRig")
        layout.operator("object.crigs")
        layout.operator("object.crigc")

# Panel for making preconfigured light set up rigs.
# Users can choose from dropdown menu.
class LitSetPnl(bpy.types.Panel):
    bl_label = "Light Setup"
    bl_idname = "quickstage_PT_LitSet"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Quick Stage"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        QSData = scene.QSProp
        
        layout.prop(QSData, "MakeLight")
        layout.operator("object.lsrig")


# ======================================================
# Below is a group of classes that are programmed to do a certain task 
# when called, acts like function. Takes an argument, usually from
# the custom properties data, context, and self, then execute lines of codes.


# Ratio Change (class RatChg), takes in the current screen height, and multiplies it based on the selected ratio
# then applying it to the screen width
# This class is also called in Resolution Change (class ResoChg) to dynamically apply the ratio
class RatChg(bpy.types.Operator):
    bl_label = "Change Ratio"
    bl_idname = "object.scrrat"
    
    def execute(self, context):
        # Same like in def draw, variables are assigned inside the execute function, so that it will be refreshed
        # with the latest data everytime the class is called.
        
        # Directly takes value from the blender data. An alternative is to use context.scene
        # but i dont like using that since it can cause discrepancies between displyed
        # values and actual values inside the blender data.
        self.ScrHeight = bpy.data.scenes['Scene'].render.resolution_y
        self.ScrWidth = bpy.data.scenes['Scene'].render.resolution_x
        
        self.QSData = bpy.context.scene.QSProp
        
        # A series of if-else statments that read the current dropdown menu selection.
        # and set the resolution accordingly.
        if self.QSData.ScrRat == 'Sqr':
            self.ScrWidth = self.ScrHeight
            bpy.data.scenes['Scene'].render.resolution_x = int(self.ScrWidth)
            
            # A report function that appears on the bottom of the screen.
            # Useful for reporting error, exception, etc. But this one ('INFO')
            # is just a simple notification.
            self.report({'INFO'},'Render set to Square')
        
        elif self.QSData.ScrRat == 'SDScr':
            self.ScrWidth = 4 * (self.ScrHeight / 3)
            bpy.data.scenes['Scene'].render.resolution_x = self.ScrWidth
            self.report({'INFO'},'Render set to SD')
            
        elif self.QSData.ScrRat == 'HDScr':
            self.ScrWidth = 16 * (self.ScrHeight / 9)
            bpy.data.scenes['Scene'].render.resolution_x = self.ScrWidth
            self.report({'INFO'},'Render set to HD')
        
        elif self.QSData.ScrRat == 'WideScr':
            self.ScrWidth = 21 * (self.ScrHeight / 9)
            bpy.data.scenes['Scene'].render.resolution_x = self.ScrWidth
            self.report({'INFO'},'Render set to Ultrawide')
        
        return {'FINISHED'}


# Based on the selected resoltion from the dropdown menu, will change the render resolution 
# of the camera.
class ResoChg(bpy.types.Operator):
    bl_label = "Change Render Resolution"
    bl_idname = "object.scrreso"
    
    # This is pretty much the same as RatChg, but deals with resolution instead.
    
    def execute(self, context):
        
        self.ScrHeight = bpy.data.scenes['Scene'].render.resolution_y
        self.ScrWidth = bpy.data.scenes['Scene'].render.resolution_x
        self.QSData = bpy.context.scene.QSProp
        
        if self.QSData.ScrReso == 'res720':
            bpy.data.scenes['Scene'].render.resolution_y = 720
            
            # Calls screen ratio class once again to dynamically adjust ratio
            bpy.ops.object.scrrat()
            
            self.report({'INFO'},'Resolution is now: 720p')
        
        elif self.QSData.ScrReso == 'res1080':
            bpy.data.scenes['Scene'].render.resolution_y = 1080
            bpy.ops.object.scrrat()
            self.report({'INFO'},'Resolution is now: 1080p')
            
        elif self.QSData.ScrReso == 'res1440':
            bpy.data.scenes['Scene'].render.resolution_y = 1440
            bpy.ops.object.scrrat()
            self.report({'INFO'},'Resolution is now: 1440p')
            
        elif self.QSData.ScrReso == 'res2160':
            bpy.data.scenes['Scene'].render.resolution_y = 2160
            bpy.ops.object.scrrat()
            self.report({'INFO'},'Resolution is now: 2160p')
            
        elif self.QSData.ScrReso == 'res4320':
            bpy.data.scenes['Scene'].render.resolution_y = 4320
            bpy.ops.object.scrrat()
            self.report({'INFO'},'Resolution is now: 4320p')
            
        return {'FINISHED'}
 

# Class for making simple camera rig.
class CamRigSmpl(bpy.types.Operator):
    bl_label = "Make Simple Cam Rig"
    bl_idname = "object.crigs"
    
    def execute(self, context):
        QSData = context.scene.QSProp
        
        # bpy.ops is part of the operator functions - this one will 'spawn' a reference point.
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        # When objects are first made, its selected as active object by default.
        # This line will take that, and assigned it to a variable as a value for future reference.
        empty = bpy.context.active_object
        
        # Make a camera, assign it to 'cam'
        bpy.ops.object.camera_add(enter_editmode=False, align='WORLD', location=(0, -10, 0), rotation=(1.5708, -0, -0), scale=(1, 1, 1))
        cam = bpy.context.active_object
        
        # Rename the camera and reference point
        cam.name = "Camera Rig"
        empty.name = "Focus Rig"
        
        # Add a constraint to the camera to always face the reference point - now called 'Focus Rig'.
        cam.constraints.new('TRACK_TO')
        cam.constraints['Track To'].target = empty
    
        selrep = 'Simple camera rig made.'
        
        # If user wanted a light attached to the camera, this part will run.
        if QSData.CamLitRig == True:
            
            bpy.ops.object.light_add(type='SPOT', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            spot = bpy.context.active_object
            spot.name = "Cam Light Rig"
            
            spot.constraints.new('COPY_TRANSFORMS')
            spot.constraints['Copy Transforms'].target = cam
            
            # Now this part modifies the value of the light.
            spot.data.energy = 1500             # Dictates brightness/luminescences.
            spot.data.shadow_soft_size = 6      # How dispersed is the light
            spot.data.spot_blend = 1            # Blured or sharp.
            spot.data.spot_size = 1.13446       # How big is the spotlight radius

            selrep = 'Simple camera rig, with camera light made.'
    
        self.report({'INFO'}, selrep)
        return {'FINISHED'}


# Class for making complex camera rig.
class CamRigCmplx(bpy.types.Operator):
    bl_label = "Make Complex Cam Rig"
    bl_idname = "object.crigc"
    
    def execute(self, context):
        QSData = context.scene.QSProp
        
        # Again, make various componenets of the camera rig.
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        empty = bpy.context.active_object
        
        bpy.ops.object.camera_add(enter_editmode=False, align='WORLD', location=(0, -10, 0), rotation=(1.5708, -0, -0), scale=(1, 1, 1))
        cam = bpy.context.active_object
        
        bpy.ops.object.empty_add(type='CUBE', align='WORLD', location=(0, -10, 0), scale=(1, 1, 1))
        cube = bpy.context.active_object
        
        bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        sphere = bpy.context.active_object
        
        # Rename the objects.
        empty.name = "Focus Rig"
        sphere.name = "Rotation Rig"
        cube.name = "Zoom Rig"
        cam.name = "Camera Rig"
        
        # Start adding constraints
        empty.constraints.new('LIMIT_ROTATION')
        empty.constraints['Limit Rotation'].use_limit_x = True
        empty.constraints['Limit Rotation'].use_limit_y = True
        empty.constraints['Limit Rotation'].use_limit_z = True

        sphere.constraints.new('COPY_LOCATION')
        sphere.constraints['Copy Location'].target = empty
        
        # This one is object parenting procedure.
        bpy.ops.object.select_all(action='DESELECT')                        # First it clears selections, so no active object.
        cube.select_set(True)                                               # select cube.
        sphere.select_set(True)                                             # select sphere.
        bpy.context.view_layer.objects.active = sphere                      # make sphere active object to be parented to.
        bpy.ops.object.parent_set(type = 'OBJECT', keep_transform = True)   # Parent the selected object(s) (this time only the cube), to the active object (sphere).
        
        # More constraints declaration and setting. This one is limit cube location movement in relation to sphere.
        cube.constraints.new('LIMIT_LOCATION')
        cube.constraints['Limit Location'].use_min_x = True
        cube.constraints['Limit Location'].use_max_x = True
        cube.constraints['Limit Location'].use_min_z = True
        cube.constraints['Limit Location'].use_max_z = True
        cube.constraints['Limit Location'].owner_space = 'CUSTOM'
        cube.constraints['Limit Location'].space_object = sphere
        
        # Constraint cam to follow cube and always face focus point.
        cam.constraints.new('COPY_LOCATION')
        cam.constraints['Copy Location'].target = cube
        cam.constraints.new('TRACK_TO')
        cam.constraints['Track To'].target = empty
        
        selrep = 'Complex camera rig made.'
        
        if QSData.CamLitRig == True:
            
            bpy.ops.object.light_add(type='SPOT', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            spot = bpy.context.active_object
            spot.name = "Cam Light Rig"
            
            spot.constraints.new('COPY_TRANSFORMS')
            spot.constraints['Copy Transforms'].target = cam
            
            spot.data.energy = 1500
            spot.data.shadow_soft_size = 6
            spot.data.spot_blend = 1
            spot.data.spot_size = 1.13446

            selrep = 'Complex camera rig, with camera light made.'
    
        self.report({'INFO'}, selrep)
        return {'FINISHED'}


class LitSetRig(bpy.types.Operator):
    bl_label = "Make Light Setup"
    bl_idname = "object.lsrig"
    
    def execute(self, context):
        self.QSData = context.scene.QSProp
        
        if self.QSData.MakeLight == 'clmshll':
            
            # This one and the next 6 if-else statement is similar in structure.
            # Just different combination of setup.
            
            # Make 2 lights, one above, one below. Set the reference (Upper light = l1, lower light = l2)
            bpy.ops.object.light_add(type='AREA', radius = 2.5, align='WORLD', location=(0, -5, 4.75), rotation=(1.13446, 0, 0), scale=(1, 1, 1))
            l1 = bpy.context.active_object
            bpy.ops.object.light_add(type='AREA', radius = 2.5, align='WORLD', location=(0, -5, 1.5), rotation=(2.00713, 0, 0), scale=(1, 1, 1))
            l2 = bpy.context.active_object

            # Set luminescence to 250 watt each
            l1.data.energy = 250
            l2.data.energy = 250
            l1.name = "Upper Light ClmShll"
            l1.name = "Lower Light ClmShll"

            # Make a focus point for the light
            bpy.ops.object.empty_add(type='SPHERE', radius = 1.15, align='WORLD', location=(0, 0, 3.12), scale=(1, 1, 1))
            litfoc = bpy.context.active_object
            litfoc.name = "Light Focus ClmShll"

            # Constraint both lights to aim to the focus point
            l1.constraints.new('TRACK_TO')
            l1.constraints['Track To'].target = litfoc
            l2.constraints.new('TRACK_TO')
            l2.constraints['Track To'].target = litfoc

            # Make base to move the entire light set.
            bpy.ops.object.empty_add(type='CIRCLE', radius=5, align='WORLD', location=(0, 0, 1.8), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
            litbase = bpy.context.active_object
            litbase.name = "Set Base ClmShll"

            # Select all light set objects, parent it to the base.
            bpy.ops.object.select_all(action='DESELECT')
            l1.select_set(True)
            l2.select_set(True)
            litfoc.select_set(True)
            litbase.select_set(True)
            bpy.context.view_layer.objects.active = litbase
            bpy.ops.object.parent_set(type = 'OBJECT', keep_transform = True)
            
            selrep = "Light setup made: Clamshell"
            
        elif self.QSData.MakeLight == 'fltlt':
            
            bpy.ops.object.light_add(type='AREA', radius=3, align='WORLD', location=(5, -5, 3), rotation=(1.5708, 0, 0.785398), scale=(1, 1, 1))
            lLeft = bpy.context.active_object
            bpy.ops.object.light_add(type='AREA', radius=3, align='WORLD', location=(-5, -5, 3), rotation=(1.5708, 0, -0.785398), scale=(1, 1, 1))
            lRight = bpy.context.active_object

            lLeft.data.energy = 250
            lRight.data.energy = 250
            lLeft.name = "Left Light FltLt"
            lRight.name = "Right Light FltLt"

            bpy.ops.object.empty_add(type='SPHERE', radius = 1.15, align='WORLD', location=(0, 0, 3), scale=(1, 1, 1))
            litfoc = bpy.context.active_object
            litfoc.name = "Light Focus FltLt"

            lLeft.constraints.new('TRACK_TO')
            lLeft.constraints['Track To'].target = litfoc
            lRight.constraints.new('TRACK_TO')
            lRight.constraints['Track To'].target = litfoc

            bpy.ops.object.empty_add(type='CIRCLE', radius=5, align='WORLD', location=(0, 0, 1.5), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
            litbase = bpy.context.active_object
            litbase.name = "Set Base FltLt"

            bpy.ops.object.select_all(action='DESELECT')
            lLeft.select_set(True)
            lRight.select_set(True)
            litfoc.select_set(True)
            litbase.select_set(True)
            bpy.context.view_layer.objects.active = litbase
            bpy.ops.object.parent_set(type = 'OBJECT', keep_transform = True)
            
            selrep = "Light setup made: Flatlight"
                        
        elif self.QSData.MakeLight == 'kfh':
            
            bpy.ops.object.light_add(type='AREA', radius=3, align='WORLD', location=(5, -5, 2.5), rotation=(1.5708, 0, 0.785398), scale=(1, 1, 1))
            lfill = bpy.context.active_object
            bpy.ops.object.light_add(type='AREA', radius=3, align='WORLD', location=(-3.5, -3.5, 3), rotation=(1.5708, 0, -0.785398), scale=(1, 1, 1))
            lkey = bpy.context.active_object

            lkey.data.energy = 400
            lfill.data.energy = 200
            lkey.name = "Key Light KFHLt"
            lfill.name = "Fill Light KFHLt"

            bpy.ops.object.light_add(type='SPOT', radius=3, align='WORLD', location=(1.5, 1.5, 8), rotation=(-0.314159, 0.314159, 0), scale=(1, 1, 1))
            lhigh = bpy.context.active_object
            lhigh.name = "Highlight KFHLt"
            lhigh.data.energy = 2500
            lhigh.data.shadow_soft_size = 1.5
            lhigh.data.spot_size = 0.872665
            lhigh.data.spot_blend = 0

            bpy.ops.object.empty_add(type='CIRCLE', radius=5, align='WORLD', location=(0, 0, 1.8), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
            litbase = bpy.context.active_object
            litbase.name = "Set Base KFHLt"

            bpy.ops.object.select_all(action='DESELECT')
            lhigh.select_set(True)
            lkey.select_set(True)
            lfill.select_set(True)
            litbase.select_set(True)
            bpy.context.view_layer.objects.active = litbase
            bpy.ops.object.parent_set(type = 'OBJECT', keep_transform = True)
            
            selrep = "Light setup made: Key & Fill lights"

        elif self.QSData.MakeLight == 'hghky':
            
            bpy.ops.object.light_add(type='AREA', radius=3, align='WORLD', location=(5, -5, 2.5), rotation=(1.5708, 0, 0.785398), scale=(1, 1, 1))
            lfill = bpy.context.active_object
            bpy.ops.object.light_add(type='AREA', radius=3, align='WORLD', location=(-3.5, -3.5, 3), rotation=(1.5708, 0, -0.785398), scale=(1, 1, 1))
            lkey = bpy.context.active_object

            lkey.data.energy = 400
            lfill.data.energy = 200
            
            lkey.name = "Key Light KF"
            lfill.name = "Fill Light KF"
            
            bpy.ops.object.empty_add(type='CIRCLE', radius=5, align='WORLD', location=(0, 0, 1.8), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
            litbase = bpy.context.active_object
            litbase.name = "Set Base KF"

            bpy.ops.object.select_all(action='DESELECT')
            lkey.select_set(True)
            lfill.select_set(True)
            litbase.select_set(True)
            bpy.context.view_layer.objects.active = litbase
            bpy.ops.object.parent_set(type = 'OBJECT', keep_transform = True)
            
            selrep = "Light setup made: Key & Fill with highlight"
            
        elif self.QSData.MakeLight == 'lprmlt':
            
            bpy.ops.object.light_add(type='AREA', radius=3, align='WORLD', location=(-3.5, -3.5, 3), rotation=(1.5708, 0, -0.785398), scale=(1, 1, 1))
            lkey = bpy.context.active_object
            lkey.data.energy = 400
            lkey.name = "Key Light LpRm"

            bpy.ops.object.light_add(type='SPOT', radius=3, align='WORLD', location=(2, 4, 5), rotation=(-1.27409, 0, -0.47473), scale=(1, 1, 1))
            lhigh = bpy.context.active_object

            lhigh.name = "Highlight LpRm"
            lhigh.data.energy = 2500
            lhigh.data.shadow_soft_size = 1.5
            lhigh.data.spot_size = 0.523599
            lhigh.data.spot_blend = 0
            
            bpy.ops.object.empty_add(type='CIRCLE', radius=5, align='WORLD', location=(0, 0, 1.8), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
            litbase = bpy.context.active_object
            litbase.name = "Set Base LpRm"
            
            bpy.ops.object.select_all(action='DESELECT')
            lkey.select_set(True)
            lfill.select_set(True)
            litbase.select_set(True)
            bpy.context.view_layer.objects.active = litbase
            bpy.ops.object.parent_set(type = 'OBJECT', keep_transform = True)
            
            selrep = "Light setup made: Loop with rim light"
            
        elif self.QSData.MakeLight == 'hkk':
            
            bpy.ops.object.light_add(type='AREA', radius=2, align='WORLD', location=(3.5, 4, 2.5), rotation=(-1.5708, 0, -0.637045), scale=(1, 1, 1))
            l1 = bpy.context.active_object
            bpy.ops.object.light_add(type='AREA', radius=2, align='WORLD', location=(-3.5, 4, 2.5), rotation=(-1.5708, 0, 0.637045), scale=(1, 1, 1))
            l2 = bpy.context.active_object

            l1.data.energy = 300
            l2.data.energy = 300
            l1.name = "Back Light1 HKK"
            l1.name = "Back Light2 HKK"
            
            bpy.ops.object.light_add(type='SPOT', radius=3, align='WORLD', location=(0.8, -5, 5), rotation=(1.22173, 0, 0.174533), scale=(1, 1, 1))
            lk = bpy.context.active_object
            lk.data.energy = 1000
            lk.name = "Kicker Light HKK"

            bpy.ops.object.empty_add(type='CIRCLE', radius=5, align='WORLD', location=(0, 0, 1.8), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
            litbase = bpy.context.active_object
            litbase.name = "Set Base HKK"

            bpy.ops.object.select_all(action='DESELECT')
            l1.select_set(True)
            l2.select_set(True)
            lk.select_set(True)
            litbase.select_set(True)
            bpy.context.view_layer.objects.active = litbase
            bpy.ops.object.parent_set(type = 'OBJECT', keep_transform = True)
            
            selrep = "Light setup made: High key with Kickers"
            
        elif self.QSData.MakeLight == 'bgr':
            
            bpy.ops.object.light_add(type='AREA', radius=2, align='WORLD', location=(3.5, 4, 2.5), rotation=(-1.5708, 0, -0.637045), scale=(1, 1, 1))
            l1 = bpy.context.active_object
            bpy.ops.object.light_add(type='AREA', radius=2, align='WORLD', location=(-3.5, 4, 2.5), rotation=(-1.5708, 0, 0.637045), scale=(1, 1, 1))
            l2 = bpy.context.active_object

            l1.data.energy = 500
            l2.data.energy = 500
            l1.name = "Upper Light Bdgr"
            l1.name = "Lower Light Bdgr"

            bpy.ops.object.empty_add(type='SPHERE', radius = 1.15, align='WORLD', location=(0, 0, 3.5), scale=(1, 1, 1))
            litfoc = bpy.context.active_object
            litfoc.name = "Light Focus Bdgr"

            l1.constraints.new('TRACK_TO')
            l1.constraints['Track To'].target = litfoc
            l2.constraints.new('TRACK_TO')
            l2.constraints['Track To'].target = litfoc

            bpy.ops.object.empty_add(type='CIRCLE', radius=5, align='WORLD', location=(0, 0, 1.8), rotation=(1.5708, 0, 0), scale=(1, 1, 1))
            litbase = bpy.context.active_object
            litbase.name = "Set Base Bdgr"

            bpy.ops.object.select_all(action='DESELECT')
            l1.select_set(True)
            l2.select_set(True)
            litfoc.select_set(True)
            litbase.select_set(True)
            bpy.context.view_layer.objects.active = litbase
            bpy.ops.object.parent_set(type = 'OBJECT', keep_transform = True)
            
            selrep = "Light setup made: Badger"
            
        self.report({'INFO'}, selrep)
        return {'FINISHED'}


# ======================================================
# Addon installation and setup.

# A list of all the classes in the python script
classes = [QSProps, RendSet, CamRigPnl, RatChg, LitSetPnl, ResoChg, CamRigCmplx, CamRigSmpl, LitSetRig]

# Will "install" the classes in 'classes' list.
def register():
    for items in classes:
        bpy.utils.register_class(items)
    
    # Will install our custom properties    
    bpy.types.Scene.QSProp = bpy.props.PointerProperty(type = QSProps)

# Uninstall 
def unregister():
    for items in classes:
        bpy.utils.unregister_class(items)
        
    # Will uninstall our custom properties   
    del bpy.types.Scene.QSProp


# ======================================================
# Script execution


# When script is run, all it does is just install the classes.
# Blender will take care of the execution of the classes, display
# of panels, custom properties values, etc.
if __name__ == "__main__":
    register()    


# ======================================================
# ======================================================
# ======================================================

# Special thanks to:
#
# Author of Blender: Ton Roosendaal - for making an amazing software...for free!
# Blender Foundation & Institute
# Blender and Open Source community in large
# Author of Python: Guido van Rossum
# 
# Curtis Holt and his youtube tutorials on Blender Python API
# https://youtu.be/XqX5wh4YeRw
#
# Digital Camera World for their handy lighting guide
# https://www.digitalcameraworld.com/tutorials/cheat-sheet-pro-portrait-lighting-setups
# 
# Darkfall studio, also for his tutorials
# https://www.youtube.com/c/DarkfallBlender/about
# https://darkfallblender.blogspot.com/
#
# Blender Stack Exchange
# https://blender.stackexchange.com/
#
# CS50 Discord community and people
#
# W3 School for help with python syntax
# https://www.w3schools.com/python/
#
# Last but not least, my fellow 3D artists friends that tested my script.

# ======================================================
# ======================================================
# ======================================================