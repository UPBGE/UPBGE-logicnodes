from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicArmature
from ...sockets import NodeSocketLogicBone
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeSetBonePosition(LogicNodeActionType):
    bl_idname = "NLActionSetBonePos"
    bl_label = "Set Bone Position"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetBonePosition"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicArmature, "Armature")
        self.add_input(NodeSocketLogicBone, "Bone Name", None, {'ref_index': 1})
        self.add_input(NodeSocketLogicVectorXYZ, "Set Pos")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "armature", "bone_name", "set_translation"]
