import bpy
import nodeitems_utils
import os
import sys
import time

bl_info = {
    "name": "Logic Nodes",
    "description": (
        "A Node System to create game logic."
    ),
    "author": "pgi, Leopold A-C (Iza Zed)",
    "version": (0, 9, 0),
    "blender": (2, 83, 0),
    "location": "View Menu",
    "warning": "Beta",
    "category": "Game Engine"
}

_loaded_nodes = []
_loaded_sockets = []
_current_user_nodes_parent_directory = None
_update_queue = []
_tree_to_name_map = {}
_tree_code_writer_started = False


def debug(*message):
    import traceback
    e = traceback.extract_stack(limit=2)
    text = ""
    for m in message:
        text = text + "{} ".format(m)
    if e:
        source = e[0][0]
        line = e[0][1]
        print('[{}:{}] {}'.format(source, line, text))


def update_current_tree_code(*ignored):
    global _tree_code_writer_started
    if not _tree_code_writer_started:
        _tree_code_writer_started = True
        bpy.ops.bgenetlogic.treecodewriter_operator()
    now = time.time()
    _update_queue.append(now)


def update_tree_name(tree, old_name):
    new_name = tree.name
    _tree_to_name_map[tree] = new_name
    old_name_code = utilities.strip_tree_name(old_name)
    new_name_code = utilities.strip_tree_name(new_name)
    new_pymodule_name = utilities.py_module_name_for_tree(tree)
    # old_pymodule_name = (
    # utilities.py_module_name_for_stripped_tree_name(old_name_code))
    new_py_controller_module_string = (
        utilities.py_controller_module_string(new_pymodule_name)
    )
    for ob in bpy.data.objects:
        old_status = None
        is_tree_applied_to_object = False
        for tree_item in ob.bgelogic_treelist:
            if tree_item.tree_name == old_name:
                tree_item.tree_name = new_name
                if old_status is not None:
                    raise RuntimeError(
                        "We have two trees with the same name in {}".format(
                            ob.name
                        )
                    )
                old_status = tree_item.tree_initial_status
                is_tree_applied_to_object = True
        if is_tree_applied_to_object:
            utilities.rename_initial_status_game_object_property(
                ob, old_name, new_name
            )
            gs = ob.game
            for sensor in gs.sensors:
                if old_name_code in sensor.name:
                    sensor.name = sensor.name.replace(
                        old_name_code, new_name_code
                    )
            for controller in gs.controllers:
                if old_name_code in controller.name:
                    controller.name = controller.name.replace(
                        old_name_code, new_name_code
                    )
                    if isinstance(controller, bpy.types.PythonController):
                        controller.module = new_py_controller_module_string
            for actuator in gs.actuators:
                if old_name_code in actuator.name:
                    actuator.name = actuator.name.replace(
                        old_name_code, new_name_code
                    )
        else:
            print("Tree name change doesn't affect object {} because the tree is not applied to it".format(ob.name))
    old_module_file = utilities.py_module_file_path_for_stripped_tree_name(old_name)
    new_module_file = utilities.py_module_file_path_for_stripped_tree_name(new_name)
    print("TODO: also rename {} to {}?".format(old_module_file, new_module_file))
    bpy.ops.bge_netlogic.generate_logicnetwork()


def _update_all_logic_tree_code():
    now = time.time()
    _update_queue.append(now)
    now = time.time()
    last_event = _update_queue[-1]
    delta = now - last_event
    try:
        bpy.ops.bge_netlogic.generate_logicnetwork_all()
    except Exception:
        print("Unknown Error, abort generating Network code")
        return


def _consume_update_tree_code_queue():
    if hasattr(bpy.context.space_data, "edit_tree") and (bpy.context.space_data.edit_tree is not None):
        edit_tree = bpy.context.space_data.edit_tree
        old_name = _tree_to_name_map.get(edit_tree)
        if not old_name:
            _tree_to_name_map[edit_tree] = edit_tree.name
        else:
            if old_name != edit_tree.name:
                update_tree_name(edit_tree, old_name)
    if not _update_queue:
        return
    now = time.time()
    last_event = _update_queue[-1]
    delta = now - last_event
    if delta > 0.25:
        debug("Updating tree code...")
        _update_queue.clear()
        try:
            bpy.ops.bge_netlogic.generate_logicnetwork()
        except Exception:
            print("Context Incorrect, abort generating Network code")
            # return update_current_tree_code()
        return True


def _get_this_module():
    global __name__
    return sys.modules[__name__]


