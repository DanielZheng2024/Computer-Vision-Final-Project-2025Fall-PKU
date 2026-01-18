import cv2
import numpy as np
import imageio
import os

INPUT_IMAGE = "anamorphic_wood.png" 
OUTPUT_GIF = "anamorphic_illusion_2_pause.gif"

FRAMES = 30         # how many frames for the transition
FPS = 15            # speed
TARGET_SCALE = 0.35 # scale by which reduced
PAUSE_SECONDS = 1.0 # how long to pause at the bottom

def create_anamorphic_gif():
    # read the pic
    if not os.path.exists(INPUT_IMAGE):
        print(f"Error: File not found {INPUT_IMAGE}")
        return

    img_bgr = cv2.imread(INPUT_IMAGE)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    height, width = img_rgb.shape[:2]
    frames = []

    print(f"size: {width}x{height}")
    print("Generating transition frames...")

    # Generate forward transition frames (from original -> illusion)
    scales = np.linspace(1.0, TARGET_SCALE, FRAMES)

    for current_scale in scales:
        # Perspective transform logic
        dst_pts = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        
        center_x = width / 2
        bottom_width_half = (width * current_scale) / 2
        
        src_pts = np.float32([
            [0, 0], [width, 0],
            [center_x - bottom_width_half, height], 
            [center_x + bottom_width_half, height]
        ])

        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(img_rgb, M, (width, height))
        frames.append(warped)

    # pause demo for better visualization
    pause_frame_count = int(FPS * PAUSE_SECONDS)
    
    # capture last frame and generate a bunch of frames alike
    last_frame = frames[-1]
    pause_sequence = [last_frame] * pause_frame_count
    
    # Combine final sequence: [transition] + [pause] + [reverse transition]
    final_frames = frames + pause_sequence + frames[::-1]

    # save the gif
    print(f"Saving GIF to {OUTPUT_GIF} ...")
    imageio.mimsave(OUTPUT_GIF, final_frames, fps=FPS, loop=0)
    print("gif saved successfully.")

if __name__ == "__main__":
    create_anamorphic_gif()