import argparse

from generators.src.frame_generator.frame_generator import FrameGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Generate frames of random noise and display or save to .TIFF",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--seed",
        "-s",
        type=int,
        default=12345,
        help="Seed to use for generating random frames",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="randomnoise",
        help="Directory to save output frames",
    )
    parser.add_argument(
        "--frames",
        type=int,
        default=120,
        help="Number of frames to generate",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=640,
        help="Width of generated frames",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=480,
        help="Height of generated frames",
    )
    parser.add_argument(
        "--mode",
        choices=("output", "display"),
        default="output",
        help="Mode of operation",
    )
    parser.add_argument(
        "--frameinfo",
        action="store_true",
        default=False,
        help="Whether to overlay frame number markings on output",
    )

    args = parser.parse_args()
    fg = FrameGenerator(args.frames, args.width, args.height, args.seed)
    fg.generate_frames(args.output, args.frameinfo)
    if args.mode == 'display':
        fg.display_as_video()


if __name__ == '__main__':
    main()
