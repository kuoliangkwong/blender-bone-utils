bl_info = {
    "name": "Bone Utils",
    "author": "Kwong Kuo Liang (KKL)",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "Pose Mode > Bone Utils (Right side of 3D View)",
    "description": "Bone Utilities",
    "category": "Pose"
}

import bpy

class MainPanel(bpy.types.Panel):
    bl_idname = "MAIN_PANEL"
    bl_label = "About"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Bone Utils'
    bl_context = "posemode"

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row() 
        row.label(text="Developed by Kwong Kuo Liang (KKL)")

class BatchEnableConstraintsPanel(MainPanel, bpy.types.Panel):
    bl_idname = "BATCH_ENABLE_CONSTRAINTS_PANEL"
    bl_label = "Enable Bone Constraints"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.label(text="Enable/Disable all bone constraints from selected bones")
        row = layout.row()
        row.operator('op.enable_constraints', text='Enable')
        row.operator('op.disable_constraints', text='Disable')

class EnableConstraintsOp(bpy.types.Operator): 
    bl_idname = "op.enable_constraints"
    bl_label = "Enable constraints in selected bones" 

    def execute(self, context):
        enableConstraints(True)
        return {'FINISHED'}

class DisableConstraintsOp(bpy.types.Operator): 
    bl_idname = "op.disable_constraints"
    bl_label = "Disable constraints in selected bones" 

    def execute(self, context):
        enableConstraints(False)
        return {'FINISHED'}

def enableConstraints(enable):
    for poseBone in bpy.context.selected_pose_bones:
            for constraint in poseBone.constraints:
                constraint.mute = not enable

class ChangeConstraintsTargetPanel(MainPanel, bpy.types.Panel):
    bl_idname = "CONSTRAINTS_TARGET_PANEL"
    bl_label = "Bone Constraints Target"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop_search(context.scene, "targetObjectForBoneConstraints", bpy.data, 'objects')
        row = layout.row()
        row.operator('op.set_constraints_target', text='Set')

class SetConstraintsTargetOp(bpy.types.Operator): 
    bl_idname = "op.set_constraints_target"
    bl_label = "Set constraints target in selected bones" 

    def execute(self, context):
        objName = context.scene.targetObjectForBoneConstraints
        setConstraintsTarget(bpy.data.objects[objName])
        return {'FINISHED'}

def setConstraintsTarget(target):
    for poseBone in bpy.context.selected_pose_bones:
            for constraint in poseBone.constraints:
                constraint.target = target

classes = (
    EnableConstraintsOp,
    DisableConstraintsOp,
    SetConstraintsTargetOp,
    BatchEnableConstraintsPanel,
    ChangeConstraintsTargetPanel,
    MainPanel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.targetObjectForBoneConstraints = bpy.props.StringProperty(
        name='Source',
        description='An source object to apply bones constraints from'
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.targetObjectForBoneConstraints

if __name__ == "__main__":
    register()