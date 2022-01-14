from bge import logic
from bge.constraints import getCharacter
from mathutils import Vector
from uplogic.utils import debug


class ULCharacter():
    def __init__(self, owner) -> None:
        self.owner = owner
        self.character = getCharacter(owner)
        self.velocity = Vector((0, 0, 0))
        self.is_walking = False
        logic.getCurrentScene().pre_draw.append(self.reset)

    def reset(self):
        if not self.is_walking:
            self.walk = Vector((0, 0, 0))
        self.is_walking = False

    def destroy(self):
        logic.getCurrentScene().pre_draw.remove(self.reset)

    @property
    def on_ground(self):
        return self.character.onGround

    @on_ground.setter
    def on_ground(self, value):
        debug('Character.on_ground is Read-Only!')

    @property
    def max_jumps(self):
        return self.character.maxJumps

    @max_jumps.setter
    def max_jumps(self, value):
        self.character.maxJumps = value

    @property
    def gravity(self):
        return self.character.gravity

    @gravity.setter
    def gravity(self, value):
        self.character.gravity = value

    @property
    def jump_count(self):
        return self.character.jumpCount

    @jump_count.setter
    def jump_count(self, value):
        debug('Character.jump_count is Read-Only!')

    @property
    def walk(self):
        return self.character.walkDirection @ self.owner.worldOrientation

    @walk.setter
    def walk(self, value):
        self.is_walking = True
        self.character.walkDirection = self.owner.worldOrientation @ value

    @property
    def move(self):
        return self.character.walkDirection

    @move.setter
    def move(self, value):
        self.character.walkDirection = value

    @property
    def velocity(self):
        return self.velocity

    @velocity.setter
    def velocity(self, value):
        self.character.setVelocity(value, 100, False)
