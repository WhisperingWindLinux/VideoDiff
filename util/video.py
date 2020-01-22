import cv2


class VideoDiff():
    def __init__(self, source):
        self.colortoindex = {
            "b": 0,
            "g": 1,
            "r": 2,
        }

        self.cap = cv2.VideoCapture(source)
        self.state = 'b'

    def __del__(self):
        # When everything done, release the capture
        cv2.destroyAllWindows()
        self.cap.release()

    @staticmethod
    def getKeyBind(key):
        if cv2.waitKey(1) and 0xFF == ord(key):
            return key

    def render(self):
        prevcolor = False
        while self.cap.isOpened():
            # Capture frame-by-frame
            ret, frame = self.cap.read()

            # Save the previous frame
            if prevcolor is not False:
                prevcolor = color


            # Need to validate if this is the proper way to extract subpixel values
            colorindex = self.colortoindex[self.state]
            color = frame[:, :, colorindex]

            # Display the resulting frame
            if prevcolor is not False:
                windowname = 'diff {}'.format(self.state)
                image = color - prevcolor
                cv2.imshow(windowname, image)
            else:
                prevcolor = color

            # quit when 'q' is pressed on the image window
            if self.getKeyBind('q'):
                break
            if self.getKeyBind('r'):
                self.state = 'r'
            if self.getKeyBind('g'):
                self.state = 'g'
            if self.getKeyBind('b'):
                self.state = 'b'
