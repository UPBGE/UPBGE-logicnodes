from bge import logic
from bge.types import KX_GameObject as GameObject
from mathutils import Vector, Euler, Matrix, Quaternion
from uplogic.data import GlobalDB
from uplogic.utils import LO_AXIS_TO_VECTOR
from uplogic.utils import LOGIC_OPERATORS
from uplogic.utils import STATUS_INVALID
from uplogic.utils import STATUS_READY
from uplogic.utils import STATUS_WAITING
from uplogic.utils import compute_distance
from uplogic.utils import debug
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met
from uplogic.utils import check_game_object
from uplogic.utils import make_unique_light
from uplogic.utils import _name_query
import bge
import bpy
import json
import math
import numbers
import operator
import os
import random
import sys


def alpha_move(a, b, fac):
    if a < b:
        return a + fac
    elif a > b:
        return a - fac
    else:
        return a


def xrot_to(
    rotating_object,
    target_pos,
    front_axis_code,
    speed,
    time_per_frame
):
    front_vector = LO_AXIS_TO_VECTOR[front_axis_code]
    vec = rotating_object.getVectTo(target_pos)[1]
    if speed == 0:
        if front_axis_code >= 3:
            vec.negate()
            front_axis_code = front_axis_code - 3
        if vec.x == vec.y == vec.z == 0:
            return
        rotating_object.alignAxisToVect(vec, front_axis_code, 1.0)
        rotating_object.alignAxisToVect(LO_AXIS_TO_VECTOR[0], 0, 1.0)
        return True
    else:
        vec = project_vector3(vec, 1, 2)
        vec.normalize()
        front_vector = rotating_object.getAxisVect(front_vector)
        front_vector = project_vector3(front_vector, 1, 2)
        signed_angle = vec.angle_signed(front_vector, None)
        if signed_angle is None:
            return
        abs_angle = abs(signed_angle)
        if abs_angle < 0.01:
            return True
        angle_sign = (signed_angle > 0) - (signed_angle < 0)
        drot = angle_sign * abs_angle * speed * time_per_frame
        eulers = rotating_object.localOrientation.to_euler()
        eulers[0] += drot
        rotating_object.localOrientation = eulers
        return False


def yrot_to(
    rotating_object,
    target_pos,
    front_axis_code,
    speed,
    time_per_frame
):
    front_vector = LO_AXIS_TO_VECTOR[front_axis_code]
    vec = rotating_object.getVectTo(target_pos)[1]
    if speed == 0:
        if front_axis_code >= 3:
            vec.negate()
            front_axis_code = front_axis_code - 3
        if vec.x == vec.y == vec.z == 0:
            return
        rotating_object.alignAxisToVect(vec, front_axis_code, 1.0)
        rotating_object.alignAxisToVect(LO_AXIS_TO_VECTOR[1], 1, 1.0)
        return True
    else:
        vec = project_vector3(vec, 2, 0)
        vec.normalize()
        front_vector = rotating_object.getAxisVect(front_vector)
        front_vector = project_vector3(front_vector, 2, 0)
        signed_angle = vec.angle_signed(front_vector, None)
        if signed_angle is None:
            return
        abs_angle = abs(signed_angle)
        if abs_angle < 0.01:
            return True
        angle_sign = (signed_angle > 0) - (signed_angle < 0)
        drot = angle_sign * abs_angle * speed * time_per_frame
        eulers = rotating_object.localOrientation.to_euler()
        eulers[1] += drot
        rotating_object.localOrientation = eulers
        return False


def zrot_to(
    rotating_object,
    target_pos,
    front_axis_code,
    speed,
    time_per_frame
):
    front_vector = LO_AXIS_TO_VECTOR[front_axis_code]
    vec = rotating_object.getVectTo(target_pos)[1]
    if speed == 0:
        if front_axis_code >= 3:
            vec.negate()
            front_axis_code = front_axis_code - 3
        if vec.x == vec.y == vec.z == 0:
            return
        rotating_object.alignAxisToVect(vec, front_axis_code, 1.0)
        rotating_object.alignAxisToVect(LO_AXIS_TO_VECTOR[2], 2, 1.0)
        return True
    else:
        # project in 2d, compute angle diff, set euler rot 2
        vec = project_vector3(vec, 0, 1)
        vec.normalize()
        front_vector = rotating_object.getAxisVect(front_vector)
        front_vector = project_vector3(front_vector, 0, 1)
        signed_angle = vec.angle_signed(front_vector, None)
        if signed_angle is None:
            return True
        abs_angle = abs(signed_angle)
        if abs_angle < 0.01:
            return True
        angle_sign = (signed_angle > 0) - (signed_angle < 0)
        drot = angle_sign * abs_angle * speed * time_per_frame
        eulers = rotating_object.localOrientation.to_euler()
        eulers[2] += drot
        rotating_object.localOrientation = eulers
        return False


def rot_to(
    rot_axis_index,
    rotating_object,
    target_pos,
    front_axis_code,
    speed,
    time_per_frame
):
    if rot_axis_index == 0:
        return xrot_to(
            rotating_object,
            target_pos,
            front_axis_code,
            speed,
            time_per_frame
        )
    elif rot_axis_index == 1:
        return yrot_to(
            rotating_object,
            target_pos,
            front_axis_code,
            speed,
            time_per_frame
        )
    elif rot_axis_index == 2:
        return zrot_to(
            rotating_object,
            target_pos,
            front_axis_code,
            speed,
            time_per_frame
        )


def move_to(
    moving_object,
    destination_point,
    speed,
    time_per_frame,
    dynamic,
    distance
):
    if dynamic:
        direction = (
            destination_point -
            moving_object.worldPosition)
        dst = direction.length
        if(dst <= distance):
            return True
        direction.z = 0
        direction.normalize()
        velocity = direction * speed
        velocity.z = moving_object.worldLinearVelocity.z
        moving_object.worldLinearVelocity = velocity
        return False
    else:
        direction = (
            destination_point -
            moving_object.worldPosition
            )
        dst = direction.length
        if(dst <= distance):
            return True
        direction.normalize()
        displacement = speed * time_per_frame
        motion = direction * displacement
        moving_object.worldPosition += motion
        return False


def project_vector3(v, xi, yi):
    return Vector((v[xi], v[yi]))


_loaded_userlogic_files = {}


def load_user_logic(module_name):
    full_path = logic.expandPath(
        "//bgelogic/cells/{}.py".format(module_name)
    )
    loaded_value = _loaded_userlogic_files.get(full_path)
    if loaded_value:
        return loaded_value
    import sys
    python_version = sys.version_info
    major = python_version[0]
    minor = python_version[1]
    if (major < 3) or (major == 3 and minor < 3):
        import imp
        loaded_value = imp.load_source(module_name, full_path)
    elif (major == 3) and (minor < 5):
        from importlib.machinery import SourceFileLoader
        loaded_value = SourceFileLoader(module_name, full_path).load_module()
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        loaded_value = module
    _loaded_userlogic_files[module_name] = loaded_value
    return loaded_value


class ULLogicBase(object):
    def get_value(self): pass
    def has_status(self, status): pass


class ULLogicContainer(ULLogicBase):

    def __init__(self):
        self._uid = None
        self._status = STATUS_WAITING
        self._value = None
        self._children = []
        self.network = None
        self.is_waiting = False

    def get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value

    def setup(self, network):
        """
        This is called by the network once, after all the
        cells have been loaded into the tree.
        :return: None
        """
        pass

    def stop(self, network):
        pass

    def _set_ready(self):
        self._status = STATUS_READY

    def _set_status(self, status):
        """
        Check the current status of the cell. Should return
        True if status equals the current status of the cell.
        :param status:
        :return:
        """
        self._status = status

    def has_status(self, status):
        return status == self._status

    def get_game_object(self, param, scene):
        if str(param) == 'NLO:U_O':
            return self.network._owner
        else:
            return check_game_object(param.split(':')[-1], scene)

    def get_socket_value(self, param, scene=None):
        if str(param).startswith('NLO:'):
            return self.get_game_object(param, scene)
        if isinstance(param, ULLogicBase):
            if param.has_status(STATUS_READY):
                return param.get_value()
            else:
                return STATUS_WAITING
        else:
            return param

    def reset(self):
        """
        Resets the status of the cell to ULLogicContainer.STATUS_WAITING.
        A cell may override this to reset other states
        or to keep the value at STATUS_READY if evaluation is required
        to happen only once (or never at all)
        :return:
        """
        self._set_status(STATUS_WAITING)

    def evaluate(self):
        """
        A logic cell implements this method to do its job. The network
        evaluates a cell until its status becomes
         LogicNetwor.STATUS_READY. When that happens, the cell is
         removed from the update queue.
        :return:
        """
        raise NotImplementedError(
            "{} doesn't implement evaluate".format(self.__class__.__name__)
        )

    def _always_ready(self, status):
        return status is STATUS_READY

    def _skip_evaluate(self):
        return

    def deactivate(self):
        self.has_status = self._always_ready
        self.evaluate = self._skip_evaluate


###############################################################################
# Socket
###############################################################################


class ULOutSocket(ULLogicBase):

    def __init__(self, node, value_getter):
        self.node = node
        self.get_value = value_getter

    def has_status(self, status):
        return self.node.has_status(status)


###############################################################################
# Basic Cells
###############################################################################


class ULLogicNode(ULLogicContainer):
    pass


class ULParameterNode(ULLogicNode):
    pass


class ULActionNode(ULLogicNode):
    pass


class ULConditionNode(ULLogicNode):
    pass


###############################################################################
# Events
###############################################################################
###############################################################################
# Game
###############################################################################
###############################################################################
# Input -> Mouse
###############################################################################
###############################################################################
# Input -> Gamepad
###############################################################################
###############################################################################
# Input -> Keyboard
###############################################################################
###############################################################################
# Unordered
###############################################################################


