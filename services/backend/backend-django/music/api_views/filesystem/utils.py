from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE
from datetime import datetime
from typing import List
import re


class Metadata:
    def __init__(self):
        self.album: str = None
        self.artist: str = None
        self.thumbnail: str = None
        self.album_release_date: int = None
        self.genre: List[str] = []
        self.track_duration: str = None
        self.track_number: str = None
        self.bpm: int = None


def get_metadata(file_path) -> Metadata:
    """
    Extract metadata from audio file
    :param str file path
    :return Metadata
    :throws MutagenError
    """
    metadata = Metadata()
    if file_path.endswith(".mp3"):
        audio = MP3(file_path)
    elif file_path.endswith(".ogg"):
        audio = OggVorbis(file_path)
    elif file_path.endswith(".wav"):
        audio = WAVE(file_path)
    else:
        return metadata

    try:
        metadata.album = audio.get("TALB", [None])[0]
    except Exception as e:
        print(f"{file_path}: Album extraction error : {e}")
    try:
        metadata.artist = audio.get("TPE1", [None])[0]
    except Exception as e:
        print(f"{file_path}: Artist extraction error : {e}")
    # TODO manage thumbnail, could be one per album, or one per file, or none
    try:
        apic = audio.get("APIC", [None])[0]
        if apic:
            if isinstance(apic, list):
                metadata.thumbnail = apic[0]
            else:
                metadata.thumbnail = apic
    except Exception as e:
        print(f"{file_path}: Thumbnail did not load : {e}")

    try:
        date_raw = audio.get("TDRC", [None])[0]
        date_string = str(date_raw)
        if date_raw and date_string:
            metadata.album_release_date = (
                datetime.strptime(date_string, "%Y").date().year
            )
        else:
            metadata.album_release_date = None
    except Exception as e:
        print(f"{file_path}: Release date album extraction error : {e}")

    try:
        metadata.genre = [
            tcon.strip()
            for tcon in re.split(r"[/,;]", audio.get("TCON", [""])[0])
            if tcon and len(tcon.strip()) > 0
        ]
    except Exception as e:
        print(f"{file_path}: Genre extraction error : {e}")
    try:
        metadata.track_duration = audio.info.length
    except Exception as e:
        print(f"{file_path}: Track duration extraction error : {e}")
    try:
        metadata.track_number = audio.get("TRCK", [None])[0]
    except Exception as e:
        print(f"{file_path}: Track number extraction error : {e}")
    try:
        metadata.bpm = int(float(audio.get("TBPM", [0])[0]))
    except Exception as e:
        print(f"{file_path}: BPM extraction error : {e}")
    return metadata
