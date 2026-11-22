
#!/usr/bin/env python3
# Shebang: tells Linux/Unix systems to execute this file using Python 3.

"""
BlazeTwo - Task Board & Focus Timer

A standalone interactive terminal application.

Run directly:
    python blazetwo.py

Import reusable components into another Python file:
    from blazetwo import TaskBoard
"""

import json                  # Used to convert Python objects into JSON and vice versa.
import os                    # Provides operating-system-related functionality.
import sys                   # Provides access to system-specific functionality and stdout.
import time                  # Provides time-related functions for the countdown timer.
from pathlib import Path     # Provides an object-oriented way to work with file paths.

# Defines the public components available through: from blazetwo import *
__all__ = ["TaskBoard", "FocusTimer"]

os.system("")                # Enables ANSI colour support in some Windows terminals.

# ANSI escape codes for terminal text formatting.
RESET, BOLD, DIM, STRIKE = "\033[0m", "\033[1m", "\033[2m", "\033[9m"

# Defines an ocean colour gradient: deep blue to aqua.
OCEAN = [27, 33, 39, 45, 51, 87]


# --------------------------------------------------------------------------
# COMMON UTILITY FUNCTIONS
# --------------------------------------------------------------------------

def color(n):
    # Generates an ANSI escape code for the requested 256-colour foreground.
    return f"\033[38;5;{n}m"


def ask(prompt):
    # Reads user input and handles Ctrl+C and Ctrl+D gracefully.
    try:
        return input(prompt).strip()  # Reads input and removes surrounding spaces.
    except (EOFError, KeyboardInterrupt):  # Handles Ctrl+D and Ctrl+C.
        print()                          # Moves the cursor to a new line.
        return "q"                       # Returns q to trigger the back/exit logic.


# --------------------------------------------------------------------------
# COMPONENT 1: WAVE TEXT
# Creates ocean-gradient coloured text.
# --------------------------------------------------------------------------

def wave(text):
    """Ocean-gradient text (BlazeTwo's own look, no BlazeOne needed)."""

    out = []  # Creates an empty list to store coloured characters.

    # Loops through every character and its index.
    for i, ch in enumerate(text):

        # Calculates the appropriate colour index for the current character.
        idx = round(i / max(len(text) - 1, 1) * (len(OCEAN) - 1))

        # Adds the selected colour code followed by the current character.
        out.append(color(OCEAN[idx]) + ch)

    # Joins all coloured characters and resets the terminal colour.
    return "".join(out) + RESET


# --------------------------------------------------------------------------
# COMPONENT 2: HEADER
# Displays a decorative heading with a coloured title and subtitle.
# --------------------------------------------------------------------------

def header(title, subtitle):

    # Creates a decorative line containing 56 approximation characters.
    line = "≈" * 56

    # Prints the top decorative line in blue.
    print(f"\n{color(33)}{line}{RESET}")

    # Prints the uppercase title using an ocean gradient and a dim subtitle.
    print(f"  {BOLD}{wave(' '.join(title.upper()))}{RESET}   {DIM}{subtitle}{RESET}")

    # Prints the bottom decorative line.
    print(f"{color(33)}{line}{RESET}")


# --------------------------------------------------------------------------
# COMPONENT 3: TASKBOARD
# Reusable class that manages tasks and stores them permanently in JSON.
# --------------------------------------------------------------------------

