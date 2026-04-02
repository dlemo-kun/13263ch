from src.subprocess_run import sp_run
from src.config import PATH_PYTHON

if __name__ == "__main__":
    
    for i in range(1, 8+1):
        command_python: list[str] = [
            PATH_PYTHON,
            "main.py",
            f"./test/test_{i}.wav",
            "--output",  f"./test/test_{i}.mp4"
        ]
        
        sp_run(
            command=command_python,
            label=f"Rendering './test/test_{i}.mp4'"
        )