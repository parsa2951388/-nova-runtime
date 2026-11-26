#!/usr/bin/env python3
"""FRAMEZERO LAB desktop setup console. Uses only Python's standard library."""
from __future__ import annotations

import json
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
FRAMEZERO_SCRIPT = ROOT / "framezero.py"
UPSTREAM_PIN = "b9320a118d46"
PALETTE = {
    "midnight": "#0B1020",
    "carbon": "#141C2E",
    "panel": "#1B2740",
    "cyan": "#45D6FF",
    "violet": "#8B7CFF",
    "amber": "#FFCA78",
    "white": "#F2F6FF",
    "slate": "#9AA8BE",
    "green": "#6DE0B1",
    "red": "#FF7F89",
}


def build_engine_args(
    mode: str,
    game_dir: str,
    output_dir: str,
    work_dir: str = "",
) -> list[str]:
    """Build the FRAMEZERO CLI arguments for one upstream build profile."""
    if mode not in {"runtime", "assets", "full"}:
        raise ValueError("mode must be runtime, assets, or full")
    if not game_dir or not game_dir.strip():
        raise ValueError("Select the local game package folder first.")
    if not output_dir or not output_dir.strip():
        raise ValueError("Select an output folder first.")

    args = [
        "build",
        "--game", str(Path(game_dir).expanduser()),
        "--out", str(Path(output_dir).expanduser()),
    ]
    if work_dir and work_dir.strip():
        args.extend(["--work", str(Path(work_dir).expanduser())])

    if mode == "runtime":
        args.extend(["--stages", "check,shaders,runtime"])
    elif mode == "assets":
        args.extend(["--stages", "check,assets"])
    # "full" intentionally omits --stages and preserves the upstream default.
    return args


def build_validation_args(game_dir: str) -> list[str]:
    """Build an upstream package-validation command without building output."""
    if not game_dir or not game_dir.strip():
        raise ValueError("Select the local game package folder first.")
    return ["build", "--game", str(Path(game_dir).expanduser()), "--check"]


