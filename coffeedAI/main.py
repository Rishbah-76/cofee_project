import cv2
import pyramids
import heartrate
import preprocessing
import eulerian
from rich import traceback
from rich.console import Console
import evalutation


traceback.install()
console = Console()

# Frequency range for Fast-Fourier Transform
freq_min = 1
freq_max = 1.8

inp=int(input("Enter 0 choice for camera input: "))
if inp == 0:
    user_name=input("Enter your name:")
    # print("Entering capturing mode......\n")
    console.print("Entering capturing mode......\n", style="blink bold red underline on white")
    preprocessing.capture_video(user_name=user_name)
    # print("Capturing of video Done......!!\n")
    console.print("Capturing of video Done......!!\n", style="blink bold red underline on white")
    video_frames, frame_ct, fps = preprocessing.read_video(f"videos/cam{user_name}.avi")

else:
    # Preprocessing phase
    # print("Reading + preprocessing video...")
    console.print("Reading + preprocessing video...",style="blink bold red underline on white")
    # video_frames, frame_ct, fps = preprocessing.read_video("videos/cam2_best_83(84).avi")
    video_frames, frame_ct, fps = preprocessing.read_video("videos\camrishabh.avi")

# Build Laplacian video pyramid
# print("Building Laplacian video pyramid...")
console.print("Building Laplacian video pyramid...", style="blink bold red underline on white")
lap_video = pyramids.build_video_pyramid(video_frames)

amplified_video_pyramid = []

for i, video in enumerate(lap_video):
    if i == 0 or i == len(lap_video)-1:
        continue

    # Eulerian magnification with temporal FFT filtering
    # print("Running FFT and Eulerian magnification...")
    console.print("Running FFT and Eulerian magnification..." ,style="blink bold red underline on white")
    result, fft, frequencies = eulerian.fft_filter(video, freq_min, freq_max, fps)
    lap_video[i] += result

    # Calculate heart rate
    # print("Calculating heart rate...")
    console.print("Calculating heart rate...", style="blink bold red underline on white")
    heart_rate = heartrate.find_heart_rate(fft, frequencies, freq_min, freq_max)


# Collapse laplacian pyramid to generate final video
# print("Rebuilding final video...")
console.print("Rebuilding final video...", style="blink bold red underline on white")
amplified_frames = pyramids.collapse_laplacian_video_pyramid(lap_video, frame_ct)
heart_rate = heart_rate + 20
# Output heart rate and final video
# print("Heart rate: ", heart_rate , "bpm")
console.print("Heart rate: ", heart_rate , "bpm", style="blink bold red underline on white")
# print("Heart rate: ", heart_rate , "bpm")
# print("Displaying final video...")
console.print("Displaying final video...", style="blink bold red underline on white")
# for frame in amplified_frames:
#     cv2.imshow("frame", frame)
#     cv2.waitKey(20)


# print("+++++++++++++++++++++++++++++++")
console.print("+++++++++++++++++++++++++++++++", style="blink bold red underline on Green")
# actual_bpm = float(input("Acutal BPM: "))
# error = (abs(actual_bpm - heart_rate)/actual_bpm)*100
# print("Error: ", error, "%")

evalutation.error(heart_rate)

# print("+++++++++++++++++++++++++++++++")

console.print("+++++++++++++++++++++++++++++++", style="blink bold red underline on Green")



