import imageio.v3 as iio
import os

source_folder = "images/"
output_name = "output.gif"
images = sorted([os.path.join(source_folder, f) for f in os.listdir(source_folder) if f.endswith(('.png', '.jpg'))])

start_duration = 120 
end_duration = 80     
num_frames = len(images)

durations = [
    start_duration - (i * (start_duration - end_duration) / (num_frames - 1))
    for i in range(num_frames)
]

frames = [iio.imread(img) for img in images]


iio.imwrite(output_name, frames, duration=durations, loop=0)

print("当前速度曲线：由 {}ms 减速至 {}ms".format(start_duration, end_duration))