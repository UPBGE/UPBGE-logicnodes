from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULSetBoneConstraintAttribute(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.armature = None
        self.bone = None
        self.constraint = None
        self.attribute = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        armature = self.get_input(self.armature)
        bone = self.get_input(self.bone)
        constraint = self.get_input(self.constraint)
        attribute = self.get_input(self.attribute)
        value = self.get_input(self.value)
        if is_waiting(
            armature,
            bone,
            constraint,
            attribute,
            value
        ):
            return
        self._set_ready()
        if is_invalid(armature):
            return
        setattr(
            (
                armature
                .blenderObject
                .pose
                .bones[bone]
                .constraints[constraint]
            ),
            attribute, value
        )
        self.done = True
