import requests
import m3u8
import os
import sys
from urllib.parse import urljoin, urlparse
import re

def get_headers():
    return {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.5",
        "origin": "https://player.hotmart.com",
        "referer": "https://player.hotmart.com/",
        "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

def download_segment(url, output_path, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        print(f"Failed to download segment: {response.status_code}")
        return False
    except Exception as e:
        print(f"Error downloading segment: {str(e)}")
        return False

def get_video_info(url):
    # Extract video ID and token from URL
    parsed = urlparse(url)
    path_parts = parsed.path.split('/')
    video_id = path_parts[2]
    token = parsed.query
    base_url = f"{parsed.scheme}://{parsed.netloc}/video/{video_id}/hls/"
    return video_id, token, base_url

def download_hotmart_video(initial_segment_url, start_segment=1, num_segments=100):
    headers = get_headers()
    video_id, token, base_url = get_video_info(initial_segment_url)
    
    # Create output directory
    os.makedirs("video_segments", exist_ok=True)
    
    # Extract quality information from the initial URL
    quality_match = re.search(r'audio=(\d+)-video=(\d+)', initial_segment_url)
    if not quality_match:
        print("Could not determine video quality from URL")
        return False
    
    audio_quality, video_quality = quality_match.groups()
    success_count = 0
    
    print(f"Starting download of {num_segments} segments...")
    for segment_num in range(start_segment, start_segment + num_segments):
        segment_url = f"{base_url}{video_id}-1723812270000-audio={audio_quality}-video={video_quality}-{segment_num}.ts?{token}"
        output_path = f"video_segments/segment_{segment_num:03d}.ts"
        
        print(f"Downloading segment {segment_num}...")
        if download_segment(segment_url, output_path, headers):
            success_count += 1
        else:
            print(f"Failed to download segment {segment_num}, stopping...")
            break
    
    print(f"\nDownload complete. Successfully downloaded {success_count} segments.")
    return success_count > 0

if __name__ == "__main__":
    # The direct video segment URL (use any segment URL as template)
    video_url = "https://vod-akm.play.hotmart.com/video/Yq4yWl8bLl/hls/Yq4yWl8bLl-1723812270000-audio=89736-video=263000-45.ts?hdntl=exp=1733070219~acl=/*~data=hdntl~hmac=f3e59eadfa310b1906db06aa5850f081bc8c5203010fa0a8644f65564b4edbd8&app=aa2d356b-e2f0-45e8-9725-e0efc7b5d29c"
    
    # Start downloading from segment 1, try to get 100 segments
    download_hotmart_video(video_url, start_segment=1, num_segments=100)
