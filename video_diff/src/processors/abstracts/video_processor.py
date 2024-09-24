import cv2
from concurrent.futures import ThreadPoolExecutor, as_completed

from video_diff.src.processors.abstracts.base_processor import ABaseProcessor


class AVideoProcessor(ABaseProcessor):
    def __init__(self, source):
        super().__init__()
        self.cap = cv2.VideoCapture(source)
        self._tdict = {}
        self._tpe = ThreadPoolExecutor()

    def __del__(self):
        # When everything done, release the capture
        cv2.destroyAllWindows()
        self.cap.release()

    @staticmethod
    def _save_frame(i, frame, output):
        if cv2.haveImageWriter(output):
            return cv2.imwrite(output, frame, None)

    def process(self, display=True, output_path=None):
        try:
            if display is True:
                cv2.namedWindow(self.window_name, flags=cv2.WINDOW_GUI_NORMAL + cv2.WINDOW_AUTOSIZE)

            for vimage in self._render(self.cap):
                if display is True:
                    cv2.imshow(self.window_name, vimage)
                if output_path is not None:
                    i = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                    output_file = "{output_path}/{frame}.tiff".format(output_path=output_path, frame=i)
                    self._tdict.update({self._tpe.submit(self._save_frame, i, vimage, output_file): i})

            for f in as_completed(self._tdict):
                if not f.result():
                    print("Error writing frame {i}".format(i=self._tdict[f]))

        except KeyboardInterrupt:
            print("\nExiting")
            exit(0)

    def _render(self, capture_source):
        raise AttributeError('Should be defined in subclass')


