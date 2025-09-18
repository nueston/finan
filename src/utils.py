def jump_detected(value1: float, value2: float, jump_percentage: float) -> bool:
    """
    Detect if value2 differs from value1 by more than jump_percentage (can be negative).

    Args:
        value1 (float): The reference value.
        value2 (float): The value to compare.
        jump_percentage (float): The jump threshold as a percent (e.g., 5 for 5%, -5 for -5%).

    Returns:
        bool: True if jump detected, False otherwise.
    """
    if value1 == 0:
        return False  # avoid division by zero
    diff_percent = ((value2 - value1) / value1) * 100
    if jump_percentage >= 0:
        return diff_percent >= jump_percentage
    else:
        return diff_percent <= jump_percentage
