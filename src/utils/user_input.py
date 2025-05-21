def user_input(prompt: str, options: list[str]) -> str:
    while True:
        response: str = input(prompt)
        if response in options:
            return response
        print(f"Invalid response, please choose one of {options}")
