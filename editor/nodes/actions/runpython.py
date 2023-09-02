from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicBoolCondition
from ...sockets import NodeSocketLogicText
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicListItem
from ...sockets import NodeSocketLogicParameter
from ...enum_types import _enum_python_types
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeRunPython(LogicNodeActionType):
    bl_idname = "NLParameterPythonModuleFunction"
    bl_label = "Run Python Code"
    nl_category = "Python"
    nl_module = 'actions'
    mode: EnumProperty(items=_enum_python_types, update=update_draw)

    def init(self, context):
        LogicNodeActionType.init(self, context)
        self.add_input(NodeSocketLogicBoolCondition, "Condition")
        self.add_input(NodeSocketLogicText, "Module Name")
        self.add_input(NodeSocketLogicString, "Function")
        self.add_output(NodeSocketLogicBoolCondition, "Done")
        self.add_output(NodeSocketLogicParameter, "Returned Value")
        self.update_draw()

    def get_netlogic_class_name(self):
        return "ULRunPython"

    def set_new_input_name(self):
        self.inputs[-1].name = 'Argument'

    def update_draw(self):
        for i, ipt in enumerate(self.inputs):
            if i > 1:
                ipt.enabled = int(self.mode) > 0

    def draw_buttons(self, context, layout):
        layout.prop(self, 'mode', text='')
        if int(self.mode) > 0:
            layout.operator('logic_nodes.add_list_item_socket', text='Add Argument') 

    def setup(
        self,
        cell_varname,
        uids
    ):
        text = ''
        socket = 0
        for t in self.get_attributes():
            field_name = t[0]
            field_value = t[1]
            if callable(field_value):
                field_value = field_value()
            text += f'        {cell_varname}.{field_name} = {field_value}\n'
        while socket <= 2:
            text += self.write_socket_field_initialization(
                self.inputs[socket],
                cell_varname,
                uids
            )
            socket += 1
        items = ''
        while socket < len(self.inputs):
            field_value = None
            if self.inputs[socket].is_linked:
                field_value = self.get_linked_socket_field_value(
                    self.inputs[socket],
                    cell_varname,
                    None,
                    uids
                )
            else:
                field_value = self.inputs[socket].get_unlinked_value()
            items += f'{field_value}, '
            socket += 1
        items = items[:-2]
        line = f'        {cell_varname}.arg = [{items}]\n'
        return text + line

    def get_input_names(self):
        return ['condition', "module_name", 'module_func']

    def get_output_names(self):
        return ["OUT", "VAL"]

    def get_attributes(self):
        return [('mode', lambda: self.mode)]
