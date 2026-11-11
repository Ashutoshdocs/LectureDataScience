# Main program imports and uses the other two Python files.

import operations
import messages

messages.show_title()

x = 20
y = 5

messages.show_result("Addition", operations.add(x, y))
messages.show_result("Subtraction", operations.subtract(x, y))
