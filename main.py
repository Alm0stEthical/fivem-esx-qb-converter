import os
from pathlib import Path

from nicegui import ui, app

from src import __version__
from src.core.patterns import PATTERNS
from src.core.converter import process_folder
from src.core.profiles import PROFILE_GENERIC, PROFILE_QB_BANKING_ESX_COMPAT
from src.ui.components import create_folder_selector, create_conversion_options, create_output_console


def detect_source_framework(folder: str) -> str:
    qb_markers = ["QBCore", "qb-core", "qb-target", "PlayerData", "citizenid"]
    esx_markers = ["ESX", "es_extended", "xPlayer", "esx:"]
    qb_hits = 0
    esx_hits = 0

    for path in Path(folder).rglob("*.lua"):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lowered = content.lower()
        qb_hits += sum(1 for marker in qb_markers if marker.lower() in lowered)
        esx_hits += sum(1 for marker in esx_markers if marker.lower() in lowered)

    if qb_hits > esx_hits and qb_hits > 0:
        return "QB-Core"
    if esx_hits > qb_hits and esx_hits > 0:
        return "ESX"
    return "Unknown"


def build_output_folder(source_folder: str, direction: str, profile: str) -> str:
    source = Path(source_folder).resolve()
    suffix = "esx_to_qb" if direction == "ESX to QB-Core" else "qb_to_esx"
    if profile == PROFILE_QB_BANKING_ESX_COMPAT and direction == "QB-Core to ESX":
        suffix = f"{suffix}_banking_compat"
    base = source.parent / f"{source.name}_{suffix}_converted"
    candidate = base
    index = 1
    while candidate.exists():
        candidate = source.parent / f"{base.name}_{index}"
        index += 1
    return str(candidate)


