def get_non_empty_string(prompt: str) -> str:
    """
    Prompts the user for input and ensures the returned string is not empty
    or whitespace-only.

    Args:
        prompt: The message to display to the user.

    Returns:
        The validated, non-empty string entered by the user.
    """
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        else:
            print("Input cannot be empty or just whitespace. Please try again.")

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    user_name = get_non_empty_string("Enter your name: ")
    print(f"Hello, {user_name}!")

    user_class = get_non_empty_string("Choose your class: ")
    print(f"You chose: {user_class}")
