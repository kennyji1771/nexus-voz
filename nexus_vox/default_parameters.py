from pathlib import Path

from nexus_vox.utils.utils import _ORIGINS_OF_PREDEFINED_VOICES

DEFAULT_LANGUAGE = "spanish_24l"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_SAMPLER_DECODE_STEPS = 1
DEFAULT_NOISE_CLAMP = None
DEFAULT_EOS_THRESHOLD = -4.0
DEFAULT_FRAMES_AFTER_EOS = 15  # colchón de frames para evitar EOS prematuro en español
# TODO: make this dynamic since english_2026-04 supports bigger chunks
MAX_TOKEN_PER_CHUNK = 50

DEFAULT_TEXT_FOR_LANGUAGE = {
    "english": (
        "Hello world. I am Nexus.Vox. "
        "I'm fast enough to run on small CPUs. "
        "I hope you'll like me."
    ),
    "french": (
        "Bonjour le monde. Je suis Nexus.Vox. "
        "Je suis assez rapide pour fonctionner sur de petits CPU. "
        "J'espère que vous m'aimerez."
    ),
    "german": (
        "Hallo Welt. Ich bin Nexus.Vox. "
        "Ich bin schnell genug, um auch auf kleinen CPUs zu laufen. "
        "Ich hoffe, ich gefalle dir."
    ),
    "portuguese": (
        "Olá mundo. Eu sou Nexus.Vox. "
        "Sou rápido o suficiente para rodar em CPUs pequenas. "
        "Espero que você goste de mim."
    ),
    "italian": (
        "Ciao mondo. Sono Nexus.Vox. "
        "Sono abbastanza veloce da funzionare su piccole CPU. "
        "Spero che ti piacerò."
    ),
    "spanish": (
        "Hola mundo. Soy Nexus Vox, tu asistente de voz en español latino. "
        "Funciono en CPUs pequeñas, sin necesidad de GPU. "
        "Espero que te guste."
    ),
}

DEFAULT_VOICE_FOR_LANGUAGE = {
    "italian": "giovanni",
    "spanish": "lola",
    "german": "juergen",
    "portuguese": "rafael",
    "french": "estelle",
}
DEFAULT_VOICE_FALLBACK = "alba"
# Predefined voices are states precomputed with the released weights of a language model,
# so neither a custom config nor a training checkpoint can use them. For those we default
# to the audio file behind the fallback voice: any model can clone it.
DEFAULT_VOICE_FOR_CUSTOM_MODEL = _ORIGINS_OF_PREDEFINED_VOICES[DEFAULT_VOICE_FALLBACK]

# Ruta a la voz clonada local del usuario (opcional).
# Si existe, se usará automáticamente como voz por defecto para español.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_LOCAL_VOICE_24L = _PROJECT_ROOT / "nexus_vox" / "voices" / "es-latam" / "kenny_ji_24l.safetensors"
# Nombre de display para logs y docs (el path físico usa guiones bajos).
DEFAULT_VOICE_DISPLAY_NAME = "Kenny.Ji"


def get_default_text_for_language(language: str | None) -> str:
    if language is None:
        language = DEFAULT_LANGUAGE
    for key, text in DEFAULT_TEXT_FOR_LANGUAGE.items():
        if key in language:
            return text
    return DEFAULT_TEXT_FOR_LANGUAGE[DEFAULT_LANGUAGE]


def get_default_voice_for_language(
    language: str | None, config: str | None = None, checkpoint: str | None = None
) -> str:
    """The voice to use when the user didn't pick one.

    `config` and `checkpoint` both mean custom weights, which cannot use the predefined
    voices, hence the audio file instead of the voice name.
    """
    if config is not None or checkpoint is not None:
        return DEFAULT_VOICE_FOR_CUSTOM_MODEL
    if language is None:
        language = DEFAULT_LANGUAGE
    # Prioridad 1: voz clonada local del usuario para español
    if "spanish" in language and _LOCAL_VOICE_24L.exists():
        return str(_LOCAL_VOICE_24L)
    # Prioridad 2: voz predefinida de Kyutai para el idioma (lola, etc.)
    for key, voice in DEFAULT_VOICE_FOR_LANGUAGE.items():
        if key in language:
            return voice
    return DEFAULT_VOICE_FALLBACK
