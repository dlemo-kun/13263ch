lsm_en_us: dict[str, int] = {}

lsm_en_uk: dict[str, int] = {}

lsm_es: dict[str, int] = {
    "X": 1, # !0
    "A": 1, # P, B, M
    "B": 3,  
    "C": 3,  
    "H": 3, # L
    "E": 4, # O, U
    "F": 4, # W, Q
    "G": 4, # F, V
    "D": 2  # A
}

lsm_ru: dict[str, int] = {}

lsm_ja: dict[str, int] = {}

def lsm_selector(language: str = "en_US") -> dict[str, int]:
    
    """
    Selects and returns the appropriate Lip-Sync Map (LSM) dictionary 
    based on the specified language code.

    Args:
        language (str, optional): The language code. Defaults to "en_US".

    Returns:
        dict[str, int]: A dictionary mapping character phonemes to mouth shape indices.
    """
    
    print(f"[INFO] Requesting Lip-Sync Map (LSM) for language: '{language}'")
    
    selected_map: dict[str, int]

    try:
        match language:
            case "en_US":
                selected_map = lsm_en_us
            case "en_UK":
                selected_map = lsm_en_uk
            case "es":
                selected_map = lsm_es
            case "ru":
                selected_map = lsm_ru
            case "ja":
                selected_map = lsm_ja
            case _:
                print(f"[WARNING] Unsupported language code '{language}'. Falling back to default 'en_US'.")
                selected_map = lsm_en_us
                
        print(f"[SUCCESS] LSM successfully loaded.")
        return selected_map

    except NameError as e:
        print(f"[ERROR] Failed to load the dictionary. Ensure all LSM variables are defined: {e}")
        return {}
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred in lsm_selector: {e}")
        return {}
