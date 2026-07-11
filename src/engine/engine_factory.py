class EngineFactory:

    @staticmethod
    def create(config):

        name = config.get(
            "tts",
            "engine"
        ).lower()


        if name == "f5":

            from src.engine.f5_engine import F5Engine
            return F5Engine(config)


        if name == "xtts":

            from src.engine.xtts_engine import XTTSEngine
            return XTTSEngine(config)


        if name == "mana":

            from src.engine.mana_engine import ManaEngine
            return ManaEngine(config)
        
        
        if name == "vits_fa":

            from src.engine.vits_fa_engine import PersianVITSEngine

            return PersianVITSEngine(config)


        raise RuntimeError(
            f"Unknown TTS engine: {name}"
        )