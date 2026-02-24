import html
from datetime import datetime
from pathlib import Path

from nicegui import ui

from src.core.profiles import PROFILES


async def _pick_directory(start_path: str) -> str | None:
    current = Path(start_path).expanduser().resolve()

    with ui.dialog() as dialog, ui.card().classes(
        "w-[46rem] max-w-[95vw] h-[34rem] max-h-[85vh] p-0 overflow-hidden"
    ):
        with ui.column().classes("w-full h-full"):
            with ui.row().classes("w-full items-center justify-between px-5 py-4 border-b border-slate-200"):
                ui.label("Choose Project Folder").classes("text-lg font-semibold text-slate-800")
                ui.button(icon="close", on_click=lambda: dialog.submit(None)).props("flat round dense")

            with ui.column().classes("w-full flex-1 px-5 py-4 gap-2 min-h-0"):
                current_label = ui.label().classes("text-xs uppercase tracking-wide text-slate-500 break-all")
                search_input = ui.input(
                    placeholder="Search folders in this directory...",
                    on_change=lambda _: render(),
                ).classes("w-full")
                search_input.props("outlined dense clearable prepend-icon=search")
                error_label = ui.label().classes("text-sm text-red-600 min-h-[1.2rem]")
                with ui.scroll_area().classes("w-full flex-1 min-h-0 bg-slate-50 rounded-xl border border-slate-200"):
                    list_container = ui.column().classes("w-full gap-1 p-2")

            with ui.row().classes("w-full justify-end gap-2 px-5 py-4 border-t border-slate-200"):
                ui.button("Cancel", on_click=lambda: dialog.submit(None)).props("flat")
                ui.button("Use This Folder", on_click=lambda: dialog.submit(str(current))).classes(
                    "app-btn app-btn-primary"
                )

    def open_folder(path: Path) -> None:
        nonlocal current
        try:
            current = path.expanduser().resolve()
            search_input.value = ""
            search_input.update()
            render()
        except OSError as exc:
            error_label.text = f"Could not open folder: {exc}"
            error_label.update()

    def render() -> None:
        current_label.text = f"Current: {current}"
        current_label.update()
        error_label.text = ""
        error_label.update()
        list_container.clear()
        with list_container:
            if current.parent != current:
                ui.button("..", icon="arrow_upward", on_click=lambda: open_folder(current.parent)).props(
                    "flat no-caps align=left"
                ).classes("w-full justify-start")

            try:
                folders = sorted(
                    [item for item in current.iterdir() if item.is_dir()],
                    key=lambda item: item.name.lower(),
                )
            except OSError as exc:
                error_label.text = f"Could not list folder: {exc}"
                error_label.update()
                folders = []

            query = (search_input.value or "").strip().lower()
            visible_folders = folders
            if query:
                visible_folders = [folder for folder in folders if query in folder.name.lower()]

            if not visible_folders:
                ui.label("No matching folders found.").classes("text-sm text-slate-500 p-2")

            for folder in visible_folders:
                ui.button(
                    folder.name,
                    icon="folder",
                    on_click=lambda target=folder: open_folder(target),
                ).props("flat no-caps align=left").classes("w-full justify-start")

    render()
    return await dialog


def create_folder_selector():
    with ui.card().classes("w-full app-panel"):
        ui.label("Target Folder").classes("text-lg font-semibold text-slate-900")
        ui.label("Pick the root folder that contains your Lua resources.").classes(
            "text-sm text-slate-500"
        )

        with ui.row().classes("w-full items-center gap-2 mt-1"):
            path_input = ui.input(placeholder=r"C:\path\to\resource").classes("flex-grow")
            path_input.props("outlined dense clearable")

            async def browse() -> None:
                start = path_input.value or str(Path.home())
                selected = await _pick_directory(start)
                if selected:
                    path_input.value = selected
                    path_input.update()

            ui.button("Browse", icon="folder_open", on_click=browse).classes("app-btn app-btn-primary")
    return path_input


def create_conversion_options():
    with ui.card().classes("w-full app-panel"):
        ui.label("Conversion Mode").classes("text-lg font-semibold text-slate-900")
        ui.label("Choose the framework direction for replacements.").classes(
            "text-sm text-slate-500 mb-1"
        )
        direction = ui.select(
            options=["ESX to QB-Core", "QB-Core to ESX"],
            value="ESX to QB-Core",
            with_input=False,
        ).classes("w-full")
        direction.props("outlined")

        ui.label("Rewrite Profile").classes("text-sm font-semibold text-slate-700 mt-2")
        ui.label(
            "Compat Bridge is content-driven for broad QB resources (not tied to fixed script names)."
        ).classes("text-sm text-slate-500 mb-1")
        profile = ui.select(
            options=PROFILES,
            value=PROFILES[0],
            with_input=False,
        ).classes("w-full")
        profile.props("outlined")
    return direction, profile


def create_output_console():
    messages: list[str] = []

    with ui.card().classes("w-full app-panel"):
        ui.label("Live Output").classes("text-lg font-semibold text-slate-900")
        scroll = ui.scroll_area().classes(
            "h-72 w-full border border-slate-200 rounded-xl p-3 bg-slate-950"
        )
        with scroll:
            output_html = ui.html().classes("font-mono text-sm whitespace-pre-wrap leading-6")

        with ui.row().classes("w-full justify-end mt-2"):

            def clear():
                messages.clear()
                output_html.content = ""

            ui.button("Clear", icon="ink_eraser", on_click=clear).classes("app-btn app-btn-danger")

    color_map = {
        "info": "text-sky-300",
        "success": "text-emerald-300",
        "error": "text-rose-300",
        "warning": "text-amber-300",
    }

    def add_message(text: str, level: str = "info"):
        css = color_map.get(level, color_map["info"])
        ts = datetime.now().strftime("%H:%M:%S")
        safe = html.escape(text)
        messages.append(f'<div class="{css}">[{ts}] {safe}</div>')
        output_html.content = "\n".join(messages)
        scroll.scroll_to(percent=1.0)

    return add_message, clear
