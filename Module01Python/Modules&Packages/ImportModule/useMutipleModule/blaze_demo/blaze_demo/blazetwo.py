#!/usr/bin/env python3
"""
BlazeTwo  -  Task Board & Focus Timer
======================================
A fully working, standalone, interactive terminal app.

Run it on its own:
    python blazetwo.py

Or borrow its components from another file:
    from blazetwo import TaskBoard
"""

import json
import os
import sys
import time
from pathlib import Path

__all__ = ["TaskBoard", "FocusTimer"]

os.system("")  # switches on ANSI colour support in Windows terminals

RESET, BOLD, DIM, STRIKE = "\033[0m", "\033[1m", "\033[2m", "\033[9m"
OCEAN = [27, 33, 39, 45, 51, 87]  # deep blue -> aqua


def color(n):
    return f"\033[38;5;{n}m"


def ask(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"


def wave(text):
    """Ocean-gradient text (BlazeTwo's own look, no BlazeOne needed)."""
    out = []
    for i, ch in enumerate(text):
        idx = round(i / max(len(text) - 1, 1) * (len(OCEAN) - 1))
        out.append(color(OCEAN[idx]) + ch)
    return "".join(out) + RESET


def header(title, subtitle):
    line = "≈" * 56
    print(f"\n{color(33)}{line}{RESET}")
    print(f"  {BOLD}{wave(' '.join(title.upper()))}{RESET}   {DIM}{subtitle}{RESET}")
    print(f"{color(33)}{line}{RESET}")


# --------------------------------------------------------------------------
# COMPONENT: TaskBoard  (imported by BlazeFinal)
# --------------------------------------------------------------------------
class TaskBoard:
    """A persistent to-do board with priorities and a progress bar.

    board = TaskBoard(storage="my_tasks.json")
    board.add("Write README", priority="high")
    board.complete(1)
    board.run()        # interactive prompt
    """

    PRIORITY = {"high": (196, "▲"), "med": (220, "●"), "low": (46, "▼")}

    def __init__(self, storage="blazetwo_tasks.json", accent=45):
        self.storage = Path(storage)
        self.accent = accent
        self.tasks = self._load()

    # --- data -----------------------------------------------------------
    def _load(self):
        try:
            return json.loads(self.storage.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self):
        self.storage.write_text(json.dumps(self.tasks, indent=2), encoding="utf-8")

    def add(self, title, priority="med"):
        task = {"title": title, "priority": priority, "done": False}
        self.tasks.append(task)
        self._save()
        return task

    def _set_done(self, index, value):
        self.tasks[index - 1]["done"] = value
        self._save()

    def complete(self, index):
        self._set_done(index, True)

    def reopen(self, index):
        self._set_done(index, False)

    def remove(self, index):
        task = self.tasks.pop(index - 1)
        self._save()
        return task

    def clear_done(self):
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t["done"]]
        self._save()
        return before - len(self.tasks)

    @property
    def stats(self):
        return sum(t["done"] for t in self.tasks), len(self.tasks)

    def progress_bar(self, width=24):
        done, total = self.stats
        ratio = done / total if total else 0
        filled = round(ratio * width)
        return (f"{color(self.accent)}{'█' * filled}{DIM}{'░' * (width - filled)}{RESET}"
                f" {BOLD}{ratio:>4.0%}{RESET} {DIM}({done}/{total}){RESET}")

    # --- view -----------------------------------------------------------
    def show(self):
        if not self.tasks:
            print(f"\n  {DIM}✨ Board is empty — try:  add Buy milk !high{RESET}")
            return
        print()
        for i, t in enumerate(self.tasks, 1):
            col, icon = self.PRIORITY.get(t["priority"], self.PRIORITY["med"])
            if t["done"]:
                print(f"  {DIM}{i:>2}. {color(46)}✔{RESET} {DIM}{STRIKE}{t['title']}{RESET}")
            else:
                print(f"  {DIM}{i:>2}.{RESET} {color(col)}{icon}{RESET} {t['title']}")
        print(f"\n  {self.progress_bar()}")

    # --- interactive screen ---------------------------------------------
    def run(self):
        a = color(self.accent)
        print(f"\n  {a}{BOLD}▌ TASK BOARD{RESET}  {DIM}type 'help' for commands, 'back' to leave{RESET}")
        self.show()
        while True:
            line = ask(f"\n  {a}tasks ❯{RESET} ")
            cmd, _, arg = line.partition(" ")
            cmd = cmd.lower()
            try:
                if cmd in ("back", "exit", "quit", "q"):
                    break
                elif cmd == "help":
                    print(f"  {DIM}add <task> [!high|!low]   done <n>   undo <n>\n"
                          f"  del <n>   clear (remove finished)   list   back{RESET}")
                    continue
                elif cmd == "add" and arg:
                    priority = "med"
                    for p in ("high", "low"):
                        if f"!{p}" in arg:
                            priority, arg = p, arg.replace(f"!{p}", "").strip()
                    self.add(arg, priority)
                    print(f"  {color(46)}＋ Added:{RESET} {arg}")
                elif cmd == "done":
                    self.complete(int(arg))
                    print(f"  {color(46)}✔ Nice work!{RESET}")
                elif cmd == "undo":
                    self.reopen(int(arg))
                elif cmd == "del":
                    print(f"  {color(196)}✖ Removed:{RESET} {self.remove(int(arg))['title']}")
                elif cmd == "clear":
                    print(f"  {DIM}Cleared {self.clear_done()} finished task(s).{RESET}")
                elif cmd in ("list", "ls", ""):
                    pass
                else:
                    print(f"  {color(196)}✖ Unknown command — type 'help'{RESET}")
                    continue
                self.show()
            except (ValueError, IndexError):
                print(f"  {color(196)}✖ Use a valid task number, e.g. done 1{RESET}")