#This is called when the program needs to ensure that the user nodes have been loaded when the
#edited file changes.
def setup_user_nodes():
    global _current_user_nodes_parent_directory
    parent_dir_for_current_blender_file = bpy.path.abspath("//")
    if parent_dir_for_current_blender_file != _current_user_nodes_parent_directory:
        nodes_dir = bpy.path.abspath("//bgelogic/nodes")
        if os.path.exists(nodes_dir) and os.path.isdir(nodes_dir):
            print("Installing user nodes for directory {}".format(_current_user_nodes_parent_directory))
            remove_project_user_nodes()#unload the current set of custom nodes
            try:
                load_nodes_from(nodes_dir)#load from the current dir
                _current_user_nodes_parent_directory = parent_dir_for_current_blender_file
            except RuntimeError as ex:
                print("Error loading user nodes from {}".format(nodes_dir))
                print("RuntimeError: {}".format(ex))
    pass


def remove_project_user_nodes():
    node_categories = set()
    for pair in _loaded_nodes:
        cat = pair[0]
        cls = pair[1]
        node_categories.add(cat)
        print("unregister class ", cls)
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError as ex:
            print("Cannot unregister class [{}]".format(cls))
            print("Error: {}".format(ex))
        pass
    for pair in _loaded_sockets:
        cat = pair[0]
        cls = pair[1]
        node_categories.add(cat)
        print("unregister class ", cls)
        bpy.utils.unregister_class(cls)
        pass
    for cat in node_categories:
        try:
            nodeitems_utils.unregister_node_categories(cat)
        except KeyError as ke:
            print("Cannot unregister node category {}".format(cat))
            print("KeyError: {}".format(ke))
    _loaded_nodes.clear()
    _loaded_sockets.clear()
    pass


def register_sockets(category_uid, *socks):
    for sock in socks:
        _loaded_sockets.append((category_uid, sock))
        if hasattr(bpy.types, sock.bl_idname):
            try:
                bpy.utils.unregister_class(getattr(bpy.types, sock.bl_idname))
            except RuntimeError as ex:
                print("Cannot unregister socket class {} for some reason {}", sock.__class__.__name__, ex)
        bpy.utils.register_class(sock)


def register_nodes(category_label, *cls):
    node_items = []
    for c in cls:
        if hasattr(bpy.types, c.bl_idname):
            try:
                print("Unregister class {}".format(c))
                bpy.utils.unregister_class(getattr(bpy.types, c.bl_idname))
            except RuntimeError as ex:
                print("Cannot unregister type {}, for some reason\n{}".format(c, ex))
        print("Register class {}".format(c))
        _loaded_nodes.append((category_label, c))
        bpy.utils.register_class(c)
        node_item = nodeitems_utils.NodeItem(c.bl_idname)
        node_items.append(node_item)
    node_category = NodeCategory(category_label, category_label, items=node_items)
    try:
        nodeitems_utils.unregister_node_categories(category_label)
    except KeyError:
        print("Info: Node Category {} has not been registered before.".format(category_label))
    nodeitems_utils.register_node_categories(category_label, [node_category])
    pass


def _reload_module(m):
    python_version = sys.version_info
    if python_version[0] == 3 and python_version[1] >= 4:
        import importlib
        importlib.reload(m)
    else:
        import imp
        imp.reload(m)


def _abs_import(module_name, full_path):
    import sys
    python_version = sys.version_info
    major = python_version[0]
    minor = python_version[1]
    if (major < 3) or (major == 3 and minor < 3):
        import imp
        return imp.load_source(module_name, full_path)
    elif (major == 3) and (minor < 5):
        from importlib.machinery import SourceFileLoader
        return SourceFileLoader(module_name, full_path).load_module()
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    pass


def _rel_import(module_name, rel_path):
    directory = os.path.dirname(__file__)
    abs_path = os.path.join(directory, rel_path)
    return _abs_import(module_name, abs_path)


def _abs_path(*relative_path_components):
    import os
    relative_path = os.path.sep.join(relative_path_components)
    this_file = __file__
    this_dir = this_file
    bugger = 0

    def is_existing_directory(path):
        if not os.path.exists(path):
            return False
        else:
            return not os.path.isfile(path)

    while (not is_existing_directory(this_dir)) and (bugger < 100):
        this_dir = os.path.dirname(this_dir)
        bugger += 1
    assert bugger < 100
    abs_path = os.path.join(this_dir, relative_path)
    return abs_path


