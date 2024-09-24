import cv2
import numpy as np

from video_diff.src.processors.abstracts.video_processor import AVideoProcessor
from video_diff.src.utils import common_utils


class SimpleDitheringDetector(AVideoProcessor):
    def __init__(self, source, fill_value=0, state="g", frame_by_frame=False):
        super(SimpleDitheringDetector, self).__init__(source=source)
        self.window_name = "SimpleDitheringDetector"
        self.fill_value = fill_value
        self.state = state
        self.frame_by_frame = frame_by_frame
        self.need_render = True

        self.color_to_index = {
            "b": 0,
            "g": 1,
            "r": 2,
            "a": 3,  # absolute (not alpha, used internally)
        }

    @staticmethod
    def __subtraction(fframe, fprevframe, colortoindex, state=None):
        # Zero out all color indexes not specified
        # instead of extracting just the index
        color_index = colortoindex[state]
        for index in colortoindex.values():
            if state == 'a':
                return fprevframe - fframe
            if index != color_index and index < 3:
                fframe[:, :, index] = 0
        frame_difference = fframe - fprevframe
        return frame_difference

    @staticmethod
    def __mask(fframe, fprev_frame, fill_value):
        # Mask frame over old frame
        # If element is different, change value to fill_value
        masked_frame = np.uint8(
            np.where((fframe != fprev_frame).any(axis=2, keepdims=True), [fill_value, fill_value, fill_value], fframe))
        return masked_frame

    def set_state(self, key):
        self.state = key
        self.need_render = True

    def __frame_input(self):
        input_key = cv2.pollKey()

        def get_key_bind(key):
            if input_key == ord(key) and self.state != key:
                return True

        # quit when 'q' is pressed on the image window
        if get_key_bind('q'):
            print("q: Quit program")
            exit(0)

        elif get_key_bind('n'):
            print("n: Switching to normal mode")
            self.set_state('n')

        elif get_key_bind('r'):
            print("r: Switching to red channel")
            self.set_state('r')

        elif get_key_bind('g'):
            print("g: Switching to green channel")
            self.set_state('g')

        elif get_key_bind('b'):
            print("b: Switching to blue channel")
            self.set_state('b')

        elif get_key_bind('a'):
            print("a: Switching to absolute subtraction method")
            self.set_state('a')

        elif get_key_bind('m'):
            print("m: Switching to masking method")
            self.set_state('m')

        elif get_key_bind('p'):
            if not self.frame_by_frame:
                print("p: Switching to frame-to-frame mode")
                self.frame_by_frame = True
            self.need_render = True

        elif get_key_bind('c'):
            if self.frame_by_frame:
                print("c: Switching back to normal playback mode")
                self.frame_by_frame = False
                self.need_render = True

    def _render(self, capture_source):
        prev_frame = None
        color = None
        image = None

        while capture_source.isOpened():
            self.__frame_input()
            if self.frame_by_frame and not self.need_render:
                continue

            # Capture frame-by-frame
            ret, frame = capture_source.read()
            if ret is True:
                # Save the previous frame
                if prev_frame is not None:
                    prev_frame = color
                color = frame

                # First run, save color as prev_frame and skip
                # create __mask of image of all changed values
                # Fill changed values to 255
                if prev_frame is not None:
                    if self.state in self.color_to_index.keys():
                        if self.state == 'b':
                            color = common_utils.zero_after_first_index(color)
                        elif self.state == 'g':
                            color = common_utils.zero_all_except_middle(color)
                        elif self.state == 'r':
                            color = common_utils.zero_all_except_last(color)
                        image = common_utils.abs_subtraction(color, prev_frame)
                    elif self.state == 'm':
                        image = self.__mask(color, prev_frame, self.fill_value)
                    elif self.state == 'n':
                        image = color
                else:
                    prev_frame = color
                    continue
                if self.frame_by_frame:
                    self.need_render = False
                yield image

            else:
                # Once video has no more frames
                break