# --------------------------------------------------------------------------
# BlazeTwo-only feature: FocusTimer  (not used by BlazeFinal)
# --------------------------------------------------------------------------
class FocusTimer:
    def countdown(self, seconds, width=30):
        start = time.time()
        try:
            while (left := seconds - (time.time() - start)) > 0:
                filled = round((1 - left / seconds) * width)
                mins, secs = divmod(int(left) + 1, 60)
                sys.stdout.write(f"\r  {color(51)}{'█' * filled}{DIM}{'░' * (width - filled)}"
                                 f"{RESET}  {BOLD}{mins:02d}:{secs:02d}{RESET} ")
                sys.stdout.flush()
                time.sleep(0.2)
            print(f"\r  {color(46)}{'█' * width}{RESET}  {BOLD}00:00{RESET}  🎉 Focus session complete!\a")
        except KeyboardInterrupt:
            print(f"\n  {DIM}Timer stopped.{RESET}")

    def run(self):
        print(f"\n  {color(51)}{BOLD}▌ FOCUS TIMER{RESET}  {DIM}e.g. 25 (minutes) or 10s (seconds). Ctrl+C stops.{RESET}")
        raw = ask(f"  {color(51)}duration ❯{RESET} ").lower()
        if raw in ("q", "back", ""):
            return
        try:
            seconds = float(raw[:-1]) if raw.endswith("s") else float(raw) * 60
            if seconds <= 0:
                raise ValueError
        except ValueError:
            print(f"  {color(196)}✖ Try 25 or 10s{RESET}")
            return
        self.countdown(seconds)


# --------------------------------------------------------------------------
# The standalone app
# --------------------------------------------------------------------------
def main():
    board = TaskBoard()
    header("BlazeTwo", "Task Board & Focus Timer")
    while True:
        print(f"\n   {color(51)}1{RESET}  Task board   {board.progress_bar(12)}"
              f"\n   {color(51)}2{RESET}  Focus timer"
              f"\n   {color(51)}3{RESET}  About this module"
              f"\n   {color(51)}0{RESET}  {DIM}Exit{RESET}")
        choice = ask(f"\n  {color(39)}blazetwo ❯{RESET} ")
        if choice == "1":
            board.run()
        elif choice == "2":
            FocusTimer().run()
        elif choice == "3":
            print(f"\n  {DIM}Importable components:{RESET} {BOLD}{', '.join(__all__)}{RESET}"
                  f"\n  {DIM}Try:{RESET} from blazetwo import TaskBoard"
                  f"\n  {DIM}Tasks are saved in:{RESET} {board.storage.resolve()}")
        elif choice in ("0", "q", "exit"):
            print("\n  " + wave("Tasks saved. See you on the next wave!") + "\n")
            break
        else:
            print(f"  {color(196)}✖ Choose 0-3{RESET}")


# Runs ONLY when started directly (python blazetwo.py)
if __name__ == "__main__":
    main()
