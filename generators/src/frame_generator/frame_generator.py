import cv2
import numpy as np


class FrameGenerator:
    def __init__(self, sequence, width, height, seed):
        self.sequence = sequence
        self.width = width
        self.height = height
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.frames = []

    def generate_random_frame(self, height, width, frameinfo=None):
        frame = self.rng.integers(256, size=(height, width, 3), dtype=np.uint8)
        if frameinfo:
            frametext = "{frame}/{totalframes}".format(frame=frameinfo['frame'], totalframes=frameinfo['totalframes'])
            fontScale = min(width, height) * 0.0017
            yPos = int(height / 20)
            cv2.putText(frame, frametext, (0, yPos), cv2.FONT_HERSHEY_SIMPLEX, fontScale, [255, 255, 255], 3,
                        cv2.FILLED)

        return frame

    def generate_frames(self, output=None, frameinfo=None):
        for i in range(0, self.sequence):
            if frameinfo:
                self.frames.append(
                    self.generate_random_frame(self.height, self.width, {'frame': i, 'totalframes': self.sequence}))
            else:
                self.frames.append(self.generate_random_frame(self.height, self.width))
            if output:
                output_file = "{output_path}/{frame}.tiff".format(output_path=output, frame=i)
                if cv2.haveImageWriter(output_file):
                    cv2.imwrite(output_file, self.frames[i], None)
            print("Generated frame {i}".format(i=i))

    def display_as_video(self):
        for frame in self.frames:
            cv2.namedWindow("Display", flags=cv2.WINDOW_GUI_NORMAL + cv2.WINDOW_AUTOSIZE)
            cv2.imshow("Display", frame)
            cv2.waitKey(16)
