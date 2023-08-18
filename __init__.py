import bpy
# import nodeitems_utils
from bpy.app.handlers import persistent
import bge_netlogic.utilities as utils
import bge_netlogic.audio as audio
import os
import sys
import time


bl_info = {
    "name": "Logic Nodes+",
    "description": (
        "A Node System to create game logic."
    ),
    "author": "pgi, Leopold A-C (Iza Zed), Teck-Freak / Lucyon Oak",
    "version": (2, 3),
    "blender": (3, 6, 0),
    "location": "View Menu",
    "category": "Game Engine"
}

_loaded_nodes = []
_loaded_sockets = []
_current_user_nodes_parent_directory = None
_update_queue = []
_tree_to_name_map = {}
_tree_code_writer_started = False

UPLOGIC_INSTALLED = False


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


def update_tree_name(context):
    print('Going In Here')
    return
    utils.set_compile_status(utils.TREE_MODIFIED)
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
            if tree_item.tree_name == new_name:
                st = tree_item.tree_initial_status
                utils.remove_tree_item_from_object(ob, tree_item.tree_name)
                new_entry = ob.bgelogic_treelist.add()
                new_entry.tree_name = tree.name
                new_entry.tree = tree
                # this will set both new_entry.tree_initial_status and add a
                # game property that makes the status usable at runtime
                utils.set_network_initial_status_key(
                    ob, tree.name, st
                )
                tree_item.tree_name = new_name
                if old_status is not None:
                    raise RuntimeError(
                        "We have two trees with the same name in {}".format(
                            ob.name
                        )
                    )
        if is_tree_applied_to_object:
            utilities.rename_initial_status_game_object_property(
                ob, old_name, new_name
            )
            gs = ob.game
            idx = 0
            check_name = utils.make_valid_name(old_name)
            comp_name = f'nl_{check_name.lower()}'
            clsname = utils.make_valid_name(new_name)
            new_comp_name = f'nl_{clsname.lower()}.{clsname}'
            for c in gs.components:
                if c.module == comp_name:
                    try:
                        ops.tree_code_generator.TreeCodeGenerator().write_code_for_tree(tree)
                    except Exception as e:
                        utils.error(f"Couldn't compile tree {tree.name}!")
                        utils.error(e)
                    text = bpy.data.texts.get(f'{comp_name}.py')
                    if text:
                        bpy.data.texts.remove(text)
                    active_object = bpy.context.object
                    bpy.context.view_layer.objects.active = ob
                    bpy.ops.logic.python_component_remove(index=idx)
                    bpy.ops.logic.python_component_register(component_name=new_comp_name)
                    bpy.context.view_layer.objects.active = active_object
                idx += 1

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
            utils.success(f'Renamed Tree {old_name_code} to {new_name_code}')
    # bpy.ops.bge_netlogic.generate_logicnetwork()


def _update_all_logic_tree_code():
    now = time.time()
    _update_queue.append(now)
    now = time.time()
    last_event = _update_queue[-1]
    utils.set_compile_status(utils.TREE_MODIFIED)
    try:
        bpy.ops.bge_netlogic.generate_logicnetwork_all()
    except Exception:
        utils.error("Unknown Error, abort generating Network code")


@persistent
def _reload_texts(self, context):
    if not hasattr(bpy.types.Scene, 'logic_node_settings'):
        return
    if not bpy.context or not bpy.context.scene:
        return
    if not bpy.context.scene.logic_node_settings.use_reload_text:
        return
    else:
        for t in bpy.data.texts:
            if t.filepath:
                path = (
                    os.path.join(bpy.path.abspath('//'), t.filepath[2:])
                    if t.filepath.startswith('//')
                    else t.filepath
                )
                with open(path) as f:
                    t.clear()
                    t.write(f.read())


@persistent
def _generate_on_game_start(self, context):
    utils.notify('Building Logic Trees on Startup...')
    bpy.ops.bge_netlogic.generate_logicnetwork_all()


@persistent
def _jump_in_game_cam(self, context):
    if bpy.context.scene.jump_in_game_cam:
        bpy.ops.view3d.view_camera()


