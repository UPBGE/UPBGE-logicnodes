from ...utilities import error
from ...utilities import debug
from ...utilities import warn
from ...utilities import deprecate
from ...utilities import OUTCELL
from ...utilities import ERROR_MESSAGES
from ...utilities import WARNING_MESSAGES
from ..nodetree import LogicNodeTree
from bpy.types import NodeReroute
from bpy.props import StringProperty
from bpy.props import BoolProperty
import bpy


_nodes = []


def node_type(obj):
    if obj.nl_module is None:
        error(f'{obj.bl_label}: Uplogic Module not defined! Node not registered.')
        return
    _nodes.append(obj)
    return obj


class LogicNode:
    nl_module = None
    nl_class = None
    nl_nodetype = 'INV'
    search_tags = []
    deprecated = False
    deprecation_message = 'Delete to avoid issues.'
    nl_label: StringProperty(default='')
    ready: BoolProperty(default=False)

    def update_draw(self, context=None):
        pass

    def draw_label(self):
        return self.label if self.label else self.nl_label

    @classmethod
    def poll(cls, node_tree):
        return isinstance(node_tree, LogicNodeTree)

    @property
    def tree(self):
        for tree in bpy.data.node_groups:
            if not isinstance(tree, LogicNodeTree):
                continue
            nodes = [node for node in tree.nodes]
            if self in nodes:
                return tree

    def group_update(self, nodetree):
        pass
    # def insert_link(self, link):
    #     to_socket = link.to_socket
    #     from_socket = link.from_socket
    #     try:
    #         to_socket.validate(link, from_socket)
    #     except Exception as e:
    #         warn(e)
    #         debug(
    #             'Receiving Node not a Logic Node Type, skipping validation.'
    #         )

    def set_ready(self):
        self.ready = True
        self.update_draw(bpy.context)

    def add_input(self, cls, name, settings={}):
        ipt = self.inputs.new(cls.bl_idname, name)
        for key, val in settings.items():
            setattr(ipt, key, val)
        return ipt

    def add_output(self, cls, name, settings={}):
        otp = self.outputs.new(cls.bl_idname, name)
        for key, val in settings.items():
            setattr(otp, key, val)
        return otp

    def free(self):
        pass

    def draw_buttons(self, context, layout):
        pass

    def write_cell_declaration(self, cell_varname, line_writer):
        classname = self.get_netlogic_class_name()
        line_writer.write_line("{} = {}()", cell_varname, classname)

    def setup(
        self,
        cell_varname,
        uids
    ):
        text = ''
        global ERROR_MESSAGES
        for t in self.get_attributes():
            field_name = t[0]
            field_value = t[1]
            if callable(field_value):
                field_value = field_value()
            text += f'        {cell_varname}.{field_name} = {field_value}\n'
        for socket in self.inputs:

            # Skip hidden Sockets to avoid clutter
            if not socket.enabled:
                continue

            try:
                text += self.write_socket_field_initialization(
                    socket,
                    cell_varname,
                    uids
                )
            except IndexError as e:
                error(
                    f"Index error for node '{self.name}'. This normally happens when a node has sockets added or removed in an update. Try re-adding the node to resolve this issue."
                )
                ERROR_MESSAGES.append(f'{self.name}: Index Error. FIX: Delete and re-add node; issue might be a linked input node as well.')
                self.use_custom_color = True
                self.color = (1, 0, 0)
            except AttributeError:
                ERROR_MESSAGES.append(f'{self.name}: Attribute Error. Select a valid entity for this node.')
            except Exception as e:
                error(
                    f'Error occured when writing sockets for {self.__class__} Node: {e}\n'
                    f'\tInfo:\n'
                    f'\tSocket: {socket}\n'
                    f'\tCellname: {cell_varname}\n'
                    f'\tNode: {self.label if self.label else self.name}\n'
                    '---END ERROR'
                )
                ERROR_MESSAGES.append(f'{self.name}: Unknown Error: {e}')
                self.use_custom_color = True
                self.color = (1, 0, 0)
        return text

    def write_socket_field_initialization(
        self,
        socket,
        cell_varname,
        uids
    ):
        text = ''
        input_names = self.get_input_names()
        input_socket_index = self._index_of(socket, self.inputs)
        field_name = None
        if input_names:
            field_name = input_names[input_socket_index]
        else:
            field_name = self.get_field_name_for_socket(socket)
        field_value = None
        if socket.is_linked:
            field_value = self.get_linked_socket_field_value(
                socket,
                cell_varname,
                field_name,
                uids
            )
        else:
            field_value = socket.get_unlinked_value()

        text += f'        {cell_varname}.{field_name} = {field_value}\n'
        return text

    def get_attributes(self):
        """
        Return a list of (field_name, field_value) tuples, where field_name
        couples to output socket with a cell field and field_value is
        either a value or a no-arg callable producing value
        :return: the non socket fields initializers
        """
        return []

    def get_import_module(self):
        return self.nl_module

    def get_input_names(self):
        return None

    def get_field_name_for_socket(self, socket):
        debug("not implemented in ", self)
        raise NotImplementedError()

    def check(self, tree):
        if self.deprecated:
            deprecate(self, tree)
            global WARNING_MESSAGES
            WARNING_MESSAGES.append(
                f"Deprecated Node: '{self.name}' in '{self.tree.name}'. {self.deprecation_message}"
            )
            self.use_custom_color = True
            self.color = (.8, .6, 0)
        for socket in self.inputs:
            socket.check(tree)
        for socket in self.outputs:
            socket.check(tree)

    def _index_of(self, item, a_iterable):
        i = 0
        for e in a_iterable:
            if e == item:
                return i
            i += 1

    def get_linked_socket_field_value(
        self,
        socket,
        cell_varname,
        field_name,
        uids
    ):
        output_node = socket.links[0].from_socket.node
        output_socket = socket.links[0].from_socket

        while isinstance(output_node, NodeReroute):
            # cycle through and reset output_node until master is met
            if not output_node.inputs[0].links:
                return None
            next_socket = output_node.inputs[0].links[0].from_socket
            next_node = next_socket.node
            output_socket = next_socket
            if isinstance(next_node, LogicNode):
                break
            output_node = next_node

        if isinstance(output_node, NodeReroute):
            output_node = output_node.inputs[0].links[0].from_socket.node
        output_socket_index = self._index_of(
            output_socket,
            output_node.outputs
        )

        if not hasattr(output_node, 'nl_module'): # xxx: if not isinstance(output_node, LogicNode):
            raise Exception(f'Not a LogicNode type: {output_node.bl_label}')
        output_node_varname = uids.get_varname_for_node(output_node)
        output_map = output_node.get_output_names()

        if output_map:
            varname = output_map[output_socket_index]
            if varname is OUTCELL:
                return output_node_varname
            else:
                return '{}.{}'.format(output_node_varname, varname)
        else:
            return output_node_varname

    def get_output_names(self):
        return None

    def update(self):
        pass


class LogicNodeConditionType(bpy.types.Node, LogicNode):
    nl_nodetype = 'CON'

    def init(self, context):
        self.set_ready()


class LogicNodeParameterType(bpy.types.Node, LogicNode):
    nl_nodetype = 'PAR'

    def init(self, context):
        self.set_ready()


class LogicNodeActionType(bpy.types.Node, LogicNode):
    nl_nodetype = 'ACT'

    def init(self, context):
        self.set_ready()