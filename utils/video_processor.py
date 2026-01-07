"""
Video Processing Utilities

Helper functions for video processing and manipulation.
"""

from pathlib import Path
from typing import Optional, Tuple
from PIL import Image
import logging

logger = logging.getLogger(__name__)


def resize_image(
    image_path: Path,
    output_path: Path,
    width: int,
    height: int,
    maintain_aspect: bool = False
) -> Path:
    """
    Resize image to specified dimensions.
    
    Args:
        image_path: Input image path
        output_path: Output image path
        width: Target width
        height: Target height
        maintain_aspect: Whether to maintain aspect ratio
    
    Returns:
        Output file path
    """
    img = Image.open(image_path)
    
    if maintain_aspect:
        img.thumbnail((width, height), Image.LANCZOS)
    else:
        img = img.resize((width, height), Image.LANCZOS)
    
    img.save(output_path)
    return output_path


def generate_thumbnail(video_path: Path, output_path: Path, timestamp: float = 1.0) -> Path:
    """
    Generate thumbnail from video.
    
    Args:
        video_path: Input video path
        output_path: Output thumbnail path
        timestamp: Timestamp in seconds to capture
    
    Returns:
        Output thumbnail path
    """
    try:
        from moviepy.editor import VideoFileClip
        
        video = VideoFileClip(str(video_path))
        timestamp = min(timestamp, video.duration - 0.1)
        video.save_frame(str(output_path), t=timestamp)
        video.close()
        
        return output_path
    except Exception as e:
        logger.error(f"Error generating thumbnail: {str(e)}")
        raise


def get_video_info(video_path: Path) -> dict:
    """
    Get video information.
    
    Args:
        video_path: Video file path
    
    Returns:
        Dictionary with video info (duration, width, height, fps)
    """
    try:
        from moviepy.editor import VideoFileClip
        
        video = VideoFileClip(str(video_path))
        info = {
            "duration": video.duration,
            "width": video.w,
            "height": video.h,
            "fps": video.fps
        }
        video.close()
        
        return info
    except Exception as e:
        logger.error(f"Error getting video info: {str(e)}")
        raise


def compress_video(
    input_path: Path,
    output_path: Path,
    bitrate: str = "5000k",
    preset: str = "medium"
) -> Path:
    """
    Compress video for web.
    
    Args:
        input_path: Input video path
        output_path: Output video path
        bitrate: Target bitrate
        preset: FFmpeg preset
    
    Returns:
        Output file path
    """
    try:
        from moviepy.editor import VideoFileClip
        
        video = VideoFileClip(str(input_path))
        video.write_videofile(
            str(output_path),
            bitrate=bitrate,
            preset=preset,
            codec='libx264',
            audio_codec='aac'
        )
        video.close()
        
        return output_path
    except Exception as e:
        logger.error(f"Error compressing video: {str(e)}")
        raise