class TaskBoard:
    """A persistent to-do board with priorities and a progress bar.

    Example:
        board = TaskBoard(storage="my_tasks.json")
        board.add("Write README", priority="high")
        board.complete(1)
        board.run()
    """

    # Defines priority levels, their terminal colours and their symbols.
    PRIORITY = {
        "high": (196, "▲"),  # High priority: red triangle.
        "med": (220, "●"),   # Medium priority: yellow circle.
        "low": (46, "▼")     # Low priority: green downward triangle.
    }

    def __init__(self, storage="blazetwo_tasks.json", accent=45):
        # Constructor: executes automatically when TaskBoard() is created.

        self.storage = Path(storage)  # Converts the filename into a Path object.
        self.accent = accent          # Stores the colour used for the progress bar.
        self.tasks = self._load()     # Loads existing tasks from the JSON file.

    # ---------------- DATA MANAGEMENT ----------------

    def _load(self):
        # Loads previously saved tasks from the JSON file.

        try:
            # Reads the file as UTF-8 text and converts JSON into a Python object.
            return json.loads(self.storage.read_text(encoding="utf-8"))

        # Handles the situation where the file does not exist or JSON is invalid.
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Starts with an empty task list.

    def _save(self):
        # Converts the task list into formatted JSON and writes it to disk.
        self.storage.write_text(
            json.dumps(self.tasks, indent=2),  # Converts Python list into JSON.
            encoding="utf-8"                   # Saves using UTF-8 encoding.
        )

    def add(self, title, priority="med"):
        # Creates a new task with the supplied title and priority.

        task = {
            "title": title,       # Stores the task description.
            "priority": priority, # Stores its priority level.
            "done": False         # Marks the task as incomplete initially.
        }

        self.tasks.append(task)  # Adds the task dictionary to the task list.

        self._save()             # Saves the updated task list to the JSON file.

        return task              # Returns the newly created task.

    def _set_done(self, index, value):
        # Updates the completion status of a task using its displayed number.

        self.tasks[index - 1]["done"] = value  # Converts 1-based index to 0-based.

        self._save()  # Persists the updated task status.

    def complete(self, index):
        # Marks the selected task as completed.
        self._set_done(index, True)

    def reopen(self, index):
        # Marks the selected task as incomplete again.
        self._set_done(index, False)

    def remove(self, index):
        # Removes the selected task from the list.

        task = self.tasks.pop(index - 1)  # Removes and returns the selected task.

        self._save()  # Saves the updated list after deletion.

        return task   # Returns the removed task details.

    def clear_done(self):
        # Removes all tasks that have already been completed.

        before = len(self.tasks)  # Stores the original number of tasks.

        # Rebuilds the list using only tasks whose done value is False.
        self.tasks = [t for t in self.tasks if not t["done"]]

        self._save()  # Saves the filtered task list.

        # Returns the number of tasks removed.
        return before - len(self.tasks)

    @property
    def stats(self):
        # Property decorator: allows access using board.stats instead of board.stats().

        # Returns a tuple containing completed task count and total task count.
        return sum(t["done"] for t in self.tasks), len(self.tasks)

    def progress_bar(self, width=24):
        # Generates a visual progress bar based on completed tasks.

        done, total = self.stats  # Retrieves completed and total task counts.

        # Calculates completion ratio; avoids division by zero.
        ratio = done / total if total else 0

        # Calculates how many progress-bar characters should be filled.
        filled = round(ratio * width)

        # Returns the coloured progress bar, percentage and task count.
        return (
            f"{color(self.accent)}{'█' * filled}"
            f"{DIM}{'░' * (width - filled)}{RESET}"
            f" {BOLD}{ratio:>4.0%}{RESET}"
            f" {DIM}({done}/{total}){RESET}"
        )

    # ---------------- DISPLAY TASKS ----------------

    def show(self):
        # Displays all tasks and the current progress.

        if not self.tasks:  # Checks whether the task list is empty.
            print(f"\n  {DIM}✨ Board is empty — try:  add Buy milk !high{RESET}")
            return           # Exits the function because there are no tasks.

        print()  # Adds spacing before displaying tasks.

        # Enumerates tasks starting from 1 for user-friendly numbering.
        for i, t in enumerate(self.tasks, 1):

            # Retrieves the colour and icon for the task's priority.
            # Defaults to medium priority if an unknown priority is found.
            col, icon = self.PRIORITY.get(
                t["priority"],
                self.PRIORITY["med"]
            )

            # Checks whether the task has been completed.
            if t["done"]:

                # Displays completed tasks in dimmed and struck-through text.
                print(
                    f"  {DIM}{i:>2}. "
                    f"{color(46)}✔{RESET} "
                    f"{DIM}{STRIKE}{t['title']}{RESET}"
                )

            else:

                # Displays pending tasks with their priority colour and icon.
                print(
                    f"  {DIM}{i:>2}.{RESET} "
                    f"{color(col)}{icon}{RESET} {t['title']}"
                )

        # Displays the current task completion progress.
        print(f"\n  {self.progress_bar()}")

    # ---------------- INTERACTIVE TASK BOARD ----------------

    def run(self):
        # Starts the interactive task management screen.

        a = color(self.accent)  # Stores the configured accent colour.

        # Displays the task board heading and instructions.
        print(
            f"\n  {a}{BOLD}▌ TASK BOARD{RESET}  "
            f"{DIM}type 'help' for commands, 'back' to leave{RESET}"
        )

        self.show()  # Displays all existing tasks.

        # Keeps accepting commands until the user chooses to go back.
        while True:

            # Displays the task prompt and reads user input.
            line = ask(f"\n  {a}tasks ❯{RESET} ")

            # Splits input into command and remaining arguments.
            # Example: "add Buy milk" becomes cmd="add", arg="Buy milk".
            cmd, _, arg = line.partition(" ")

            # Converts the command into lowercase.
            cmd = cmd.lower()

            # Handles possible invalid inputs and index errors.
            try:

                # Exits the task board when the user enters a back command.
                if cmd in ("back", "exit", "quit", "q"):
                    break

                # Displays the available task board commands.
                elif cmd == "help":
                    print(
                        f"  {DIM}add <task> [!high|!low]   done <n>   undo <n>\n"
                        f"  del <n>   clear (remove finished)   list   back{RESET}"
                    )
                    continue  # Returns to the next command prompt.

                # Adds a task if the command is add and a description is provided.
                elif cmd == "add" and arg:

                    priority = "med"  # Uses medium priority by default.

                    # Checks whether the user specified high or low priority.
                    for p in ("high", "low"):

                        # Searches for the priority marker in the task description.
                        if f"!{p}" in arg:

                            priority = p  # Updates the selected priority.

                            # Removes the priority marker from the task title.
                            arg = arg.replace(f"!{p}", "").strip()

                    self.add(arg, priority)  # Adds and saves the new task.

                    # Confirms successful task creation.
                    print(f"  {color(46)}＋ Added:{RESET} {arg}")

                # Marks a task as completed.
                elif cmd == "done":
                    self.complete(int(arg))  # Converts task number to integer.
                    print(f"  {color(46)}✔ Nice work!{RESET}")

                # Reopens a previously completed task.
                elif cmd == "undo":
                    self.reopen(int(arg))

                # Deletes the selected task.
                elif cmd == "del":
                    print(
                        f"  {color(196)}✖ Removed:{RESET} "
                        f"{self.remove(int(arg))['title']}"
                    )

                # Removes all completed tasks.
                elif cmd == "clear":
                    print(
                        f"  {DIM}Cleared {self.clear_done()} "
                        f"finished task(s).{RESET}"
                    )

                # Accepts list, ls or an empty command to refresh the task display.
                elif cmd in ("list", "ls", ""):
                    pass  # No data modification is needed.

                else:
                    # Handles commands that are not recognized.
                    print(f"  {color(196)}✖ Unknown command — type 'help'{RESET}")
                    continue

                # Refreshes the task display after a successful operation.
                self.show()

            # Handles invalid numbers and task indexes outside the valid range.
            except (ValueError, IndexError):
                print(
                    f"  {color(196)}✖ Use a valid task number, "
                    f"e.g. done 1{RESET}"
                )