def load_nodes_from(abs_dir):
    print("loading project nodes and cells from {}".format(abs_dir))
    dir_file_names = os.listdir(abs_dir)
    py_file_names = [x for x in dir_file_names if x.endswith(".py")]
    for fname in py_file_names:
        mod_name = fname[:-3]
        full_path = os.path.join(abs_dir, fname)
        source = None
        with open(full_path, "r") as f:
            source = f.read()
        if source:
            bge_netlogic = _get_this_module()
            locals = {
                "bge_netlogic": _get_this_module(),
                "__name__": mod_name,
                "bpy": bpy}
            globals = locals
            print("loading... {}".format(mod_name))
            exec(source, locals, globals)
            #TODO: reload source to refresh intermediate compilation?


@bpy.app.handlers.persistent
def refresh_custom_nodes(dummy):
     setup_user_nodes()

@bpy.app.handlers.persistent
def request_tree_code_writer_start(dummy):
    global _tree_code_writer_started
    _tree_code_writer_started = False
    print("updating tree code on file open...")
    generator = ops.tree_code_generator.TreeCodeGenerator()
    for node_tree in bpy.data.node_groups:
        if node_tree.bl_idname == ui.BGELogicTree.bl_idname:
            print("writing tree script for ", node_tree.name)
            generator.write_code_for_tree(node_tree)


bpy.app.handlers.load_post.append(refresh_custom_nodes)
bpy.app.handlers.load_post.append(request_tree_code_writer_start)
bpy.app.handlers.save_post.append(refresh_custom_nodes)

#import modules and definitions
ui = _abs_import("ui", _abs_path("ui", "__init__.py"))
ops = _abs_import("ops", _abs_path("ops", "__init__.py"))
ops.abstract_text_buffer = _abs_import("abstract_text_buffer", _abs_path("ops", "abstract_text_buffer.py"))
ops.bl_text_buffer = _abs_import("bl_text_buffer", _abs_path("ops","bl_text_buffer.py"))
ops.file_text_buffer = _abs_import("file_text_buffer", _abs_path("ops","file_text_buffer.py"))
ops.tree_code_generator = _abs_import("tree_code_generator", _abs_path("ops","tree_code_generator.py"))
ops.uid_map = _abs_import("uid_map", _abs_path("ops", "uid_map.py"))
utilities = _abs_import("utilities", _abs_path("utilities", "__init__.py"))


def update_node_colors(self, context):
    for tree in bpy.data.node_groups:
        if isinstance(tree, ui.BGELogicTree):
            for node in tree.nodes:
                if isinstance(node, bpy.types.NodeFrame):
                    continue
                node.use_custom_color = bpy.context.scene.logic_node_settings.use_custom_node_color


class NLNodeTreeReference(bpy.types.PropertyGroup):
    tree_name: bpy.props.StringProperty()
    tree_initial_status: bpy.props.BoolProperty()


class NLAddonSettings(bpy.types.PropertyGroup):
    use_custom_node_color: bpy.props.BoolProperty(update=update_node_colors)
    use_node_debug: bpy.props.BoolProperty()


class NodeCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == ui.BGELogicTree.bl_idname)
        return enabled


class LogicNodesAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col_2 = layout.column()
        use_color_row = col.row()
        use_color_row.prop(context.scene.logic_node_settings, 'use_custom_node_color', text="Dark Node Color")
        use_color_row.prop(context.scene.logic_node_settings, 'use_node_debug', text="Debug Mode (Print Errors to Console)")
        contrib_row = col.row()
        contrib_row.label(text='Contributors: L_P, Mike King')


basicnodes = _abs_import("basicnodes", _abs_path("basicnodes", "__init__.py"))
_registered_classes = [
    ui.BGELogicTree,
    ops.NLSelectTreeByNameOperator,
    ops.NLRemoveTreeByNameOperator,
    ops.NLApplyLogicOperator,
    ops.NLAdd4KeyTemplateOperator,
    ops.NLGenerateLogicNetworkOperatorAll,
    ops.NLGenerateLogicNetworkOperator,
    ops.NLImportProjectNodes,
    ops.NLLoadProjectNodes,
    ops.WaitForKeyOperator,
    ops.TreeCodeWriterOperator,
    ops.NLMakeGroupOperator,
    ops.NLSwitchInitialNetworkStatusOperator,
    ops.NLAddPropertyOperator,
    ops.NLAddComponentOperator,
    ops.NLRemovePropertyOperator,
    ops.NLMovePropertyOperator,
    ops.NLLoadSoundOperator,
    ops.NLPopupTemplatesOperator,
    NLNodeTreeReference
]

_registered_classes.extend(basicnodes._sockets)

_registered_classes.extend(basicnodes._nodes)

