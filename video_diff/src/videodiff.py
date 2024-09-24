import argparse
import os
from sys import argv, exit

from video_diff.src.processors.processor_factory import ProcessorFactory


def process_cmd_args():
    parser = argparse.ArgumentParser(description="Compare frames from a video or capture device")

    parser.add_argument("--fill-value", type=int, default=255, help="Fill value for detected image changes.")
    parser.add_argument("--processors-method", "-x", default="g", choices=("r", "g", "b", "a", "m", "n"),
                        help="Dither detection method")
    parser.add_argument("--mode", "-m", default="dithering", choices=("simple_dithering", "spatial_dithering", "image"),
                        help="Operation mode: dithering or image comparison")
    parser.add_argument("--display", "-d", action='store_true', default=False, help="Display output")
    parser.add_argument("--output", "-o", type=str, help="Output directory for sequential image output")
    parser.add_argument("--pause", '-p', action='store_true', default=False, help="Pause at start")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--cap", type=int, help="Index value of cv2.VideoCapture device")
    group.add_argument("--file", type=str, nargs="*", help="Path to AVI file(s)")

    if len(argv) < 2:
        parser.print_usage()
        exit(1)

    args = parser.parse_args()

    if args.output and not os.path.exists(args.output):
        try:
            os.makedirs(args.output)
        except Exception as e:
            error_str = str.format("Unable to create directory: {0}", e)
            raise RuntimeError(error_str)

        if os.path.exists(f"{args.output}/2.tiff"):
            raise RuntimeError("Refusing to overwrite existing capture output")

    processor = ProcessorFactory.create_processor(
        args.mode,
        args.file,
        args.cap,
        args.processors_method,
        args.fill_value,
        args.pause
    )
    processor.process(display=args.display, output_path=args.output)


def main():
    try:
        process_cmd_args()
    except RuntimeError as e:
        print(e)
        exit(1)

    print("The application has completed successfully!")


if __name__ == '__main__':
    main()
