from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from faster_whisper import WhisperModel

import tempfile
import subprocess
import os

app = FastAPI()

# Load model once
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8",
    cpu_threads=12,
    num_workers=1,
)

# ==========================
# 1. VIDEO -> AUDIO
# ==========================

@app.post("/video-to-audio")
async def video_to_audio(file: UploadFile = File(...)):

    video_suffix = os.path.splitext(file.filename)[1]

    fd, video_path = tempfile.mkstemp(suffix=video_suffix)
    os.close(fd)

    audio_path = video_path + ".m4a"

    try:

        with open(video_path, "wb") as f:
            while chunk := await file.read(4 * 1024 * 1024):
                f.write(chunk)

        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",

            "-i", video_path,

            "-vn",

            "-c:a", "copy",

            audio_path,
            "-y",
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        # If copy fails (unsupported codec), encode AAC
        if result.returncode != 0:

            cmd = [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",

                "-i", video_path,

                "-vn",

                "-c:a", "aac",
                "-b:a", "64k",

                audio_path,
                "-y",
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise HTTPException(
                    status_code=500,
                    detail=result.stderr
                )

        return FileResponse(
            audio_path,
            media_type="audio/mp4",
            filename="audio.m4a",
            background=None
        )

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)


# ==========================
# 2. AUDIO -> TEXT
# ==========================

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    ext = os.path.splitext(file.filename)[1]

    fd, audio_path = tempfile.mkstemp(suffix=ext)
    os.close(fd)

    try:

        with open(audio_path, "wb") as f:
            while chunk := await file.read(4 * 1024 * 1024):
                f.write(chunk)

        segments, info = model.transcribe(
            audio_path,

            beam_size=1,

            vad_filter=True,

            condition_on_previous_text=False,
        )

        text = "".join(segment.text for segment in segments)

        return {
            "language": info.language,
            "duration": info.duration,
            "text": text.strip()
        }

    finally:

        if os.path.exists(audio_path):
            os.remove(audio_path)