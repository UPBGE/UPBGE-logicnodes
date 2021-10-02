from bge import events
from uplogic.nodes import GEConditionNode


class GEMouseMoved(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.pulse = False

    def evaluate(self):
        self._set_ready()
        mstat = self.network.mouse_events
        if self.pulse:
            self._set_value(
                mstat[events.MOUSEX].active or
                mstat[events.MOUSEX].activated or
                mstat[events.MOUSEY].active or
                mstat[events.MOUSEY].activated
            )
        else:
            self._set_value(
                mstat[events.MOUSEX].activated or
                mstat[events.MOUSEY].activated
            )
