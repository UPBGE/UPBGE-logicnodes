from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicArmature
from ...sockets import NodeSocketLogicBone
from ...sockets import NodeSocketLogicBoneConstraint
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeSetBoneConstraintAttr(LogicNodeActionType):
    bl_idname = "NLSetBoneConstraintAttribute"
    bl_label = "Set Attribute"
    nl_module = 'actions'
    nl_class = "ULSetBoneConstraintAttribute"

    search_tags = [
        ['Set Bone Constraint Attribute', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicArmature, "Armature")
        self.add_input(NodeSocketLogicBone, "", {'ref_index': 1})
        self.add_input(NodeSocketLogicBoneConstraint, "", {'ref_index': 2})
        self.add_input(NodeSocketLogicString, "Attribute")
        self.add_input(NodeSocketLogicValue, "")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    # def update_draw(self, context=None):
    #     self.inputs[2].enabled = (
    #         self.inputs[1].value is not None or
    #         self.inputs[1].is_linked or
    #         self.inputs[1].use_owner
    #     )
    #     self.inputs[3].enabled = (
    #         self.inputs[2].enabled and
    #         (self.inputs[2].value != '' or
    #          self.inputs[2].is_linked)
    #     )

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            "armature",
            "bone",
            "constraint",
            "attribute",
            "value",
        ]
