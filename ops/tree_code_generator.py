import os
import bpy
import shutil
import bge_netlogic
import bge_netlogic.utilities as utils
from bge_netlogic.basicnodes import NLAbstractNode
from bge_netlogic.ops.file_text_buffer import FileTextBuffer
from bge_netlogic.ops.abstract_text_buffer import AbstractTextBuffer
from bge_netlogic.ops.uid_map import UIDMap


class BLTextWrapper(AbstractTextBuffer):
    _indent = ''

    def __init__(self, name):
        text = self.get_text(name)
        if text is None:
            utils.error('Could not find or generate text file')
        print(text)
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

    def write_line(self, string, *args):
        self.text.write(f'{self._indent}{string}\n'.format(*args))

    def close(self):
        pass


MODULE_TEMPLATE = """\
# MACHINE GENERATED
import bge, bpy, sys
import mathutils
import math
from collections import OrderedDict


class {}Wrapper():

    def __init__(self, args):
        {}
        self.condition = args['Execution Condition']
        self.consumed = False
        owner = self.object
        network = self.network = ULLogicTree()
        CON0000 = ULOnInit()
        ACT0001 = ULPrintValue()
        ACT0002 = ULPlayAction()
        ACT0001.condition = ACT0002.STARTED
        ACT0001.value = ACT0002.FRAME
        ACT0002.condition = CON0000
        ACT0002.game_object = "NLO:U_O"
        ACT0002.action_name = "CubeAction"
        ACT0002.start_frame = 0.0
        ACT0002.end_frame = 13.170000076293945
        ACT0002.layer = 0
        ACT0002.priority = 0
        ACT0002.play_mode = bge.logic.KX_ACTION_MODE_PLAY + 3
        ACT0002.stop = False
        ACT0002.layer_weight = 1.0
        ACT0002.speed = 1.0
        ACT0002.blendin = 0.0
        ACT0002.blend_mode = bge.logic.KX_ACTION_BLEND_BLEND
        network.add_cell(CON0000)
        network.add_cell(ACT0002)
        network.add_cell(ACT0001)
        network._owner = owner
        network.setup()
        network.stopped = not owner.get('NL__NodeTree')
        if args['Only Run At Startup']:
            self.consumed = True
        network.evaluate()

    def evaluate(self):
        if self.consumed:
            return
        owner = self.object
        if self.condition:
            cond = owner[self.condition]
            if not cond: return
        network = self.network
        if network.stopped: return
        shutdown = network.evaluate()
        if shutdown is True:
            self.consumed = True


class NodeTree(bge.types.KX_PythonComponent):

    args = OrderedDict([
        ("Only Run At Startup", False),
        ("Execution Condition", "")
    ])

    def start(self, args):
        self.logictree = NodeTreeWrapper(args)

    def update(self):
        self.logictree.evaluate()

"""

# MODULE_TEMPLATE % {'start': lines}


