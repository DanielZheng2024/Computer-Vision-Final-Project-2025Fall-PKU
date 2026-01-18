import cv2
import numpy as np
import imageio
import os

INPUT_IMAGE = "cylinder_illusion_flat.png"
OUTPUT_GIF = "cylinder_reflection_demo.gif"

# Animation parameters
FRAMES = 80          # frames for the transition
FPS = 20             # speed
PAUSE_SECONDS = 1.5  # how long to pause at result
# Geometric parameters (must match generation settings)
CYLINDER_RADIUS = 0.2
R_MAX = 0.98
VIEW_ANGLE = 180

def create_cylinder_demo():
    # Read the image
    if not os.path.exists(INPUT_IMAGE):
        print(f"Error: File not found {INPUT_IMAGE}")
        return

    img_bgr = cv2.imread(INPUT_IMAGE)
    # OpenCV reads as BGR, convert to RGB
    if img_bgr is None:
        print(f"Error: Unable to read image {INPUT_IMAGE}")
        return

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    height, width = img_rgb.shape[:2]
    frames = []

    print(f"Size: {width}x{height}")
    print("Generating Cylinder Illusion transition frames...")

    # Prepare coordinate grid
    # Create coordinate system (u, v) for reflection view
    # u, v range from -1 to 1
    nx, ny = width, height
    x_range = np.linspace(-1, 1, nx)
    y_range = np.linspace(-1, 1, ny)
    
    xv, yv = np.meshgrid(x_range, y_range) 

    # Define unified ux, uy
    ux = xv
    uy = yv
    
    # Final State: Cylindrical Reflection View (Polar Logic)
    angle_half_rad = np.deg2rad(VIEW_ANGLE / 2)
    theta_cyl = ux * angle_half_rad - (np.pi / 2.0)
    
    # uy=-1 (Top) -> r_min. uy=1 (Bottom) -> r_max.
    radius_cyl = CYLINDER_RADIUS + ((uy + 1) / 2) * (R_MAX - CYLINDER_RADIUS)
    
    # At initial state, source sampling point is (ux, uy)
    radius_flat = np.sqrt(ux**2 + uy**2)
    theta_flat = np.arctan2(uy, ux)

    # 3. Generate Transition Frames (Polar Interpolation)
    # Polar interpolation simulates "unrolling/rolling" effect
    t_values = np.linspace(0, 1, FRAMES)
    
    # Helper: calculate minimal angular difference (dst - src)
    def angular_diff(a_dst, a_src):
        diff = a_dst - a_src
        # Normalize to [-pi, pi]
        diff = (diff + np.pi) % (2 * np.pi) - np.pi
        return diff

    diff_theta = angular_diff(theta_cyl, theta_flat)

    for i, t in enumerate(t_values):
        # Polar interpolation
        curr_radius = (1 - t) * radius_flat + t * radius_cyl
        curr_theta = theta_flat + t * diff_theta
        
        # Convert back to Cartesian (Normalized [-1, 1])
        curr_map_x_norm = curr_radius * np.cos(curr_theta)
        curr_map_y_norm = curr_radius * np.sin(curr_theta)
        
        # Map normalized [-1, 1] to pixel coords [0, W-1], [0, H-1]
        map_x = ((curr_map_x_norm + 1) / 2 * (width - 1)).astype(np.float32)
        map_y = ((curr_map_y_norm + 1) / 2 * (height - 1)).astype(np.float32)
        
        # Remap
        warped = cv2.remap(img_rgb, map_x, map_y, 
                           interpolation=cv2.INTER_LINEAR, 
                           borderMode=cv2.BORDER_CONSTANT, 
                           borderValue=(0,0,0))
        frames.append(warped)
        if i % 10 == 0:
            print(f"   Processing frame {i}/{FRAMES}...")

    # 4. Add pause and reverse
    pause_frame_count = int(FPS * PAUSE_SECONDS)
    
    last_frame = frames[-1]
    pause_sequence = [last_frame] * pause_frame_count
    
    # Sequence: Transition -> Pause -> Reverse
    final_frames = frames + pause_sequence + frames[::-1]

    # 5. Save GIF
    print(f"Saving GIF to {OUTPUT_GIF} ...")
    imageio.mimsave(OUTPUT_GIF, final_frames, fps=FPS, loop=0)
    print("Gif saved successfully.")

if __name__ == "__main__":
    create_cylinder_demo()
