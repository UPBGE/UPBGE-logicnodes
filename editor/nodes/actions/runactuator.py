from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBrick
from ....utilities import NLPREFIX
import bpy


@node_type
class LogicNodeRunActuator(LogicNodeActionType):
    bl_idname = "NLRunActuatorNode"
    bl_label = "Run Actuator"
    nl_module = 'uplogic.nodes.actions'
    deprecated = True
    deprecation_message = 'Node will be removed in future update.'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, 'Object')
        self.add_input(NodeSocketLogicBrick, "From Controller", None, {'ref_index': 1})
        self.add_input(NodeSocketLogicBrick, "Actuator", None, {'ref_index': 1, 'brick_type': 'actuators'})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_controller(self):
        tree = getattr(bpy.context.space_data, 'edit_tree', None)
        obj_socket = self.inputs[1]
        cont_name = self.inputs[2].default_value
        if not cont_name:
            return False
        if not obj_socket.use_owner and obj_socket.default_value:
            if cont_name in obj_socket.default_value.game.controllers:
                cont = obj_socket.default_value.game.controllers[cont_name]
                return isinstance(cont, bpy.types.PythonController)
        else:
            for sc_ob in bpy.data.objects:
                if f'{NLPREFIX}{tree.name}' in sc_ob.game.properties:
                    if cont_name in sc_ob.game.controllers:
                        cont = sc_ob.game.controllers[cont_name]
                        return isinstance(cont, bpy.types.PythonController)
        return False

    def draw_buttons(self, context, layout):
        if not self.get_controller():
            col = layout.column()
            col.label(text='Selected Brick', icon='ERROR')
            col.label(text='not a Python Controller!')

    def update_draw(self, context=None):
        self.inputs[3].enabled = self.get_controller()

    def get_output_names(self):
        return ["OUT"]

    nl_class = "ULRunActuator"

    def get_input_names(self):
        return ["condition", 'game_obj', 'cont_name', 'act_name']
