import bpy
# import nodeitems_utils
from bpy.app.handlers import persistent
# import bge_netlogic.utilities as utils
import os
import sys
import time
from .editor.sockets.socket import _sockets
from .editor.nodes.node import _nodes
from .editor.nodes.node import _node_manual_map
from .ops.operator import _operators
from .props.property import _properties
from .ui.interface import _panels
from .ui.interface import _lists
from .ui.interface import _menu_items
from .ui import node_menu
from .props.propertyfilter import LogicNodesPropertyFilter
from .props.globalcategory import LogicNodesGlobalCategory
from .preferences import LogicNodesAddonPreferences
from .utilities import preferences as prefs
from .editor.nodetree import LogicNodeTree
# from . import basicnodes
from . import utilities as utils
from . import audio

from .props.customnode import custom_node
from .props.customnode import CustomNodeReference


bl_info = {
    "name": "Logic Nodes+",
    "description": (
        "A Node System to create game logic."
    ),
    "author": "pgi, Leopold A-C (Iza Zed)",
    "version": (3, 0),
    "blender": (4, 1, 0),
    "location": "View Menu",
    "category": "Game Engine",
    "wiki_url": "https://upbge.org/#/documentation/docs/latest/manual/manual/logic_nodes/index.html",
    "tracker_url": "https://github.com/UPBGE/UPBGE-logicnodes/issues"
}

_loaded_nodes = []
_loaded_sockets = []
_current_user_nodes_parent_directory = None
_tree_to_name_map = {}


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


@persistent
def _reload_texts(self, context):
    if not prefs().use_reload_text:
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
    for tree in bpy.data.node_groups:
        if isinstance(tree, LogicNodeTree):
            tree.changes_staged = True
    bpy.ops.logic_nodes.generate_code()


@persistent
def _jump_in_game_cam(self, context):
    if prefs().jump_in_game_cam:
        bpy.ops.view3d.view_camera()


@persistent
def _set_vr_mode(self, context):
    if prefs().use_vr_audio_space and not bpy.context.window_manager.xr_session_state:
        bpy.context.scene.game_settings.use_viewport_render = True
        utils.notify('Starting in VR mode...')
        utils.start_vr_session()
    elif bpy.context.window_manager.xr_session_state and not prefs().use_vr_audio_space:
        utils.notify('Shutting down VR mode...')
        utils.stop_vr_session()


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
def _watch_tree_names(self, context):
    global RENAMING
    if RENAMING:
        return
    else:
        RENAMING = True
        for tree in bpy.data.node_groups:
            if isinstance(tree, LogicNodeTree):
                if tree.name != tree.old_name:
                    tree.update_name()
        RENAMING = False


for f in [
    refresh_custom_nodes
]:
    if f in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(f)
    bpy.app.handlers.load_post.append(f)


class NLNodeTreeReference(bpy.types.PropertyGroup):
    tree: bpy.props.PointerProperty(type=LogicNodeTree)
    tree_name: bpy.props.StringProperty()
    tree_initial_status: bpy.props.BoolProperty()


class LogicNodeTreeReference(bpy.types.PropertyGroup):
    tree: bpy.props.PointerProperty(type=LogicNodeTree)
    tree_name: bpy.props.StringProperty()
    tree_initial_status: bpy.props.BoolProperty()


_registered_classes = []


_registered_classes.extend(_sockets)
_registered_classes.extend(_nodes)
_registered_classes.extend(_operators)
_registered_classes.extend(_properties)
_registered_classes.extend(_panels)
_registered_classes.extend(_lists)
_registered_classes.extend(_menu_items)
# _registered_classes.append(LogicNodeTree)

def _get_key_for_class(c):
    if hasattr(c, "bl_label"):
        return c.bl_label
    else:
        return "zzz"


_registered_classes = sorted(_registered_classes, key=_get_key_for_class)


# Create the menu items that allow the user to add nodes to a tree


def update_uplogic_module():
    try:
        prefs = bpy.context.preferences.addons['bge_netlogic'].preferences
        os.system(f'"{sys.executable}" -m ensurepip')
        os.system(f'"{sys.executable}" -m pip install uplogic --upgrade')
    except Exception:
        pass