# Condition cells
class ConditionAlways(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.repeat = False
        self._set_status(STATUS_READY)
        self._value = True

    def reset(self):
        if not self.repeat:
            self._value = False

    def evaluate(self):
        pass


class ObjectPropertyOperator(ULConditionNode):
    def __init__(self, operator='EQUAL'):
        ULActionNode.__init__(self)
        self.game_object = None
        self.property_name = None
        self.operator = operator
        self.compare_value = None
        self.val = 0
        self.VAL = ULOutSocket(self, self.get_val)

    def get_val(self):
        return self.val

    def evaluate(self):
        game_object = self.get_socket_value(self.game_object)
        property_name = self.get_socket_value(self.property_name)
        compare_value = self.get_socket_value(self.compare_value)
        operator = self.get_socket_value(self.operator)
        if is_waiting(property_name, compare_value):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        value = self.val = game_object[property_name]
        if operator > 1:  # eq and neq are valid for None
            if is_invalid(value, compare_value):
                return
        if operator is None:
            return
        self._set_value(LOGIC_OPERATORS[operator](value, compare_value))


class ConditionNot(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.condition = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if is_waiting(condition):
            return
        self._set_ready()
        self._set_value(not condition)


class ConditionLNStatus(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.game_object = None
        self.tree_name = None
        self._running = False
        self._stopped = False
        self.IFRUNNING = ULOutSocket(self, self.get_running)
        self.IFSTOPPED = ULOutSocket(self, self.get_stopped)

    def get_running(self):
        return self._running

    def get_stopped(self):
        return self._stopped

    def evaluate(self):
        game_object = self.get_socket_value(self.game_object)
        tree_name = self.get_socket_value(self.tree_name)
        if is_waiting(game_object, tree_name):
            return
        self._set_ready()
        self._running = False
        self._stopped = False
        if is_invalid(game_object):
            return
        tree = game_object.get(f'IGNLTree_{tree_name}')
        if tree is None:
            return
        self._running = tree.is_running()
        self._stopped = tree.is_stopped()


class ConditionLogicOp(ULConditionNode):
    def __init__(self, operator='GREATER'):
        ULConditionNode.__init__(self)
        self.operator = operator
        self.param_a = None
        self.param_b = None
        self.threshold = None

    def evaluate(self):
        a = self.get_socket_value(self.param_a)
        b = self.get_socket_value(self.param_b)
        threshold = self.get_socket_value(self.threshold)
        operator = self.get_socket_value(self.operator)
        if is_waiting(a, b, threshold):
            return
        self._set_ready()
        if operator > 1:  # eq and neq are valid for None
            if a is None:
                return
            if b is None:
                return
        if threshold is None:
            threshold = 0
        if threshold > 0 and abs(a - b) < threshold:
            a = b
        if operator is None:
            return
        self._set_value(LOGIC_OPERATORS[operator](a, b))


class ConditionCompareVecs(ULConditionNode):
    def __init__(self, operator='GREATER'):
        ULConditionNode.__init__(self)
        self.operator = operator
        self.all = None
        self.threshold = None
        self.param_a = None
        self.param_b = None

    def get_vec_val(self, op, a, b, xyz, threshold):
        for ax in ['x', 'y', 'z']:
            av = getattr(a, ax)
            bv = getattr(b, ax)
            av = bv if abs(av - bv) < threshold else av
            if xyz[ax] and not LOGIC_OPERATORS[op](av, bv):
                return False
        return True

    def evaluate(self):
        a = self.get_socket_value(self.param_a)
        b = self.get_socket_value(self.param_b)
        all_values = self.get_socket_value(self.all)
        operator = self.get_socket_value(self.operator)
        threshold = self.get_socket_value(self.threshold)
        if is_waiting(a, b, all_values, operator, threshold):
            return
        if (
            not isinstance(a, Vector)
            or not isinstance(b, Vector)
        ):
            return
        self._set_ready()
        if operator > 1:  # eq and neq are valid for None
            if a is None:
                return
            if b is None:
                return
        if operator is None:
            return
        self._set_value(
            self.get_vec_val(
                operator,
                a,
                b,
                all_values,
                threshold
            )
        )


class ConditionDistanceCheck(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.param_a = None
        self.param_b = None
        self.operator = None
        self.dist = None
        self.hyst = None
        self._check = self._strict_check

    def _strict_check(self, opindex, value, hyst, threshold):
        v = LOGIC_OPERATORS[opindex](value, threshold)
        if v is True:
            self._set_value(True)
        else:
            self._set_value(False)
            self._check = self._hyst_check

    def _hyst_check(self, opindex, value, hyst, threshold):
        if (opindex == 2) or (opindex == 4):
            v = LOGIC_OPERATORS[opindex](value, threshold + hyst)
            if v is True:
                self._set_value(True)
                self._check = self._strict_check
            else:
                self._set_value(False)
        elif (opindex == 3) or (opindex == 5):
            v = LOGIC_OPERATORS[opindex](value, threshold - hyst)
            if v is True:
                self._set_value(True)
                self._check = self._strict_check
            else:
                self._set_value(False)

    def evaluate(self):
        a = self.get_socket_value(self.param_a)
        b = self.get_socket_value(self.param_b)
        op = self.get_socket_value(self.operator)
        dist = self.get_socket_value(self.dist)
        hyst = self.get_socket_value(self.hyst)
        if is_waiting(a, b, op, dist, hyst):
            return
        self._set_ready()
        if is_invalid(a):
            return
        if is_invalid(b):
            return
        if op is None:
            return
        if dist is None:
            return
        distance = compute_distance(a, b)
        if distance is None:
            return self._set_value(False)
        if hyst is None:  # plain check, no threshold
            v = LOGIC_OPERATORS[op](distance, dist)
            self._set_value(v)
        else:  # check with hysteresys value, if >, >=, <, <=
            self._check(op, distance, hyst, dist)


class ConditionAnd(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.condition_a = None
        self.condition_b = None

    def evaluate(self):
        ca = self.get_socket_value(self.condition_a)
        cb = self.get_socket_value(self.condition_b)
        self._set_ready()
        if is_waiting(ca, cb):
            self._set_value(False)
            return
        self._set_value(ca and cb)
    pass


class ConditionAndNot(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.condition_a = None
        self.condition_b = None

    def evaluate(self):
        ca = self.get_socket_value(self.condition_a)
        cb = not self.get_socket_value(self.condition_b)
        self._set_ready()
        if is_waiting(ca, cb):
            self._set_value(False)
            return
        self._set_value(ca and cb)
    pass


class ConditionNotNone(ULConditionNode):

    def __init__(self):
        ULConditionNode.__init__(self)
        self.checked_value = None

    def evaluate(self):
        value = self.get_socket_value(self.checked_value)
        self._set_ready()
        self._set_value(value is not None)


class ConditionNone(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.checked_value = None

    def evaluate(self):
        self._set_ready()
        value = self.get_socket_value(self.checked_value)
        self._set_value(value is None)


class ConditionValueValid(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.checked_value = None

    def evaluate(self):
        self._set_ready()
        value = self.get_socket_value(self.checked_value)
        self._set_value(not is_invalid(value))


class ConditionOr(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.condition_a = True
        self.condition_b = True

    def evaluate(self):
        ca = self.get_socket_value(self.condition_a)
        cb = self.get_socket_value(self.condition_b)
        if is_waiting(ca):
            ca = False
        if is_waiting(cb):
            cb = False
        self._set_ready()
        self._set_value(ca or cb)


class ConditionOrList(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.ca = False
        self.cb = False
        self.cc = False
        self.cd = False
        self.ce = False
        self.cf = False

    def evaluate(self):
        ca = self.get_socket_value(self.ca)
        cb = self.get_socket_value(self.cb)
        cc = self.get_socket_value(self.cc)
        cd = self.get_socket_value(self.cd)
        ce = self.get_socket_value(self.ce)
        cf = self.get_socket_value(self.cf)
        if is_waiting(ca, cb, cc, cd, ce, cf):
            self._set_ready()
            self._set_value(False)
        self._set_ready()
        self._set_value(ca or cb or cc or cd or ce or cf)


class ConditionAndList(ULConditionNode):

    def __init__(self):
        ULConditionNode.__init__(self)
        self.ca = True
        self.cb = True
        self.cc = True
        self.cd = True
        self.ce = True
        self.cf = True

    def evaluate(self):
        ca = self.get_socket_value(self.ca)
        cb = self.get_socket_value(self.cb)
        cc = self.get_socket_value(self.cc)
        cd = self.get_socket_value(self.cd)
        ce = self.get_socket_value(self.ce)
        cf = self.get_socket_value(self.cf)
        self._set_ready()
        if is_waiting(ca, cb, cc, cd, ce, cf):
            self._set_value(False)
            return
        self._set_value(ca and cb and cc and cd and ce and cf)


class ActionKeyLogger(ULActionNode):
    def __init__(self, pulse=False):
        ULActionNode.__init__(self)
        self.condition = None
        self.pulse = pulse
        self._key_logged = None
        self._key_code = None
        self._character = None
        self.KEY_LOGGED = ULOutSocket(self, self.get_key_logged)
        self.KEY_CODE = ULOutSocket(self, self.get_key_code)
        self.CHARACTER = ULOutSocket(self, self.get_character)

    def get_key_logged(self):
        return self._key_logged

    def get_key_code(self):
        return self._key_code

    def get_character(self):
        return self._character

    def reset(self):
        ULLogicContainer.reset(self)
        self._key_logged = False
        self._key_code = None
        self._character = None

    def evaluate(self):
        self._set_ready()
        condition = self.get_socket_value(self.condition)
        if not condition:
            return
        network = self.network
        keyboard_status = network.keyboard_events
        left_shift_status = keyboard_status[bge.events.LEFTSHIFTKEY].active
        right_shift_status = keyboard_status[bge.events.RIGHTSHIFTKEY].active
        shift_down = (
            left_shift_status or
            right_shift_status or
            network.capslock_pressed
        )
        active_events = network.active_keyboard_events
        active = (
            'active' if self.pulse
            else 'activated'
        )
        for keycode in active_events:
            event = active_events[keycode]
            if getattr(event, active):
                # something has been pressed
                self._character = bge.events.EventToCharacter(
                    event.type,
                    shift_down
                )
                self._key_code = keycode
                self._key_logged = True


class ConditionTimeElapsed(ULConditionNode):

    def __init__(self):
        ULConditionNode.__init__(self)
        self.condition = None
        self.delta_time = None
        self._trigger = 0
        self.network = None

    def setup(self, network):
        self.network = network

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        delta_time = self.get_socket_value(self.delta_time)
        if is_waiting(delta_time):
            return
        self._set_ready()
        now = self.network.timeline

        if not not_met(condition):
            self._trigger = now + delta_time

        if now >= self._trigger:
            self._set_value(True)
        else:
            self._set_value(False)


class ConditionKeyReleased(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.pulse = False
        self.key_code = None
        self.network = None

    def setup(self, network):
        self.network = network

    def evaluate(self):
        keycode = self.get_socket_value(self.key_code)
        if is_waiting(keycode):
            return
        self._set_ready()
        keystat = self.network.keyboard_events[keycode]
        if self.pulse:
            self._set_value(
                keystat.released or
                keystat.inactive
            )
        else:
            self._set_value(keystat.released)
    pass


class ConditionMouseLeft(ULConditionNode):
    def __init__(self, repeat=None):
        ULConditionNode.__init__(self)
        self.network = None
        self.repeat = repeat
        self._consumed = False

    def setup(self, network):
        self.network = network

    def reset(self):
        if self._consumed:
            self._set_value(False)
            self._set_status(STATUS_READY)
        else:
            ULConditionNode.reset(self)

    def evaluate(self):
        repeat = self.get_socket_value(self.repeat)
        if is_waiting(repeat):
            return
        self._set_ready()
        dx = self.network.mouse_motion_delta[0]
        self._set_value(dx > 0)
        if not self.repeat:
            self._consumed = True


class ConditionMouseRight(ULConditionNode):
    def __init__(self, repeat=None):
        ULConditionNode.__init__(self)
        self.network = None
        self.repeat = repeat
        self._consumed = False

    def setup(self, network):
        self.network = network

    def reset(self):
        if self._consumed:
            self._set_value(False)
            self._set_status(STATUS_READY)
        else:
            ULConditionNode.reset(self)

    def evaluate(self):
        repeat = self.get_socket_value(self.repeat)
        if is_waiting(repeat):
            return
        self._set_ready()
        dx = self.network.mouse_motion_delta[0]
        self._set_value(dx < 0)
        if not self.repeat:
            self._consumed = True


class ActionRepeater(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.input_value = None
        self.output_cells = []
        self.output_value = None

    def setup(self, network):
        super(ULActionNode, self).setup(network)
        for cell in self.output_cells:
            cell.setup(network)

    def evaluate(self):
        self._set_ready()
        condition = self.get_socket_value(self.condition)
        if not condition:
            return
        input_value = self.get_socket_value(self.input_value)
        if isinstance(input_value, numbers.Number):
            for e in range(0, input_value):
                self._set_value(e)
                for cell in self.output_cells:
                    cell.evaluate()
        else:
            for e in input_value:
                self._set_value(e)
                for cell in self.output_cells:
                    cell.evaluate()
                pass
            pass
        for cell in self.output_cells:
            cell.reset()
            pass
        pass
    pass


class ConditionCollision(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.game_object = None
        self.use_mat = None
        self.prop = None
        self.material = None
        self._set_value("False")
        self.pulse = False
        self._target = None
        self._point = None
        self._normal = None
        self._collision_triggered = False
        self._consumed = False
        self._last_monitored_object = None
        self._objects = []
        self.TARGET = ULOutSocket(self, self.get_target)
        self.POINT = ULOutSocket(self, self.get_point)
        self.NORMAL = ULOutSocket(self, self.get_normal)
        self.OBJECTS = ULOutSocket(self, self.get_objects)

    def get_point(self):
        return self._point

    def get_normal(self):
        return self._normal

    def get_target(self):
        return self._target

    def get_objects(self):
        return self._objects

    def _collision_callback(self, obj, point, normal):
        self._objects.append(obj)
        use_mat = self.get_socket_value(self.use_mat)
        if use_mat:
            material = self.get_socket_value(self.material)
            if material:
                for obj in self._objects:
                    bo = obj.blenderObject
                    if material not in [
                        slot.material.name for
                        slot in
                        bo.material_slots
                    ]:
                        self._objects.remove(obj)
                    else:
                        self._collision_triggered = True
                        self._target = obj
                        self._point = point
                        self._normal = normal
                        return
                self._collision_triggered = False
                return
        else:
            prop = self.get_socket_value(self.prop)
            if prop:
                for obj in self._objects:
                    if prop not in obj:
                        self._objects.remove(obj)
                    else:
                        self._collision_triggered = True
                        self._target = obj
                        self._point = point
                        self._normal = normal
                        return
                self._collision_triggered = False
                return
        self._collision_triggered = True
        self._target = obj
        self._point = point
        self._normal = normal

    def reset(self):
        ULLogicContainer.reset(self)
        self._collision_triggered = False
        self._objects = []

    def _reset_last_monitored_object(self, new_monitored_object):
        if is_invalid(new_monitored_object):
            new_monitored_object = None
        if self._last_monitored_object == new_monitored_object:
            return
        if not isinstance(new_monitored_object, bge.types.KX_GameObject):
            if self._last_monitored_object is not None:
                self._last_monitored_object.collisionCallbacks.remove(
                    self._collision_callback
                )
                self._last_monitored_object = None
        else:
            if self._last_monitored_object is not None:
                self._last_monitored_object.collisionCallbacks.remove(
                    self._collision_callback
                )
            if new_monitored_object is not None:
                new_monitored_object.collisionCallbacks.append(
                    self._collision_callback
                )
                self._last_monitored_object = new_monitored_object
        self._set_value(False)
        self._target = None
        self._point = None
        self._normal = None
        self._collision_triggered = False

    def evaluate(self):
        last_target = self._target
        game_object = self.get_socket_value(self.game_object)
        self._reset_last_monitored_object(game_object)
        if is_waiting(game_object):
            return
        self._set_ready()
        collision = self._collision_triggered
        if last_target is not self._target:
            self._consumed = False
        if collision and not self.pulse:
            self._set_value(collision and not self._consumed)
            self._consumed = True
        elif self.pulse:
            self._set_value(collision)
        else:
            self._consumed = False
            self._set_value(False)


# Action Cells


class ActionAddObject(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.name = None
        self.reference = None
        self.life = None
        self.done = False
        self.obj = False
        self.OBJ = ULOutSocket(self, self._get_obj)
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def _get_obj(self):
        return self.obj

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        life = self.get_socket_value(self.life)
        name = self.get_socket_value(self.name)
        self._set_ready()
        reference = self.get_socket_value(self.reference)
        scene = logic.getCurrentScene()
        if is_waiting(life, name, reference):
            return
        self.obj = scene.addObject(name, reference, life)
        self.done = True


class ActionSetGameObjectGameProperty(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.property_value = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        property_name = self.get_socket_value(self.property_name)
        property_value = self.get_socket_value(self.property_value)
        if is_waiting(property_name, property_value):
            return
        if is_invalid(game_object):
            return
        if condition:
            self.done = True
            self._set_ready()
            game_object[property_name] = property_value


class SetMaterial(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.slot = None
        self.mat_name = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        game_object = self.get_socket_value(self.game_object)
        slot = self.get_socket_value(self.slot) - 1
        mat_name = self.get_socket_value(self.mat_name)
        if not_met(condition):
            return
        if is_invalid(game_object):
            return
        if is_waiting(mat_name, slot):
            return
        self._set_ready()
        bl_obj = game_object.blenderObject
        if slot > len(bl_obj.material_slots) - 1:
            debug('Set Material: Slot does not exist!')
            return
        bl_obj.material_slots[slot].material = bpy.data.materials[mat_name]
        self.done = True


class ActionSetNodeTreeNodeValue(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.tree_name = None
        self.node_name = None
        self.input_slot = None
        self.value = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        tree_name = self.get_socket_value(self.tree_name)
        node_name = self.get_socket_value(self.node_name)
        input_slot = self.get_socket_value(self.input_slot)
        value = self.get_socket_value(self.value)
        if is_waiting(node_name, input_slot, value):
            return
        if is_invalid(tree_name):
            return
        if condition:
            self.done = True
            self._set_ready()
            (
                bpy.data.node_groups[tree_name]
                .nodes[node_name]
                .inputs[input_slot]
                .default_value
            ) = value


class ActionSetNodeTreeNodeAttribute(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.tree_name = None
        self.node_name = None
        self.internal = None
        self.attribute = None
        self.value = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        tree_name = self.get_socket_value(self.tree_name)
        node_name = self.get_socket_value(self.node_name)
        attribute = self.get_socket_value(self.attribute)
        internal = self.get_socket_value(self.internal)
        value = self.get_socket_value(self.value)
        if is_waiting(node_name, attribute, internal, value):
            return
        if is_invalid(tree_name):
            return
        if condition:
            self._set_ready()
            target = (
                bpy
                .data
                .node_groups[tree_name]
                .nodes[node_name]
            )
            if internal:
                target = getattr(target, internal, target)
            if hasattr(target, attribute):
                setattr(target, attribute, value)
            self.done = True


class ActionSetMaterialNodeValue(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.mat_name = None
        self.node_name = None
        self.input_slot = None
        self.value = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        mat_name = self.get_socket_value(self.mat_name)
        node_name = self.get_socket_value(self.node_name)
        input_slot = self.get_socket_value(self.input_slot)
        value = self.get_socket_value(self.value)
        if is_waiting(node_name, input_slot, value):
            return
        if is_invalid(mat_name):
            return
        if condition:
            self.done = True
            self._set_ready()
            (
                bpy.data.materials[mat_name]
                .node_tree
                .nodes[node_name]
                .inputs[input_slot]
                .default_value
            ) = value


class ActionSetMaterialNodeAttribute(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.mat_name = None
        self.node_name = None
        self.internal = None
        self.attribute = None
        self.value = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        mat_name = self.get_socket_value(self.mat_name)
        node_name = self.get_socket_value(self.node_name)
        attribute = self.get_socket_value(self.attribute)
        internal = self.get_socket_value(self.internal)
        value = self.get_socket_value(self.value)
        if is_waiting(node_name, attribute, internal, value):
            return
        if is_invalid(mat_name):
            return
        if condition:
            self._set_ready()
            target = (
                bpy.data.materials[mat_name]
                .node_tree
                .nodes[node_name]
            )
            if internal:
                target = getattr(target, internal, target)
            if hasattr(target, attribute):
                setattr(target, attribute, value)
            self.done = True


class ActionPlayMaterialSequence(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.mat_name = None
        self.node_name = None
        self.play_mode = None
        self.play_continue = None
        self.frames = None
        self.fps = None
        self.reverse = False
        self.time = 0.0
        self.on_start = False
        self.running = False
        self.on_finish = False
        self.frame = 0
        self._consumed = False
        self.ON_START = ULOutSocket(self, self._get_on_start)
        self.RUNNING = ULOutSocket(self, self._get_running)
        self.ON_FINISH = ULOutSocket(self, self._get_on_finish)
        self.FRAME = ULOutSocket(self, self._get_frame)

    def _get_on_start(self):
        return self.on_start

    def _get_running(self):
        return self.running

    def _get_on_finish(self):
        return self.on_finish

    def _get_frame(self):
        return self.frame

    def evaluate(self):
        self.done = False
        self.on_finish = False
        self.on_start = False
        running = self.running
        condition = self.get_socket_value(self.condition)
        play_continue = self.get_socket_value(self.play_continue)
        if not_met(condition) and not running:
            return
        self.time += self.network.time_per_frame
        mat_name = self.get_socket_value(self.mat_name)
        node_name = self.get_socket_value(self.node_name)
        play_mode = self.get_socket_value(self.play_mode)
        frames = self.get_socket_value(self.frames)
        fps = self.get_socket_value(self.fps)
        if is_waiting(
            mat_name,
            node_name,
            play_mode,
            frames,
            fps
        ):
            return
        rate = 1/fps
        speed = self.time / rate
        self._set_ready()
        if speed < 1:
            return
        self.time -= rate * speed
        player = (
            bpy.data.materials[mat_name]
            .node_tree
            .nodes[node_name]
        ).image_user
        start_frame = frames.y if self.reverse else frames.x
        end_frame = frames.x if self.reverse else frames.y
        inverted = (start_frame > end_frame)
        frame = self.frame = player.frame_offset
        reset_cond = (frame <= end_frame) if inverted else (frame >= end_frame)
        if not running:
            if not play_continue and play_mode > 2 or reset_cond:
                player.frame_offset = start_frame if inverted else end_frame
            if not play_continue:
                self.reverse = False
            self.on_start = True
            self._consumed = False
        stops = [3, 4, 5]

        start_cond = (frame > start_frame) if inverted else (frame < start_frame)

        if not condition and play_mode in stops:
            self.on_finish = True
            self.running = False
            return
        if start_cond:
            self.running = True
            player.frame_offset = start_frame
        frame = player.frame_offset
        run_cond = (frame > end_frame) if inverted else (frame < end_frame)
        if run_cond:
            self.running = True
            s = round(speed)
            if inverted:
                if frame - s < end_frame:
                    if play_mode in [1, 4]:
                        leftover = abs(frame - s - end_frame)
                        span = start_frame - end_frame
                        while leftover > span:
                            leftover -= span
                        player.frame_offset = start_frame - leftover
                    else:
                        player.frame_offset = end_frame
                else:
                    player.frame_offset -= s
            else:
                if frame + s > end_frame:
                    if play_mode in [1, 4]:
                        leftover = frame + s - end_frame
                        span = end_frame - start_frame
                        while leftover > span:
                            leftover -= span
                        player.frame_offset = start_frame + leftover
                    else:
                        player.frame_offset = end_frame
                else:
                    player.frame_offset += s
        elif play_mode == 1 and condition:
            player.frame_offset = start_frame
        elif play_mode == 4:
            player.frame_offset = start_frame
        elif play_mode == 3:
            if running and not self._consumed:
                self.on_finish = True
                self._consumed = True
        elif play_mode == 0 or play_mode == 3:
            if running and not self._consumed:
                self.on_finish = True
                self._consumed = True
            if not condition:
                self.running = False
        elif play_mode == 2 or play_mode == 5:
            if running and not condition:
                self.on_finish = True
            if not condition:
                self.running = False
            self.reverse = not self.reverse
        else:
            if running:
                self.on_finish = True
            self.running = False
        self.done = True


class ActionToggleGameObjectGameProperty(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        property_name = self.get_socket_value(self.property_name)
        if is_waiting(property_name):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        if condition:
            value = game_object[property_name]
            game_object[property_name] = not value
        self.done = True


class ActionAddToGameObjectGameProperty(ULActionNode):

    @classmethod
    def op_by_code(cls, str):
        import operator
        opmap = {
            "ADD": operator.add,
            "SUB": operator.sub,
            "DIV": operator.truediv,
            "MUL": operator.mul
        }
        return opmap.get(str)

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.property_value = None
        self.operator = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        property_name = self.get_socket_value(self.property_name)
        property_value = self.get_socket_value(self.property_value)
        if is_waiting(property_name, property_value):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        value = game_object[property_name]
        game_object[property_name] = (
            self.operator(value, property_value)
        )
        self.done = True


class CopyPropertyFromObject(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.from_object = None
        self.to_object = None
        self.property_name = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        from_object = self.get_socket_value(self.from_object)
        to_object = self.get_socket_value(self.to_object)
        if is_invalid(from_object, to_object):
            return
        property_name = self.get_socket_value(self.property_name)
        if is_waiting(property_name):
            return
        self._set_ready()
        val = from_object.get(property_name)
        if val is not None:
            to_object[property_name] = val
        self.done = True


class ActionClampedAddToGameObjectGameProperty(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.property_value = None
        self.range = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        game_object = self.get_socket_value(self.game_object)
        if not_met(condition):
            return
        if is_invalid(game_object):
            return
        property_name = self.get_socket_value(self.property_name)
        property_value = self.get_socket_value(self.property_value)
        val_range = self.get_socket_value(self.range)
        if is_waiting(property_name, property_value):
            return
        self._set_ready()
        value = game_object[property_name]
        new_val = value + property_value
        if new_val > val_range.y:
            new_val = val_range.y
        if new_val < val_range.x:
            new_val = val_range.x
        game_object[property_name] = (
            new_val
        )
        self.done = True


class ValueSwitch(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.conditon = None
        self.val_a = None
        self.val_b = None
        self.out_value = False
        self.VAL = ULOutSocket(self, self._get_out_value)

    def _get_out_value(self):
        return self.out_value

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        val_a = self.get_socket_value(self.val_a)
        val_b = self.get_socket_value(self.val_b)
        self._set_ready()
        self.out_value = (
            val_a if condition is True else val_b
        )


class InvertBool(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.value = None
        self.out_value = False
        self.OUT = ULOutSocket(self, self._get_out_value)

    def _get_out_value(self):
        return self.out_value

    def evaluate(self):
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            self.out_value = False
            return
        self._set_ready()
        self.out_value = not value


class InvertValue(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.value = None
        self.out_value = False
        self.OUT = ULOutSocket(self, self._get_out_value)

    def _get_out_value(self):
        return self.out_value

    def evaluate(self):
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            self.out_value = 0
            return
        self._set_ready()
        self.out_value = -value


class AbsoluteValue(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.value = None
        self.out_value = False
        self.OUT = ULOutSocket(self, self._get_out_value)

    def _get_out_value(self):
        return self.out_value

    def evaluate(self):
        if is_invalid(self.value):
            return
        value = self.get_socket_value(self.value)
        self._set_ready()
        self.out_value = math.fabs(value)


class ActionPrint(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        self._set_ready()
        print(value)
        self.done = True


class ActionCreateVehicle(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.wheels_steering = None
        self.wheels = None
        self.suspension = None
        self.stiffness = None
        self.damping = None
        self.friction = None
        self.done = None
        self.vehicle = None
        self.wheels = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.VEHICLE = ULOutSocket(self, self.get_vehicle)
        self.WHEELS = ULOutSocket(self, self.get_wheels)

    def get_done(self):
        return self.done

    def get_vehicle(self):
        return self.vehicle

    def get_wheels(self):
        return self.wheels

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        wheels_steering = self.get_socket_value(self.wheels_steering)
        wheels = self.get_socket_value(self.wheels)
        suspension = self.get_socket_value(self.suspension)
        stiffness = self.get_socket_value(self.stiffness)
        damping = self.get_socket_value(self.damping)
        friction = self.get_socket_value(self.friction)
        if is_waiting(
            game_object,
            wheels_steering,
            wheels,
            suspension,
            stiffness,
            damping,
            friction
        ):
            return
        self._set_ready()
        orig_ori = game_object.worldOrientation
        game_object.worldOrientation = Euler((0, 0, 0), 'XYZ')
        ph_id = game_object.getPhysicsId()
        car = bge.constraints.createVehicle(ph_id)
        down = Vector((0, 0, -1))
        axle_dir = Vector((0, -1, 0))
        wheels_steering = bpy.data.collections[wheels_steering]
        wheels = bpy.data.collections[wheels]
        for wheel in wheels_steering.objects:
            wheel = check_game_object(wheel.name)
            car.addWheel(
                wheel,
                wheel.worldPosition - game_object.worldPosition,
                down,
                axle_dir,
                suspension,
                abs(wheel.worldScale.x/2),
                True
            )
        for wheel in wheels.objects:
            wheel = check_game_object(wheel.name)
            car.addWheel(
                wheel,
                wheel.worldPosition - game_object.worldPosition,
                down,
                axle_dir,
                suspension,
                abs(wheel.worldScale.x/2),
                False
            )
        for wheel in range(car.getNumWheels()):
            car.setSuspensionStiffness(stiffness, wheel)
            car.setSuspensionDamping(damping, wheel)
            car.setTyreFriction(friction, wheel)
        self.vehicle = car
        game_object.worldOrientation = orig_ori
        self.done = True


class ActionCreateVehicleFromParent(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.suspension = None
        self.stiffness = None
        self.damping = None
        self.friction = None
        self.wheel_size = None
        self.done = None
        self.vehicle = None
        self.wheels = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.VEHICLE = ULOutSocket(self, self.get_vehicle)
        self.WHEELS = ULOutSocket(self, self.get_wheels)

    def get_done(self):
        return self.done

    def get_vehicle(self):
        return self.vehicle

    def get_wheels(self):
        return self.wheels

    def evaluate(self):
        self.done = False
        game_object = self.get_socket_value(self.game_object)
        if not_met(self.get_socket_value(self.condition)):
            if game_object.get('_vconst'):
                self._set_ready()
                self.vehicle = game_object['_vconst']
            return
        suspension = self.get_socket_value(self.suspension)
        stiffness = self.get_socket_value(self.stiffness)
        damping = self.get_socket_value(self.damping)
        friction = self.get_socket_value(self.friction)
        wheel_size = self.get_socket_value(self.wheel_size)
        if is_waiting(
            game_object,
            suspension,
            stiffness,
            damping,
            friction,
            wheel_size
        ):
            return
        self._set_ready()
        orig_ori = game_object.localOrientation.copy()
        game_object.localOrientation = Euler((0, 0, 0), 'XYZ')
        ph_id = game_object.getPhysicsId()
        car = bge.constraints.createVehicle(ph_id)
        down = Vector((0, 0, -1))
        axle_dir = game_object.getAxisVect(Vector((0, -1, 0)))
        wheels = []
        cs = sorted(game_object.children, key=lambda c: c.name)
        for c in cs:
            if 'FWheel' in c.name:
                c.removeParent()
                car.addWheel(
                    c,
                    c.worldPosition - game_object.worldPosition,
                    down,
                    axle_dir,
                    suspension,
                    abs(c.worldScale.x/2) * wheel_size,
                    True
                )
                wheels.append(c)
            elif 'RWheel' in c.name:
                c.removeParent()
                car.addWheel(
                    c,
                    c.worldPosition - game_object.worldPosition,
                    down,
                    axle_dir,
                    suspension,
                    abs(c.worldScale.x/2) * wheel_size,
                    False
                )
                wheels.append(c)
        for wheel in range(car.getNumWheels()):
            car.setSuspensionStiffness(stiffness, wheel)
            car.setSuspensionDamping(damping, wheel)
            car.setTyreFriction(friction, wheel)
        game_object.localOrientation = orig_ori
        self.vehicle = game_object['_vconst'] = car
        self.wheels = wheels
        self.done = True


class VehicleApplyForce(ULActionNode):
    def __init__(self, value_type='REAR'):
        ULActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.vehicle = None
        self.wheelcount = None
        self._reset = False
        self.power = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        vehicle = self.get_socket_value(self.vehicle)
        if is_invalid(vehicle):
            return
        constraint = vehicle.get('_vconst', None)
        if not constraint:
            return
        if not_met(condition):
            if self._reset:
                for wheel in range(constraint.getNumWheels()):
                    constraint.applyEngineForce(0, wheel)
                self._reset = False
            return
        value = self.get_socket_value(self.value_type)
        wheelcount = self.get_socket_value(self.wheelcount)
        power = self.get_socket_value(self.power)
        if is_waiting(value, wheelcount, power):
            return
        self._reset = True
        self._set_ready()
        if value == 'FRONT':
            for wheel in range(wheelcount):
                constraint.applyEngineForce(power, wheel)
        if value == 'REAR':
            for wheel in range(wheelcount):
                wheel = constraint.getNumWheels() - wheel - 1
                constraint.applyEngineForce(power, wheel)
        if value == 'ALL':
            for wheel in range(constraint.getNumWheels()):
                constraint.applyEngineForce(power, wheel)
        self.done = True


class VehicleApplyBraking(ULActionNode):
    def __init__(self, value_type='REAR'):
        ULActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.vehicle = None
        self.wheelcount = None
        self._reset = False
        self.power = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        vehicle = self.get_socket_value(self.vehicle)
        if is_invalid(vehicle):
            return
        constraint = vehicle.get('_vconst', None)
        if not constraint:
            return
        if not_met(condition):
            if self._reset:
                for wheel in range(constraint.getNumWheels()):
                    constraint.applyBraking(0, wheel)
                self._reset = False
            return
        value_type = self.get_socket_value(self.value_type)
        wheelcount = self.get_socket_value(self.wheelcount)
        power = self.get_socket_value(self.power)
        if is_waiting(value_type, wheelcount, power):
            return
        self._reset = True
        self._set_ready()
        if value_type == 'FRONT':
            for wheel in range(wheelcount):
                constraint.applyBraking(power, wheel)
        if value_type == 'REAR':
            for wheel in range(wheelcount):
                wheel = constraint.getNumWheels() - wheel - 1
                constraint.applyBraking(power, wheel)
        if value_type == 'ALL':
            for wheel in range(constraint.getNumWheels()):
                constraint.applyBraking(power, wheel)
        self.done = True


class VehicleApplySteering(ULActionNode):
    def __init__(self, value_type='REAR'):
        ULActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.vehicle = None
        self.wheelcount = None
        self._reset = False
        self.power = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        vehicle = self.get_socket_value(self.vehicle)
        if is_invalid(vehicle):
            return
        constraint = vehicle.get('_vconst', None)
        if not constraint:
            return
        if not_met(condition):
            if self._reset:
                for wheel in range(constraint.getNumWheels()):
                    constraint.setSteeringValue(0, wheel)
                self._reset = False
            return
        value_type = self.get_socket_value(self.value_type)
        wheelcount = self.get_socket_value(self.wheelcount)
        power = self.get_socket_value(self.power)
        if is_waiting(value_type, wheelcount, power):
            return
        self._reset = True
        self._set_ready()
        if value_type == 'FRONT':
            for wheel in range(wheelcount):
                constraint.setSteeringValue(power, wheel)
        if value_type == 'REAR':
            for wheel in range(wheelcount):
                wheel = constraint.getNumWheels() - wheel - 1
                constraint.setSteeringValue(power, wheel)
        if value_type == 'ALL':
            for wheel in range(constraint.getNumWheels()):
                constraint.setSteeringValue(power, wheel)
        self.done = True


class VehicleSetAttributes(ULActionNode):
    def __init__(self, value_type='REAR'):
        ULActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.vehicle = None
        self.wheelcount = None
        self.set_suspension_compression = False
        self.suspension_compression = False
        self.set_suspension_stiffness = False
        self.suspension_stiffness = False
        self.set_suspension_damping = False
        self.suspension_damping = False
        self.set_tyre_friction = False
        self.tyre_friction = False
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def set_attributes(self, car, wheel, attrs, values):
        if attrs[0] is True:
            car.setSuspensionCompression(values[0], wheel)
        if attrs[1] is True:
            car.setSuspensionStiffness(values[1], wheel)
        if attrs[2] is True:
            car.setSuspensionDamping(values[2], wheel)
        if attrs[3] is True:
            car.setTyreFriction(values[3], wheel)

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        vehicle = self.get_socket_value(self.vehicle)
        value_type = self.get_socket_value(self.value_type)
        wheelcount = self.get_socket_value(self.wheelcount)
        if is_waiting(value_type, wheelcount):
            return
        if is_invalid(vehicle):
            return
        attrs_to_set = [
            self.get_socket_value(self.set_suspension_compression),
            self.get_socket_value(self.set_suspension_stiffness),
            self.get_socket_value(self.set_suspension_damping),
            self.get_socket_value(self.set_tyre_friction)
        ]
        values_to_set = [
            self.get_socket_value(self.suspension_compression),
            self.get_socket_value(self.suspension_stiffness),
            self.get_socket_value(self.suspension_damping),
            self.get_socket_value(self.tyre_friction)
        ]
        constraint = vehicle.get('_vconst', None)
        if not constraint:
            return
        self._set_ready()
        if value_type == 'FRONT':
            for wheel in range(wheelcount):
                self.set_attributes(
                    constraint,
                    wheel,
                    attrs_to_set,
                    values_to_set
                )
        if value_type == 'REAR':
            for wheel in range(wheelcount):
                wheel = constraint.getNumWheels() - wheel - 1
                self.set_attributes(
                    constraint,
                    wheel,
                    attrs_to_set,
                    values_to_set
                )
        if value_type == 'ALL':
            for wheel in range(constraint.getNumWheels()):
                self.set_attributes(
                    constraint,
                    wheel,
                    attrs_to_set,
                    values_to_set
                )
        self.done = True


class ActionSetObjectAttribute(ULActionNode):
    def __init__(self, value_type='worldPosition'):
        ULActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.xyz = None
        self.game_object = None
        self.attribute_value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        xyz = self.get_socket_value(self.xyz)
        game_object = self.get_socket_value(self.game_object)
        attribute = self.get_socket_value(self.value_type)
        value = self.get_socket_value(self.attribute_value)
        if is_waiting(xyz, game_object, attribute, value):
            return

        if hasattr(value, attribute):
            value = getattr(value, attribute).copy()
        self._set_ready()
        if not hasattr(game_object, attribute):
            debug(
                'Set Object Data Node: {} has no attribute {}!'
                .format(game_object, attribute)
            )
            return
        data = getattr(game_object, attribute)
        if 'Orientation' in attribute:
            data = data.to_euler()
        for axis in xyz:
            if not xyz[axis]:
                setattr(value, axis, getattr(data, axis))
        setattr(
            game_object,
            attribute,
            value
        )
        if value == 'worldScale':
            game_object.reinstancePhysicsMesh(
                game_object,
                game_object.meshes[0]
            )
        self.done = True


class ActionInstalSubNetwork(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.target_object = None
        self.tree_name = None
        self.initial_status = None
        self._network = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def setup(self, network):
        self._network = network

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        target_object = self.get_socket_value(self.target_object)
        tree_name = self.get_socket_value(self.tree_name)
        initial_status = self.get_socket_value(self.initial_status)
        if is_waiting(
            target_object,
            tree_name,
            initial_status
        ):
            return
        self._set_ready()
        if is_invalid(target_object):
            return
        self._network.install_subnetwork(
            target_object,
            tree_name,
            initial_status
        )
        self.done = True


class ActionExecuteNetwork(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.target_object = None
        self.tree_name = None
        self._network = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def setup(self, network):
        self._network = network

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        target_object = self.get_socket_value(self.target_object)
        tree_name = self.get_socket_value(self.tree_name)
        self._set_ready()
        if is_invalid(target_object):
            return
        added_network = target_object.get(f'IGNLTree_{tree_name}', None)
        if not added_network:
            self._network.install_subnetwork(
                target_object,
                tree_name,
                False
            )
            added_network = target_object.get(f'IGNLTree_{tree_name}', None)
        if condition:
            added_network.stopped = False
        else:
            added_network.stop()
            added_network.stopped = True
            return
        self.done = True


class ActionStartLogicNetwork(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.logic_network_name = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        logic_network_name = self.get_socket_value(self.logic_network_name)
        if is_waiting(game_object, logic_network_name):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        network = game_object.get(f'IGNLTree_{logic_network_name}')
        if network is not None:
            network.stopped = False
        self.done = True


class ActionStopLogicNetwork(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.logic_network_name = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        logic_network_name = self.get_socket_value(self.logic_network_name)
        if is_waiting(game_object, logic_network_name):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        network = game_object.get(f'IGNLTree_{logic_network_name}')
        network.stop()
        self.done = True


class ActionSendMessage(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.from_obj = None
        self.to_obj = None
        self.subject = None
        self.body = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            self._set_value(False)
            return
        from_obj = self.get_socket_value(self.from_obj)
        to_obj = self.get_socket_value(self.to_obj)
        subject = self.get_socket_value(self.subject)
        body = self.get_socket_value(self.body)
        if is_waiting(from_obj, to_obj, subject, body):
            return
        self._set_ready()
        if body and to_obj:
            from_obj.sendMessage(subject, body=body, to=to_obj)
        elif body:
            from_obj.sendMessage(subject, body=body)
        elif to_obj:
            from_obj.sendMessage(subject, to=to_obj)
        else:
            from_obj.sendMessage(subject)
        self._set_value(True)


class ActionSetGameObjectVisibility(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.visible: bool = None
        self.recursive: bool = None
        self.done: bool = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        visible: bool = self.get_socket_value(self.visible)
        recursive: bool = self.get_socket_value(self.recursive)
        if is_waiting(visible, recursive):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        if visible is None:
            return
        if recursive is None:
            return
        game_object.setVisible(visible, recursive)
        self.done = True


class SetCurvePoints(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.curve_object = None
        self.points: list = None
        self.done: bool = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        curve_object = self.get_socket_value(self.curve_object)
        points = self.get_socket_value(self.points)
        if is_waiting(points):
            return
        if is_invalid(curve_object):
            return
        self._set_ready()
        if not points:
            return
        curve = curve_object.blenderObject.data
        for spline in curve.splines:
            curve.splines.remove(spline)
        spline = curve.splines.new('NURBS')
        pos = curve_object.worldPosition
        spline.points.add(len(points))
        for p, new_co in zip(spline.points, points):
            p.co = ([new_co.x - pos.x, new_co.y - pos.y, new_co.z - pos.z] + [1.0])
        self.done = True


class ActionRayPick(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.origin = None
        self.destination = None
        self.local: bool = None
        self.property_name: str = None
        self.xray: bool = None
        self.custom_dist: bool = None
        self.distance: float = None
        self.visualize: bool = None
        self._picked_object = None
        self._point = None
        self._normal = None
        self._direction = None
        self.PICKED_OBJECT = ULOutSocket(self, self.get_picked_object)
        self.POINT = ULOutSocket(self, self.get_point)
        self.NORMAL = ULOutSocket(self, self.get_normal)
        self.DIRECTION = ULOutSocket(self, self.get_direction)
        self.network = None

    def setup(self, network):
        self.network = network

    def get_picked_object(self):
        return self._picked_object

    def get_point(self):
        return self._point

    def get_normal(self):
        return self._normal

    def get_direction(self):
        return self._direction

    def _compute_direction(self, origin, dest, local, dist):
        custom_dist = self.get_socket_value(self.custom_dist)
        start = origin.worldPosition.copy() if hasattr(origin, "worldPosition") else origin
        if hasattr(dest, "worldPosition"):
            dest = dest.worldPosition.copy()
        if local:
            dest = start + dest
        d = dest - start
        d.normalize()
        return d, dist if custom_dist else (start - dest).length, dest

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            self._normal = None
            self._object = None
            # self._point = None
            return
        origin = self.get_socket_value(self.origin)
        destination = self.get_socket_value(self.destination)
        local: bool = self.get_socket_value(self.local)
        property_name: str = self.get_socket_value(self.property_name)
        xray: bool = self.get_socket_value(self.xray)
        distance: float = self.get_socket_value(self.distance)
        visualize: bool = self.get_socket_value(self.visualize)

        if is_waiting(origin, destination, local, property_name, distance):
            return
        self._set_ready()
        caster = self.network._owner
        obj, point, normal = None, None, None
        direction, distance, destination = self._compute_direction(origin, destination, local, distance)
        if not property_name:
            obj, point, normal = caster.rayCast(
                destination,
                origin,
                distance,
                xray=xray
            )
        else:
            obj, point, normal = caster.rayCast(
                destination,
                origin,
                distance,
                property_name,
                xray=xray
            )
        if visualize:
            origin = getattr(origin, 'worldPosition', origin)
            line_dest: Vector = direction.copy()
            line_dest.x *= distance
            line_dest.y *= distance
            line_dest.z *= distance
            line_dest = line_dest + origin
            bge.render.drawLine(
                origin,
                line_dest,
                [
                    1,
                    0,
                    0,
                    1
                ]
            )
            if obj:
                bge.render.drawLine(
                    origin,
                    point,
                    [
                        0,
                        1,
                        0,
                        1
                    ]
                )
        self._set_value(obj is not None)
        self._picked_object = obj
        self._point = point
        self._normal = normal
        self._direction = direction


class ProjectileRayCast(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.origin = None
        self.destination = None
        self.power: float = None
        self.resolution: float = None
        self.property_name: str = None
        self.xray: bool = None
        self.distance: float = None
        self.visualize: bool = None
        self._picked_object = None
        self._point = None
        self._normal = None
        self._parabola = None
        self.PICKED_OBJECT = ULOutSocket(self, self.get_picked_object)
        self.POINT = ULOutSocket(self, self.get_point)
        self.NORMAL = ULOutSocket(self, self.get_normal)
        self.PARABOLA = ULOutSocket(self, self.get_parabola)
        self.network = None

    def setup(self, network):
        self.network = network

    def get_picked_object(self):
        return self._picked_object

    def get_parabola(self):
        return self._parabola

    def get_point(self):
        return self._point

    def get_normal(self):
        return self._normal

    def calc_projectile(self, t, vel, pos):
        half: float = logic.getCurrentScene().gravity.z * (.5 * t * t)
        vel = vel * t
        return Vector((0, 0, half)) + vel + pos

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            self._out_normal = None
            self._out_object = None
            self._out_point = None
            return
        origin = self.get_socket_value(self.origin)
        power: float = self.get_socket_value(self.power)
        destination = self.get_socket_value(self.destination)
        resolution: float = 1 - (self.get_socket_value(self.resolution) * .99)
        property_name: str = self.get_socket_value(self.property_name)
        xray: bool = self.get_socket_value(self.xray)
        distance: float = self.get_socket_value(self.distance)
        visualize: bool = self.get_socket_value(self.visualize)

        if is_waiting(origin, destination, property_name, distance):
            return
        destination.normalize()
        destination *= power
        origin = getattr(origin, 'worldPosition', origin)

        points: list = []
        color: list = [1, 0, 0]
        idx = 0
        total_dist: float = 0
        found: bool = False
        owner = self.network._owner

        self._set_ready()

        while total_dist < distance:
            target = (self.calc_projectile(idx, destination, origin))
            start = origin if not points else points[-1]
            obj, point, normal = owner.rayCast(start, target, prop=property_name, xray=xray)
            total_dist += (target-start).length
            if not obj:
                points.append(target)
            else:
                points.append(point)
                color = [0, 1, 0]
                found = True
                break
            idx += resolution
        if visualize:
            for i, p in enumerate(points):
                if i < len(points) - 1:
                    bge.render.drawLine(p, points[i+1], color)
        self._set_value(points[-1] if found else None)
        self._picked_object = obj
        self._point = point
        self._normal = normal
        self._parabola = points


class ActionMousePick(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.distance = None
        self.property = None
        self.xray = None
        self.camera = None
        self._set_value(False)
        self._out_object = None
        self._out_normal = None
        self._out_point = None
        self.OUTOBJECT = ULOutSocket(self, self.get_out_object)
        self.OUTNORMAL = ULOutSocket(self, self.get_out_normal)
        self.OUTPOINT = ULOutSocket(self, self.get_out_point)

    def get_out_object(self):
        return self._out_object

    def get_out_normal(self):
        return self._out_normal

    def get_out_point(self):
        return self._out_point

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        distance = self.get_socket_value(self.distance)
        property_name = self.get_socket_value(self.property)
        xray = self.get_socket_value(self.xray)
        camera = self.get_socket_value(self.camera)
        if is_waiting(distance, property_name, xray, camera):
            return
        self._set_ready()
        if not condition:
            self._set_value(False)
            self._out_normal = None
            self._out_object = None
            self._out_point = None
            return
        if is_invalid(camera):
            return
        mpos = logic.mouse.position
        vec = 10 * camera.getScreenVect(*mpos)
        ray_target = camera.worldPosition - vec
        target, point, normal = self.network.ray_cast(
            camera,
            None,
            ray_target,
            property_name,
            xray,
            distance
        )
        self._set_value(target is not None)
        self._out_object = target
        self._out_normal = normal
        self._out_point = point


class ActionCameraPick(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.camera = None
        self.aim = None
        self.property_name = None
        self.xray = None
        self.distance = None
        self._picked_object = None
        self._picked_point = None
        self._picked_normal = None
        self.PICKED_OBJECT = ULOutSocket(self, self.get_picked_object)
        self.PICKED_POINT = ULOutSocket(self, self.get_picked_point)
        self.PICKED_NORMAL = ULOutSocket(self, self.get_picked_normal)

    def get_picked_object(self):
        return self._picked_object

    def get_picked_point(self):
        return self._picked_point

    def get_picked_normal(self):
        return self._picked_normal

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        camera = self.get_socket_value(self.camera)
        aim = self.get_socket_value(self.aim)
        property_name = self.get_socket_value(self.property_name)
        xray = self.get_socket_value(self.xray)
        distance = self.get_socket_value(self.distance)
        if is_waiting(camera, aim, property_name, xray, distance):
            return
        self._set_ready()
        if not condition:
            self._set_value(False)
            self._out_normal = None
            self._out_object = None
            self._out_point = None
            return
        if is_invalid(camera):
            return
        if is_invalid(aim):
            return
        obj, point, normal = None, None, None
        # assume screen coordinates
        if isinstance(aim, Vector) and len(aim) == 2:
            vec = 10 * camera.getScreenVect(aim[0], aim[1])
            ray_target = camera.worldPosition - vec
            aim = ray_target
        if not property_name:
            obj, point, normal = camera.rayCast(aim, None, distance)
        else:
            obj, point, normal = camera.rayCast(
                aim,
                None,
                distance,
                property_name,
                xray=xray
            )
        self._set_value(obj is not None)
        self._picked_object = obj
        self._picked_point = point
        self._picked_normal = normal


class ActionSetActiveCamera(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.camera = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        camera = self.get_socket_value(self.camera)
        if is_waiting(camera):
            return
        self._set_ready()
        if is_invalid(camera):
            return
        scene = logic.getCurrentScene()
        scene.active_camera = camera
        self.done = True


class ActionSetCameraFov(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.camera = None
        self.fov = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        camera = self.get_socket_value(self.camera)
        fov = self.get_socket_value(self.fov)
        if is_waiting(camera, fov):
            return
        self._set_ready()
        if is_invalid(camera):
            return
        camera.fov = fov
        self.done = True


class ActionSetCameraOrthoScale(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.camera = None
        self.scale = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        camera = self.get_socket_value(self.camera)
        scale = self.get_socket_value(self.scale)
        if is_waiting(camera, scale):
            return
        self._set_ready()
        if is_invalid(camera):
            return
        camera.ortho_scale = scale
        self.done = True


class ActionSetResolution(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.x_res = None
        self.y_res = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        x_res = self.get_socket_value(self.x_res)
        y_res = self.get_socket_value(self.y_res)
        if is_waiting(x_res, y_res):
            return
        self._set_ready()
        bge.render.setWindowSize(x_res, y_res)
        self.done = True


class ActionSetFullscreen(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.use_fullscreen = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        use_fullscreen = self.get_socket_value(self.use_fullscreen)
        if is_waiting(use_fullscreen):
            return
        self._set_ready()
        bge.render.setFullScreen(use_fullscreen)
        self.done = True


class ULSetProfile(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.use_profile = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        use_profile = self.get_socket_value(self.use_profile)
        if is_waiting(use_profile):
            return
        self._set_ready()
        bge.render.showProfile(use_profile)
        self.done = True


class ULShowFramerate(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.use_framerate = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        use_framerate = self.get_socket_value(self.use_framerate)
        if is_waiting(use_framerate):
            return
        self._set_ready()
        bge.render.showFramerate(use_framerate)
        self.done = True


class GetVSync(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(bge.render.getVsync())


class GetFullscreen(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(bge.render.getFullScreen())


class ULDrawLine(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.color = None
        self.from_point = None
        self.to_point = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        from_point = self.get_socket_value(self.from_point)
        to_point = self.get_socket_value(self.to_point)
        color = self.get_socket_value(self.color)
        if is_invalid(from_point, to_point, color):
            return
        self._set_ready()
        bge.render.drawLine(
            from_point,
            to_point,
            [
                color.x,
                color.y,
                color.z,
                1
            ]
        )
        self._set_value(True)


class GetResolution(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.width = None
        self.height = None
        self.res = None
        self.WIDTH = ULOutSocket(self, self.get_width)
        self.HEIGHT = ULOutSocket(self, self.get_height)
        self.RES = ULOutSocket(self, self.get_res)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_res(self):
        return self.res

    def evaluate(self):
        self._set_ready()
        self.width = bge.render.getWindowWidth()
        self.height = bge.render.getWindowHeight()
        self.res = Vector((self.width, self.height))


class ActionSetVSync(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.vsync_mode = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        vsync_mode = self.get_socket_value(self.vsync_mode)
        if is_waiting(vsync_mode):
            return
        self._set_ready()
        bge.render.setVsync(vsync_mode)
        self.done = True


class InitEmptyDict(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.dict = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.DICT = ULOutSocket(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.dict

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        self.dict = {}
        self.done = True


class InitNewDict(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.dict = None
        self.key = None
        self.val = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.DICT = ULOutSocket(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.dict

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        key = self.get_socket_value(self.key)
        value = self.get_socket_value(self.val)
        if is_waiting(key, value):
            return
        if not condition:
            return
        self._set_ready()
        self.dict = {str(key): value}
        self.done = True


class SetDictKeyValue(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.dict = None
        self.key = None
        self.val = None
        self.new_dict = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.DICT = ULOutSocket(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.new_dict

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        dictionary = self.get_socket_value(self.dict)
        key = self.get_socket_value(self.key)
        val = self.get_socket_value(self.val)
        if is_waiting(dictionary, key, val):
            return
        self._set_ready()
        dictionary[key] = val
        self.new_dict = dictionary
        self.done = True


class SetDictDelKey(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.dict = None
        self.key = None
        self.new_dict = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.DICT = ULOutSocket(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.new_dict

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        dictionary = self.get_socket_value(self.dict)
        key = self.get_socket_value(self.key)
        if is_waiting(dictionary, key):
            return
        self._set_ready()
        if key in dictionary:
            del dictionary[key]
        else:
            debug("Dict Delete Key Node: Key '{}' not in Dict!".format(key))
            return
        self.new_dict = dictionary
        self.done = True


class InitEmptyList(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.length = None
        self.items = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.LIST = ULOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.items

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        length = self.get_socket_value(self.length)
        if is_waiting(length):
            return
        self._set_ready()
        self.items = [None for x in range(length)]
        self.done = True


class AppendListItem(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.items: list = None
        self.val = None
        self.new_list: list = None
        self.done: bool = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.LIST = ULOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done: bool = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        list_d: list = self.get_socket_value(self.items)
        val = self.get_socket_value(self.val)
        if is_waiting(list_d, val):
            return
        self._set_ready()
        list_d.append(val)
        self.new_list = list_d
        self.done = True


class SetListIndex(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.items: list = None
        self.index: int = None
        self.val = None
        self.new_list: list = None
        self.done: bool = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.LIST = ULOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        list_d: list = self.get_socket_value(self.items)
        index: int = self.get_socket_value(self.index)
        val = self.get_socket_value(self.val)
        if is_invalid(list_d, index, val):
            return
        self._set_ready()
        list_d[index] = val
        self.new_list = list_d
        self.done = True


class RemoveListValue(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.items = None
        self.val = None
        self.new_list = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.LIST = ULOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        list_d = self.get_socket_value(self.items)
        val = self.get_socket_value(self.val)
        if is_invalid(list_d, val):
            return
        self._set_ready()
        if val in list_d:
            list_d.remove(val)
        else:
            debug("List Remove Value Node: Item '{}' not in List!".format(val))
            return
        self.new_list = list_d
        self.done = True


class RemoveListIndex(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.items = None
        self.idx = None
        self.new_list = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.LIST = ULOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        list_d = self.get_socket_value(self.items)
        idx = self.get_socket_value(self.idx)
        if is_invalid(list_d, idx):
            return
        self._set_ready()
        if len(list_d) > idx:
            del list_d[idx]
        else:
            debug("List Index exceeds length!")
            return
        self.new_list = list_d
        self.done = True


class ActionSetParent(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.child_object = None
        self.parent_object = None
        self.compound = True
        self.ghost = True
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        child_object = self.get_socket_value(self.child_object)
        parent_object = self.get_socket_value(self.parent_object)
        compound = self.get_socket_value(self.compound)
        ghost = self.get_socket_value(self.ghost)
        self._set_ready()
        if is_invalid(child_object, parent_object, compound, ghost):
            return
        if child_object.parent is parent_object:
            return
        child_object.setParent(parent_object, compound, ghost)
        self.done = True


class ActionRemoveParent(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.child_object = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        child_object = self.get_socket_value(self.child_object)
        if is_waiting(child_object):
            return
        self._set_ready()
        if is_invalid(child_object):
            return
        if not child_object.parent:
            return
        child_object.removeParent()
        self.done = True


class ActionPerformanceProfile(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.network = None
        self.print_profile = False
        self.check_evaluated_cells = False
        self.check_average_cells_per_sec = False
        self.check_cells_per_tick = False
        self.done = None
        self.data = ''
        self.OUT = ULOutSocket(self, self.get_done)
        self.DATA = ULOutSocket(self, self.get_data)

    def get_done(self):
        return self.done

    def get_data(self):
        return self.data

    def setup(self, network):
        self.network = network

    def evaluate(self):
        self.done = False
        self.data = '----------------------------------Start Profile\n'
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        print_profile = self.get_socket_value(
            self.print_profile
        )
        check_evaluated_cells = self.get_socket_value(
            self.check_evaluated_cells
        )
        check_average_cells_per_sec = self.get_socket_value(
            self.check_average_cells_per_sec
        )
        check_cells_per_tick = self.get_socket_value(
            self.check_cells_per_tick
        )
        if is_waiting(
            print_profile,
            check_evaluated_cells,
            check_average_cells_per_sec,
            check_cells_per_tick
        ):
            self._set_ready()
            return
        self._set_ready()
        if check_evaluated_cells:
            self.data += 'Evaluated Nodes:\t{}\n'.format(
                self.network.evaluated_cells
            )
        if check_average_cells_per_sec:
            self.data += 'Nodes per Sec (avg):\t{}\n'.format(
                self.network.evaluated_cells / self.network.timeline
            )
        if check_cells_per_tick:
            self.data += 'Nodes per Tick:\t{}\n'.format(
                len(self.network._cells)
            )
        self.data += '----------------------------------End Profile'
        if print_profile:
            print(self.data)
        self.done = True


class ULSetBoneConstraintInfluence(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.armature = None
        self.bone = None
        self.constraint = None
        self.influence = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_socket_value(self.armature)
        bone = self.get_socket_value(self.bone)
        constraint = self.get_socket_value(self.constraint)
        influence = self.get_socket_value(self.influence)
        if is_waiting(
            armature,
            bone,
            constraint,
            influence
        ):
            return
        self._set_ready()
        if is_invalid(armature):
            return
        armature.blenderObject.pose.bones[bone].constraints[constraint].influence = influence
        self.done = True


class ULSetBoneConstraintTarget(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.armature = None
        self.bone = None
        self.constraint = None
        self.target = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_socket_value(self.armature)
        bone = self.get_socket_value(self.bone)
        constraint = self.get_socket_value(self.constraint)
        target = self.get_socket_value(self.target)
        if is_waiting(
            armature,
            bone,
            constraint,
            target
        ):
            return
        self._set_ready()
        if is_invalid(armature):
            return
        armature.blenderObject.pose.bones[bone].constraints[constraint].target = target.blenderObject
        self.done = True


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
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_socket_value(self.armature)
        bone = self.get_socket_value(self.bone)
        constraint = self.get_socket_value(self.constraint)
        attribute = self.get_socket_value(self.attribute)
        value = self.get_socket_value(self.value)
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
        setattr(armature.blenderObject.pose.bones[bone].constraints[constraint], attribute, value)
        self.done = True


class ActionEditBone(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.armature = None
        self.bone_name = None
        self.set_translation = None
        self.set_orientation = None
        self.set_scale = None
        self.translate = None
        self.rotate = None
        self.scale = None
        self._eulers = Euler((0, 0, 0), "XYZ")
        self._vector = Vector((0, 0, 0))
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def _convert_orientation(self, ch, xyzrot):
        eulers = self._eulers
        eulers[:] = xyzrot
        if ch.rotation_mode is logic.ROT_MODE_QUAT:
            return eulers.to_quaternion()
        else:
            return xyzrot

    def _set_orientation(self, ch, rot):
        orientation = self._convert_orientation(ch, rot)
        if ch.rotation_mode is logic.ROT_MODE_QUAT:
            ch.rotation_quaternion = orientation
        else:
            ch.rotation_euler = orientation

    def _rotate(self, ch, xyzrot):
        orientation = self._convert_orientation(ch, xyzrot)
        if ch.rotation_mode is logic.ROT_MODE_QUAT:
            ch.rotation_quaternion = (
                Quaternion(ch.rotation_quaternion) * orientation
            )
        else:
            ch.rotation_euler = ch.rotation_euler.rotate(orientation)

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_socket_value(self.armature)
        bone_name = self.get_socket_value(self.bone_name)
        set_translation = self.get_socket_value(self.set_translation)
        set_orientation = self.get_socket_value(self.set_orientation)
        set_scale = self.get_socket_value(self.set_scale)
        translate = self.get_socket_value(self.translate)
        rotate = self.get_socket_value(self.rotate)
        scale = self.get_socket_value(self.scale)
        if is_waiting(
            armature,
            bone_name,
            set_translation,
            set_orientation,
            set_scale,
            translate,
            rotate,
            scale
        ):
            return
        self._set_ready()
        if is_invalid(armature):
            return
        if not bone_name:
            return
        # TODO cache the bone index
        bone_channel = armature.channels[bone_name]
        if set_translation is not None:
            bone_channel.location = set_translation
        if set_orientation is not None:
            self._set_orientation(bone_channel, set_orientation)
        if set_scale is not None:
            bone_channel.scale = set_scale
        if translate is not None:
            vec = self._vector
            vec[:] = translate
            bone_channel.location = bone_channel.location + vec
        if scale is not None:
            vec = self._vector
            vec[:] = scale
            bone_channel.scale = bone_channel.scale + vec
        if rotate is not None:
            self._rotate(bone_channel, rotate)
        armature.update()
        self.done = True


class ActionSetBonePos(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.armature = None
        self.bone_name = None
        self.set_translation = None
        self._eulers = Euler((0, 0, 0), "XYZ")
        self._vector = Vector((0, 0, 0))
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_socket_value(self.armature)
        bone_name = self.get_socket_value(self.bone_name)
        set_translation = self.get_socket_value(self.set_translation)
        self._set_ready()
        if is_invalid(armature, bone_name, set_translation):
            return
        if not bone_name:
            return
        # TODO cache the bone index
        bone_channel = armature.channels[bone_name]
        if set_translation is not None:
            bone_channel.location = set_translation
        else:
            debug('Set Bone Node: Position is None!')
        armature.update()
        self.done = True


class ActionTimeFilter(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.delay = None
        self._triggered = False
        self._triggered_time = None
        self._trigger_delay = None

    def evaluate(self):
        if self._triggered is True:
            self._set_ready()
            delta = self.network.timeline - self._triggered_time
            if delta < self._trigger_delay:
                self._set_value(False)
                return
        condition = self.get_socket_value(self.condition)
        delay = self.get_socket_value(self.delay)
        if is_waiting(condition, delay):
            return
        self._set_ready()
        self._set_value(False)
        if delay is None:
            return
        if condition is None:
            return
        if condition:
            self._triggered = True
            self._triggered_time = self.network.timeline
            self._trigger_delay = delay
            self._set_value(True)


class ULBarrier(ULActionNode):
    consumed: bool
    trigger: float

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.time = None
        self.consumed = False
        self.trigger = 0

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        time = self.get_socket_value(self.time)
        if is_waiting(time):
            return

        self._set_ready()

        now = self.network.timeline

        if not not_met(condition):
            if not self.consumed:
                self.consumed = True
                self.trigger = now + time

            if now >= self.trigger:
                self._set_value(True)

        else:
            self._set_value(False)
            self.consumed = False


class ActionTimeDelay(ULActionNode):
    consumed: bool
    triggers: list

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.delay = None
        self.triggers = []

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        delay = self.get_socket_value(self.delay)
        if is_invalid(delay):
            return
        self._set_ready()

        now = self.network.timeline

        if not not_met(condition):
            self.triggers.append(now + delay)

        if not self.triggers:
            self._set_value(False)
            return
        t = self.triggers[0]
        if now >= t:
            self._set_value(True)
            self.triggers.remove(t)
            return
        self._set_value(False)


class ActionSetDynamics(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.activate = False
        self.ghost = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        ghost = self.get_socket_value(self.ghost)
        activate = self.get_socket_value(self.activate)
        if is_waiting(game_object, ghost, activate):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if activate:
            game_object.restoreDynamics()
        else:
            game_object.suspendDynamics(ghost)
        self.done = True


class ActionSetPhysics(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.activate = False
        self.free_const = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        activate = self.get_socket_value(self.activate)
        free_const = self.get_socket_value(self.free_const)
        if is_waiting(game_object, free_const, activate):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if activate:
            game_object.restorePhysics()
        else:
            game_object.suspendPhysics(free_const)
        self.done = True


class ActionSetRigidBody(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.activate = False
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        activate = self.get_socket_value(self.activate)
        if is_waiting(game_object, activate):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        if activate:
            game_object.enableRigidBody()
        else:
            game_object.disableRigidBody()
        self.done = True


class ActionEndObject(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.scene = None
        self.game_object = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        game_object = self.get_socket_value(self.game_object)
        if not_met(condition):
            return
        if is_waiting(game_object):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if game_object is self.network._owner:
            self.network._do_remove = True
        game_object.endObject()
        self.done = True


class ActionSetTimeScale(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.scene = None
        self.timescale = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        timescale = self.get_socket_value(self.timescale)
        if is_waiting(timescale):
            return
        self._set_ready()
        if is_invalid(timescale):
            return
        logic.setTimeScale(timescale)
        self.done = True


class ActionSetGravity(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.scene = None
        self.gravity = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        gravity = self.get_socket_value(self.gravity)
        if is_waiting(gravity):
            return
        self._set_ready()
        if is_invalid(gravity):
            return
        logic.setGravity(gravity)
        self.done = True


class ActionApplyGameObjectValue(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.movement = None
        self.rotation = None
        self.force = None
        self.torque = None
        self.local = False

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        if is_waiting(game_object):
            return
        movement = self.get_socket_value(self.movement)
        rotation = self.get_socket_value(self.rotation)
        force = self.get_socket_value(self.force)
        torque = self.get_socket_value(self.torque)
        local = self.local
        if is_waiting(movement, rotation, force, torque, local):
            return
        self._set_ready()
        if not condition:
            return
        if is_invalid(game_object):
            return
        if movement:
            game_object.applyMovement(movement, local)
        if rotation:
            if len(rotation) == 3:
                game_object.applyRotation(rotation, local)
            else:
                game_object.applyRotation(rotation.to_euler("XYZ"), local)
        if force:
            game_object.applyForce(force, local)
        if torque:
            game_object.applyTorque(torque, local)


class ActionApplyLocation(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.movement = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        movement = self.get_socket_value(self.movement)
        local = self.local
        if is_waiting(game_object, movement, local):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if movement:
            game_object.applyMovement(movement, local)
        self.done = True


class ActionApplyRotation(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.rotation = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        rotation = self.get_socket_value(self.rotation)
        local = self.local
        if is_waiting(game_object, rotation, local):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if rotation:
            if len(rotation) == 3:
                game_object.applyRotation(rotation, local)
            else:
                game_object.applyRotation(rotation.to_euler("XYZ"), local)
        self.done = True


class ActionApplyForce(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.force = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        force = self.get_socket_value(self.force)
        local = self.local
        if is_waiting(game_object, force):
            return
        self._set_ready()
        game_object.applyForce(force, local)
        self.done = True


class ActionApplyImpulse(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.point = None
        self.impulse = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        point = self.get_socket_value(self.point)
        impulse = self.get_socket_value(self.impulse)
        local = self.local
        if hasattr(point, 'worldPosition'):
            point = point.worldPosition
        if is_waiting(point, impulse) or is_invalid(game_object):
            return
        self._set_ready()
        if impulse:
            game_object.applyImpulse(point, impulse, local)
        self.done = True


class GamepadLook(ULActionNode):
    def __init__(self, axis=0):
        ULActionNode.__init__(self)
        self.axis: int = axis
        self.condition = None
        self.main_obj: GameObject = None
        self.head_obj: GameObject = None
        self.inverted: bool = None
        self.index: int = None
        self.sensitivity: float = None
        self.exponent: float = None
        self.use_cap_x: bool = None
        self.cap_x: Vector = None
        self.use_cap_y: bool = None
        self.cap_y: Vector = None
        self.threshold: float = None
        self.done: bool = None
        self.DONE = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        axis: int = self.get_socket_value(self.axis)
        condition: GameObject = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        main_obj: GameObject = self.get_socket_value(self.main_obj)
        head_obj: GameObject = self.get_socket_value(self.head_obj)
        if is_invalid(head_obj):
            head_obj = main_obj
        if is_invalid(axis):
            debug('Gamepad Sticks Node: Invalid Controller Stick!')
            return
        inverted: bool = self.get_socket_value(self.inverted)
        index: int = self.get_socket_value(self.index)
        sensitivity: float = self.get_socket_value(self.sensitivity)
        exponent: float = self.get_socket_value(self.exponent)
        threshold: float = self.get_socket_value(self.threshold)
        use_cap_x: Vector = self.get_socket_value(self.use_cap_x)
        cap_x: Vector = self.get_socket_value(self.cap_x)
        uppercapX: float = cap_x.x
        lowercapX: float = -cap_x.y
        use_cap_y: Vector = self.get_socket_value(self.use_cap_y)
        cap_y: Vector = self.get_socket_value(self.cap_y)
        uppercapY: float = cap_y.x
        lowercapY: float = -cap_y.y

        self._set_ready()
        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            debug('Gamepad Sticks Node: No Joystick at that Index!')
            return
        if is_invalid(joystick):
            return
        raw_values = joystick.axisValues
        if axis == 0:
            x, y = raw_values[0], raw_values[1]
        elif axis == 1:
            x, y = raw_values[2], raw_values[3]
        neg_x = -1 if x < 0 else 1
        neg_y = -1 if y < 0 else 1

        if -threshold < x < threshold:
            x = 0
        else:
            x = abs(x) ** exponent

        if -threshold < y < threshold:
            y = 0
        else:
            y = abs(y) ** exponent
        if x == y == 0:
            self.done = True
            return

        x *= neg_x
        y *= neg_y

        x = -x if inverted['x'] else x
        y = -y if inverted['y'] else y

        x *= sensitivity
        if use_cap_x:
            objectRotation = main_obj.localOrientation.to_euler()
            if objectRotation.z + x > uppercapX:
                x = 0
                objectRotation.z = uppercapX
                main_obj.localOrientation = objectRotation.to_matrix()

            if objectRotation.z + x < lowercapX:
                x = 0
                objectRotation.z = lowercapX
                main_obj.localOrientation = objectRotation.to_matrix()

        y *= sensitivity
        if use_cap_y:
            objectRotation = head_obj.localOrientation.to_euler()
            if objectRotation.y + y > uppercapY:
                y = 0
                objectRotation.y = uppercapY
                head_obj.localOrientation = objectRotation.to_matrix()

            if objectRotation.y + y < lowercapY:
                y = 0
                objectRotation.y = lowercapY
                head_obj.localOrientation = objectRotation.to_matrix()

        main_obj.applyRotation(Vector((0, 0, x)), True)
        head_obj.applyRotation(Vector((0, y, 0)), True)
        self.done = True


class ActionCharacterJump(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        if is_waiting(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        self._set_ready()
        if is_invalid(game_object):
            return
        physics.jump()

        self.done = True


class SetCharacterJumpSpeed(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.force = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        force = self.get_socket_value(self.force)
        if is_waiting(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        self._set_ready()
        if is_invalid(game_object):
            return
        physics.jumpSpeed = force
        self.done = True


class SetCollisionGroup(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.slots = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        slots = self.get_socket_value(self.slots)
        if is_waiting(game_object, slots):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        game_object.collisionGroup = slots

        self.done = True


class SetCollisionMask(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.slots = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        slots = self.get_socket_value(self.slots)
        if is_waiting(game_object, slots):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        game_object.collisionMask = slots

        self.done = True


class ActionSaveVariable(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.name = None
        self.val = None
        self.path = ''
        self.file_name = ''
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path, name, val):
        data = None
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if os.path.isfile(path):
            f = open(path, 'r')
            data = json.load(f)
            data[name] = val
            f.close()
            f = open(path, 'w')
            json.dump(data, f, indent=2)
        else:
            debug('Variable file does not exist - creating...')
            f = open(path, 'w')
            data = {name: val}
            json.dump(data, f, indent=2)
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        name = self.get_socket_value(self.name)
        val = self.get_socket_value(self.val)
        if is_waiting(name, val):
            return
        self._set_ready()

        cust_path = self.get_custom_path(self.path)
        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )

        os.makedirs(path, exist_ok=True)

        self.write_to_json(path, name, val)
        self.done = True


class ActionSaveVariables(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.val = None
        self.path = ''
        self.file_name = ''
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path, val):
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if os.path.isfile(path):
            f = open(path, 'w')
            json.dump(val, f, indent=2)
        else:
            debug('file does not exist - creating...')
            f = open(path, 'w')
            json.dump(val, f, indent=2)
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        val = self.get_socket_value(self.val)
        if is_waiting(val):
            return
        self._set_ready()

        cust_path = self.get_custom_path(self.path)
        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path, val)
        self.done = True


class ActionLoadVariable(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.name = None
        self.path = ''
        self.file_name = ''
        self.var = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.VAR = ULOutSocket(self, self.get_var)

    def get_done(self):
        return self.done

    def get_var(self):
        return self.var

    def read_from_json(self, path, name):
        self.done = False
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if path:
            f = open(path, 'r')
            data = json.load(f)
            if name not in data:
                debug('"{}" is not a saved Variabe!')
            self.var = data[name]
            f.close()
        else:
            debug('No saved variables!')

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        name = self.get_socket_value(self.name)
        if is_waiting(name):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.read_from_json(path, name)
        self.done = True


class ActionLoadVariables(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.path = ''
        self.file_name = ''
        self.var = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.VAR = ULOutSocket(self, self.get_var)

    def get_done(self):
        return self.done

    def get_var(self):
        return self.var

    def read_from_json(self, path):
        self.done = False
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if not os.path.isfile(path):
            debug('No Saved Variables!')
            return
        f = open(path, 'r')
        data = json.load(f)
        self.var = data
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.read_from_json(path)
        self.done = True


class ActionRemoveVariable(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.name = None
        self.path = ''
        self.file_name = ''
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path, name):
        data = None
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if os.path.isfile(path):
            f = open(path, 'r')
            data = json.load(f)
            if name in data:
                del data[name]
            f.close()
            f = open(path, 'w')
            json.dump(data, f, indent=2)
            f.close()
        else:
            debug('File does not exist!')

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        name = self.get_socket_value(self.name)
        if is_waiting(name):
            return
        self._set_ready()

        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path, name)
        self.done = True


class ActionClearVariables(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.path = ''
        self.file_name = ''
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path):
        data = None
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if os.path.isfile(path):
            data = {}
            f = open(path, 'w')
            json.dump(data, f, indent=2)
        else:
            debug('File does not exist - creating...')
            f = open(path, 'w')
            data = {}
            json.dump(data, f, indent=2)
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path)
        self.done = True


class ActionListVariables(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.print_list = None
        self.path = ''
        self.file_name = ''
        self.done = None
        self.items = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.LIST = ULOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.items

    def write_to_json(self, path, p_l):
        data = None
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if os.path.isfile(path):
            f = open(path, 'r')
            data = json.load(f)
            if len(data) == 0:
                debug('There are no saved variables')
                return
            li = []
            for x in data:
                if p_l:
                    print('{}\t->\t{}'.format(x, data[x]))
                li.append(x)
            self.items = li
        else:
            debug('There are no saved variables')
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        print_list = self.get_socket_value(self.print_list)
        if is_waiting(print_list):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path, print_list)
        self.done = True


class ActionSetCharacterJump(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.max_jumps = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        max_jumps = self.get_socket_value(self.max_jumps)
        if is_waiting(game_object, max_jumps):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        physics.maxJumps = max_jumps
        self.done = True


class ActionSetCharacterGravity(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.gravity = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        gravity = self.get_socket_value(self.gravity)
        if is_waiting(gravity):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        if physics:
            physics.gravity = gravity
        else:
            game_object.gravity = gravity
        self.done = True


class ActionSetCharacterWalkDir(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.walkDir = None
        self.local = False
        self.active = False
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            if self.active:
                game_object = self.get_socket_value(self.game_object)
                physics = bge.constraints.getCharacter(game_object)
                physics.walkDirection = Vector((0, 0, 0))
                self.active = False
            return
        elif not self.active:
            self.active = True
        game_object = self.get_socket_value(self.game_object)
        local = self.local
        walkDir = self.get_socket_value(self.walkDir)
        if is_waiting(game_object, local, walkDir):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if local:
            walkDir = game_object.worldOrientation @ walkDir
        physics = bge.constraints.getCharacter(game_object)
        physics.walkDirection = walkDir / bpy.data.scenes[bge.logic.getCurrentScene().name].game_settings.physics_step_sub
        self.done = True


class ActionSetCharacterVelocity(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.vel = None
        self.time = None
        self.local = False
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        if is_waiting(game_object):
            return
        local = self.local
        physics = bge.constraints.getCharacter(game_object)
        vel = self.get_socket_value(self.vel)
        time = self.get_socket_value(self.time)
        self._set_ready()
        if is_invalid(game_object):
            return
        physics.setVelocity(vel, time, local)
        self.done = True


class ActionApplyTorque(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.torque = None
        self.local = False
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        torque = self.get_socket_value(self.torque)
        local = self.local
        if is_waiting(game_object, torque):
            return
        self._set_ready()
        if torque:
            game_object.applyTorque(torque, local)
        self.done = True


class ActionPlayAction(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.action_name = None
        self.stop_anim = None
        self.frames = None
        self.start_frame = None
        self.end_frame = None
        self.layer = None
        self.priority = None
        self.play_mode = None
        self.layer_weight = None
        self.old_layer_weight = None
        self.speed = None
        self.old_speed = None
        self.blendin = None
        self.blend_mode = None
        self._started = False
        self._running = False
        self._finished = False
        self._frame = 0.0
        self._finish_notified = False
        self.STARTED = ULOutSocket(self, self._get_started)
        self.FINISHED = ULOutSocket(self, self._get_finished)
        self.RUNNING = ULOutSocket(self, self._get_running)
        self.FRAME = ULOutSocket(self, self._get_frame)

    def _get_started(self):
        return self._started

    def _get_finished(self):
        return self._finished

    def _get_running(self):
        return self._running

    def _get_frame(self):
        return self._frame

    def _reset_subvalues(self):
        self._started = False
        self._finished = False
        self._running = False
        self._frame = 0.0
        self._finish_notified = False

    def _notify_finished(self, obj, layer):
        if not self._finish_notified and self.stop_anim:
            self._finish_notified = True
            self._finished = True
            obj.stopAction(layer)
        else:
            self._finished = False

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        game_object = self.get_socket_value(self.game_object)
        action_name = self.get_socket_value(self.action_name)
        start_frame = self.get_socket_value(self.start_frame)
        end_frame = self.get_socket_value(self.end_frame)
        layer = self.get_socket_value(self.layer)
        priority = self.get_socket_value(self.priority)
        play_mode = self.get_socket_value(self.play_mode)
        layer_weight = self.get_socket_value(self.layer_weight)
        speed = self.get_socket_value(self.speed)
        blendin = self.get_socket_value(self.blendin)
        blend_mode = self.get_socket_value(self.blend_mode)
        if is_invalid(
            game_object,
            action_name,
            start_frame,
            end_frame,
            layer,
            priority,
            play_mode,
            layer_weight,
            speed,
            blendin,
            blend_mode
        ):
            return
        if play_mode > 2:
            if not_met(condition):
                self._notify_finished(game_object, layer)
                return
            else:
                play_mode -= 3
        if layer_weight <= 0:
            layer_weight = 0.0
        elif layer_weight >= 1:
            layer_weight = 1.0
        if speed <= 0:
            speed = 0.01
        self._set_ready()
        if is_invalid(game_object):  # can't play
            self._reset_subvalues()
        else:
            # Condition might be false and the animation running
            # because it was started in a previous evaluation
            playing_action = game_object.getActionName(layer)
            playing_frame = game_object.getActionFrame(layer)
            min_frame = start_frame
            max_frame = end_frame
            if end_frame < start_frame:
                min_frame = end_frame
                max_frame = max_frame
            if (
                (playing_action == action_name) and
                (playing_frame >= min_frame) and
                (playing_frame <= max_frame)
            ):
                self._started = False
                self._running = True
                is_near_end = False
                self._frame = playing_frame
                if (
                    layer_weight != self.old_layer_weight or
                    speed != self.old_speed
                ):
                    reset_frame = start_frame if play_mode == bge.logic.KX_ACTION_MODE_LOOP else end_frame
                    next_frame = (
                        playing_frame + speed
                        if
                        playing_frame + speed <= end_frame
                        else
                        reset_frame
                    )
                    game_object.stopAction(layer)
                    game_object.playAction(
                        action_name,
                        start_frame,
                        end_frame,
                        layer=layer,
                        priority=priority,
                        blendin=blendin,
                        play_mode=play_mode,
                        speed=speed,
                        layer_weight=1 - layer_weight,
                        blend_mode=blend_mode)
                    game_object.setActionFrame(next_frame, layer)
                # TODO: the meaning of start-end depends
                # also on the action mode
                if end_frame > start_frame:  # play 0 to 100
                    is_near_end = (playing_frame >= (end_frame - 0.5))
                else:  # play 100 to 0
                    is_near_end = (playing_frame <= (end_frame + 0.5))
                if is_near_end:
                    self._notify_finished(game_object, layer)
            elif condition:  # start the animation if the condition is True
                is_playing = game_object.isPlayingAction(layer)
                same_action = game_object.getActionName(layer) == action_name
                if not same_action and is_playing:
                    game_object.stopAction(layer)
                if not (is_playing or same_action):
                    game_object.playAction(
                        action_name,
                        start_frame,
                        end_frame,
                        layer=layer,
                        priority=priority,
                        blendin=blendin,
                        play_mode=play_mode,
                        speed=speed,
                        layer_weight=1-layer_weight,
                        blend_mode=blend_mode)
                    self._started = True
                    self._frame = start_frame
                self._running = True
                self._finished = False
                self._finish_notified = False
            else:  # game_object is existing and valid but condition is False
                self._reset_subvalues()
        self.old_layer_weight = layer_weight
        self.old_speed = speed


class ActionStopAnimation(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.action_layer = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not condition:
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        action_layer = self.get_socket_value(self.action_layer)
        if is_waiting(game_object, action_layer):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if is_invalid(action_layer):
            return
        game_object.stopAction(action_layer)
        self.done = True


class ActionSetAnimationFrame(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.action_layer = None
        self.action_frame = None
        self.freeze = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not condition:
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        action_layer = self.get_socket_value(self.action_layer)
        action_frame = self.get_socket_value(self.action_frame)
        freeze = self.get_socket_value(self.freeze)
        action_name = self.get_socket_value(self.action_name)
        layer_weight = self.get_socket_value(self.layer_weight)
        self._set_ready()
        if is_invalid(
            game_object,
            action_layer,
            action_frame,
            layer_weight
        ):
            debug('Set Animation Frame Node: Invalid Parameters!')
            return
        is_playing = game_object.isPlayingAction(action_layer)
        same_action = game_object.getActionName(action_layer) == action_name
        action = bpy.data.actions[action_name]
        start_frame = action.frame_range[0]
        end_frame = action.frame_range[1]
        finished = game_object.getActionFrame(action_layer) >= end_frame
        if not (is_playing or same_action) or finished:
            game_object.stopAction(action_layer)
            speed = .000000000000000001 if freeze else 1
            game_object.playAction(
                action_name,
                start_frame,
                end_frame,
                action_layer,
                layer_weight=1-layer_weight,
                speed=speed
            )
        game_object.setActionFrame(action_frame, action_layer)
        self.done = True


class ActionFindScene(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.query = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def has_status(self, status):
        found_scene = self.get_value()
        if (
            (self.condition is None) and
            (found_scene is not None) and
            (not found_scene.invalid) and
            (found_scene is not None)
        ):
            return status is STATUS_READY
        else:
            return ULActionNode.has_status(self, status)

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        query = self.get_socket_value(self.query)
        if is_waiting(query):
            return
        self._set_ready()
        if self.condition is None:
            scene = _name_query(logic.getSceneList(), query)
            self._set_value(scene)
        scene = _name_query(logic.getSceneList(), query)
        self._set_value(scene)
        self.done = True


class ActionStopSound(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.sound = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        sound = self.get_socket_value(self.sound)
        if is_waiting(sound):
            return
        self._set_ready()
        if sound is None:
            return
        sound.stop()


class ActionStopAllSounds(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        aud_sys = GlobalDB.retrieve('.uplogic_audio').get('nl_audio_system')
        if not aud_sys:
            return
        self._set_ready()
        aud_sys.device.stopAll()


class ActionPauseSound(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.sound = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        sound = self.get_socket_value(self.sound)
        if is_waiting(sound):
            return
        self._set_ready()
        if sound is None:
            return
        sound.pause()


class ActionResumeSound(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.sound = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        sound = self.get_socket_value(self.sound)
        if is_waiting(sound):
            return
        self._set_ready()
        if sound is None:
            return
        sound.resume()


class ActionListGlobalValues(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.data_id = None
        self.print_d = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        data_id = self.get_socket_value(self.data_id)
        print_d = self.get_socket_value(self.print_d)
        if is_waiting(data_id, print_d):
            return
        self._set_ready()
        db = GlobalDB.retrieve(data_id)
        if print_d:
            print(f'[Logic Nodes] Global category "{data_id}":')
            for e in db.data:
                print('{}\t->\t{}'.format(e, db.data[e]))
            print('END ------------------------------------')
        self._set_value(db.data)


class ActionSetGlobalValue(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.data_id = None
        self.key = None
        self.value = None
        self.persistent = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        data_id = self.get_socket_value(self.data_id)
        persistent = self.get_socket_value(self.persistent)
        key = self.get_socket_value(self.key)
        value = self.get_socket_value(self.value)
        if is_waiting(data_id, persistent, key, value):
            return
        self._set_ready()
        if self.condition is None or condition:
            if data_id is None:
                return
            if persistent is None:
                return
            if key is None:
                return
            db = GlobalDB.retrieve(data_id)
            db.put(key, value, persistent)
            if self.condition is None:
                self.deactivate()
        self.done = True


class ActionRandomInt(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.max_value = None
        self.min_value = None
        self.OUT_A = ULOutSocket(self, self._get_output)

    def _get_output(self):
        min_value = self.get_socket_value(self.min_value)
        max_value = self.get_socket_value(self.max_value)
        if is_waiting(max_value, min_value):
            return STATUS_WAITING
        if min_value > max_value:
            min_value, max_value = max_value, min_value
        if min_value == max_value:
            min_value = -sys.maxsize
            max_value = sys.maxsize

        return random.randint(min_value, max_value)

    def evaluate(self):
        self._set_ready()


class ActionRandomFloat(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.max_value = None
        self.min_value = None
        self.OUT_A = ULOutSocket(self, self._get_output)

    def _get_output(self):
        min_value = self.get_socket_value(self.min_value)
        max_value = self.get_socket_value(self.max_value)
        if is_waiting(min_value, max_value):
            return STATUS_WAITING
        if min_value > max_value:
            min_value, max_value = max_value, min_value
        if min_value == max_value:
            min_value = sys.float_info.min
            max_value = sys.float_info.max

        delta = max_value - min_value
        return min_value + (delta * random.random())

    def evaluate(self):
        self._set_ready()


class ULRandomVect(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.xyz = None
        self.OUT_A = ULOutSocket(self, self._get_output)

    def _get_output(self):
        xyz = self.get_socket_value(self.xyz)
        if is_waiting(xyz):
            return
        vmin, vmax = -999999999, 999999999
        delta = vmax - vmin
        x = vmin + (delta * random.random()) if xyz['x'] else 0
        y = vmin + (delta * random.random()) if xyz['y'] else 0
        z = vmin + (delta * random.random()) if xyz['z'] else 0
        return Vector((x, y, z))

    def evaluate(self):
        self._set_ready()


class ActionTranslate(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.moving_object = None
        self.local = None
        self.vect = None
        self.speed = None
        self._t = None
        self._old_values = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        moving_object = self.get_socket_value(self.moving_object)
        vect = self.get_socket_value(self.vect)
        dx = vect.x
        dy = vect.y
        dz = vect.z
        speed = self.get_socket_value(self.speed)
        local = self.get_socket_value(self.local)
        if is_waiting(
            vect,
            dx,
            dy,
            dz,
            speed,
            local
        ):
            return
        if is_invalid(moving_object):
            return
        self._set_ready()
        if dx is None:
            return
        if dy is None:
            return
        if dz is None:
            return
        if speed is None:
            return
        if local is None:
            return
        new_values = (moving_object, dx, dy, dz, speed, local)
        if new_values != self._old_values:
            start_pos = (
                moving_object.localPosition if
                local else moving_object.worldPosition
            )
            end_pos = Vector((
                start_pos.x + dx, start_pos.y + dy, start_pos.z + dz
            ))
            distance = (start_pos - end_pos).length
            time_to_destination = distance / speed
            t_speed = 1.0 / time_to_destination
            self._old_values = new_values
            self._start_pos = start_pos.copy()
            self._end_pos = end_pos.copy()
            self._d_pos = (end_pos - start_pos)
            self._t_speed = t_speed
            self._t = 0.0
        t = self._t
        dt = self._t_speed * self.network.time_per_frame
        t += dt
        if t >= 1.0:
            self._set_value(True)
            self._t = 0.0
            if local:
                moving_object.localPosition = self._end_pos.copy()
            else:
                moving_object.worldPosition = self._end_pos.copy()
        else:
            npos = self._start_pos + (self._d_pos * t)
            if local:
                moving_object.localPosition = npos
            else:
                moving_object.worldPosition = npos
            self._t = t
            self._set_value(False)


class SetGamma(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[
            scene.name
        ].view_settings.gamma = value
        self.done = True


class SetExposure(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[
            scene.name
        ].view_settings.exposure = value
        self.done = True


class SetEeveeAO(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_gtao = value
        self.done = True


class SetEeveeBloom(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_bloom = value
        self.done = True


class SetEeveeSSR(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_ssr = value
        self.done = True


class SetEeveeVolumetrics(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[
            scene.name
        ].eevee.use_volumetric_lights = value
        self.done = True


class SetEeveeSMAA(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_eevee_smaa = value
        self.done = True


class SetEeveeSMAAQuality(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_eevee_smaa = value
        self.done = True


class SetLightEnergy(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.lamp = None
        self.energy = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        lamp = self.get_socket_value(self.lamp)
        energy = self.get_socket_value(self.energy)
        if is_waiting(lamp, energy):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        light.energy = energy
        self.done = True


class ULMakeUniqueLight(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.light = None
        self.done = None
        self._light = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.LIGHT = ULOutSocket(self, self.get_light)

    def get_done(self):
        return self.done

    def get_light(self):
        return self._light

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        old_lamp_ge = self.get_socket_value(self.light)
        if is_waiting(old_lamp_ge):
            return
        self._set_ready()

        make_unique_light(old_lamp_ge)

        self.done = True


class SetLightShadow(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.lamp = None
        self.use_shadow = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        lamp = self.get_socket_value(self.lamp)
        use_shadow = self.get_socket_value(self.use_shadow)
        if is_waiting(lamp, use_shadow):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        light.use_shadow = use_shadow
        self.done = True


class SetLightColor(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.lamp = None
        self.color = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        lamp = self.get_socket_value(self.lamp)
        color = self.get_socket_value(self.color)
        if is_waiting(lamp, color):
            return
        if len(color) > 3:
            color = color[:-1]
        self._set_ready()
        light = lamp.blenderObject.data
        light.color = color
        self.done = True


class GetLightEnergy(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.lamp = None
        self.energy = 0
        self.ENERGY = ULOutSocket(self, self.get_energy)

    def get_energy(self):
        return self.energy

    def evaluate(self):
        lamp = self.get_socket_value(self.lamp)
        if is_waiting(lamp):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        self.energy = light.energy


class GetLightColor(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.lamp = None
        self.color = 0
        self.COLOR = ULOutSocket(self, self.get_color)

    def get_color(self):
        return self.color

    def evaluate(self):
        lamp = self.get_socket_value(self.lamp)
        if is_waiting(lamp):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        self.color = light.color


# Action "Move To": an object will follow a point
class ActionMoveTo(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        # list of parameters of this action
        self.condition = None
        self.moving_object = None
        self.destination_point = None
        self.speed = None
        self.dynamic = None
        self.distance = None

    def evaluate(self):  # the actual execution of this cell
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        moving_object = self.get_socket_value(self.moving_object)
        destination_point = self.get_socket_value(self.destination_point)
        speed = self.get_socket_value(self.speed)
        distance = self.get_socket_value(self.distance)
        dynamic = self.get_socket_value(self.dynamic)
        if hasattr(destination_point, 'worldPosition'):
            destination_point = destination_point.worldPosition
        if is_waiting(
            moving_object,
            destination_point,
            speed,
            distance,
            dynamic
        ):
            return
        self._set_ready()
        self._set_value(move_to(
            moving_object,
            destination_point,
            speed,
            self.network.time_per_frame,
            dynamic,
            distance))


class ActionTrackTo(ULActionNode):
    def __init__(self):
        self.condition = None
        self.moving_object = None
        self.target_object = None
        self.rot_axis = 2
        self.front_axis = 0
        self.speed = 20

    def evaluate(self):
        self._set_value(False)
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return self._set_ready()
        moving_object = self.get_socket_value(self.moving_object)
        target_object = self.get_socket_value(self.target_object)
        speed = self.get_socket_value(self.speed)
        rot_axis = self.get_socket_value(self.rot_axis)
        front_axis = self.get_socket_value(self.front_axis)
        if is_waiting(speed, rot_axis, front_axis):
            return
        if is_invalid(moving_object):
            return
        if is_invalid(target_object):
            return
        self._set_ready()
        if rot_axis is None:
            return
        if front_axis is None:
            return
        if rot_axis == 0:
            self._set_value(
                xrot_to(
                    moving_object,
                    target_object.worldPosition,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 1:
            self._set_value(
                yrot_to(
                    moving_object,
                    target_object.worldPosition,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 2:
            self._set_value(
                zrot_to(
                    moving_object,
                    target_object.worldPosition,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )


class ActionRotateTo(ULActionNode):
    def __init__(self):
        self.condition = None
        self.moving_object = None
        self.target_point = None
        self.speed = None
        self.rot_axis = 2
        self.front_axis = 0

    def evaluate(self):
        self._set_value(False)
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        moving_object = self.get_socket_value(self.moving_object)
        target_point = self.get_socket_value(self.target_point)
        speed = self.get_socket_value(self.speed)
        if hasattr(target_point, 'worldPosition'):
            target_point = target_point.worldPosition
        rot_axis = self.get_socket_value(self.rot_axis)
        front_axis = self.get_socket_value(self.front_axis)
        if is_waiting(moving_object, target_point, speed, rot_axis, front_axis):
            return
        self._set_ready()
        if rot_axis == 0:
            self._set_value(
                xrot_to(
                    moving_object,
                    target_point,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 1:
            self._set_value(
                yrot_to(
                    moving_object,
                    target_point,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 2:
            self._set_value(
                zrot_to(
                    moving_object,
                    target_point,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )


class ActionNavigateWithNavmesh(ULActionNode):

    class MotionPath(object):
        def __init__(self):
            self.points = []
            self.cursor = 0
            self.destination = None

        def next_point(self):
            if self.cursor < len(self.points):
                return self.points[self.cursor]
            else:
                return None

        def destination_changed(self, new_destination):
            return self.destination != new_destination

        def advance(self):
            self.cursor += 1
            return self.cursor < len(self.points)

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.moving_object = None
        self.rotating_object = None
        self.navmesh_object = None
        self.destination_point = None
        self.move_dynamic = None
        self.linear_speed = None
        self.reach_threshold = None
        self.look_at = None
        self.rot_axis = None
        self.front_axis = None
        self.rot_speed = None
        self.visualize = None
        self._motion_path = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        moving_object = self.get_socket_value(self.moving_object)
        rotating_object = self.get_socket_value(self.rotating_object)
        navmesh_object = self.get_socket_value(self.navmesh_object)
        destination_point = self.get_socket_value(self.destination_point)
        move_dynamic = self.get_socket_value(self.move_dynamic)
        linear_speed = self.get_socket_value(self.linear_speed)
        reach_threshold = self.get_socket_value(self.reach_threshold)
        look_at = self.get_socket_value(self.look_at)
        rot_axis = self.get_socket_value(self.rot_axis)
        front_axis = self.get_socket_value(self.front_axis)
        rot_speed = self.get_socket_value(self.rot_speed)
        visualize = self.get_socket_value(self.visualize)
        if is_invalid(
            destination_point,
            move_dynamic,
            linear_speed,
            reach_threshold,
            look_at,
            rot_axis,
            front_axis,
            rot_speed,
            visualize
        ):
            return
        if is_invalid(moving_object, navmesh_object):
            return
        if is_invalid(rotating_object):
            rotating_object = None
        self._set_ready()
        if (
            (self._motion_path is None) or
            (self._motion_path.destination_changed(destination_point))
        ):
            points = navmesh_object.findPath(
                moving_object.worldPosition,
                destination_point
            )
            motion_path = ActionNavigateWithNavmesh.MotionPath()
            motion_path.points = points[1:]
            motion_path.destination = destination_point
            self._motion_path = motion_path
        next_point = self._motion_path.next_point()
        if visualize:
            points = [moving_object.worldPosition.copy()]
            points.extend(self._motion_path.points[self._motion_path.cursor:])
            points.append(self._motion_path.destination)
            for i, p in enumerate(points):
                if i < len(points) - 1:
                    bge.render.drawLine(
                        p, points[i + 1], [1, 0, 0, 1]
                    )
        if next_point:
            tpf = self.network.time_per_frame
            if look_at and (rotating_object is not None):
                rot_to(
                    rot_axis,
                    rotating_object,
                    next_point,
                    front_axis,
                    rot_speed,
                    tpf
                )
            ths = reach_threshold  # if next_point == self._motion_path.destination else .1
            reached = move_to(
                moving_object,
                next_point,
                linear_speed,
                tpf,
                move_dynamic,
                ths
            )
            if reached:
                has_more = self._motion_path.advance()
                if not has_more:
                    self._set_value(True)


class ActionFollowPath(ULActionNode):
    class MotionPath(object):
        def __init__(self):
            self.points = []
            self.cursor = 0
            self.loop = False
            self.loop_start = 0

        def next_point(self):
            if self.cursor < len(self.points):
                return self.points[self.cursor]
            else:
                return None

        def advance(self):
            self.cursor += 1
            if self.cursor < len(self.points):
                return True
            else:
                if self.loop:
                    self.cursor = self.loop_start
                    return True
                return False

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.moving_object = None
        self.rotating_object = None
        self.path_points = None
        self.loop = None
        self.path_continue = None
        self.navmesh_object = None
        self.move_dynamic = None
        self.linear_speed = None
        self.reach_threshold = None
        self.look_at = None
        self.rot_speed = None
        self.rot_axis = None
        self.front_axis = None
        self._motion_path = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        path_continue = self.get_socket_value(self.path_continue)
        if not_met(condition):
            if not path_continue:
                self._motion_path = None
            self._set_ready()
            return
        moving_object = self.get_socket_value(self.moving_object)
        rotating_object = self.get_socket_value(self.rotating_object)
        path_points = self.get_socket_value(self.path_points)
        navmesh_object = self.get_socket_value(self.navmesh_object)
        move_dynamic = self.get_socket_value(self.move_dynamic)
        linear_speed = self.get_socket_value(self.linear_speed)
        reach_threshold = self.get_socket_value(self.reach_threshold)
        look_at = self.get_socket_value(self.look_at)
        rot_axis = self.get_socket_value(self.rot_axis)
        front_axis = self.get_socket_value(self.front_axis)
        rot_speed = self.get_socket_value(self.rot_speed)
        loop = self.get_socket_value(self.loop)
        if is_invalid(
            path_points,
            move_dynamic,
            linear_speed,
            reach_threshold,
            look_at,
            rot_axis,
            front_axis,
            loop
        ):
            return
        if is_invalid(rot_speed):
            rot_speed = 0
        if loop is None:
            return
        if is_invalid(moving_object):
            return
        if is_invalid(navmesh_object):
            navmesh_object = None
        self._set_ready()
        self._set_value(False)
        if (self._motion_path is None) or (self._motion_path.loop != loop):
            self.generate_path(
                moving_object.worldPosition,
                path_points,
                navmesh_object,
                loop
            )
        next_point = self._motion_path.next_point()
        if next_point:
            tpf = self.network.time_per_frame
            if look_at:
                rot_to(
                    rot_axis,
                    rotating_object,
                    next_point,
                    front_axis,
                    rot_speed,
                    tpf
                )
            reached = move_to(
                moving_object,
                next_point,
                linear_speed,
                tpf,
                move_dynamic,
                reach_threshold
            )
            if reached:
                has_more = self._motion_path.advance()
                if not has_more:
                    self._set_value(True)
                    self.done = True

    def generate_path(self, start_position, path_points, navmesh_object, loop):
        if not path_points:
            return self._motion_path.points.clear()
        path = ActionFollowPath.MotionPath()
        path.loop = loop
        points = path.points
        self._motion_path = path
        if not navmesh_object:
            points.append(Vector(start_position))
            if loop:
                path.loop_start = 1
            for p in path_points:
                points.append(Vector(p))
        else:
            last = path_points[-1]
            mark_loop_position = loop
            for p in path_points:
                subpath = navmesh_object.findPath(
                    start_position,
                    Vector(p)
                )
                if p is last:
                    points.extend(subpath)
                else:
                    points.extend(subpath[:-1])
                if mark_loop_position:
                    path.loop_start = len(points)
                    mark_loop_position = False
                start_position = Vector(p)
            if loop:
                subpath = navmesh_object.findPath(
                    Vector(last),
                    Vector(path_points[0])
                )
                points.extend(subpath[1:])


class ActionReplaceMesh(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.target_game_object = None
        self.new_mesh_name = None
        self.use_display = None
        self.use_physics = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        self._set_ready()
        if not condition:
            return
        target = self.get_socket_value(self.target_game_object)
        mesh = self.get_socket_value(self.new_mesh_name)
        display = self.get_socket_value(self.use_display)
        physics = self.get_socket_value(self.use_physics)
        if is_invalid(target):
            return
        if mesh is None:
            return
        if display is None:
            return
        if physics is None:
            return
        target.replaceMesh(mesh, display, physics)
        if physics:
            target.reinstancePhysicsMesh()
        self.done = True


class RemovePhysicsConstraint(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.object = None
        self.name = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not condition:
            return
        obj = self.get_socket_value(self.object)
        if is_invalid(obj):
            return
        name = self.get_socket_value(self.name)
        if is_invalid(name):
            return
        self._set_ready()
        bge.constraints.removeConstraint(obj[name].getConstraintId())
        self.done = True


class AddPhysicsConstraint(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.target = None
        self.child = None
        self.name = None
        self.constraint = None
        self.use_world = None
        self.pivot = None
        self.use_limit = None
        self.axis_limits = None
        self.linked_col = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        target = self.get_socket_value(self.target)
        child = self.get_socket_value(self.child)
        name = self.get_socket_value(self.name)
        constraint = self.get_socket_value(self.constraint)
        pivot = self.get_socket_value(self.pivot)
        use_limit = self.get_socket_value(self.use_limit)
        use_world = self.get_socket_value(self.use_world)
        axis_limits = self.get_socket_value(self.axis_limits)
        linked_col = self.get_socket_value(self.linked_col)
        if is_invalid(
            target,
            child,
            name,
            constraint,
            pivot,
            use_limit,
            use_world,
            axis_limits,
            linked_col
        ):
            return
        self._set_ready()
        flag = 0 if linked_col else 128
        if use_world:
            pivot.x -= target.localPosition.x
            pivot.y -= target.localPosition.y
            pivot.z -= target.localPosition.z
        if use_limit:
            target[name] = bge.constraints.createConstraint(
                target.getPhysicsId(),
                child.getPhysicsId(),
                constraint,
                pivot_x=pivot.x,
                pivot_y=pivot.y,
                pivot_z=pivot.z,
                axis_x=axis_limits.x,
                axis_y=axis_limits.y,
                axis_z=axis_limits.z,
                flag=flag
            )
        else:
            target[name] = bge.constraints.createConstraint(
                target.getPhysicsId(),
                child.getPhysicsId(),
                constraint,
                pivot_x=pivot.x,
                pivot_y=pivot.y,
                pivot_z=pivot.z,
                flag=flag
            )
        self.done = True


class ActionAlignAxisToVector(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.vector = None
        self.axis = None
        self.factor = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        self._set_ready()
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        v = self.get_socket_value(self.vector)
        axis = self.get_socket_value(self.axis)
        factor = self.get_socket_value(self.factor)
        if is_invalid(game_object):
            return
        if axis is None:
            return
        if factor is None:
            return
        v = getattr(v, 'worldPosition', v).copy()
        if not self.local:
            v -= game_object.worldPosition
        if axis > 2:
            matvec = v.copy()
            matvec.negate()
            v = matvec
            axis -= 3
        game_object.alignAxisToVect(v, axis, factor)
        self.done = True


class ActionUpdateBitmapFontQuads(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.game_object = None
        self.text = None
        self.grid_size = None
        self.condition = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):  # no status waiting, test
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not condition:
            return self._set_ready()
        self._set_ready()
        game_object = self.get_socket_value(self.game_object)
        text = eval(self.get_socket_value(self.text))
        grid_size = self.get_socket_value(self.grid_size)
        if is_invalid(game_object):
            return
        if text is None:
            text = ""
        if grid_size is None:
            return
        uv_size = 1.0 / grid_size
        mesh = game_object.meshes[0]
        quad_count = int(mesh.getVertexArrayLength(0) / 4)
        text_size = len(text)
        char_index = 0
        ASCII_START = 32
        for i in range(0, quad_count):
            row = 0
            column = 0
            if char_index < text_size:
                ascii_code = ord(text[char_index])
                grid_code = ascii_code - ASCII_START
                row = int(grid_code / grid_size)
                column = int(grid_code % grid_size)
                char_index += 1
            v0 = mesh.getVertex(0, i * 4)
            v1 = mesh.getVertex(0, i * 4 + 1)
            v2 = mesh.getVertex(0, i * 4 + 2)
            v3 = mesh.getVertex(0, i * 4 + 3)
            xmin = uv_size * column
            xmax = uv_size * (column + 1)
            ymax = 1.0 - (uv_size * row)
            ymin = 1.0 - (uv_size * (row + 1))
            v0.u = xmin
            v0.v = ymin
            v1.u = xmax
            v1.v = ymin
            v2.u = xmax
            v2.v = ymax
            v3.u = xmin
            v3.v = ymax
        self.done = True


class ActionSetCurrentScene(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.scene_name = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        self._set_ready()
        if not condition:
            return
        scene_name = self.get_socket_value(self.scene_name)
        if scene_name is None:
            return
        current_scene = logic.getCurrentScene()
        current_scene_name = current_scene.name
        if current_scene_name != scene_name:
            logic.addScene(scene_name)
            current_scene.end()
        self.done = True


class ActionStringOp(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.opcode = None
        self.condition = None
        self.input_string = None
        self.input_param_a = None
        self.input_param_b = None

    def evaluate(self):
        self._set_ready()
        code = self.get_socket_value(self.opcode)
        condition = self.get_socket_value(self.condition)
        input_string = self.get_socket_value(self.input_string)
        input_param_a = self.get_socket_value(self.input_param_a)
        input_param_b = self.get_socket_value(self.input_param_b)
        if not condition:
            return
        if input_string is None:
            return
        input_string = str(input_string)
        if code == 0:  # postfix
            self._set_value(input_string + str(input_param_a))
        elif code == 1:  # prefix
            self._set_value(str(input_param_a) + input_string)
        elif code == 2:  # infix
            self._set_value(
                str(input_param_a) +
                input_string +
                str(input_param_b)
            )
        elif code == 3:  # remove last
            self._set_value(input_string[:-1])
        elif code == 4:  # remove first
            self._set_value(input_string[1:])
        elif code == 5:  # replace a with b in string
            self._set_value(
                input_string.replace(
                    str(input_param_a),
                    str(input_param_b)
                )
            )
        elif code == 6:  # upper case
            self._set_value(input_string.upper())
        elif code == 7:  # lower case
            self._set_value(input_string.lower())
        elif code == 8:  # remove range
            self._set_value(
                input_string[:input_param_a] +
                input_string[input_param_b:]
            )
        elif code == 9:  # insert at
            self._set_value(
                input_string[:input_param_b] +
                str(input_param_a) +
                input_string[input_param_b:]
            )
        elif code == 10:  # length
            self._set_value(len(input_string))
        elif code == 11:  # substring
            self._set_value(input_string[input_param_a:input_param_b])
        elif code == 12:  # first index of
            self._set_value(input_string.find(str(input_param_a)))
        elif code == 13:  # last index of
            self._set_value(input_string.rfind(str(input_param_a)))
        pass
    pass