def main() -> int:
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
    except ImportError as exc:
        print(f"FRAMEZERO GUI requires Tk support in this Python installation: {exc}", file=sys.stderr)
        return 2

    class FramezeroApp:
        def __init__(self, root: Any) -> None:
            self.root = root
            self.events: queue.Queue[tuple[str, Any]] = queue.Queue()
            self.worker_running = False
            self.process: subprocess.Popen[str] | None = None
            self.pending_kind = ""
            self.pending_output = ""
            self.output_dir = tk.StringVar(value=str(Path.home() / "Documents" / "FRAMEZERO"))
            self.work_dir = tk.StringVar(value="")
            self.game_dir = tk.StringVar(value="")
            self.mode = tk.StringVar(value="runtime")
            self.footer = tk.StringVar(value="Ready — local setup only")
            self._configure_window()
            self._build_header()
            self._build_tabs()
            self._build_console()
            self.root.protocol("WM_DELETE_WINDOW", self._close)
            self.root.after(120, self._poll_events)
            self._refresh_overview()

        def _configure_window(self) -> None:
            self.root.title("FRAMEZERO LAB — Setup Console")
            self.root.geometry("1080x760")
            self.root.minsize(850, 620)
            self.root.configure(bg=PALETTE["midnight"])
            style = ttk.Style(self.root)
            try:
                style.theme_use("clam")
            except tk.TclError:
                pass
            style.configure(
                "TNotebook",
                background=PALETTE["midnight"],
                borderwidth=0,
                tabmargins=(0, 6, 0, 0),
            )
            style.configure(
                "TNotebook.Tab",
                background=PALETTE["carbon"],
                foreground=PALETTE["slate"],
                padding=(18, 10),
                borderwidth=0,
                font=("Segoe UI", 10, "bold"),
            )
            style.map(
                "TNotebook.Tab",
                background=[("selected", PALETTE["panel"])],
                foreground=[("selected", PALETTE["cyan"])],
            )
            style.configure(
                "Treeview",
                background=PALETTE["carbon"],
                fieldbackground=PALETTE["carbon"],
                foreground=PALETTE["white"],
                rowheight=28,
                borderwidth=0,
                font=("Segoe UI", 9),
            )
            style.configure(
                "Treeview.Heading",
                background=PALETTE["panel"],
                foreground=PALETTE["white"],
                relief="flat",
                font=("Segoe UI", 9, "bold"),
            )
            style.map(
                "Treeview",
                background=[("selected", "#263C5A")],
                foreground=[("selected", PALETTE["white"])],
            )
            style.configure(
                "TCombobox",
                fieldbackground=PALETTE["carbon"],
                background=PALETTE["carbon"],
                foreground=PALETTE["white"],
                arrowcolor=PALETTE["cyan"],
            )

        def _label(self, parent: Any, text: str, size: int = 10, color: str | None = None, bold: bool = False) -> Any:
            return tk.Label(
                parent,
                text=text,
                bg=PALETTE["midnight"] if parent is self.root else parent.cget("bg"),
                fg=color or PALETTE["white"],
                font=("Segoe UI", size, "bold" if bold else "normal"),
                anchor="w",
                justify="left",
                wraplength=900,
            )

        def _button(self, parent: Any, text: str, command: Any, primary: bool = False) -> Any:
            return tk.Button(
                parent,
                text=text,
                command=command,
                bg=PALETTE["cyan"] if primary else PALETTE["panel"],
                fg=PALETTE["midnight"] if primary else PALETTE["white"],
                activebackground=PALETTE["violet"],
                activeforeground=PALETTE["white"],
                relief="flat",
                bd=0,
                padx=16,
                pady=8,
                font=("Segoe UI", 9, "bold"),
                cursor="hand2",
            )

        def _build_header(self) -> None:
            header = tk.Frame(self.root, bg=PALETTE["midnight"])
            header.pack(fill="x", padx=26, pady=(20, 14))
            title = tk.Label(
                header,
                text="FRAMEZERO",
                bg=PALETTE["midnight"],
                fg=PALETTE["white"],
                font=("Segoe UI", 30, "bold"),
            )
            title.pack(side="left")
            runtime = tk.Label(
                header,
                text="RUNTIME  /  SETUP CONSOLE",
                bg=PALETTE["midnight"],
                fg=PALETTE["cyan"],
                font=("Segoe UI", 10, "bold"),
            )
            runtime.pack(side="left", padx=(14, 0), pady=(12, 0))
            pin = tk.Label(
                header,
                text=f"ENGINE PIN  {UPSTREAM_PIN}",
                bg=PALETTE["midnight"],
                fg=PALETTE["slate"],
                font=("Consolas", 9),
            )
            pin.pack(side="right", pady=(14, 0))

        def _build_tabs(self) -> None:
            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(fill="both", expand=True, padx=24, pady=(0, 10))
            self.overview_tab = tk.Frame(self.notebook, bg=PALETTE["midnight"])
            self.diagnostics_tab = tk.Frame(self.notebook, bg=PALETTE["midnight"])
            self.build_tab = tk.Frame(self.notebook, bg=PALETTE["midnight"])
            self.notebook.add(self.overview_tab, text="OVERVIEW")
            self.notebook.add(self.diagnostics_tab, text="DIAGNOSTICS")
            self.notebook.add(self.build_tab, text="BUILD")
            self._make_overview()
            self._make_diagnostics()
            self._make_build()

        def _card(self, parent: Any, padx: int = 18, pady: int = 16) -> Any:
            return tk.Frame(parent, bg=PALETTE["carbon"], padx=padx, pady=pady)

        def _make_overview(self) -> None:
            hero = self._card(self.overview_tab, 24, 22)
            hero.pack(fill="x", padx=8, pady=(12, 10))
            tk.Label(
                hero,
                text="A local-first runtime engineering console",
                bg=PALETTE["carbon"],
                fg=PALETTE["white"],
                font=("Segoe UI", 19, "bold"),
                anchor="w",
            ).pack(fill="x")
            tk.Label(
                hero,
                text=(
                    "FRAMEZERO provides environment checks and a clean front end for the pinned engine. "
                    "Build commands are delegated to the upstream engine; game files are never downloaded "
                    "or copied by this console."
                ),
                bg=PALETTE["carbon"],
                fg=PALETTE["slate"],
                font=("Segoe UI", 10),
                anchor="w",
                justify="left",
                wraplength=900,
            ).pack(fill="x", pady=(8, 16))
            actions = tk.Frame(hero, bg=PALETTE["carbon"])
            actions.pack(fill="x")
            self._button(actions, "Run diagnostics", self._run_diagnostics, primary=True).pack(side="left")
            self._button(actions, "Find local package", self._find_package).pack(side="left", padx=(8, 0))
            self._button(actions, "Engine help", lambda: self._start(["engine-help"], "help")).pack(side="left", padx=(8, 0))

            status = self._card(self.overview_tab)
            status.pack(fill="x", padx=8, pady=10)
            tk.Label(
                status,
                text="UPSTREAM STATUS SNAPSHOT",
                bg=PALETTE["carbon"],
                fg=PALETTE["cyan"],
                font=("Segoe UI", 9, "bold"),
            ).pack(anchor="w")
            tk.Label(
                status,
                text=(
                    "The pinned upstream reports reaching the world phase after the story load, but a first "
                    "world frame is not verified and playable story mode is not reported. This is upstream "
                    "information, not a FRAMEZERO test result."
                ),
                bg=PALETTE["carbon"],
                fg=PALETTE["white"],
                font=("Segoe UI", 10),
                wraplength=900,
                justify="left",
            ).pack(anchor="w", pady=(8, 2))
            self._button(status, "Open diagnostics tab", lambda: self.notebook.select(self.diagnostics_tab)).pack(anchor="w", pady=(10, 0))

        def _make_diagnostics(self) -> None:
            frame = tk.Frame(self.diagnostics_tab, bg=PALETTE["midnight"])
            frame.pack(fill="both", expand=True, padx=8, pady=12)
            title = tk.Label(
                frame,
                text="LOCAL ENVIRONMENT",
                bg=PALETTE["midnight"],
                fg=PALETTE["white"],
                font=("Segoe UI", 14, "bold"),
            )
            title.pack(anchor="w", pady=(0, 6))
            tk.Label(
                frame,
                text="Checks tool availability, versions, and free space. It does not inspect game files.",
                bg=PALETTE["midnight"],
                fg=PALETTE["slate"],
                font=("Segoe UI", 9),
            ).pack(anchor="w", pady=(0, 10))
            self.check_tree = ttk.Treeview(frame, columns=("status", "component", "details"), show="headings")
            self.check_tree.heading("status", text="STATUS")
            self.check_tree.heading("component", text="COMPONENT")
            self.check_tree.heading("details", text="DETAILS")
            self.check_tree.column("status", width=92, minwidth=92, stretch=False)
            self.check_tree.column("component", width=190, minwidth=160, stretch=False)
            self.check_tree.column("details", width=600, minwidth=300, stretch=True)
            self.check_tree.tag_configure("ready", foreground=PALETTE["green"])
            self.check_tree.tag_configure("missing", foreground=PALETTE["red"])
            self.check_tree.tag_configure("warning", foreground=PALETTE["amber"])
            self.check_tree.tag_configure("info", foreground=PALETTE["slate"])
            self.check_tree.tag_configure("optional", foreground=PALETTE["slate"])
            self.check_tree.pack(fill="both", expand=True)
            self._button(frame, "Refresh checks", self._run_diagnostics, primary=True).pack(anchor="w", pady=(12, 0))

        def _make_build(self) -> None:
            frame = tk.Frame(self.build_tab, bg=PALETTE["midnight"])
            frame.pack(fill="both", expand=True, padx=8, pady=12)
            tk.Label(
                frame,
                text="LOCAL BUILD CONFIGURATION",
                bg=PALETTE["midnight"],
                fg=PALETTE["white"],
                font=("Segoe UI", 14, "bold"),
            ).pack(anchor="w", pady=(0, 10))
            self._path_row(frame, "Game package folder", self.game_dir, self._browse_game)
            self._path_row(frame, "Output folder", self.output_dir, self._browse_output)
            self._path_row(frame, "Work folder (optional)", self.work_dir, self._browse_work)

            mode_frame = tk.Frame(frame, bg=PALETTE["midnight"])
            mode_frame.pack(fill="x", pady=(10, 12))
            tk.Label(mode_frame, text="BUILD PROFILE", bg=PALETTE["midnight"], fg=PALETTE["slate"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
            mode_values = [
                ("runtime", "Runtime only — about 30 GiB"),
                ("assets", "Asset export — about 370 GiB"),
                ("full", "Full upstream pipeline — about 400 GiB"),
            ]
            self.mode_map = {label: key for key, label in mode_values}
            self.mode_label = tk.StringVar(value=mode_values[0][1])
            self.mode_box = ttk.Combobox(
                mode_frame,
                textvariable=self.mode_label,
                values=[label for _key, label in mode_values],
                state="readonly",
                width=45,
            )
            self.mode_box.pack(anchor="w", pady=(5, 0))

            buttons = tk.Frame(frame, bg=PALETTE["midnight"])
            buttons.pack(fill="x", pady=(4, 12))
            self._button(buttons, "Validate package", self._validate_package).pack(side="left")
            self._button(buttons, "Find package", self._find_package).pack(side="left", padx=(8, 0))
            self.run_button = self._button(buttons, "Start selected build", self._start_selected_build, primary=True)
            self.run_button.pack(side="left", padx=(8, 0))
            self.stop_button = self._button(buttons, "Stop", self._stop_process)
            self.stop_button.pack(side="left", padx=(8, 0))
            self.stop_button.config(state="disabled")

            tk.Label(
                frame,
                text=(
                    "Storage estimates are from the pinned upstream documentation. The full profile can require "
                    "about 400 GiB. You can place work and output directories on separate drives."
                ),
                bg=PALETTE["midnight"],
                fg=PALETTE["amber"],
                font=("Segoe UI", 9),
                anchor="w",
                justify="left",
                wraplength=900,
            ).pack(anchor="w", pady=(0, 4))

        def _path_row(self, parent: Any, label: str, variable: Any, browse: Any) -> None:
            group = tk.Frame(parent, bg=PALETTE["midnight"])
            group.pack(fill="x", pady=5)
            tk.Label(group, text=label.upper(), bg=PALETTE["midnight"], fg=PALETTE["slate"], font=("Segoe UI", 8, "bold")).pack(anchor="w")
            line = tk.Frame(group, bg=PALETTE["midnight"])
            line.pack(fill="x", pady=(4, 0))
            entry = tk.Entry(
                line,
                textvariable=variable,
                bg=PALETTE["carbon"],
                fg=PALETTE["white"],
                insertbackground=PALETTE["cyan"],
                relief="flat",
                bd=0,
                font=("Segoe UI", 9),
            )
            entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
            self._button(line, "Browse", browse).pack(side="right")

        def _build_console(self) -> None:
            box = tk.Frame(self.root, bg=PALETTE["carbon"], padx=10, pady=8)
            box.pack(fill="both", padx=24, pady=(0, 8))
            header = tk.Frame(box, bg=PALETTE["carbon"])
            header.pack(fill="x")
            tk.Label(
                header,
                text="ACTIVITY LOG",
                bg=PALETTE["carbon"],
                fg=PALETTE["cyan"],
                font=("Segoe UI", 8, "bold"),
            ).pack(side="left")
            self.console = tk.Text(
                box,
                height=8,
                bg="#080D18",
                fg=PALETTE["white"],
                insertbackground=PALETTE["cyan"],
                relief="flat",
                bd=0,
                wrap="word",
                font=("Consolas", 9),
                state="disabled",
            )
            self.console.pack(fill="both", expand=True, pady=(6, 0))

            footer = tk.Frame(self.root, bg=PALETTE["midnight"])
            footer.pack(fill="x", padx=26, pady=(0, 12))
            tk.Label(
                footer,
                textvariable=self.footer,
                bg=PALETTE["midnight"],
                fg=PALETTE["slate"],
                font=("Segoe UI", 8),
            ).pack(side="left")

        def _log(self, message: str) -> None:
            self.console.config(state="normal")
            self.console.insert("end", message.rstrip() + "\n")
            # Keep the visible console bounded during long builds.
            line_count = int(self.console.index("end-1c").split(".")[0])
            if line_count > 5000:
                self.console.delete("1.0", f"{line_count - 5000}.0")
            self.console.see("end")
            self.console.config(state="disabled")

        def _refresh_overview(self) -> None:
            if (ROOT / "engine" / "leonida" / "make_game.py").is_file():
                self.footer.set(f"Engine submodule detected · pin {UPSTREAM_PIN}")
            else:
                self.footer.set("Engine submodule missing · run git submodule update --init --recursive")

        def _start(self, args: list[str], kind: str = "command") -> None:
            if self.worker_running:
                messagebox.showinfo("FRAMEZERO LAB", "A command is already running.")
                return

            command = [sys.executable, str(FRAMEZERO_SCRIPT), *args]
            self._log("$ " + " ".join(f'"{part}"' if " " in part else part for part in command))
            try:
                creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
                process = subprocess.Popen(
                    command,
                    cwd=ROOT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                    creationflags=creationflags,
                )
            except OSError as exc:
                self._log("ERROR: " + str(exc))
                self._set_idle("Could not start command")
                return

            # The process handle is created on the Tk thread before Stop can be pressed.
            self.process = process
            self.worker_running = True
            self.pending_kind = kind
            self.pending_output = ""
            self.run_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.footer.set("Running — see activity log")
            threading.Thread(
                target=self._worker,
                args=(process, kind == "doctor"),
                daemon=True,
            ).start()

        def _worker(self, process: subprocess.Popen[str], collect_output: bool) -> None:
            output_parts: list[str] = []
            batch: list[str] = []
            batch_size = 0
            try:
                if process.stdout is not None:
                    for line in process.stdout:
                        if collect_output:
                            output_parts.append(line)
                        batch.append(line)
                        batch_size += len(line)
                        if len(batch) >= 40 or batch_size >= 16000:
                            self.events.put(("output", "".join(batch)))
                            batch.clear()
                            batch_size = 0
                if batch:
                    self.events.put(("output", "".join(batch)))
                code = process.wait()
                self.events.put(("done", (code, "".join(output_parts) if collect_output else "")))
            except OSError as exc:
                self.events.put(("error", str(exc)))

        def _poll_events(self) -> None:
            try:
                while True:
                    kind, payload = self.events.get_nowait()
                    if kind == "output":
                        self._log(str(payload))
                    elif kind == "error":
                        self._log("ERROR: " + str(payload))
                        self.worker_running = False
                        self.process = None
                        self._set_idle("Could not start command")
                    elif kind == "done":
                        code, output = payload
                        self.worker_running = False
                        self.process = None
                        self._set_idle("Command finished" if code == 0 else f"Command exited with code {code}")
                        if self.pending_kind == "doctor":
                            self._show_diagnostics(output)
            except queue.Empty:
                pass
            self.root.after(120, self._poll_events)

        def _set_idle(self, message: str) -> None:
            self.run_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.footer.set(message)

        def _show_diagnostics(self, output: str) -> None:
            try:
                items = json.loads(output)
            except json.JSONDecodeError:
                self._log("Could not parse diagnostic JSON; inspect the activity log.")
                return
            for row in self.check_tree.get_children():
                self.check_tree.delete(row)
            for item in items:
                status = item.get("status", "info")
                self.check_tree.insert(
                    "",
                    "end",
                    values=(status.upper(), item.get("name", ""), item.get("detail", "")),
                    tags=(status,),
                )
            self.notebook.select(self.diagnostics_tab)

        def _run_diagnostics(self) -> None:
            self._start(["doctor", "--json"], "doctor")

        def _browse_game(self) -> None:
            selected = filedialog.askdirectory(title="Select local game package folder")
            if selected:
                self.game_dir.set(selected)

        def _browse_output(self) -> None:
            selected = filedialog.askdirectory(title="Select FRAMEZERO output folder")
            if selected:
                self.output_dir.set(selected)

        def _browse_work(self) -> None:
            selected = filedialog.askdirectory(title="Select work folder")
            if selected:
                self.work_dir.set(selected)

        def _find_package(self) -> None:
            self.notebook.select(self.build_tab)
            self._start(["build", "--find"], "find")

        def _game_folder_ready(self) -> bool:
            folder = Path(self.game_dir.get()).expanduser()
            if not folder.is_dir():
                messagebox.showerror("FRAMEZERO", "Select an existing local package folder.")
                return False
            if not (folder / "MicrosoftGame.Config").is_file():
                messagebox.showerror(
                    "FRAMEZERO",
                    "MicrosoftGame.Config was not found in this folder. Select the package folder described in the upstream documentation.",
                )
                return False
            return True

        def _validate_package(self) -> None:
            if not self._game_folder_ready():
                return
            try:
                args = build_validation_args(self.game_dir.get())
            except ValueError as exc:
                messagebox.showerror("FRAMEZERO", str(exc))
                return
            self._start(args, "validate")

        def _start_selected_build(self) -> None:
            if not self._game_folder_ready():
                return
            mode = self.mode_map.get(self.mode_label.get())
            try:
                args = build_engine_args(mode or "", self.game_dir.get(), self.output_dir.get(), self.work_dir.get())
            except ValueError as exc:
                messagebox.showerror("FRAMEZERO", str(exc))
                return
            if mode == "full":
                accepted = messagebox.askyesno(
                    "Full build",
                    "The upstream estimates about 400 GiB of work space for a full build. Start the full pipeline?",
                )
                if not accepted:
                    return
            self._start(args, "build")

        def _stop_process(self) -> None:
            process = self.process
            if process and process.poll() is None:
                try:
                    process.terminate()
                    self.footer.set("Stop requested — waiting for process to exit")
                    self.root.after(2500, self._force_stop, process)
                except OSError as exc:
                    self._log("ERROR stopping process: " + str(exc))
                    self.footer.set("Could not stop process")

        def _force_stop(self, process: subprocess.Popen[str]) -> None:
            if self.process is process and process.poll() is None:
                try:
                    process.kill()
                    self.footer.set("Process force-stopped")
                except OSError as exc:
                    self._log("ERROR force-stopping process: " + str(exc))

        def _close(self) -> None:
            process = self.process
            if process and process.poll() is None:
                try:
                    process.terminate()
                except OSError:
                    pass
            self.root.destroy()

    root = tk.Tk()
    FramezeroApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
