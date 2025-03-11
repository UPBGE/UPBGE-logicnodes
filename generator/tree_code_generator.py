import bpy
from .. import utilities as utils
from .abstract_text_buffer import AbstractTextBuffer
from .uid_map import UIDMap
from ..utilities import make_valid_name, preferences
from ..utilities import check_uplogic_module
from ..utilities import ERROR_MESSAGES
from ..utilities import WARNING_MESSAGES
from ..editor.nodetree import LogicNodeTree
from time import time


def generate_logic_node_code():
    check_uplogic_module()
    global ERROR_MESSAGES
    ERROR_MESSAGES.clear()
    global WARNING_MESSAGES
    WARNING_MESSAGES.clear()

    logic_trees = [tree for tree in bpy.data.node_groups if tree.bl_idname == LogicNodeTree.bl_idname]
    for tree in logic_trees:
        tree.mark_invalid_links()
        # if tree.changes_staged:
        TreeCodeGenerator().write_code_for_tree(tree)
    # try:
    #     context.region.tag_redraw()
    # except Exception:
    #     warn("Couldn't redraw panel, code updated.")
    
    if ERROR_MESSAGES or WARNING_MESSAGES:
        def error_log(self, context):
            self.layout.label(text=f"Warnings, these may or may not be problematic, but it is recommended to resolve these.", icon='CONSOLE')
            self.layout.label(text=f"Concerned nodes have been marked YELLOW.")
            if WARNING_MESSAGES:
                self.layout.separator()
            for e in WARNING_MESSAGES:
                self.layout.label(text=f'{e}')
            if ERROR_MESSAGES:
                self.layout.separator()
                self.layout.label(text=f"Errors, these have to be resolved for the tree to work.", icon="ERROR")
                self.layout.label(text=f"Concerned nodes have been marked RED.")
                self.layout.separator()
            for e in ERROR_MESSAGES:
                self.layout.label(text=f'{e}')

        bpy.context.window_manager.popup_menu(error_log, title="Something happened during compilation.", icon='INFO')
        # bpy.app.handlers.game_post.append(
            
        # )
    else:
        for tree in logic_trees:
            tree.changes_staged = False
    bpy.context.window_manager.update_tag()


class BLTextWrapper(AbstractTextBuffer):
    _indent = ''

    def __init__(self, name):
        text = self.get_text(name)
        if text is None:
            utils.error('Could not find or generate text file')
        self.text = text

    def get_text(self, name):
        text = bpy.data.texts.get(name)
        if text is None:
            bpy.ops.text.new()
            for t in bpy.data.texts:
                if t.library is not None:
                    break
                else:
                    text = t
            text.name = name
        return text

    def clear(self):
        self.text.clear()

    def write_line(self, string):
        self.text.write(f'{self._indent}{string}\n')

    def close(self):
        pass


MODULE_TEMPLATE = """\
# MACHINE GENERATED
import bge, bpy, sys
import mathutils
import math
from collections import OrderedDict
from mathutils import Vector


class {}_Tree():

    def __init__(self, game_object, component=None, exec_cond="", startup=False):
        import uplogic
        from uplogic import nodes, utils
        from uplogic.nodes.logictree import ULLogicTree
        from uplogic.utils import OPERATORS, LOGIC_OPERATORS, MATH_OPERATORS
        from uplogic import console
{}
        self.condition = exec_cond
        owner = self.owner = game_object
        scene = self.scene = bge.logic.getCurrentScene()
        network = self.network = ULLogicTree()
        network.component = component
{}
        owner["IGNLTree_{}"] = network
        network._owner = game_object
        network.setup()
        network.stopped = not owner.get('NL__{}')
        self.consumed = startup

    def evaluate(self):
        if self.consumed:
            return
        owner = self.owner
        if self.condition:
            cond = owner[self.condition]
            if not cond: return
        network = self.network
        if network.stopped: return
        shutdown = network.evaluate()
        if shutdown is True:
            self.consumed = True


class {}(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("OnlyRunAtStartup", False),
        ("ExecutionCondition", ""){}
    ])

    def start(self, args):
        self.logictree = {}_Tree(
            self.object,
            component=self,
            exec_cond=args["ExecutionCondition"],
            startup=args["OnlyRunAtStartup"]
        )
{}
        self.logictree.evaluate()

    def update(self):
        if not self.logictree.consumed:
            self.logictree.evaluate()


def get_tree(obj):
    return {}_Tree(obj)

"""

# MODULE_TEMPLATE % {'start': lines}


