import numpy as np
import imageio
import argparse

# Video parameters
width, height = 640, 480
num_frames = 60
frame_rate = 30


def create_frame(frame_index, bit_depth, color, dither_intensity):
    # Generate a single color frame
    max_value = (2 ** bit_depth) - 1

    if bit_depth > 8:
        frame = np.full((height, width, 3), color, dtype=np.uint16)
    else:
        frame = np.full((height, width, 3), color, dtype=np.uint8)

    # Apply dithering if intensity is greater than 0
    if dither_intensity > 0:
        noise_level = int(max_value * (dither_intensity / 100.0))
        noise = np.random.randint(-noise_level, noise_level + 1, (height, width, 3), dtype=np.int16)
        frame = np.clip(frame.astype(np.int16) + noise, 0, max_value).astype(frame.dtype)

    return frame


def create_video(bit_depth, color, dither_intensity):
    output_filename = f'output_video_{bit_depth}bit_dither_{dither_intensity}.mp4'

    if bit_depth == 8:
        writer = imageio.get_writer(output_filename, fps=frame_rate, codec='libx264', quality=10)
    elif bit_depth == 10 or bit_depth == 12:
        writer = imageio.get_writer(output_filename, fps=frame_rate, codec='hevc', quality=10)

    for frame_index in range(num_frames):
        frame = create_frame(frame_index, bit_depth, color, dither_intensity)

        # Convert the frame to the appropriate dtype for writing
        if bit_depth == 8:
            frame = frame.astype(np.uint8)
        else:
            frame = (frame / 256).astype(np.uint8)  # Downscale to 8-bit for writing

        writer.append_data(frame)

    writer.close()
    print(f"Video saved to file {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create videos with different bit depths and dithering intensities.')
    parser.add_argument('bit_depths', metavar='N', type=int, nargs='+',
                        help='an integer for the bit depth (e.g., 8, 10, 12)')
    parser.add_argument('--color', type=int, nargs=3, default=[128, 128, 128],
                        help='RGB color values (e.g., --color 128 128 128)')
    parser.add_argument('--dither_intensity', type=float, default=0,
                        help='dithering intensity from 0 to 100')

    args = parser.parse_args()

    for bit_depth in args.bit_depths:
        create_video(bit_depth, args.color, args.dither_intensity)