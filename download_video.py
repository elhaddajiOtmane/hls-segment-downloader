import requests
import m3u8
import os
import sys
from urllib.parse import urljoin

def download_video_segment(url, output_path, headers=None):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

def download_hotmart_video(video_url, output_filename="output.ts"):
    # Extract the base URL and parameters
    base_url = video_url.split('/hls/')[0] + '/hls/'
    
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    try:
        # Download the segment
        print(f"Downloading video segment...")
        success = download_video_segment(video_url, output_filename, headers)
        
        if success:
            print(f"Successfully downloaded video to {output_filename}")
        else:
            print("Failed to download video segment")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    # The direct video segment URL
    video_url = "https://vod-akm.play.hotmart.com/video/Yq4yWl8bLl/hls/Yq4yWl8bLl-1723812270000-audio=89736-video=263000-45.ts?hdntl=exp=1733070219~acl=/*~data=hdntl~hmac=f3e59eadfa310b1906db06aa5850f081bc8c5203010fa0a8644f65564b4edbd8&app=aa2d356b-e2f0-45e8-9725-e0efc7b5d29c"
    
    # Download the video
    download_hotmart_video(video_url, "cantrill_course_video.ts")
