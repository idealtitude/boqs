import bpy

bl_info = {
    "name": "Object Selector by Collection",
    "author": "idealtitude",
    "version": (0, 1, 5),
    "blender": (3, 3, 0),
    "location": "Object > Select Object",
    "description": "Popup to select any object via a collection filter. Adds it to current selection and makes it active.",
    "warning": "",
    "category": "Object",
    "support": "COMMUNITY",
    "tracker_url": "https://github.com/idealtitude/boqs/issues",
    "license": "MIT"
}


# Return list of collection names
def get_collections(self, context):
    return [(col.name, col.name, "") for col in bpy.data.collections]


# Return list of object names in the selected collection
def get_objects(self, context):
    col = bpy.data.collections.get(self.collection)
    if col:
        return [(obj.name, obj.name, "") for obj in col.objects]
    return []


class OBJECT_OT_select_from_list(bpy.types.Operator):
    bl_idname = "object.select_from_list"
    bl_label = "Select Object From List"
    bl_description = "Popup to select an object by collection and make it active (adds to current selection)"

    # Called when collection is changed
    def update_collection(self, context):
        obj_items = get_objects(self, context)
        obj_names = [item[0] for item in obj_items]

        # Only change object if current one is invalid
        if self.objects not in obj_names:
            if obj_names:
                self.objects = obj_names[0]
            else:
                self.objects = ""

    collection: bpy.props.EnumProperty(
        name="Collection",
        description="Filter objects by this collection",
        items=get_collections,
        update=update_collection
    )

    objects: bpy.props.EnumProperty(
        name="Object",
        description="Select the object to add to selection and make active",
        items=get_objects
    )

    def execute(self, context):
        obj = bpy.data.objects.get(self.objects)
        if obj:
            obj.select_set(True)
            context.view_layer.objects.active = obj
        return {'FINISHED'}

    def invoke(self, context, event):
        if not bpy.data.collections:
            self.report({'WARNING'}, "No collections found in the scene")
            return {'CANCELLED'}

        # Set default collection and update object list accordingly
        self.collection = list(bpy.data.collections)[0].name
        self.update_collection(context)

        context.window_manager.invoke_props_dialog(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "collection")
        layout.prop(self, "objects")


# Add menu entry in Object > menu
def menu_func(self, context):
    self.layout.operator(OBJECT_OT_select_from_list.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_select_from_list)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_select_from_list)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