@persistent
def _set_vr_mode(self, context):
    if bpy.context.scene.use_vr_audio_space and not bpy.context.window_manager.xr_session_state:
        bpy.context.scene.game_settings.use_viewport_render = True
        utils.notify('Starting in VR mode...')
        utils.start_vr_session()
    elif bpy.context.window_manager.xr_session_state and not bpy.context.scene.use_vr_audio_space:
        utils.notify('Shutting down VR mode...')
        utils.stop_vr_session()


def _consume_update_tree_code_queue():
    # edit_tree = getattr(bpy.context.space_data, "edit_tree", None)
    # if edit_tree:
    #     # edit_tree = bpy.context.space_data.edit_tree
    #     old_name = _tree_to_name_map.get(edit_tree)
    #     if not old_name:
    #         _tree_to_name_map[edit_tree] = edit_tree.name
    #     else:
    #         if old_name != edit_tree.name:
    #             update_tree_name(edit_tree, old_name)
    if not _update_queue:
        return
    now = time.time()
    last_event = _update_queue[-1]
    delta = now - last_event
    if delta > 0.25:
        _update_queue.clear()
        bpy.ops.bge_netlogic.generate_logicnetwork_all()
        return True


def _get_this_module():
    global __name__
    return sys.modules[__name__]


# This is called when the program needs to ensure that the user nodes have been loaded when the
# edited file changes.
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
                # print("Unregister class {}".format(c))
                bpy.utils.unregister_class(getattr(bpy.types, c.bl_idname))
            except RuntimeError as ex:
                print("Cannot unregister type {}, for some reason\n{}".format(c, ex))
        print("Register class {}".format(c))
        _loaded_nodes.append((category_label, c))
        bpy.utils.register_class(c)

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
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module


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


#import modules and definitions
utilities = _abs_import("utilities", _abs_path("utilities", "__init__.py"))
ops = _abs_import("ops", _abs_path("ops", "__init__.py"))
ui = _abs_import("ui", _abs_path("ui", "__init__.py"))
node_menu = _abs_import("node_menu", _abs_path("ui", "node_menu.py"))
ops.abstract_text_buffer = _abs_import("abstract_text_buffer", _abs_path("ops", "abstract_text_buffer.py"))
ops.bl_text_buffer = _abs_import("bl_text_buffer", _abs_path("ops","bl_text_buffer.py"))
ops.file_text_buffer = _abs_import("file_text_buffer", _abs_path("ops","file_text_buffer.py"))
ops.uid_map = _abs_import("uid_map", _abs_path("ops", "uid_map.py"))
ops.tree_code_generator = _abs_import("tree_code_generator", _abs_path("ops","tree_code_generator.py"))


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
            # TODO: reload source to refresh intermediate compilation?


@persistent
def refresh_custom_nodes(dummy):
    setup_user_nodes()


RENAMING = False


@persistent
def request_tree_code_writer_start(dummy):
    global _tree_code_writer_started
    _tree_code_writer_started = False
    # generator = bpy.ops.tree_code_generator.TreeCodeGenerator()
    if getattr(bpy.context.scene.logic_node_settings, 'use_generate_on_open', False):
        utils.debug('Writing trees on file open...')
        bpy.ops.bge_netlogic.generate_logicnetwork_all()
        utils.debug('FINISHED')

    global RENAMING
    RENAMING = True
    for tree in bpy.data.node_groups:
        if isinstance(tree, ui.LogicNodeTree):
            if tree.name != tree.old_name:
                tree.update_name(False)
    RENAMING = False


@persistent
def _watch_tree_names(self, context):
    global RENAMING
    if RENAMING:
        return
    else:
        RENAMING = True
        for tree in bpy.data.node_groups:
            if isinstance(tree, ui.LogicNodeTree):
                if tree.name != tree.old_name:
                    tree.update_name()
        RENAMING = False


for f in [
    refresh_custom_nodes,
    request_tree_code_writer_start,
    refresh_custom_nodes
]:
    if f in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(f)
    bpy.app.handlers.load_post.append(f)




def update_node_colors(self, context):
    for tree in bpy.data.node_groups:
        if isinstance(tree, ui.LogicNodeTree):
            for node in tree.nodes:
                if isinstance(node, bpy.types.NodeFrame):
                    continue
                node.use_custom_color = getattr(bpy.context.scene.logic_node_settings, 'use_custom_node_color', False)


