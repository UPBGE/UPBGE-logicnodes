from ...utilities import error
from ...utilities import warn
from ...utilities import debug
from ...utilities import deprecate
from ...utilities import preferences
from ...utilities import ERROR_MESSAGES
from ...utilities import WARNING_MESSAGES
from ..nodetree import LogicNodeTree
from bpy.types import NodeReroute
from bpy.props import StringProperty
from bpy.props import BoolProperty
import bpy


WIDGETS = {}


_nodes = []
_node_manual_map = []


def node_type(obj):
    if obj.nl_module is None:
        error(f'{obj.bl_label}: Uplogic Module not defined! Node not registered.')
        return
    _nodes.append(obj)
    _node_manual_map.append((f"bpy.types.{obj.bl_idname}", "page_one"),)
    return obj


class LogicNode:
    nl_module = None
    nl_class = None
    nl_nodetype = 'INV'
    bl_description = 'Add a Logic Node'
    search_tags = []
    deprecated = False
    deprecation_message = 'Delete to avoid issues.'
    nl_label: StringProperty(default='')
    ready: BoolProperty(default=False)

    def set_socket_state(self, socket, enabled=True, name=None):
        socket.enabled = enabled
        if name:
            socket.name = name

    def update_draw(self, context=None):
        pass

    def draw_label(self):
        return self.label if self.label else (self.nl_label if self.nl_label else self.bl_label)

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

    def rebuild(self, name_map={}):
        ipts = {}
        for i in self.inputs:
            connected = []
            for link in i.links:
                connected.append(link.from_socket)
            ipts[name_map.get(i.name, i.name)] = connected
        opts = {}
        for i in self.outputs:
            connected = []
            for link in i.links:
                connected.append(link.to_socket)
            opts[name_map.get(i.name, i.name)] = connected
        self.inputs.clear()
        self.outputs.clear()
        self.init(bpy.context)
        for i in self.inputs:
            linked = ipts.get(i.name, None)
            if linked:
                for socket in linked:
                    self.tree.links.new(socket, i)
        for i in self.outputs:
            linked = opts.get(i.name, None)
            if linked:
                for socket in opts[i.name]:
                    self.tree.links.new(i, socket)

    def group_update(self, nodetree):
        pass

    def set_ready(self):
        self.ready = True
        self.update_draw(bpy.context)

    def add_input(self, cls, name, attr_name: str = '', settings: dict = {}, description='', shape=None, multi=False):
        if not attr_name:
            warn(f'"{self.bl_idname}.{name}" has no attribute name assigned!')
        attr_name = '' if attr_name is None else attr_name
        ipt = self.inputs.new(cls.bl_idname, name, use_multi_input=multi)
        # ipt.display_shape = shape if shape else cls.nl_shape
        self.nl_shape = shape if shape else 'CIRCLE'
        if description:
            ipt.description = description
        if settings:
            ipt.use_default_value = True
        for key, val in settings.items():
            setattr(ipt, key, val)
        setattr(ipt, 'identifier', attr_name)
        return ipt

    def add_output(self, cls, name, attr_name: str = '', settings: dict = {}, description='', shape=None):
        if not attr_name:
            warn(f'"{self.bl_idname}.{name}" has no attribute name assigned!')
        attr_name = '' if attr_name is None else attr_name
        otp = self.outputs.new(cls.bl_idname, name)
        # otp.display_shape = shape if shape else cls.nl_shape
        otp.display_shape = self.nl_shape = shape if shape else 'CIRCLE'
        if description:
            otp.descrtiption = description
        if settings:
            otp.use_default_value = True
        for key, val in settings.items():
            setattr(otp, key, val)
        setattr(otp, 'identifier', attr_name)
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

            # XXX Make this try-except block optional for better error reporting
            try:
                text += self.set_socket(
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
            except AttributeError as e:
                ERROR_MESSAGES.append(f'{self.name}: Attribute Error. Select a valid entity for this node: {e}')
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

    def set_socket(
        self,
        socket,
        cell_varname,
        uids
    ):
        text = ''
        input_names = self.get_input_names()
        input_socket_index = self._index_of(socket, self.inputs)
        field_name = None
        if input_socket_index is None:
            return text
        if input_names and input_names[input_socket_index] != socket.identifier:
            error(f'"{self.bl_idname}.{socket.name}": identifier does not match input name: {socket.identifier} != {input_names[input_socket_index]}!')
            field_name = input_names[input_socket_index]
            setattr(socket, 'identifier', field_name)
        elif getattr(socket, 'identifier', ''):
            field_name = socket.identifier
        elif input_names:
            field_name = input_names[input_socket_index]
            setattr(socket, 'identifier', field_name)
        else:
            field_name = self.get_socket_name(socket)
            warn(f'Node "{self.bl_label}" has called "()"! This is a bug, please report if receiving this message.')
        if socket.is_multi_input:
            field_value = ''
            for i, e in enumerate(socket.links):
                if not socket.linked_valid:
                    field_value = '[]  '  # 2 spaces needed for splicing
                else:
                    field_value += f'{self.get_linked_value(socket, uids, i)}, '

            field_value = field_value[:-2]
            field_value = f'[{field_value}]'
        else:
            field_value = None
            if not socket.linked_valid:
                field_value = socket.get_default_value()
            else:
                field_value = self.get_linked_value(socket, uids)
            

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

    def get_socket_name(self, socket):
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

    # XXX: Remove for 5.0
    def check_socket_identifiers(self):
        input_names = self.get_input_names()
        output_names = self.get_output_names()
        if input_names:
            for i, e in enumerate(input_names):
                if e != self.inputs[i].identifier:
                    error(f'"{self.bl_idname}.{self.inputs[i].identifier}": identifier does not match input name: {self.inputs[i].identifier} != {e}!')
        if output_names:
            for i, e in enumerate(output_names):
                if e != self.outputs[i].identifier:
                    error(f'"{self.bl_idname}.{self.outputs[i].identifier}": identifier does not match output name: {self.outputs[i].identifier} != {e}!')

    def get_linked_value(
        self,
        socket,
        uids,
        idx=0
    ):
        output_node = socket.links[idx].from_socket.node
        output_socket = socket.links[idx].from_socket

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

        if not hasattr(output_node, 'nl_module'): # XXX: if not isinstance(output_node, LogicNode):
            raise Exception(f'Not a LogicNode type: {output_node.bl_label}')
        output_node_varname = uids.get_varname_for_node(output_node)
        output_map = output_node.get_output_names()

        if output_map and output_map[output_socket_index] != output_socket.identifier:
            error(f'"{output_node.bl_idname}.{socket.name}": identifier does not match output name: {socket.identifier} != {output_map[output_socket_index]}!')
            varname = output_map[output_socket_index]
            setattr(output_socket, 'identifier', varname)
            return '{}.{}'.format(output_node_varname, varname)
        elif getattr(output_socket, 'identifier', ''):
            varname = output_socket.identifier
            return '{}.{}'.format(output_node_varname, varname)
        elif output_map:
            varname = output_map[output_socket_index]
            setattr(output_socket, 'identifier', varname)
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
        

class LogicNodeUIType(LogicNodeActionType):

    def get_ui_class(self):
        return None

    def update_widget(self):
        pass

    def show_widget(self, context):
        w = WIDGETS.get(self, None)
        if w is None:
            return
        elif self.preview:
            w.show = True
        else:
            w.show = False

    def free(self) -> None:
        w = WIDGETS.get(self, None)
        if w is not None and w.parent is not None:
            w.parent.remove_widget(w)
        return super().free()

    preview: BoolProperty(name='Show in preview', update=show_widget, default=True)
    
    def start_ui_preview(self):
        if self.get_ui_class() is None:
            return
        if WIDGETS.get(self, None) is None:
            w = WIDGETS[self] = self.get_ui_class()()
            w.update = self.update_widget
        for link in self.outputs[1].links:
            if isinstance(link.to_node, LogicNodeUIType):
                WIDGETS[self].add_widget(link.to_node.start_ui_preview())
        WIDGETS[self].register()
        self.update_widget()
        return WIDGETS[self]

    def end_ui_preview(self):
        pass


class LogicNodeCustomType(bpy.types.Node, LogicNode):
    nl_nodetype = 'CUS'
    nl_code = ''

    @classmethod
    def get_ref(cls):
        for n in preferences().custom_logic_nodes:
            if n.idname == cls.bl_idname:
                return n

    def init(self, context):
        self.set_ready()
        modname = self.nl_module[1:] + '.py'
        text = bpy.data.texts.get(modname, None)
        if text is None:
            text = bpy.data.texts.new(modname)
            text.clear()
            text.write(self.__class__.get_ref().logic_code)
