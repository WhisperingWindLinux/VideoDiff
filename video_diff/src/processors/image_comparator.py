import cv2
import numpy as np

from video_diff.src.processors.abstracts.image_processor import AImageProcessor
from video_diff.src.utils import common_utils


class ImageComparator(AImageProcessor):
    def __init__(self, source, fill_value=0, state="g"):
        super(ImageComparator, self).__init__(source=source)
        self.window_name = "ImageComparator"
        self.fill_value = fill_value
        self.state = state
        self.source = source
        self.color_to_index = {
            "b": 0,
            "g": 1,
            "r": 2,
        }
        self.need_render = True

    def set_state(self, key):
        self.state = key
        self.need_render = True

    @staticmethod
    def __subtraction(fframe, fprev_frame, state):
        # Zero out all color indexes not specified
        # instead of extracting just the index
        fframe2 = fframe.copy()
        fprev_frame2 = fprev_frame.copy()
        for i in range(0, 3):
            if i == state:
                continue
            fframe2[:, :, i] = 0
        frame_difference = fframe2 - fprev_frame2
        return frame_difference

    @staticmethod
    def __abs_subtraction(fframe, fprev_frame):
        return fframe - fprev_frame

    @staticmethod
    def __mask(fframe, fprev_frame, fill_value):
        # Mask frame over old frame
        # If element is different, change value to fill_value
        masked_frame = np.uint8(
            np.where((fframe != fprev_frame).any(axis=2, keepdims=True), [fill_value, fill_value, fill_value], fframe))
        return masked_frame

    def __frame_input(self):
        input_key = cv2.pollKey()

        def get_key_bind(key):
            if input_key == ord(key) and self.state != key:
                return True

        # quit when 'q' is pressed on the image window
        if get_key_bind('q'):
            print("q: Quit program")
            exit(0)

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

        elif get_key_bind('i'):
            print("i: Inverting pair of images")
            self.frame_a, self.frame_b = self.frame_b, self.frame_a
            self.need_render = True

        elif get_key_bind('1'):
            print("1: Only displaying the first image")
            self.set_state(1)

        elif get_key_bind('2'):
            print("2: Only displaying the second image")
            self.set_state(2)

    def _render(self, source):
        image = None
        self.__frame_input()
        if self.need_render:
            if self.state in self.color_to_index.keys():
                image = self.__process_bgr_states()
            elif self.state == 'a':
                image = self.__abs_subtraction(self.frame_a, self.frame_b)
            elif self.state == 'm':
                image = self.__mask(self.frame_a, self.frame_b, self.fill_value)
            elif self.state == 1:
                image = self.frame_a
            elif self.state == 2:
                image = self.frame_b

            self.need_render = False
            yield image

    def __process_bgr_states(self):
        frame_a = None
        frame_b = None
        if self.state == 'b':
            frame_a = common_utils.zero_after_first_index(self.frame_a.copy())
            frame_b = common_utils.zero_after_first_index(self.frame_b.copy())
        elif self.state == 'g':
            frame_a = common_utils.zero_all_except_middle(self.frame_a.copy())
            frame_b = common_utils.zero_all_except_middle(self.frame_b.copy())
        elif self.state == 'r':
            frame_a = common_utils.zero_all_except_last(self.frame_a.copy())
            frame_b = common_utils.zero_all_except_last(self.frame_b.copy())
        image = self.__abs_subtraction(frame_a, frame_b)
        return image
