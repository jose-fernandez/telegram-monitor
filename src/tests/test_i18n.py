from src.utils.i18n import TRANSLATIONS

def test_translation_keys_match():
    en_keys = set(TRANSLATIONS['en'].keys())
    es_keys = set(TRANSLATIONS['es'].keys())
    
    missing_in_es = en_keys - es_keys
    missing_in_en = es_keys - en_keys
    
    assert not missing_in_es, f"Missing keys in ES translation: {missing_in_es}"
    assert not missing_in_en, f"Missing keys in EN translation: {missing_in_en}"
