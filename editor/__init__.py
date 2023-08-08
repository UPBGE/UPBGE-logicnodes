import bpy
from ..utilities import Color
from . import sockets



TOO_OLD = bpy.app.version < (2, 80, 0)

CONDITION_NODE_COLOR = Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
PARAMETER_NODE_COLOR = Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
ACTION_NODE_COLOR = Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
PYTHON_NODE_COLOR = Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]


OUTCELL = "__standard_logic_cell_value__"


def parse_field_value(value_type, value):
    t = value_type
    v = value

    if t == "NONE":
        return "None"

    if t == "INTEGER":
        try:
            return int(v)
        except ValueError:
            return "0.0"

    if t == "FLOAT":
        try:
            return float(v)
        except ValueError:
            return "0.0"

    if t == "STRING":
        return '"{}"'.format(v)

    if t == "FILE_PATH":
        return '"{}"'.format(v)

    if t == "BOOLEAN":
        return v

    raise ValueError(
        "Cannot parse enum {} type for NLValueFieldSocket".format(t)
    )


def socket_field(s):
    return parse_field_value(s.value_type, s.value)


def keyboard_key_string_to_bge_key(ks):
    ks = ks.replace("ASTERIX", "ASTER")

    if ks == "NONE":
        return "None"

    if ks == "RET":
        ks = "ENTER"

    if ks.startswith("NUMPAD_"):
        ks = ks.replace("NUMPAD_", "PAD")
        if("SLASH" in ks or "ASTER" in ks or "PLUS" in ks):
            ks = ks.replace("SLASH", "SLASHKEY")
            ks = ks.replace("ASTER", "ASTERKEY")
            ks = ks.replace("PLUS", "PLUSKEY")
        return "bge.events.{}".format(ks)

    x = "{}KEY".format(ks.replace("_", ""))

    return "bge.events.{}".format(x)


class NetLogicType:
    pass

def update_tree_code(self, context):
    if not hasattr(context.space_data, 'edit_tree'):
        return
    tree = context.space_data.edit_tree
    for node in tree.nodes:
        if isinstance(node, NLNode):
            try:
                node.update_draw()
            except Exception:
                pass
    if not getattr(bpy.context.scene.logic_node_settings, 'auto_compile'):
        return
    bge_netlogic.update_current_tree_code()


class NLNode(NetLogicType):
    nl_module = None

    def write_cell_declaration(self, cell_varname, line_writer):
        classname = self.get_netlogic_class_name()
        line_writer.write_line("{} = {}()", cell_varname, classname)

    def setup(
        self,
        cell_varname,
        uids,
        line_writer
    ):
        for t in self.get_nonsocket_fields():
            field_name = t[0]
            field_value = t[1]
            if callable(field_value):
                field_value = field_value()
            line_writer.write_line(
                '{}.{} = {}',
                cell_varname,
                field_name,
                field_value
            )
        for socket in self.inputs:
            self.write_socket_field_initialization(
                socket,
                cell_varname,
                uids,
                line_writer
            )
        self.set_props(line_writer, cell_varname)

    def set_props(self, writer, node):
        pass

    def write_socket_field_initialization(
        self,
        socket,
        cell_varname,
        uids,
        line_writer
    ):
        input_names = self.get_input_sockets_field_names()
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
        line_writer.write_line(
            "{}.{} = {}",
            cell_varname,
            field_name,
            field_value
        )

    def get_nonsocket_fields(self):
        """
        Return a list of (field_name, field_value) tuples, where field_name
        couples to output socket with a cell field and field_value is
        either a value or a no-arg callable producing value
        :return: the non socket fields initializers
        """
        return []

    def get_import_module(self):
        return self.nl_module

    def get_input_sockets_field_names(self):
        return None

    def get_field_name_for_socket(self, socket):
        debug("not implemented in ", self)
        raise NotImplementedError()

    def get_netlogic_class_name(self):
        raise NotImplementedError()

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

        while isinstance(output_node, bpy.types.NodeReroute):
            # cycle through and reset output_node until master is met
            if not output_node.inputs[0].links:
                return None
            next_socket = output_node.inputs[0].links[0].from_socket
            next_node = next_socket.node
            output_socket = next_socket
            if isinstance(next_node, NLNode):
                break
            output_node = next_node

        if isinstance(output_node, bpy.types.NodeReroute):
            output_node = output_node.inputs[0].links[0].from_socket.node
        output_socket_index = self._index_of(
            output_socket,
            output_node.outputs
        )

        if not isinstance(output_node, NLNode):
            raise Exception('No NLNode')
        output_node_varname = uids.get_varname_for_node(output_node)
        output_map = output_node.get_output_socket_varnames()

        if output_map:
            varname = output_map[output_socket_index]
            if varname is OUTCELL:
                return output_node_varname
            else:
                return '{}.{}'.format(output_node_varname, varname)
        else:
            return output_node_varname

    def get_output_socket_varnames(self):
        return None

    def update(self):
        pass