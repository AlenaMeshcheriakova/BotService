import os
import gettext

SUPPORTED_LANGUAGE = ["ru_RU", "en_US"]

def active_translation(lang: str):
    global _default_lang
    _default_lang = (
        "ru_RU" if lang not in SUPPORTED_LANGUAGE else lang
    )

def trans(message: str) -> str:
    # Get the directory containing the current script
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # Set localedir to point to the 'locale' directory
    localedir = os.path.join(current_dir, '..', '..', 'locale')

    # Ensure the localedir path is absolute
    localedir = os.path.abspath(localedir)

    try:
        return gettext.translation(
            "botService", localedir=localedir, languages=[_default_lang]
        ).gettext(message)
    except NameError as name_ex:
        return gettext.translation(
            "botService", localedir=localedir, languages=["en_US"]
        ).gettext(message)