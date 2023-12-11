import bpy
import inspect
import os


_registered_custom_classes = []


def custom_node(cls):
    prefs = bpy.context.preferences.addons['bge_netlogic'].preferences
    for node in _registered_custom_classes:
        if cls.bl_idname == node.bl_idname:
            bpy.utils.unregister_class(node)
            _registered_custom_classes.remove(node)
            for i, e in enumerate(prefs.custom_logic_nodes):
                if e.idname == cls.bl_idname:
                    prefs.custom_logic_nodes.remove(i)
    modname = cls.nl_module[1:] + '.py'
    if cls.bl_idname not in [n.idname for n in prefs.custom_logic_nodes]:
        logic_code = bpy.data.texts.get(modname, None)
        if logic_code is None:
            def error_log(self, context):
                self.layout.label(text=f'Text Block "{modname}" not found!', icon='CONSOLE')

            bpy.context.window_manager.popup_menu(error_log, title=f'Custom Logic Node could not register!', icon='INFO')

            print(f'Custom Logic Node could not register! Text Block "{modname}" not found!')
            return
        noderef = prefs.custom_logic_nodes.add()
        noderef.idname = cls.bl_idname
        noderef.label = cls.bl_label
        ui_code = getattr(bpy.context.space_data, 'text', None)
        if ui_code is None:
            ui_code = bpy.data.texts['__customnodetemp__']
        noderef.ui_code = ui_code.as_string()

        noderef.modname = modname
        noderef.logic_code = logic_code.as_string()
        bpy.ops.wm.save_userpref()
    bpy.utils.register_class(cls)
    _registered_custom_classes.append(cls)
    return cls


class CustomNodeReference(bpy.types.PropertyGroup):
    idname: bpy.props.StringProperty()
    label: bpy.props.StringProperty()
    modname: bpy.props.StringProperty()
    ui_code: bpy.props.StringProperty()
    logic_code: bpy.props.StringProperty()
