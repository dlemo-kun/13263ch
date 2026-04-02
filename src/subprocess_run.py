import subprocess

def sp_run(
        command: list[str],
        label: str = ""
    ) -> int:

    """
    Executes a subprocess command and handles errors consistently with the
    logging style of the reference script.

    Args:
        command (list[str]): The list of command arguments to execute.
        label (str, optional): A descriptive label for the operation. Defaults to an empty string.

    Returns:
        int: 0 if the command executes successfully, 1 if an error occurs.
    """

    if label: print(f"[INFO] {label}")

    try:
        result = subprocess.run(
            args=command,
            check=True
            # capture_output=True,
            # text=True
        )
        print(f"[SUCCESS] Command executed successfully: {" ".join(command)}")
        if result.stdout: print(f"[INFO] Standard output: {result.stdout.strip()}")
        return 0

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed with exit code {e.returncode}: {" ".join(command)}")
        if e.stdout: print(f"[ERROR] Standard output: {e.stdout.strip()}")
        if e.stderr: print(f"[ERROR] Standard error: {e.stderr.strip()}")
        return 1

    except FileNotFoundError:
        print(f"[ERROR] Command not found: {command[0]}. Ensure it is installed and in the PATH.")
        return 1

    except Exception as e:
        print(f"[ERROR] An unexpected error occurred while executing the command: {e}")
        return 1
