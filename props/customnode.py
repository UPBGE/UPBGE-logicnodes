import bpy


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
    bpy.utils.register_class(cls)
    _registered_custom_classes.append(cls)
    modname = cls.nl_module[1:] + '.py'
    if cls.bl_idname not in [n.idname for n in prefs.custom_logic_nodes]:
        noderef = prefs.custom_logic_nodes.add()
        noderef.idname = cls.bl_idname
        noderef.label = cls.bl_label
        noderef.ui_code = bpy.context.space_data.text.as_string()
        noderef.modname = modname
        noderef.logic_code = bpy.data.texts[modname].as_string()
        bpy.ops.wm.save_userpref()
    # else:
    #     text = bpy.data.texts.get(node.modname, None)
    #     if text is None:
    #         t = bpy.data.texts.new(node.modname)
    #         t.write(node.logic_code)
    return cls


class CustomNodeReference(bpy.types.PropertyGroup):
    idname: bpy.props.StringProperty()
    label: bpy.props.StringProperty()
    modname: bpy.props.StringProperty()
    ui_code: bpy.props.StringProperty()
    logic_code: bpy.props.StringProperty()