class TreeCodeGenerator(object):

    def write_code_for_tree(self, tree):
        if preferences().use_node_debug:
            utils.notify("Generating code for tree {}".format(tree.name))
        tree_name = utils.make_valid_name(tree.name)
        line_writer = BLTextWrapper(f'nl_{tree_name.lower()}.py')
        imports = self.write_imports(tree)
        properties = self.get_properties(tree)
        text = self.add_nodes(tree)
        line_writer.clear()
        prop = self.get_property_defs(tree)
        text = MODULE_TEMPLATE.format(
            tree_name,
            imports,
            text,
            tree_name,
            tree_name,
            tree_name,
            properties,
            tree_name,
            prop,
            tree_name
        )
        line_writer.write_line(text)

    def write_imports(self, tree):
        text = ''
        imp = []
        for n in tree.nodes:
            try:
                mod = n.get_import_module()
                clsname = n.nl_class
                if clsname not in imp and mod:
                    imp.append(clsname)
                    # writer.write_line(f'from uplogic.nodes.{mod} import {clsname}')
                    text += f'        from {mod} import {clsname}\n'
            except Exception:
                continue
        return text

    def get_properties(self, tree):
        text = ''
        options = [
            0.0,
            '""',
            0,
            False,
            'mathutils.Vector((0., 0., 0.))',
            'mathutils.Color((.5, .5, .5))',
            'mathutils.Vector((.5, .5, .5, 1.0))',
            'bpy.types.Object',
            'bpy.types.Collection',
            'bpy.types.Material',
            'bpy.types.Mesh',
            'bpy.types.NodeTree',
            'bpy.types.Action',
            'bpy.types.Text',
            'bpy.types.Sound',
            'bpy.types.Image',
            'bpy.types.VectorFont'
        ]
        for prop in tree.properties:
            val = options[int(prop.value_type)]
            text += f',\n        ("{prop.name}", {val})'
        return text

    def get_property_defs(self, tree):
        text = ''
        for prop in tree.properties:
            getter = f'Vector(args["{prop.name}"])' if int(prop.value_type) in [4, 5, 6] else f'args["{prop.name}"]'
            text += f'        self.{make_valid_name(prop.name).lower()} = {getter}\n'
        return text

    def add_nodes(self, tree):
        cell_var_names, uid_map, text = self._write_tree(tree)
        for varname in self._sort_cellvarnames(cell_var_names, uid_map):
            if not uid_map.is_removed(varname):
                text += f"        network.add_cell({varname})\n"
        return text

    def _write_tree(self, tree):
        text = ''
        uid_map = UIDMap()
        cell_uid = 0
        # node_cellvar_list = []
        for node in tree.nodes:
            if not hasattr(node, 'nl_module') or node.mute:
                # utils.debug("Skipping TreeNode of type {} because it is not an instance of NLNode".format(node.__class__.__name__))
                continue
            if hasattr(node, 'nl_module'):
                node.check(tree)
                name = node.bl_idname.replace('.', '')
                name = name.replace(' ', '')
            else:
                raise ValueError(
                        "netlogic node {} must extend one of NLActionNode, NLConditionNode or NLParameterNode".format(
                                node.__class__.__name__))
            varname = "{0}{1:03d}".format(name, cell_uid)
            uid_map._register(varname, cell_uid, node)
            text += f'        {varname} = {node.nl_class}()\n'
            cell_uid += 1
        for uid in range(0, cell_uid):
            tree_node = uid_map._get_node_for_uid(uid)
            cell_varname = uid_map._get_varname_for_uid(uid)
            text += tree_node.setup(cell_varname, uid_map)
        # return text
        return uid_map._list_cell_names(), uid_map, text

    def _sort_cellvarnames(self, node_cellvar_list, uid_map):
        # sorting is effective only in serial execution context. Because the python vm is basically a serial only
        # machine, we force a potentially parallel network to work as a serial one. Shame on GIL.
        start = time()
        available_cells = list(node_cellvar_list)
        added_cells = []
        while available_cells:
            now = time()
            if now - start > 4:
                utils.error('Timeout Error. Check tree for unlinked Reroutes or other issues.')
                return []
            for cell_name in available_cells:
                node = uid_map.get_node_for_varname(cell_name)
                # if all the links of node are either constant or cells in added_cells, then this node can be put in the list
                if self._test_node_links(node, added_cells, uid_map) == 'GOOD':
                    available_cells.remove(cell_name)
                    added_cells.append(cell_name)
                elif self._test_node_links(node, added_cells, uid_map) == 'FAULTY':
                    name = node.label if node.label else node.name
                    utils.error(f'A Reroute does not have any input links! Skipping {name}.')
                    available_cells.remove(cell_name)
        return added_cells

    def _test_node_links(self, node, added_cell_names, uid_map):
        for input in node.inputs:
            if input.is_linked:
                # XXX: MAYBE THIS IS THE CAUSE OF ACCESS VIOLATION
                linked_node = input.links[0].from_socket.node
                if linked_node.mute:
                    return 'GOOD'
                while isinstance(linked_node, bpy.types.NodeReroute):
                    if not linked_node.inputs[0].links:
                        return 'FAULTY'
                    linked_node = linked_node.inputs[0].links[0].from_socket.node
                linked_node_varname = uid_map.get_varname_for_node(linked_node)
                if not (linked_node_varname in added_cell_names):
                    return 'WAITING'  # node is linked to a cell that has not been resolved
        # all inputs are constant expressions or linked to resolved cells
        return 'GOOD'
