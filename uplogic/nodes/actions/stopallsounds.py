from uplogic.nodes import ULActionNode
from uplogic.data import GlobalDB
from uplogic.utils import not_met


class ULStopAllSounds(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None

    def evaluate(self):
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        aud_sys = GlobalDB.retrieve('.uplogic_audio').get('nl_audio_system')
        if not aud_sys:
            return
        self._set_ready()
        aud_sys.device.stopAll()
        self._set_value(True)
