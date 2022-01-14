import bpy
from bge import logic
import time


class ULSequence():
    def __init__(
        self,
        material,
        node,
        start_frame,
        end_frame,
        fps=60,
        mode=0
    ) -> None:
        self.material = material
        self.node = node
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.fps = fps
        self.mode = mode
        self.time = 0.0
        self.frame = 0
        self.initialized = False
        self.reverse = False
        self.running = True
        self._consumed = False
        self.active = True
        self._pause = False
        self._time_then = time.time()
        self.on_start = False
        self.on_finish = False
        self.player = (
            bpy.data.materials[material]
            .node_tree
            .nodes[node]
        ).image_user

        logic.getCurrentScene().pre_draw.append(self.update)

    def stop(self):
        self.on_finish = True
        logic.getCurrentScene().pre_draw.remove(self.update)

    def pause(self):
        self._pause = True
        self.running = False

    def restart(self):
        self.initialized = False

    def unpause(self):
        self._pause = False
        self.running = True

    def update(self):
        now = time.time()
        player = self.player
        self.time += now - self._time_then
        self._time_then = now
        fps = self.fps
        rate = 1 / fps
        speed = self.time / rate
        if speed < 1:
            return
        self.time -= rate * speed
        if self._pause:
            return
        play_mode = self.mode
        running = self.running
        start_frame = self.end_frame if self.reverse else self.start_frame
        end_frame = self.start_frame if self.reverse else self.end_frame
        if not self.initialized:
            player.frame_offset = start_frame
            self.initialized = True
        inverted = (start_frame > end_frame)
        frame = self.frame = player.frame_offset
        reset_cond = (frame <= end_frame) if inverted else (frame >= end_frame)
        if not running:
            if reset_cond:
                player.frame_offset = start_frame if inverted else end_frame
            self.on_start = True
            self._consumed = False

        start_cond = frame > start_frame if inverted else frame < start_frame

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
                    if play_mode == 1:
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
                    if play_mode == 1:
                        leftover = frame + s - end_frame
                        span = end_frame - start_frame
                        while leftover > span:
                            leftover -= span
                        player.frame_offset = start_frame + leftover
                    else:
                        player.frame_offset = end_frame
                else:
                    player.frame_offset += s
        elif play_mode == 1:
            player.frame_offset = end_frame if inverted else start_frame
        elif play_mode == 2:
            self.reverse = not self.reverse
        else:
            self.stop()