class TreeCodeGenerator(object):

    def get_netlogic_module_for_node(self, node):
        try:
            netlogic_class = node.get_netlogic_class_name()
            lastdot = netlogic_class.rfind(".")
            if lastdot < 0:
                return None  # assuming basicnodes
            return netlogic_class[0:lastdot]
        except AttributeError:
            return None

    def list_user_modules_needed_by_tree(self, tree):
        result = set()
        for node in tree.nodes:
            module_name = self.get_netlogic_module_for_node(node)
            if module_name is not None:  # if none assume is one in bgelogic.py
                if module_name != "bgelogic":
                    result.add(module_name)
        return result

    def create_text_file(self, name, path=None):
        if not path:
            path = bpy.path.abspath('//bgelogic/')
        return FileTextBuffer(os.path.join(path, name))

    def write_code_for_tree(self, tree):
        if getattr(bpy.context.scene.logic_node_settings, 'use_node_debug', False):
            utils.notify("Generating code for tree {}".format(tree.name))
        if tree.mode:
            writer = self.write_to_text(tree)
        else:
            writer = self.write_to_file(tree)
        self.write_init_content(tree, writer)
        indent = self.write_pulse_line(tree, writer)
        self.write_pulse_content(tree, writer, indent)
        if tree.mode:
            self.write_component_part(tree, writer, 0)

    def write_unloader(self, writer):
        writer.write_line("def unload_pyd(a, b):")
        writer.set_indent_level(1)
        writer.write_line("for m in sorted(sys.modules.keys()):")
        writer.set_indent_level(2)
        writer.write_line("if 'bge' in m:")
        writer.set_indent_level(3)
        writer.write_line("print(m)")
        writer.set_indent_level(1)
        writer.write_line("filter(lambda a: a.__name__ == 'unload_pyd', bpy.app.handlers.game_post)")
        writer.write_line("remove_f = []")
        writer.write_line("for f in bpy.app.handlers.game_post:")
        writer.set_indent_level(2)
        writer.write_line("if f.__name__ == 'unload_pyd':")
        writer.set_indent_level(3)
        writer.write_line("remove_f.append(f)")
        writer.set_indent_level(1)
        writer.write_line("for f in remove_f:")
        writer.set_indent_level(2)
        writer.write_line("bpy.app.handlers.game_post.remove(f)")
        writer.write_line('')
        writer.set_indent_level(0)

    def write_imports(self, tree, writer):
        imp = []
        for n in tree.nodes:
            try:
                mod = n.get_import_module()
                clsname = n.get_netlogic_class_name()
                if clsname not in imp and mod:
                    imp.append(clsname)
                    writer.write_line(f'from uplogic.nodes.{mod} import {clsname}')
            except Exception:
                continue

    def write_to_text(self, tree):
        tree_name = utils.make_valid_name(tree.name)
        line_writer = BLTextWrapper(f'nl_{tree_name.lower()}.py')
        line_writer.clear()
        line_writer.write_line("# MACHINE GENERATED")
        line_writer.write_line("import bge, bpy, sys")
        line_writer.write_line("import mathutils")
        line_writer.write_line("import math")
        line_writer.write_line("from collections import OrderedDict")
        # user_modules = self.list_user_modules_needed_by_tree(tree)
        # for module in user_modules:
        #     line_writer.write_line('{} = bgelogic.load_user_logic("{}")', module, module)
        line_writer.write_line('')
        line_writer.write_line('')
        line_writer.write_line(f'class {tree_name}Wrapper():')
        line_writer.write_line('')
        line_writer.set_indent_level(1)
        line_writer.write_line('def __init__(self, game_object, exec_cond="", startup=False):')
        line_writer.set_indent_level(2)
        line_writer.write_line("from uplogic import nodes, utils")
        line_writer.write_line("from uplogic.nodes.logictree import ULLogicTree")
        line_writer.write_line("from uplogic.utils import OPERATORS, LOGIC_OPERATORS")
        self.write_imports(tree, line_writer)
        line_writer.write_line("self.condition = exec_cond")
        line_writer.write_line("owner = self.owner = game_object")
        return line_writer

    def write_to_file(self, tree):
        buffer_name = utils.py_module_filename_for_tree(tree)
        line_writer = self.create_text_file(buffer_name)
        line_writer.write_line("# MACHINE GENERATED")
        line_writer.write_line("import bge, bpy, sys, importlib")
        line_writer.write_line("import mathutils")
        line_writer.write_line("from uplogic import nodes, utils")
        line_writer.write_line("from uplogic.nodes.logictree import ULLogicTree")
        self.write_imports(tree, line_writer)
        line_writer.write_line("import math")
        # user_modules = self.list_user_modules_needed_by_tree(tree)
        # for module in user_modules:
        #     if module == 'bgelogic.game':
        #         continue
        #     line_writer.write_line('{} = game.load_user_logic("{}")', module, module)
        line_writer.write_line("")
        # self.write_unloader(line_writer)
        # line_writer.write_line("bpy.app.handlers.game_post.append(unload_pyd)")
        line_writer.write_line("def _initialize(owner):")
        line_writer.set_indent_level(1)
        return line_writer

    def write_init_content(self, tree, line_writer):
        line_writer.write_line("network = self.network = ULLogicTree()")
        cell_var_names, uid_map = self._write_tree(tree, line_writer)
        for varname in self._sort_cellvarnames(cell_var_names, uid_map):
            if not uid_map.is_removed(varname):
                line_writer.write_line("network.add_cell({})", varname)
        tree_name = utils.make_valid_name(tree.name)
        line_writer.write_line('owner["IGNLTree_{}"] = network', tree_name)
        line_writer.write_line("network._owner = owner")
        line_writer.write_line("network.setup()")
        line_writer.write_line("network.stopped = not owner.get('{}')", utils.get_key_network_initial_status_for_tree(tree))
        line_writer.write_line("self.consumed = startup")

    def write_pulse_line(self, tree, line_writer):
        line_writer.set_indent_level(line_writer._indent_level - 1)
        line_writer.write_line("")
        if isinstance(line_writer, BLTextWrapper):
            line_writer.write_line('def evaluate(self):')
            line_writer.set_indent_level(2)
            line_writer.write_line("if self.consumed:")
            line_writer.set_indent_level(3)
            line_writer.write_line("return")
            line_writer.set_indent_level(2)
            line_writer.write_line("owner = self.owner")
            line_writer.write_line("if self.condition:")
            line_writer.set_indent_level(3)
            line_writer.write_line("cond = owner[self.condition]")
            line_writer.write_line("if not cond: return")
            line_writer.set_indent_level(2)
        else:
            line_writer.write_line('def pulse_network(controller):')
            line_writer.set_indent_level(1)
            line_writer.write_line("owner = controller.owner")
        return line_writer._indent_level

    def write_pulse_content(self, tree, line_writer, indent):
        # line_writer.write_line('network = owner.get("IGNLTree_{}")', tree.name)
        line_writer.write_line('network = self.network')
        if not isinstance(line_writer, BLTextWrapper):
            line_writer.write_line("if network is None:")
            line_writer.set_indent_level(indent + 1)
            line_writer.write_line("network = _initialize(owner)")
        line_writer.set_indent_level(indent)
        line_writer.write_line("if network.stopped: return")
        line_writer.write_line("shutdown = network.evaluate()")
        line_writer.write_line("if shutdown is True:")
        line_writer.set_indent_level(indent + 1)
        if not isinstance(line_writer, BLTextWrapper):
            line_writer.write_line("controller.sensors[0].repeat = False")
        else:
            line_writer.write_line("self.consumed = True")

    def write_component_part(self, tree, line_writer, indent=0):
        line_writer.set_indent_level(0)
        line_writer.write_line('')
        line_writer.write_line('')
        tree_name = utils.make_valid_name(tree.name)
        line_writer.write_line(f'class {tree_name}(bge.types.KX_PythonComponent):')
        line_writer.set_indent_level(1)
        line_writer.write_line('args = OrderedDict([')
        line_writer.set_indent_level(2)
        line_writer.write_line('("Only Run At Startup", False),')
        line_writer.write_line('("Execution Condition", "")')
        line_writer.set_indent_level(1)
        line_writer.write_line('])')
        line_writer.write_line('def start(self, args):')
        line_writer.set_indent_level(2)
        line_writer.write_line(f'self.logictree = {tree_name}Wrapper(')
        line_writer.set_indent_level(3)
        line_writer.write_line('self.object,')
        line_writer.write_line('exec_cond=args["Execution Condition"],')
        line_writer.write_line('startup=args["Only Run At Startup"]')
        line_writer.set_indent_level(2)
        line_writer.write_line(')')
        line_writer.write_line('self.logictree.evaluate()')
        line_writer.set_indent_level(1)
        line_writer.write_line('def update(self):')
        line_writer.set_indent_level(2)
        line_writer.write_line('if not self.logictree.consumed:')
        line_writer.set_indent_level(3)
        line_writer.write_line('self.logictree.evaluate()')
        line_writer.set_indent_level(0)
        line_writer.write_line('')
        line_writer.write_line('')
        # self.write_unloader(line_writer)
        line_writer.write_line('def get_tree(obj):')
        line_writer.set_indent_level(1)
        line_writer.write_line(f'return {tree_name}Wrapper(obj)')

    def _write_tree(self, tree, line_writer):
        uid_map = UIDMap()
        cell_uid = 0
        # node_cellvar_list = []
        for node in tree.nodes:
            prefix = None
            if not (
                isinstance(node, bge_netlogic.basicnodes.NLNode)
            ):
                # utils.debug("Skipping TreeNode of type {} because it is not an instance of NLNode".format(node.__class__.__name__))
                continue
            if isinstance(node, bge_netlogic.basicnodes.NLActionNode):
                prefix = "ACT"
            elif isinstance(node, bge_netlogic.basicnodes.NLConditionNode):
                prefix = "CON"
            elif isinstance(node, bge_netlogic.basicnodes.NLParameterNode):
                prefix = "PAR"
            else:
                raise ValueError(
                        "netlogic node {} must extend one of NLActionNode, NLConditionNode or NLParameterNode".format(
                                node.__class__.__name__))
            varname = "{0}{1:04d}".format(prefix, cell_uid)
            uid_map._register(varname, cell_uid, node)
            node.write_cell_declaration(varname, line_writer)
            cell_uid += 1
        for uid in range(0, cell_uid):
            tree_node = uid_map._get_node_for_uid(uid)
            cell_varname = uid_map._get_varname_for_uid(uid)
            tree_node.setup(cell_varname, uid_map, line_writer)
        return uid_map._list_cell_names(), uid_map

    def _sort_cellvarnames(self, node_cellvar_list, uid_map):
        # sorting is effective only in serial execution context. Because the python vm is basically a serial only
        # machine, we force a potentially parallel network to work as a serial one. Shame on GIL.
        available_cells = list(node_cellvar_list)
        added_cells = []
        while available_cells:
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
                while isinstance(linked_node, bpy.types.NodeReroute):
                    if not linked_node.inputs[0].links:
                        return 'FAULTY'
                    linked_node = linked_node.inputs[0].links[0].from_socket.node
                linked_node_varname = uid_map.get_varname_for_node(linked_node)
                if not (linked_node_varname in added_cell_names):
                    return 'WAITING'  # node is linked to a cell that has not been resolved
        # all inputs are constant expressions or linked to resolved cells
        return 'GOOD'