_registered_classes.extend([
    NLAddonSettings,
    LogicNodesAddonPreferences,
    ui.BGEPropFilter,
    ui.BGEGroupName,
    ui.BGE_PT_LogicPanel,
    ui.BGE_PT_LogicTreeInfoPanel,
    ui.BGE_PT_GamePropertyPanel,
    # ui.BGEGameComponentPanel,
    ui.BGE_PT_GamePropertyPanel3DView,
    ui.BGE_PT_PropertiesPanelObject,
    ui.BGE_PT_LogicTreeGroups
])


def _get_key_for_class(c):
    if hasattr(c, "bl_label"):
        return c.bl_label
    else:
        return "zzz"


_registered_classes = sorted(_registered_classes, key=_get_key_for_class)


# Create the menu items that allow the user to add nodes to a tree


def _list_menu_nodes():
    proxy_map = {}

    def get_param_list(c): return proxy_map["Basic Uncategorized Parameters"]

    def get_cond_list(c): return proxy_map["Basic Uncategorized Conditions"]

    def get_act_list(c): return proxy_map["Basic Uncategorized Actions"]

    def get_cat_list(cat):
        catlist = proxy_map.get(cat)
        if catlist is None:
            catlist = []
            proxy_map[cat] = catlist
        return catlist
    for c in _registered_classes:
        if hasattr(c, "nl_category") and not hasattr(c, 'nl_subcat'):
            get_cat_list(c.nl_category).append(nodeitems_utils.NodeItem(c.bl_idname))
        elif issubclass(c, basicnodes.NLParameterNode):
            get_param_list(c).append(nodeitems_utils.NodeItem(c.bl_idname))
        elif issubclass(c, basicnodes.NLConditionNode):
            get_cond_list(c).append(nodeitems_utils.NodeItem(c.bl_idname))
        elif issubclass(c, basicnodes.NLActionNode):
            get_act_list(c).append(nodeitems_utils.NodeItem(c.bl_idname))

    pmap_keys = list(proxy_map.keys())
    pmap_keys.sort()
    menu_nodes = []
    for name in pmap_keys:
        itemlist = proxy_map[name]
        menu_nodes.append(NodeCategory(name, name, items=itemlist))
    return menu_nodes


# blender add-on registration callback
def register():
    print(bpy.app.version)
    for cls in _registered_classes:
        print("Registering... {}".format(cls.__name__))
        bpy.utils.register_class(cls)
    menu_nodes = _list_menu_nodes()
    nodeitems_utils.register_node_categories("NETLOGIC_NODES", menu_nodes)
    bpy.types.Object.bgelogic_treelist = bpy.props.CollectionProperty(
        type=NLNodeTreeReference
    )
    bpy.types.Scene.prop_filter = bpy.props.PointerProperty(
        type=ui.BGEPropFilter
    )
    bpy.types.Scene.group_name = bpy.props.PointerProperty(
        type=ui.BGEGroupName
    )
    bpy.types.Scene.logic_node_settings = bpy.props.PointerProperty(
        type=NLAddonSettings
    )


# blender add-on unregistration callback
def unregister():
    print("Unregister node category [{}]".format("NETLOGIC_NODES"))
    nodeitems_utils.unregister_node_categories("NETLOGIC_NODES")
    for cls in reversed(_registered_classes):
        print("Unregister node class [{}]".format(cls.__name__))
        bpy.utils.unregister_class(cls)
    user_node_categories = set()
    for pair in _loaded_nodes:
        cat = pair[0]
        cls = pair[1]
        user_node_categories.add(cat)
        try:
            node_id = cls.__name__
            if hasattr(bpy.types, node_id):
                print("Unregister user node [{}]".format(node_id))
                bpy.utils.unregister_class(getattr(bpy.types, node_id))
        except RuntimeError as ex:
            print("Custom node {} not unloaded [{}]".format(cls.__name__, ex))
    for pair in _loaded_sockets:
        cat = pair[0]
        cls = pair[1]
        user_node_categories.add(cat)
        try:
            node_id = cls.__name__
            if hasattr(bpy.types, node_id):
                print("Unregister user socket [{}]".format(node_id))
                bpy.utils.unregister_class(getattr(bpy.types, node_id))
        except RuntimeError as ex:
            print("Custom socket {} not unloaded [{}]".format(cls.__name__, ex))
    for cat in user_node_categories:
        print("Unregister user node category [{}]".format(cat))
        try:
            nodeitems_utils.unregister_node_categories(cat)
        except RuntimeError as ex:
            print("Custom category {} not unloaded [{}]".format(cat, ex))