def get_uplogic_module():
    try:
        os.system(f'"{sys.executable}" -m ensurepip')
        os.system(f'"{sys.executable}" -m pip install uplogic')
    except Exception:
        pass



@persistent
def _update_properties(file):
    for obj in bpy.data.objects:
        applied_trees = obj.get('bgelogic_treelist', None)
        if applied_trees is not None:
            for tree in obj.bgelogic_treelist:
                _tree = obj.logic_trees.add()
                _tree.tree = tree.tree
                _tree.tree_name = tree.tree_name
                _tree.tree_initial_status = tree.tree_initial_status
                # XXX: del obj['bgelogic_treelist']


def node_manual():
    prefix = "https://myaddon.org/manual/"
    ret = (prefix, _node_manual_map)
    return ret


# blender add-on registration callback
def register():
    print('Registering Logic Nodes...')
    bpy.utils.register_manual_map(node_manual)
    bpy.types.NODE_MT_add.append(node_menu.draw_add_menu)
    bpy.app.handlers.game_pre.append(_generate_on_game_start)
    bpy.app.handlers.game_pre.append(_jump_in_game_cam)
    bpy.app.handlers.game_pre.append(_set_vr_mode)
    bpy.app.handlers.game_pre.append(_reload_texts)
    bpy.app.handlers.load_post.append(_update_properties)

    bpy.app.handlers.depsgraph_update_post.append(_watch_tree_names)
    for cls in _registered_classes:
        bpy.utils.register_class(cls)

    bpy.utils.register_class(LogicNodeTree)
    bpy.utils.register_class(LogicNodeTreeReference)
    bpy.utils.register_class(CustomNodeReference)
    bpy.utils.register_class(LogicNodesAddonPreferences)

    for node in prefs().custom_logic_nodes:
        exec(node.ui_code)
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

    # XXX: Remove bgelogic_treelist attr in the future
    bpy.types.Object.bgelogic_treelist = bpy.props.CollectionProperty(
        type=LogicNodeTreeReference
    )

    bpy.types.Object.logic_trees = bpy.props.CollectionProperty(
        type=LogicNodeTreeReference
    )

    def filter_components(self, item=bpy.types.Text):
        if not item.name.startswith('nl_'):
            return True

    bpy.types.Scene.componenthelper = bpy.props.PointerProperty(
        type=bpy.types.Text,
        poll=filter_components,
        name='Component',
        description='Add a component defined in this file'
    )
    bpy.types.Scene.nl_global_categories = bpy.props.CollectionProperty(type=LogicNodesGlobalCategory)
    bpy.types.Scene.nl_global_cat_selected = bpy.props.IntProperty(name='Category')
    bpy.types.Scene.custom_mainloop_tree = bpy.props.PointerProperty(
        name='Custom Mainloop Tree',
        type=bpy.types.NodeTree
    )
    # get_uplogic_module()


# blender add-on unregistration callback
def unregister():
    print('Unregistering Logic Nodes...')
    bpy.utils.unregister_manual_map(node_manual)
    bpy.types.NODE_MT_add.remove(node_menu.draw_add_menu)
    utils.debug('Removing Game Start Compile handler...')
    remove_f = []
    filter(lambda a: a.__name__ == '_generate_on_game_start', bpy.app.handlers.game_pre)
    filter(lambda a: a.__name__ == '_watch_tree_names', bpy.app.handlers.depsgraph_update_post)
    filter(lambda a: a.__name__ == '_reload_texts', bpy.app.handlers.game_pre)
    filter(lambda a: a.__name__ == '_update_properties', bpy.app.handlers.load_post)
    for f in bpy.app.handlers.game_pre:
        if f.__name__ == '_generate_on_game_start' or f.__name__ == '_reload_texts':
            remove_f.append(f)
    for f in remove_f:
        bpy.app.handlers.game_pre.remove(f)

    for cls in reversed(_registered_classes):
        bpy.utils.unregister_class(cls)

    for cls in reversed(ui.node_menu._registered_custom_classes):
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