# --------------------------------------------------------------------------
# COMPONENT 4: FOCUS TIMER
# Standalone timer class that can be imported and reused.
# --------------------------------------------------------------------------

class FocusTimer:

    def countdown(self, seconds, width=30):
        # Starts a countdown for the specified number of seconds.

        start = time.time()  # Captures the starting timestamp.

        try:
            # Calculates remaining time and loops until the countdown reaches zero.
            # The walrus operator := assigns left and checks it in one expression.
            while (left := seconds - (time.time() - start)) > 0:

                # Calculates the number of completed progress-bar blocks.
                filled = round((1 - left / seconds) * width)

                # Converts remaining seconds into minutes and seconds.
                mins, secs = divmod(int(left) + 1, 60)

                # Updates the progress bar and timer on the same terminal line.
                sys.stdout.write(
                    f"\r  {color(51)}{'█' * filled}"
                    f"{DIM}{'░' * (width - filled)}"
                    f"{RESET}  {BOLD}{mins:02d}:{secs:02d}{RESET} "
                )

                sys.stdout.flush()  # Forces the terminal to display the update.

                time.sleep(0.2)  # Waits 0.2 seconds before updating again.

            # Displays a full progress bar and completion message.
            # \a produces a terminal bell sound where supported.
            print(
                f"\r  {color(46)}{'█' * width}{RESET}  "
                f"{BOLD}00:00{RESET}  🎉 Focus session complete!\a"
            )

        # Allows the user to stop the timer using Ctrl+C.
        except KeyboardInterrupt:
            print(f"\n  {DIM}Timer stopped.{RESET}")

    def run(self):
        # Starts the interactive focus timer screen.

        print(
            f"\n  {color(51)}{BOLD}▌ FOCUS TIMER{RESET}  "
            f"{DIM}e.g. 25 (minutes) or 10s (seconds). Ctrl+C stops.{RESET}"
        )

        # Reads the requested timer duration.
        raw = ask(f"  {color(51)}duration ❯{RESET} ").lower()

        # Returns without starting if the user chooses back or enters nothing.
        if raw in ("q", "back", ""):
            return

        try:
            # If input ends with s, interpret it as seconds; otherwise minutes.
            seconds = (
                float(raw[:-1])
                if raw.endswith("s")
                else float(raw) * 60
            )

            # Rejects zero or negative durations.
            if seconds <= 0:
                raise ValueError

        # Handles invalid timer duration input.
        except ValueError:
            print(f"  {color(196)}✖ Try 25 or 10s{RESET}")
            return

        # Starts the countdown with the calculated number of seconds.
        self.countdown(seconds)


