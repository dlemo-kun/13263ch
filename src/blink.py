import random

eye_close: int = 0
eye_open: int = 0

def reset_blink() -> None:
    """
    Resets the global eye_close and eye_open counters to random values
    to simulate natural blinking behavior.
    """
    global eye_close, eye_open
    eye_close = random.randint(2, 6)
    eye_open = random.randint(48, 240)

def blink_state() -> int:
    """
    Determines the current blink state (open or closed) based on internal counters.
    If the eye is open, it decrements the open counter. If closed, it decrements
    the close counter. When both counters reach zero, they are reset.

    Returns:
        int: 0 if the eye is open, 1 if the eye is closed.
    """
    global eye_close, eye_open
    if eye_open > 0:
        eye_open -= 1
        return 0
    elif eye_close > 0:
        eye_close -= 1
        return 1
    else:
        reset_blink()
        return 0
