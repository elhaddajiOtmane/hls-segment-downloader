import requests
import m3u8
import os
import sys
from urllib.parse import urljoin, urlparse
import re
from Crypto.Cipher import AES

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

def download_key(video_id, token):
    key_url = f"https://contentplayer.hotmart.com/video/{video_id}/mp4/key/{video_id}-1723812270000.key?{token}"
    headers = get_headers()
    response = requests.get(key_url, headers=headers)
    if response.status_code == 200:
        return response.content
    return None

def decrypt_segment(encrypted_data, key):
    try:
        # The IV is typically the first 16 bytes of the segment
        iv = encrypted_data[:16]
        encrypted_content = encrypted_data[16:]
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_content = cipher.decrypt(encrypted_content)
        
        # Remove PKCS7 padding
        padding_length = decrypted_content[-1]
        return decrypted_content[:-padding_length]
    except Exception as e:
        print(f"Error decrypting segment: {str(e)}")
        return None

def download_segment(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
        print(f"Failed to download segment: {response.status_code}")
        return None
    except Exception as e:
        print(f"Error downloading segment: {str(e)}")
        return None

def get_video_info(url):
    parsed = urlparse(url)
    path_parts = parsed.path.split('/')
    video_id = path_parts[2]
    token = parsed.query
    base_url = f"{parsed.scheme}://{parsed.netloc}/video/{video_id}/hls/"
    return video_id, token, base_url

def download_hotmart_video(initial_segment_url, start_segment=1, num_segments=100):
    headers = get_headers()
    video_id, token, base_url = get_video_info(initial_segment_url)
    
    # Download decryption key
    key = download_key(video_id, token)
    if not key:
        print("Failed to download decryption key")
        return False
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    ts_file = os.path.join(output_dir, "complete_video.ts")
    mp4_file = os.path.join(output_dir, "complete_video.mp4")
    
    # Extract quality information from the initial URL
    quality_match = re.search(r'audio=(\d+)-video=(\d+)', initial_segment_url)
    if not quality_match:
        print("Could not determine video quality from URL")
        return False
    
    audio_quality, video_quality = quality_match.groups()
    success_count = 0
    
    print(f"Starting download of {num_segments} segments...")
    
    # Open output file for writing
    with open(ts_file, 'wb') as outfile:
        for segment_num in range(start_segment, start_segment + num_segments):
            segment_url = f"{base_url}{video_id}-1723812270000-audio={audio_quality}-video={video_quality}-{segment_num}.ts?{token}"
            print(f"Downloading segment {segment_num}...")
            
            # Download and decrypt segment
            encrypted_data = download_segment(segment_url, headers)
            if encrypted_data:
                decrypted_data = decrypt_segment(encrypted_data, key)
                if decrypted_data:
                    outfile.write(decrypted_data)
                    success_count += 1
                    continue
            
            print(f"Failed to process segment {segment_num}, stopping...")
            break
    
    print(f"\nDownload complete. Successfully downloaded and decrypted {success_count} segments.")
    
    if success_count > 0:
        print("\nConverting TS file to MP4...")
        # Convert TS to MP4 using ffmpeg
        os.system(f'ffmpeg -i "{ts_file}" -c copy "{mp4_file}" -y')
        if os.path.exists(mp4_file):
            print(f"\nConversion successful! Video saved as: {mp4_file}")
            # Optionally remove the .ts file
            os.remove(ts_file)
        else:
            print("\nError: MP4 conversion failed")
    
    return success_count > 0

if __name__ == "__main__":
    # The direct video segment URL (use any segment URL as template)
    video_url = "https://vod-akm.play.hotmart.com/video/Yq4yWl8bLl/hls/Yq4yWl8bLl-1723812270000-audio=89736-video=263000-45.ts?hdntl=exp=1733070219~acl=/*~data=hdntl~hmac=f3e59eadfa310b1906db06aa5850f081bc8c5203010fa0a8644f65564b4edbd8&app=aa2d356b-e2f0-45e8-9725-e0efc7b5d29c"
    
    # Start downloading from segment 1, try to get 100 segments
    download_hotmart_video(video_url, start_segment=1, num_segments=100)