# --------------------------------------------------------------------------
# MAIN APPLICATION
# Runs when blazetwo.py is executed directly.
# --------------------------------------------------------------------------

def main():
    # Creates a TaskBoard object and loads existing tasks from JSON.
    board = TaskBoard()

    # Displays the BlazeTwo application header.
    header("BlazeTwo", "Task Board & Focus Timer")

    # Continuously displays the main menu.
    while True:

        # Displays the task board option and its current progress.
        print(
            f"\n   {color(51)}1{RESET}  Task board   {board.progress_bar(12)}"
            f"\n   {color(51)}2{RESET}  Focus timer"
            f"\n   {color(51)}3{RESET}  About this module"
            f"\n   {color(51)}0{RESET}  {DIM}Exit{RESET}"
        )

        # Reads the user's menu selection.
        choice = ask(f"\n  {color(39)}blazetwo ❯{RESET} ")

        # Opens the task board when the user selects option 1.
        if choice == "1":
            board.run()

        # Opens the focus timer when the user selects option 2.
        elif choice == "2":
            FocusTimer().run()

        # Displays information about the reusable module components.
        elif choice == "3":
            print(
                f"\n  {DIM}Importable components:{RESET} "
                f"{BOLD}{', '.join(__all__)}{RESET}"
                f"\n  {DIM}Try:{RESET} from blazetwo import TaskBoard"
                f"\n  {DIM}Tasks are saved in:{RESET} {board.storage.resolve()}"
            )

        # Exits the application when the user selects 0, q or exit.
        elif choice in ("0", "q", "exit"):

            # Displays the final ocean-gradient exit message.
            print(
                "\n  " +
                wave("Tasks saved. See you on the next wave!") +
                "\n"
            )

            break  # Terminates the main menu loop.

        else:
            # Handles invalid main menu selections.
            print(f"  {color(196)}✖ Choose 0-3{RESET}")


# --------------------------------------------------------------------------
# MODULE EXECUTION CONTROL
# --------------------------------------------------------------------------

# When Python executes this file directly, __name__ becomes "__main__".
# When another Python file imports it, __name__ becomes "blazetwo".
# Therefore, main() will not execute automatically during an import.

if __name__ == "__main__":
    main()  # Starts the standalone BlazeTwo application.
