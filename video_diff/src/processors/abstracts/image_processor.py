import cv2

from video_diff.src.processors.abstracts.base_processor import ABaseProcessor


class AImageProcessor(ABaseProcessor):
    def __init__(self, source):
        super().__init__()
        self.frame_a = cv2.imread(source[0])
        self.frame_b = cv2.imread(source[1])

    def __del__(self):
        # When everything done, release the capture
        cv2.destroyAllWindows()

    def process(self, display=True, output_path=None):
        try:
            if display is True:
                cv2.namedWindow(self.window_name, flags=cv2.WINDOW_GUI_NORMAL + cv2.WINDOW_AUTOSIZE)
            while True:
                for image in self._render(self.source):
                    if output_path is not None:
                        if cv2.haveImageWriter(output_path):
                            cv2.imwrite(output_path, image, None)
                    if display:
                        cv2.imshow(self.window_name, image)
                    else:
                        exit(0)

        except KeyboardInterrupt:
            print("\nExiting")
            exit(0)

    def _render(self, capture_source):
        raise AttributeError('Should be defined in subclass')