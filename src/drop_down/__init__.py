bl_info = {
    "name": "Drop Down",
    "author": "PengCheng",
    "version": (1, 0, 0, 2),
    "blender": (3, 6, 0),
    "location": "View3D > Object Menu > Drop Down",
    "description": "drop objects",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object",
}


import bpy

def generate_simple_enum_property(items):
    gitems = []
    for i, item in enumerate(items):
        gitems.append((item, item, item, i))
    return bpy.props.EnumProperty(items=gitems)

class DropDownSetting(bpy.types.PropertyGroup):
    behavior: generate_simple_enum_property('123')
    direction: generate_simple_enum_property(['-Z', 'center'])

class DropDownDoOperator(bpy.types.Operator):
    bl_idname = 'object.drop_me_do'
    bl_label = 'Drop down'
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    # behavior: generate_simple_enum_property('123')
    # direction: generate_simple_enum_property(['-Z', 'center'])

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        import drop_down.core
        drop_down.core.drop_action()
        return {'FINISHED'}

    def invoke(self, context, event):
        # self.report({'INFO'}, 'DropDownDoOperator.invoke')
        return self.execute(context)

class DropDownToolPanel(bpy.types.Panel):
    bl_idname = "DROPME_PT_tool_panel"
    bl_label = "Drop Down"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Selection Tools")
        box.operator("object.select_all").action = 'TOGGLE'
        row = box.row()
        row.operator("object.select_all").action = 'INVERT'
        row.operator("object.select_random")        
        box.prop(data=context.scene.drop_me_settings, property='behavior')
        box.prop(data=context.scene.drop_me_settings, property='direction')
        box.operator(DropDownDoOperator.bl_idname)
        box.operator('mesh.subdivide')

def draw_menu(self, context):
    self.layout.operator('object.drop_me_do')

REGISTER_CLASSES = [DropDownSetting, DropDownDoOperator]

def register():
    for cls in REGISTER_CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.drop_me_settings = bpy.props.PointerProperty(type=DropDownSetting)
    bpy.types.VIEW3D_MT_object.append(draw_menu)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(draw_menu)
    del bpy.types.Scene.dorp_me_settings
    for cls in reversed(REGISTER_CLASSES):
        bpy.utils.unregister_class(cls)
