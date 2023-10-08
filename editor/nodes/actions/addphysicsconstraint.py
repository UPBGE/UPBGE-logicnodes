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
    nl_module = 'actions'
    nl_class = "ULAddPhysicsConstraint"

    def update_draw(self, context=None):
        if len(self.inputs) < 9:
            return
        if self.constraint == 'bge.constraints.POINTTOPOINT_CONSTRAINT':
            self.inputs[6].enabled = False
            self.inputs[7].enabled = False
            return
        else:
            self.inputs[6].enabled = True
        if not self.inputs[6].value:
            self.inputs[7].enabled = False
        else:
            self.inputs[7].enabled = True

    constraint: EnumProperty(
        items=_enum_constraint_types,
        update=update_draw,
        name='Constraint Type'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicObject, "Target")
        self.add_input(NodeSocketLogicString, 'Name')
        self.add_input(NodeSocketLogicBoolean, 'Use World Space')
        self.add_input(NodeSocketLogicVectorXYZ, 'Pivot')
        self.add_input(NodeSocketLogicBoolean, 'Limit Axis')
        self.add_input(NodeSocketLogicVectorXYZ, 'Axis Limits')
        self.add_input(NodeSocketLogicBoolean, 'Linked Collision', {'value': True})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'constraint', text='')

    def get_output_names(self):
        return ["OUT"]

    def get_attributes(self):
        return [('constraint', self.constraint)]

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
