"""
Audio Processing Utilities

Helper functions for audio processing and manipulation.
"""

from pathlib import Path
from typing import Optional, Tuple
from pydub import AudioSegment
import logging

logger = logging.getLogger(__name__)


def normalize_audio(audio_path: Path, target_dBFS: float = -20.0) -> AudioSegment:
    """
    Normalize audio to target dBFS level.
    
    Args:
        audio_path: Path to audio file
        target_dBFS: Target dBFS level
    
    Returns:
        Normalized AudioSegment
    """
    audio = AudioSegment.from_file(str(audio_path))
    change_in_dBFS = target_dBFS - audio.dBFS
    normalized_audio = audio.apply_gain(change_in_dBFS)
    return normalized_audio


def trim_audio(audio_path: Path, start_time: float, end_time: float) -> AudioSegment:
    """
    Trim audio to specified time range.
    
    Args:
        audio_path: Path to audio file
        start_time: Start time in seconds
        end_time: End time in seconds
    
    Returns:
        Trimmed AudioSegment
    """
    audio = AudioSegment.from_file(str(audio_path))
    start_ms = int(start_time * 1000)
    end_ms = int(end_time * 1000)
    trimmed = audio[start_ms:end_ms]
    return trimmed


def adjust_volume(audio_path: Path, volume_change_db: float) -> AudioSegment:
    """
    Adjust audio volume.
    
    Args:
        audio_path: Path to audio file
        volume_change_db: Volume change in dB (positive = louder, negative = quieter)
    
    Returns:
        Adjusted AudioSegment
    """
    audio = AudioSegment.from_file(str(audio_path))
    adjusted = audio.apply_gain(volume_change_db)
    return adjusted


def get_audio_duration(audio_path: Path) -> float:
    """
    Get audio duration in seconds.
    
    Args:
        audio_path: Path to audio file
    
    Returns:
        Duration in seconds
    """
    audio = AudioSegment.from_file(str(audio_path))
    return len(audio) / 1000.0


def convert_audio_format(
    audio_path: Path,
    output_path: Path,
    format: str = "mp3",
    bitrate: str = "192k"
) -> Path:
    """
    Convert audio to different format.
    
    Args:
        audio_path: Input audio file path
        output_path: Output audio file path
        format: Output format (mp3, wav, etc.)
        bitrate: Bitrate for output
    
    Returns:
        Output file path
    """
    audio = AudioSegment.from_file(str(audio_path))
    audio.export(str(output_path), format=format, bitrate=bitrate)
    return output_path
