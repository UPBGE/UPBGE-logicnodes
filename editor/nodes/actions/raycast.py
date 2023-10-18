from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicBitMask
from bpy.props import BoolProperty


@node_type
class LogicNodeRaycast(LogicNodeActionType):
    bl_idname = "NLActionRayCastNode"
    bl_label = "Raycast"
    nl_class = "ULRaycast"
    nl_module = 'uplogic.nodes.actions'

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.outputs[5].enabled = self.face_data
        self.outputs[6].enabled = self.face_data
        self.inputs[9].enabled = self.inputs[8].default_value

    face_data: BoolProperty(
        name='Get Face Data',
        description='Show advanced options for this node. Hidden sockets will not be reset',
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicVectorXYZ, "Origin")
        self.add_input(NodeSocketLogicVectorXYZ, "Aim")
        self.add_input(NodeSocketLogicBoolean, "Local")
        self.add_input(NodeSocketLogicString, "Property")
        self.add_input(NodeSocketLogicMaterial, "Material")
        self.add_input(NodeSocketLogicBoolean, "Exclude")
        self.add_input(NodeSocketLogicBoolean, 'X-Ray')
        self.add_input(NodeSocketLogicBoolean, "Custom Distance")
        self.add_input(NodeSocketLogicFloatPositive, "Distance", {'default_value': 100.0})
        self.add_input(NodeSocketLogicBitMask, "Mask")
        self.add_input(NodeSocketLogicBoolean, 'Visualize')
        self.add_output(NodeSocketLogicCondition, "Has Result")
        self.add_output(NodeSocketLogicObject, "Picked Object")
        self.add_output(NodeSocketLogicVectorXYZ, "Picked Point")
        self.add_output(NodeSocketLogicVectorXYZ, "Picked Normal")
        self.add_output(NodeSocketLogicVectorXYZ, "Ray Direction")
        self.add_output(NodeSocketLogicParameter, "Face Material Name")
        self.add_output(NodeSocketLogicVectorXY, "UV Coords")
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'face_data', text='Face Data')

    def get_attributes(self):
        return [("face_data", self.face_data)]

    def get_input_names(self):
        return [
            "condition",
            "origin",
            "destination",
            'local',
            "property_name",
            "material",
            "exclude",
            'xray',
            'custom_dist',
            "distance",
            'mask',
            "visualize"
        ]

    def get_output_names(self):
        return ['RESULT', "PICKED_OBJECT", "POINT", "NORMAL", "DIRECTION", "MATERIAL", "UV"]
