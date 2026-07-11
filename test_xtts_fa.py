from TTS.utils.synthesizer import Synthesizer

tts = Synthesizer(
    tts_checkpoint=r"D:\Projects\tts_py\models\persian_vits\model.pth",
    tts_config_path=r"D:\Projects\tts_py\models\persian_vits\config.json",
    use_cuda=False,
)

tts.save_wav(
    tts.tts("سلام، این یک تست از موتور فارسی است."),
    "test.wav"
)

print("DONE")