class NLNodeTreeReference(bpy.types.PropertyGroup):
    tree: bpy.props.PointerProperty(type=ui.LogicNodeTree)
    tree_name: bpy.props.StringProperty()
    tree_initial_status: bpy.props.BoolProperty()


class NLAddonSettings(bpy.types.PropertyGroup):
    use_custom_node_color: bpy.props.BoolProperty(
        update=update_node_colors
    )
    use_node_debug: bpy.props.BoolProperty(default=True)
    use_node_notify: bpy.props.BoolProperty(default=True)
    use_reload_text: bpy.props.BoolProperty(default=False)
    use_generate_on_open: bpy.props.BoolProperty(default=False)
    use_generate_all: bpy.props.BoolProperty(default=True)
    auto_compile: bpy.props.BoolProperty(default=False)
    tree_compiled: bpy.props.StringProperty(default=utils.TREE_NOT_INITIALIZED)


class NodeCategory():

    def __init__(self, identifier, name, description="", items=None):
        self.identifier = identifier
        self.name = name
        self.description = description

        if items is None:
            self.items = lambda context: []
        elif callable(items):
            self.items = items
        else:
            def items_gen(context):
                for item in items:
                    if item.poll is None or item.poll(context):
                        yield item
            self.items = items_gen

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == ui.LogicNodeTree.bl_idname)
        return enabled

    def draw(self, item, layout, context, separate=False):
        if separate:
            layout.separator()



class NodeSearch(bpy.types.Operator):
    bl_idname = "an.node_search"
    bl_label = "Node Search"
    bl_options = {"REGISTER"}
    bl_property = "item"

    def getSearchItems(self, context):
        # itemsByIdentifier.clear()
        items = []
        # for item in itertools.chain(iterSingleNodeItems()):
        #     itemsByIdentifier[item.identifier] = item
        #     items.append((item.identifier, item.searchTag, ""))
        return items

    item: bpy.props.EnumProperty(items=getSearchItems)

    @classmethod
    def poll(cls, context):
        try: return context.space_data.node_tree.bl_idname == "an_AnimationNodeTree"
        except: return False

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"CANCELLED"}

    def execute(self, context):
        # itemsByIdentifier[self.item].insert()
        return {"FINISHED"}


class LogicNodesAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column()
        col.label(
            text='Logic Nodes require the uplogic module, please install if missing.',
            icon='CHECKMARK' if 'uplogic' in sys.modules else 'ERROR'
        )
        col.operator('bge_netlogic.install_uplogic_module', icon='IMPORT')
        # col.operator('bge_netlogic.install_fake_bge_module', icon='IMPORT')
        main_row = layout.row()
        col = layout.column()
        debug_col = main_row.column()
        ui_col = main_row.column()
        code_col = main_row.column()
        ui_col.prop(
            context.scene.logic_node_settings,
            'use_custom_node_color',
            text="Dark Node Color"
        )
        ui_col.prop(
            context.scene.logic_node_settings,
            'use_reload_text',
            text="Reload Scripts on Game Start"
        )
        debug_col.prop(
            context.scene.logic_node_settings,
            'use_node_notify',
            text="Notifications"
        )
        debug_col.prop(
            context.scene.logic_node_settings,
            'use_node_debug',
            text="Debug Mode (Print Errors to Console)"
        )
        code_col.label(text='Generate Code:')
        code_col.prop(
            context.scene.logic_node_settings,
            'use_generate_all',
            text="On Fail."
        )
        code_col.prop(
            context.scene.logic_node_settings,
            'auto_compile',
            text="After Editing (Slow)."
        )
        code_col.prop(
            context.scene.logic_node_settings,
            'use_generate_on_open',
            text="On File Open."
        )
        col.separator()
        link_row = col.row(align=True)
        link_row.operator("bge_netlogic.github", icon="URL")
        # link_row.operator("bge_netlogic.update_tree_version", icon='PLUGIN')
        link_row.operator("bge_netlogic.donate", icon="FUND")
        contrib_row = col.row()
        contrib_row.label(text='Contributors: VUAIEO, Simon, L_P, p45510n')


