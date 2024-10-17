from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXYZ
from ...enum_types import _enum_constraint_types
from bpy.props import EnumProperty


@node_type
class LogicNodeAddPhysicsConstraint(LogicNodeActionType):
    bl_idname = "NLActionAddPhysicsConstraint"
    bl_label = "Add Constraint"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULAddPhysicsConstraint"
    bl_description = 'Add a physical constraint to an object'
    deprecated = True
    deprecation_message = 'Replaced by newer version, please re-add'

    def update_draw(self, context=None):
        if len(self.inputs) < 9:
            return
        if self.constraint == 'bge.constraints.POINTTOPOINT_CONSTRAINT':
            self.inputs[6].enabled = False
            self.inputs[7].enabled = False
            return
        else:
            self.inputs[6].enabled = True
        if not self.inputs[6].default_value:
            self.inputs[7].enabled = False
        else:
            self.inputs[7].enabled = True

    constraint: EnumProperty(
        items=_enum_constraint_types,
        update=update_draw,
        name='Constraint Type'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", "condition")
        self.add_input(NodeSocketLogicObject, "Object", "target")
        self.add_input(NodeSocketLogicObject, "Target", "child")
        self.add_input(NodeSocketLogicString, 'Name', "name")
        self.add_input(NodeSocketLogicBoolean, 'Use World Space', 'use_world')
        self.add_input(NodeSocketLogicVectorXYZ, 'Pivot', "pivot")
        self.add_input(NodeSocketLogicBoolean, 'Limit Axis', 'use_limit')
        self.add_input(NodeSocketLogicVectorXYZ, 'Axis Limits', "axis_limits")
        self.add_input(NodeSocketLogicBoolean, 'Linked Collision', None, {'default_value': True}, "linked_col")
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'constraint', text='')

    def get_attributes(self):
        return [('constraint', self.constraint)]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "target",
            "child",
            "name",
            'use_world',
            "pivot",
            'use_limit',
            "axis_limits",
            "linked_col"
        ]
