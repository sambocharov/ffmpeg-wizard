import os
import subprocess

def convert_to_webm(input_folder, temp_folder):
    os.makedirs(temp_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".mp4"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(temp_folder, filename.rsplit('.', 1)[0] + ".webm")
            
            command = [
                "ffmpeg", "-i", input_path, "-c:v", "libvpx-vp9", "-b:v", "1M", "-c:a", "libopus", output_path
            ]
            
            subprocess.run(command, check=True)
            print(f"Converted to WebM: {filename}")

def process_videos(temp_folder, output_folder, speedup_factor=1.0):
    os.makedirs(output_folder, exist_ok=True)
    speedup_pts = 1.0 / speedup_factor  
    
    for filename in os.listdir(temp_folder):
        if filename.lower().endswith(".webm"):
            input_path = os.path.join(temp_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            command = [
                "ffmpeg", "-i", input_path, "-vf", f"scale=512:512,setpts={speedup_pts}*PTS", "-an", "-c:v", "libvpx-vp9", "-b:v", "500k", "-crf", "30", "-r", "24", output_path
            ]
            
            subprocess.run(command, check=True)
            print(f"Processed: {filename}")

if __name__ == "__main__":
    input_folder = "./videos"  
    temp_folder = "./temp"  
    output_folder = "./result_videos"  
    speedup_factor = 1  

    convert_to_webm(input_folder, temp_folder)
    process_videos(temp_folder, output_folder, speedup_factor)