basicnodes = _abs_import("basicnodes", _abs_path("basicnodes", "__init__.py"))
_registered_classes = [
    ui.LogicNodeTree,
    ops.NLInstallUplogicModuleOperator,
    ops.NLInstallFakeBGEModuleOperator,
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
    ops.NLLoadSoundOperator,
    ops.NLLoadImageOperator,
    ops.NLSwitchInitialNetworkStatusOperator,
    ops.NLUpdateTreeVersionOperator,
    ops.NLAddPropertyOperator,
    ops.NLAddComponentOperator,
    ops.NLRemovePropertyOperator,
    ops.NLMovePropertyOperator,
    ops.NLPopupTemplatesOperator,
    ops.NLAddonPatreonButton,
    ops.NLAddonGithubButton,
    ops.NLBGEDocsButton,
    ops.NLUPBGEDocsButton,
    ops.NLDocsButton,
    ops.NLAddGlobalOperator,
    ops.NLRemoveGlobalOperator,
    ops.NLAddGlobalCatOperator,
    ops.NLRemoveGlobalCatOperator,
    ops.NLResetEmptySize,
    ops.NLMakeCustomMainLoop,
    ops.NLMakeCustomLoopTree,
    ops.NLSelectAppliedObject,
    ops.NLReloadTexts,
    ops.NLReloadComponents,
    ops.NLStartAudioSystem,
    ops.NLRemoveListItemSocket,
    ops.NLAddListItemSocket,
    ops.NLLoadFontOperator,
    ops.NLNodeSearch,
    # ops.NLStartGameHere,
    NLNodeTreeReference
]

_registered_classes.extend(basicnodes._sockets)


_registered_classes.extend(basicnodes._nodes)


_registered_classes.extend(node_menu._items)


_registered_classes.extend([
    NLAddonSettings,
    LogicNodesAddonPreferences,
    ui.BGEPropFilter,
    ui.BGEGroupName,
    ui.BGEGlobalValue,
    ui.BGEGlobalValueCategory,
    ui.BGE_PT_GameComponentHelperPanel,
    # ui.BGEComponentHelper,
    ui.NL_UL_glcategory,
    ui.NL_UL_glvalue,
    ui.BGE_PT_LogicPanel,
    ui.BGE_PT_LogicTreeInfoPanel,
    ui.BGE_PT_ObjectTreeInfoPanel,
    ui.BGE_PT_GlobalValuePanel,
    ui.BGE_PT_LogicNodeSettingsScene,
    # ui.BGE_PT_NLEditorPropertyPanel,
    # ui.BGE_PT_HelpPanel,
    # ui.BGE_PT_GameComponentPanel,
    ui.BGE_PT_LogicNodeSettingsObject,
    ui.BGE_PT_LogicTreeOptions,
    ui.BGE_PT_GamePropertyPanel3DView,
    # ui.BGE_PT_PropertiesPanelObject,
    ui.BGE_PT_LogicTreeGroups
])


def _get_key_for_class(c):
    if hasattr(c, "bl_label"):
        return c.bl_label
    else:
        return "zzz"


_registered_classes = sorted(_registered_classes, key=_get_key_for_class)


# Create the menu items that allow the user to add nodes to a tree


def update_uplogic_module():
    try:
        os.system(f'"{sys.executable}" -m ensurepip')
        os.system(f'"{sys.executable}" -m pip install uplogic --upgrade')
        global UPLOGIC_INSTALLED
        UPLOGIC_INSTALLED = True
    except Exception:
        pass


def get_uplogic_module():
    try:
        os.system(f'"{sys.executable}" -m ensurepip')
        os.system(f'"{sys.executable}" -m pip install uplogic')
        global UPLOGIC_INSTALLED
        UPLOGIC_INSTALLED = True
    except Exception:
        pass


def filter_components(self, item=bpy.types.Text):
    if not item.name.startswith('nl_'):
        return True
    return False


