"""Module B: can be imported or executed directly."""

def message_from_b():
    """Return a message from Module B."""
    return "Hello from Module B"


def call_module_a():
    """Import Module A only when this function is called."""
    # Local import avoids a circular-import problem at module load time.
    import module_a
    return module_a.message_from_a()


def main():
    """Demo that runs only when this file is executed directly."""
    print(message_from_b())
    print(call_module_a())


if __name__ == "__main__":
    main()
