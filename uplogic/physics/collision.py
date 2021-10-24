from bge import logic


class ULCollision():
    target = None
    point = None
    normal = None
    tap = False
    consumed = False
    active = False
    _objects = []

    def __init__(self, game_object, callback, prop, mat, tap):
        self.callback = callback
        self.prop = prop
        self.mat = mat
        self.tap = tap
        self.game_object = game_object
        if self.collision not in game_object.collisionCallbacks:
            game_object.collisionCallbacks.append(self.collision)
        logic.getCurrentScene().pre_draw.append(self.update)

    def collision(self, obj, point, normal):
        if self.tap and self.consumed:
            return
        self._objects.append(obj)
        material = self.mat
        prop = self.prop
        for obj in self._objects:
            bo = obj.blenderObject
            if material:
                if material not in [
                    slot.material.name for
                    slot in
                    bo.material_slots
                ]:
                    self._objects.remove(obj)
            if prop:
                for obj in self._objects:
                    if prop not in obj:
                        self._objects.remove(obj)

        for obj in self._objects:
            self.callback(obj, point, normal)
            self.active = True
            if self.tap:
                self.consumed = True

        self._objects = []

    def update(self, cam):
        self.active = False

    def unregister(self):
        self.game_object.collisionCallbacks.remove(self.collision)
        logic.getCurrentScene().pre_draw.remove(self.update)


def on_collision(obj, callback, prop='', mat='', tap=False):
    return ULCollision(obj, callback, prop, mat, tap)
