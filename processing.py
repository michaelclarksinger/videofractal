import cv2
import numpy as np
from moviepy.editor import VideoFileClip, vfx

def kaleidoscope(frame, segments=6):
    """Apply a simple kaleidoscope effect by averaging rotated copies."""
    h, w = frame.shape[:2]
    center = (w / 2, h / 2)
    result = np.zeros_like(frame, dtype=np.float32)
    for i in range(segments):
        angle = 360 / segments * i
        m = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(frame, m, (w, h))
        result += rotated.astype(np.float32) / segments
    return np.clip(result, 0, 255).astype('uint8')

def mirror_fractal(frame):
    """Create a 4-way mirrored fractal pattern."""
    h, w = frame.shape[:2]
    top_left = frame
    top_right = cv2.flip(frame, 1)
    bottom_left = cv2.flip(frame, 0)
    bottom_right = cv2.flip(frame, -1)
    top = np.concatenate([top_left, top_right], axis=1)
    bottom = np.concatenate([bottom_left, bottom_right], axis=1)
    return np.concatenate([top, bottom], axis=0)

def process_video(input_path, output_path, effect="kaleidoscope", segments=6, speed=1.0):
    """Process a video with the selected effect and speed."""
    clip = VideoFileClip(input_path)

    def process(frame):
        if effect == "mirror":
            return mirror_fractal(frame)
        return kaleidoscope(frame, segments=segments)

    processed = clip.fl_image(process)
    if speed != 1.0:
        processed = processed.fx(vfx.speedx, factor=speed)
    processed.write_videofile(output_path, audio=False)