# blender add-on registration callback
def register():
    bpy.types.NODE_MT_add.append(node_menu.draw_add_menu)
    bpy.app.handlers.game_pre.append(_generate_on_game_start)
    bpy.app.handlers.game_pre.append(_jump_in_game_cam)
    bpy.app.handlers.game_pre.append(_set_vr_mode)
    bpy.app.handlers.game_pre.append(_reload_texts)
    bpy.app.handlers.depsgraph_update_post.append(_watch_tree_names)
    for cls in _registered_classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.sound_occluder = bpy.props.BoolProperty(
        default=True,
        name='Sound Occluder',
        description='Whether this object will dampen sound'
    )
    bpy.types.Object.sound_blocking = bpy.props.FloatProperty(
        min=0.0,
        max=1.0,
        default=.05,
        name='Sound Blocking',
        description='The amount of sound blocking caused by this wall. A value of 1 will block all sound'
    )
    bpy.types.Object.reverb_volume = bpy.props.BoolProperty(
        default=False,
        name='Reverb Volume',
        description='Whether this volume will cause sound to reverberate (Range Limit: 50m)'
    )
    bpy.types.Object.reverb_samples = bpy.props.IntProperty(
        min=0,
        max=30,
        default=10,
        name='Reverb Bounces',
        description='Samples used by this reverb volume. More samples mean a longer reverberation'
    )

    bpy.types.Object.bgelogic_treelist = bpy.props.CollectionProperty(
        type=NLNodeTreeReference
    )
    bpy.types.Scene.prop_filter = bpy.props.PointerProperty(
        type=ui.BGEPropFilter
    )
    bpy.types.Scene.nl_group_name = bpy.props.PointerProperty(
        type=ui.BGEGroupName
    )
    bpy.types.Scene.logic_node_settings = bpy.props.PointerProperty(
        type=NLAddonSettings
    )
    bpy.types.Scene.nl_global_categories = bpy.props.CollectionProperty(
        type=ui.BGEGlobalValueCategory
    )
    bpy.types.Scene.nl_componenthelper = bpy.props.PointerProperty(
        type=bpy.types.Text, poll=filter_components, name='Component', description='Add the first component defined in this file'
    )
    bpy.types.Scene.nl_global_cat_selected = bpy.props.IntProperty(
        name='Category'
    )
    bpy.types.Scene.use_vr_audio_space = bpy.props.BoolProperty(
        name='Use VR Audio Space'
    )
    bpy.types.Scene.jump_in_game_cam = bpy.props.BoolProperty(
        name='Use Game Camera On Start'
    )
    bpy.types.Scene.custom_mainloop_tree = bpy.props.PointerProperty(
        name='Custom Mainloop Tree',
        type=bpy.types.NodeTree
    )
    bpy.types.Scene.use_screen_console = bpy.props.BoolProperty(
        name='Screen Console',
        description='Print messages to an on-screen console.\nNeeds at least one uplogic import or Logic Node Tree.\nNote: Errors are not printed to this console'
    )
    bpy.types.Scene.screen_console_open = bpy.props.BoolProperty(
        name='Open',
        description='Start the game with the on-screen console already open'
    )
    get_uplogic_module()


# blender add-on unregistration callback
def unregister():
    bpy.types.NODE_MT_add.remove(node_menu.draw_add_menu)
    utils.debug('Removing Game Start Compile handler...')
    remove_f = []
    filter(lambda a: a.__name__ == '_generate_on_game_start', bpy.app.handlers.game_pre)
    filter(lambda a: a.__name__ == '_watch_tree_names', bpy.app.handlers.depsgraph_update_post)
    filter(lambda a: a.__name__ == '_reload_texts', bpy.app.handlers.game_pre)
    for f in bpy.app.handlers.game_pre:
        if f.__name__ == '_generate_on_game_start' or f.__name__ == '_reload_texts':
            remove_f.append(f)
    for f in remove_f:
        bpy.app.handlers.game_pre.remove(f)
    for cls in reversed(_registered_classes):
        bpy.utils.unregister_class(cls)
    user_node_categories = set()
    for pair in _loaded_nodes:
        cat = pair[0]
        cls = pair[1]
        user_node_categories.add(cat)
        try:
            node_id = cls.__name__
            if hasattr(bpy.types, node_id):
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
                bpy.utils.unregister_class(getattr(bpy.types, node_id))
        except RuntimeError as ex:
            print("Custom socket {} not unloaded [{}]".format(cls.__name__, ex))
