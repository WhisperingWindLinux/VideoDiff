from video_diff.src.processors.abstracts.video_processor import AVideoProcessor


class SpatialDitheringDetector(AVideoProcessor):
    def __init__(self, source, fill_value=0, state="g", frame_by_frame=False):
        super(SpatialDitheringDetector, self).__init__(source=source)
        self.window_name = "SpatialDitheringDetector"
        self.fill_value = fill_value
        self.state = state
        self.frame_by_frame = frame_by_frame
        self.need_render = True

    def _render(self, capture_source):
        raise RuntimeError("Not implemented")
