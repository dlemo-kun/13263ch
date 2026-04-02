import os
from dotenv import load_dotenv

if load_dotenv():
    print("[SUCCESS] .env file found and loaded successfully.")
else:
    print("[WARNING] No .env file found. Relying on system environment variables or default fallbacks.")

def get_env(
        var_name: str, 
        default_value: str
    ) -> str:
    """
    Safely retrieves an environment variable. If the variable is missing or empty,
    it assigns a default value and logs a warning.

    Args:
        var_name (str): The name of the environment variable to look for.
        default_value (str): The fallback value to use if the variable is not found.

    Returns:
        str: The retrieved value or the default fallback.
    """
    value: str | None = os.getenv(var_name)
    
    if not value:
        print(f"[WARNING] Environment variable '{var_name}' not set. Using default: '{default_value}'")
        return default_value
    
    print(f"[INFO] '{var_name}' loaded successfully: '{value}'")
    return value

# Executable Paths
PATH_RHUBARB: str = get_env("PATH_RHUBARB", "rhubarb")
PATH_GODOT:   str = get_env("PATH_GODOT"  , "godot"  )
PATH_FFMPEG:  str = get_env("PATH_FFMPEG" , "ffmpeg" )

print("[SUCCESS] All configuration variables have been set and are ready to use.\n")