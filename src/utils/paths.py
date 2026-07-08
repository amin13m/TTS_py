from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = ROOT / "models" / "xtts_v2"
VOICE_DIR = ROOT / "voices"
OUTPUT_DIR = ROOT / "output"
TEMP_DIR = ROOT / "temp"

CONFIG_FILE = MODEL_DIR / "config.json"
MODEL_FILE = MODEL_DIR / "model.pth"
VOCAB_FILE = MODEL_DIR / "vocab.json"