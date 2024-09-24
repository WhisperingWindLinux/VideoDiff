

class ABaseProcessor:
    def __init__(self):
        self.window_name = None

    def process(self, display=True, output_path=None):
        raise AttributeError('Should be defined in subclass')

    def _render(self, capture_source):
        raise AttributeError('Should be defined in subclass')
