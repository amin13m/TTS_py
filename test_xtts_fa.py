from TTS.utils.synthesizer import Synthesizer


MODEL = r"D:\Projects\tts_py\models\persian_vits\model.pth"
CONFIG = r"D:\Projects\tts_py\models\persian_vits\config.json"


print("Loading model...")

tts = Synthesizer(
    tts_checkpoint=MODEL,
    tts_config_path=CONFIG,
    use_cuda=False
)

print("Model loaded")


text = "سلام دنیا. این یک آزمایش تولید صدای فارسی است."

wav = tts.tts(text)

tts.save_wav(
    wav,
    r"D:\Projects\tts_py\test_farsi.wav"
)

print("DONE")