def setup():
    ui.add_head_html(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
        <style>
            :root {
                --app-ink: #0f172a;
                --app-bg-start: #f8fafc;
                --app-bg-end: #e2e8f0;
                --app-primary: #0ea5a4;
                --app-primary-hover: #0b8a89;
                --app-danger: #dc2626;
                --app-danger-hover: #b91c1c;
            }
            body {
                font-family: "Space Grotesk", "Segoe UI", sans-serif;
                color: var(--app-ink);
                background:
                    radial-gradient(circle at 12% 16%, #bae6fd 0%, transparent 24%),
                    radial-gradient(circle at 85% 20%, #99f6e4 0%, transparent 22%),
                    linear-gradient(165deg, var(--app-bg-start) 0%, var(--app-bg-end) 90%);
                min-height: 100vh;
            }
            .font-mono, code, pre { font-family: "JetBrains Mono", Consolas, monospace; }
            .app-shell { width: 100%; max-width: 64rem; margin: 0 auto; padding: 2rem 1rem 1.5rem; gap: 1rem; }
            .app-panel {
                border-radius: 1rem;
                border: 1px solid #cbd5e1;
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.07);
                background: rgba(255, 255, 255, 0.92);
                padding: 1rem;
            }
            .app-btn {
                border-radius: 0.7rem;
                font-weight: 600;
                text-transform: none;
                padding: 0.5rem 0.95rem;
                letter-spacing: 0.01em;
            }
            .app-btn-primary { background: var(--app-primary); color: white; }
            .app-btn-primary:hover { background: var(--app-primary-hover); }
            .app-btn-danger { background: var(--app-danger); color: white; }
            .app-btn-danger:hover { background: var(--app-danger-hover); }
        </style>
        """
    )

    ui.colors(
        primary="#0ea5a4",
        secondary="#0f172a",
        accent="#0284c7",
        positive="#22c55e",
        negative="#ef4444",
        warning="#f59e0b",
        info="#0ea5e9",
    )

    ui.page_title("ESX/QB-Core Converter")

    with ui.column().classes("app-shell"):
        with ui.row().classes("w-full justify-end"):
            ui.badge(f"v{__version__}").classes("bg-cyan-700 text-white py-2 px-3")

        path_input = create_folder_selector()
        direction, profile = create_conversion_options()
        add_message, clear_output = create_output_console()

        with ui.card().classes("w-full app-panel"):
            with ui.row().classes("w-full justify-end gap-2"):
                ui.button("Convert", on_click=lambda: convert(
                    path_input, direction, profile, add_message, clear_output
                ), icon="bolt").classes("app-btn app-btn-primary")
                ui.button("Exit", on_click=lambda: app.shutdown(), icon="power_settings_new").props("flat")


def convert(path_input, direction, profile, add_message, clear_output):
    folder = path_input.value or ""
    if not folder:
        ui.notify("Please select a folder", type="negative")
        return

    if not os.path.isdir(folder):
        ui.notify("Not a valid directory", type="negative")
        return

    selected = direction.value
    selected_profile = profile.value or PROFILE_GENERIC
    patterns = PATTERNS[selected] if selected_profile == PROFILE_GENERIC else []
    source_framework = detect_source_framework(folder)

    if selected_profile == PROFILE_QB_BANKING_ESX_COMPAT and selected != "QB-Core to ESX":
        ui.notify("Compat Bridge profile is only for QB-Core to ESX direction.", type="warning")
        add_message("Selected profile only supports QB-Core to ESX. Switch direction.", "warning")
        return

    if selected == "ESX to QB-Core" and source_framework == "QB-Core":
        ui.notify("Direction mismatch: source looks QB-Core. Use 'QB-Core to ESX'.", type="warning")
        add_message("Direction mismatch detected. Source appears to be QB-Core.", "warning")
        return
    if selected == "QB-Core to ESX" and source_framework == "ESX":
        ui.notify("Direction mismatch: source looks ESX. Use 'ESX to QB-Core'.", type="warning")
        add_message("Direction mismatch detected. Source appears to be ESX.", "warning")
        return

    if selected == "QB-Core to ESX" and selected_profile == PROFILE_GENERIC:
        add_message(
            "Generic mode is conservative and may skip unsafe rewrites. "
            "Use 'QB-Core -> ESX (Compat Bridge)' for broad compatibility.",
            "warning",
        )

    output_folder = build_output_folder(folder, selected, selected_profile)

    clear_output()
    add_message(f"Starting conversion: {selected}", "info")
    add_message(f"Profile: {selected_profile}", "info")
    add_message(f"Detected source framework: {source_framework}", "info")
    add_message(f"Source: {folder}", "info")
    add_message(f"Output: {output_folder}", "info")

    def on_progress(msg: str):
        if msg.startswith("Converted:"):
            add_message(msg, "success")
        elif msg.startswith("Error:"):
            add_message(msg, "error")
        else:
            add_message(msg, "info")

    try:
        stats = process_folder(folder, output_folder, patterns, selected, selected_profile, on_progress)

        add_message("--- Summary ---", "info")
        add_message(f"Total files: {stats['total']}", "info")
        add_message(f"Converted: {stats['converted']}", "success")
        add_message(f"Skipped: {stats['skipped']}", "info")
        if stats.get("unsafe_skipped", 0) > 0:
            add_message(
                f"Unsafe mixed outputs prevented: {stats['unsafe_skipped']} file(s) kept original",
                "warning",
            )
        if stats["errors"] > 0:
            add_message(f"Errors: {stats['errors']}", "error")
        if stats.get("flagged", 0) > 0:
            add_message(f"Needs manual review: {stats['flagged']} file(s)", "warning")
            hints = stats.get("review_hints", [])
            for hint in hints[:5]:
                add_message(f"Review: {hint}", "warning")

        add_message(f"Output folder ready: {output_folder}", "success")
        add_message("Done.", "success")
        ui.notify(f"Conversion complete. Output: {output_folder}", type="positive", timeout=6000)
    except Exception as e:
        add_message(f"Fatal error: {e}", "error")
        ui.notify(f"Error: {e}", type="negative")


def main():
    setup()
    ui.run(title="ESX/QB-Core Converter")


if __name__ in {"__main__", "__mp_main__"}:
    main()
