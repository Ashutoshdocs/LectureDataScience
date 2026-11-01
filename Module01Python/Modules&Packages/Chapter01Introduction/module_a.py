"""Module A: can be imported or executed directly."""

def message_from_a():
    """Return a message from Module A."""
    return "Hello from Module A"


def call_module_b():
    """Import Module B only when this function is called."""
    # Local import avoids a circular-import problem at module load time.
    import module_b
    return module_b.message_from_b()


def main():
    """Demo that runs only when this file is executed directly."""
    print(message_from_a())
    print(call_module_b())


if __name__ == "__main__":
    main()
