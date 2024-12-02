# HLS Segment Downloader

This project allows you to download and combine HLS video segments into a single video file.

## Setting Up the Environment

1. Clone the repository:
   ```sh
   git clone https://github.com/elhaddajiOtmane/hls-segment-downloader.git
   cd hls-segment-downloader
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Project

To run the project, execute the `download_video_v3.py` script:

```sh
python download_video_v3.py
```

## Downloading a Video

To download a video, place its URL in the `video_url` variable in the `download_video_v3.py` script:

```python
# The direct video segment URL (use any segment URL as template)
video_url = "https://vod-akm.play.hotmart.com/video/Yq4yWl8bLl/hls/Yq4yWl8bLl-1723812270000-audio=89736-video=263000-45.ts?hdntl=exp=1733070219~acl=/*~data=hdntl~hmac=f3e59eadfa310b1906db06aa5850f081bc8c5203010fa0a8644f65564b4edbd8&app=aa2d356b-e2f0-45e8-9725-e0efc7b5d29c"
```

Then run the script to start downloading the video segments and combine them into a single video file.
