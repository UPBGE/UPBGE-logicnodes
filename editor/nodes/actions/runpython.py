from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicText
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicParameter
from ...enum_types import _enum_python_types
from bpy.props import EnumProperty


@node_type
class LogicNodeRunPython(LogicNodeActionType):
    bl_idname = "NLParameterPythonModuleFunction"
    bl_description = 'Execute a piece of python code'
    bl_label = "Run Python Code"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULRunPython"

    def update_draw(self, context=None):
        if not self.ready:
            return
        for i, ipt in enumerate(self.inputs):
            enabled = int(self.mode) > 0
            if i > 1:
                ipt.enabled = enabled
            self.outputs[1].enabled = enabled

    mode: EnumProperty(items=_enum_python_types, update=update_draw, name='Mode')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition', {'default_value': True, 'show_prop': True})
        self.add_input(NodeSocketLogicText, "Module Name", 'module_name')
        self.add_input(NodeSocketLogicString, "Function", 'module_func')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicParameter, "Returned Value", 'VAL')
        LogicNodeActionType.init(self, context)

    def set_new_input_name(self):
        self.inputs[-1].name = 'Argument'

    def draw_buttons(self, context, layout):
        layout.prop(self, 'mode', text='')
        if int(self.mode) > 0:
            op = layout.operator('logic_nodes.add_socket', text='Add Argument')
            op.socket_type = 'NodeSocketLogicArgumentItem'

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
            text += self.set_socket(
                self.inputs[socket],
                cell_varname,
                uids
            )
            socket += 1
        items = ''
        while socket < len(self.inputs):
            field_value = None
            if self.inputs[socket].linked_valid:
                field_value = self.get_linked_value(
                    self.inputs[socket],
                    uids
                )
            else:
                field_value = self.inputs[socket].get_default_value()
            items += f'{field_value}, '
            socket += 1
        items = items[:-2]
        line = f'        {cell_varname}.arg = [{items}]\n'
        return text + line

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['condition', "module_name", 'module_func']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", "VAL"]

    def get_attributes(self):
        return [('mode', self.mode)]
