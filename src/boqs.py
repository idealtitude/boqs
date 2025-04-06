bl_info = {
    "name": "Object Quick Selection",
    "blender": (3, 3, 0),
    "category": "Object",
    "author": "idealtitude",
}

import bpy

class OBJECT_OT_select_from_list(bpy.types.Operator):
    bl_idname = "object.select_from_list"
    bl_label = "Select Object From List"

    # EnumProperty lists aall objects
    objects: bpy.props.EnumProperty(
        name="Objects",
        items=lambda self, context: [(obj.name, obj.name, "") for obj in bpy.data.objects]
    )

    def execute(self, context):
        # Retreive selected object
        obj = bpy.data.objects[self.objects]
        context.view_layer.objects.active = obj
        obj.select_set(True)
        return {'FINISHED'}

    def invoke(self, context, event):
        # Open dialog popup
        return context.window_manager.invoke_props_dialog(self)

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_select_from_list.bl_idname)

# Register addon
def register():
    bpy.utils.register_class(OBJECT_OT_select_from_list)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_select_from_list)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
