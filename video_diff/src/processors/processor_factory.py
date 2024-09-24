from video_diff.src.processors.abstracts.base_processor import ABaseProcessor
from video_diff.src.processors.image_comparator import ImageComparator
from video_diff.src.processors.simple_dithering_detector import SimpleDitheringDetector
from video_diff.src.processors.spatial_dithering_detector import SpatialDitheringDetector


class ProcessorFactory:
    @staticmethod
    def create_processor(mode, file, cap, processors_method, fill_value, pause) -> ABaseProcessor:
        if mode == "simple_dithering":
            if len(file) > 1:
                raise RuntimeError("Only one file is allowed for dithering mode")
            source = cap if cap is not None else file[0]
            processor = SimpleDitheringDetector(source, fill_value=fill_value, state=processors_method,
                                                frame_by_frame=pause)

        elif mode == "spatial_dithering":
            if len(file) > 1:
                raise RuntimeError("Only one file is allowed for dithering mode")
            source = cap if cap is not None else file[0]
            processor = SpatialDitheringDetector(source, fill_value=fill_value, state=processors_method,
                                                 frame_by_frame=pause)

        elif mode == 'image':
            if len(file) != 2:
                print("Need two files for image differentiation mode")
            processor = ImageComparator(file, fill_value=fill_value, state=processors_method)
        else:
            raise RuntimeError("Illegal processor method")

        return processor
