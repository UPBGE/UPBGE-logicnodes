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
    bl_description = 'Perform a linear raycast from one point to another'
    nl_class = "ULRaycast"
    nl_module = 'uplogic.nodes.actions'

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.outputs[5].enabled = self.face_data
        self.outputs[6].enabled = self.face_data
        self.inputs[9].enabled = self.inputs[8].default_value
        self.inputs[2].name = 'Direction' if self.inputs[3].default_value else 'Target'

    face_data: BoolProperty(
        name='Get Face Data',
        description='Show advanced options for this node. Hidden sockets will not be reset',
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", "condition")
        self.add_input(NodeSocketLogicObject, "Caster", 'caster', {'use_owner': True})
        self.add_input(NodeSocketLogicVectorXYZ, "Origin", "origin")
        self.add_input(NodeSocketLogicVectorXYZ, "Aim", "destination")
        self.add_input(NodeSocketLogicBoolean, "Local", 'local')
        self.add_input(NodeSocketLogicString, "Property", "property_name")
        self.add_input(NodeSocketLogicMaterial, "Material", "material")
        self.add_input(NodeSocketLogicBoolean, "Exclude", "exclude")
        self.add_input(NodeSocketLogicBoolean, 'X-Ray', 'xray')
        self.add_input(NodeSocketLogicBoolean, "Custom Distance", 'custom_dist')
        self.add_input(NodeSocketLogicFloatPositive, "Distance", 'distance', {'default_value': 100.0})
        self.add_input(NodeSocketLogicBitMask, "Mask", 'mask')
        self.add_input(NodeSocketLogicBoolean, 'Visualize', 'visualize')
        self.add_output(NodeSocketLogicCondition, "Has Result", 'RESULT')
        self.add_output(NodeSocketLogicObject, "Picked Object", 'PICKED_OBJECT')
        self.add_output(NodeSocketLogicVectorXYZ, "Picked Point", 'POINT')
        self.add_output(NodeSocketLogicVectorXYZ, "Picked Normal", 'NORMAL')
        self.add_output(NodeSocketLogicVectorXYZ, "Ray Direction", 'DIRECTION')
        self.add_output(NodeSocketLogicParameter, "Face Material Name", 'MATERIAL')
        self.add_output(NodeSocketLogicVectorXY, "UV Coords", 'UV')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'face_data', text='Face Data')

    def get_attributes(self):
        return [("face_data", self.face_data)]

    # XXX: Remove for 5.0
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

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['RESULT', "PICKED_OBJECT", "POINT", "NORMAL", "DIRECTION", "MATERIAL", "UV"]
