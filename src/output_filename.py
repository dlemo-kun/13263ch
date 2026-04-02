
from pathlib import Path

def get_unique_filename(base_path: Path, suffix: str) -> Path:
    """
    Generates a unique filename by appending an incremental suffix if the file already exists.

    Args:
        base_path (Path): The initial desired path for the file.
        suffix (str): The file extension (e.g., ".mp4").

    Returns:
        Path: A unique path for the file.
    """
    if not base_path.exists():
        return base_path

    counter = 1
    while True:
        new_name = f"{base_path.stem}_{counter}{suffix}"
        new_path = base_path.parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1