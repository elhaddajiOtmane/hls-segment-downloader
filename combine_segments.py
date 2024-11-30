import os
import glob

def combine_ts_segments(output_filename="complete_video.ts"):
    # Get all .ts files in the video_segments directory
    segments = sorted(glob.glob("video_segments/*.ts"))
    
    if not segments:
        print("No video segments found!")
        return False
    
    print(f"Found {len(segments)} segments. Combining them...")
    
    # Combine all segments into one file
    with open(output_filename, 'wb') as outfile:
        for segment in segments:
            print(f"Adding segment: {segment}")
            with open(segment, 'rb') as infile:
                outfile.write(infile.read())
    
    print(f"\nAll segments combined into {output_filename}")
    return True

if __name__ == "__main__":
    combine_ts_segments()
