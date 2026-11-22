#!/usr/bin/env python3
"""
BlazeFinal  -  Productivity Hub
================================
A standalone, interactive app built by IMPORTING components
from the two other apps:

    from blazeone import banner, Calculator   ->  2 components from BlazeOne
    from blazetwo import TaskBoard            ->  1 component  from BlazeTwo

Run it:
    python blazefinal.py
(keep blazeone.py and blazetwo.py in the same folder)
"""

import os

# ---------------------------------------------------------------------------
#  THE "FROM ... IMPORT ..." DEMO
#  Importing does NOT start BlazeOne or BlazeTwo, because their main()
#  sits behind  `if __name__ == "__main__":`
# ---------------------------------------------------------------------------
from blazeone import banner, Calculator      # <- 2 components from BlazeOne
from blazetwo import TaskBoard               # <- 1 component  from BlazeTwo

os.system("")

RESET, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"
AURORA = [129, 135, 141, 147, 153, 159]  # violet -> ice blue


def color(n):
    return f"\033[38;5;{n}m"


def ask(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"


class Hub:
    def __init__(self):
        # Re-using the imported components, re-themed in BlazeFinal colours
        self.calc = Calculator(accent=141)
        self.board = TaskBoard(storage="blazefinal_tasks.json", accent=147)

    # ---- BlazeFinal's own feature: dashboard -----------------------------
    def dashboard(self):
        done, total = self.board.stats
        last = (f"{self.calc.history[-1][0]} = {Calculator.fmt(self.calc.history[-1][1])}"
                if self.calc.history else "—")
        print(f"\n  {color(141)}{BOLD}▌ DASHBOARD{RESET}")
        print(f"  {DIM}Tasks       {RESET}{self.board.progress_bar(20)}")
        print(f"  {DIM}Open tasks  {RESET}{BOLD}{total - done}{RESET}")
        print(f"  {DIM}Calculations{RESET} {BOLD}{len(self.calc.history)}{RESET}  {DIM}last: {last}{RESET}")
        pending = [t["title"] for t in self.board.tasks if not t["done"]][:3]
        if pending:
            print(f"  {DIM}Up next     {RESET}" + f"{DIM} · {RESET}".join(pending))

    # ---- BlazeFinal's own feature: bill splitter (powered by Calculator) --
    def bill_splitter(self):
        print(f"\n  {color(153)}{BOLD}▌ BILL SPLITTER{RESET}  {DIM}amounts can be maths, e.g. 450+120*2{RESET}")
        try:
            total = self.calc.evaluate(ask(f"  {color(153)}bill total ❯{RESET} ") or "0")
            tip = self.calc.evaluate(ask(f"  {color(153)}tip %      ❯{RESET} ") or "0")
            people = int(self.calc.evaluate(ask(f"  {color(153)}people     ❯{RESET} ") or "1"))
            if people < 1:
                raise ValueError("need at least 1 person")
            grand = total * (1 + tip / 100)
            share = self.calc.evaluate(f"{grand} / {people}")
            print(f"\n  {DIM}Total with tip{RESET} {BOLD}{grand:,.2f}{RESET}")
            print(f"  {DIM}Each person   {RESET} {BOLD}{color(46)}{share:,.2f}{RESET}")
            if ask(f"  {DIM}Add 'Collect payments' to your tasks? (y/n){RESET} ").lower() == "y":
                self.board.add(f"Collect {share:,.2f} from {people - 1} friend(s)", "high")
                print(f"  {color(46)}＋ Added to task board{RESET}")
        except (ValueError, SyntaxError, ZeroDivisionError, TypeError) as exc:
            print(f"  {color(196)}✖ {exc or 'invalid input'}{RESET}")

    # ---- shows the import in action ---------------------------------------
    def under_the_hood(self):
        rows = [("banner", banner.__module__), ("Calculator", Calculator.__module__),
                ("TaskBoard", TaskBoard.__module__)]
        print(f"\n  {color(159)}{BOLD}▌ UNDER THE HOOD{RESET}")
        print(f"  {DIM}from blazeone import banner, Calculator\n  from blazetwo import TaskBoard{RESET}\n")
        for name, module in rows:
            print(f"   {BOLD}{name:<11}{RESET} {DIM}comes from{RESET} {color(147)}{module}.py{RESET}")

    def run(self):
        banner("BlazeFinal", "Productivity Hub  ·  BlazeOne + BlazeTwo", palette=AURORA)
        menu = [("Dashboard", self.dashboard),
                ("Calculator      [from BlazeOne]", self.calc.run),
                ("Task board      [from BlazeTwo]", self.board.run),
                ("Bill splitter", self.bill_splitter),
                ("Under the hood  (see the imports)", self.under_the_hood)]
        while True:
            print()
            for i, (label, _) in enumerate(menu, 1):
                print(f"   {color(AURORA[i % len(AURORA)])}{i}{RESET}  {label}")
            print(f"   {color(129)}0{RESET}  {DIM}Exit{RESET}")
            choice = ask(f"\n  {color(135)}blazefinal ❯{RESET} ")
            if choice in ("0", "q", "exit"):
                banner("Goodbye", "BlazeFinal signing off", palette=AURORA, width=40)
                break
            if choice.isdigit() and 1 <= int(choice) <= len(menu):
                menu[int(choice) - 1][1]()
            else:
                print(f"  {color(196)}✖ Choose 0-{len(menu)}{RESET}")


if __name__ == "__main__":
    Hub().run()
