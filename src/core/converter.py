import os
import shutil
from pathlib import Path

from src.core.profiles import (
    PROFILE_GENERIC,
    PROFILE_QB_BANKING_ESX_COMPAT,
    apply_profile_rewrite,
    write_profile_extras,
)


LEFTOVER_MARKERS = {
    "ESX to QB-Core": ["ESX.", "es_extended", "xPlayer.", "esx:"],
    "QB-Core to ESX": ["QBCore", "qb-core", "qb-target", "citizenid", "PlayerData"],
}

PROFILE_LEFTOVER_MARKERS = {
    ("QB-Core to ESX", PROFILE_QB_BANKING_ESX_COMPAT): [
        "exports['qb-core']",
        'exports["qb-core"]',
        "@qb-core/shared/locale.lua",
        "ESX.GetPlayerFromIdByCitizenId",
    ]
}


def convert_script(content: str, patterns: list[tuple[str, str]]) -> str:
    for old, new in patterns:
        content = content.replace(old, new)
    return content


def find_leftover_markers(content: str, direction: str, profile: str) -> list[str]:
    scoped = PROFILE_LEFTOVER_MARKERS.get((direction, profile))
    if scoped is not None:
        lower = content.lower()
        return [marker for marker in scoped if marker.lower() in lower]
    lower = content.lower()
    return [marker for marker in LEFTOVER_MARKERS.get(direction, []) if marker.lower() in lower]


def find_marker_hits(
    content: str,
    direction: str,
    profile: str,
    max_hits: int = 6,
) -> list[tuple[int, str]]:
    markers = PROFILE_LEFTOVER_MARKERS.get((direction, profile), LEFTOVER_MARKERS.get(direction, []))
    hits: list[tuple[int, str]] = []
    seen: set[tuple[int, str]] = set()

    for line_no, line in enumerate(content.splitlines(), start=1):
        lowered = line.lower()
        for marker in markers:
            if marker.lower() in lowered:
                entry = (line_no, marker)
                if entry not in seen:
                    seen.add(entry)
                    hits.append(entry)
                    if len(hits) >= max_hits:
                        return hits
    return hits


def is_mixed_framework_result(content: str, direction: str, profile: str) -> bool:
    if profile != PROFILE_GENERIC:
        return False
    lower = content.lower()
    has_qb = "qbcore" in lower or "qb-core" in lower
    has_esx = "esx" in lower or "es_extended" in lower
    if direction == "QB-Core to ESX":
        return has_qb and has_esx
    if direction == "ESX to QB-Core":
        return has_qb and has_esx
    return False


def process_file(
    source_path: str,
    destination_path: str,
    patterns: list[tuple[str, str]],
    direction: str,
    profile: str,
    relative_path: str,
) -> tuple[bool, list[str], bool]:
    try:
        content = Path(source_path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise RuntimeError(f"Failed to read {source_path}: {exc}") from exc

    rewritten = apply_profile_rewrite(content, relative_path, direction, profile)
    converted = convert_script(rewritten, patterns)
    unsafe_mixed = is_mixed_framework_result(converted, direction, profile)
    final_content = content if unsafe_mixed else converted

    try:
        Path(destination_path).write_text(final_content, encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Failed to write {destination_path}: {exc}") from exc

    if unsafe_mixed:
        return False, ["mixed-framework symbols"], True
    return converted != content, find_leftover_markers(converted, direction, profile), False


def process_folder(
    source_folder: str,
    destination_folder: str,
    patterns: list[tuple[str, str]],
    direction: str,
    profile: str = PROFILE_GENERIC,
    callback=None,
) -> dict[str, object]:
    stats = {
        "total": 0,
        "converted": 0,
        "skipped": 0,
        "errors": 0,
        "flagged": 0,
        "unsafe_skipped": 0,
        "review_hints": [],
    }
    source_root = Path(source_folder)
    destination_root = Path(destination_folder)

    destination_root.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(source_folder):
        for name in files:
            source_path = Path(root) / name
            relative_path = source_path.relative_to(source_root)
            destination_path = destination_root / relative_path
            destination_path.parent.mkdir(parents=True, exist_ok=True)

            if source_path.suffix != ".lua":
                try:
                    shutil.copy2(source_path, destination_path)
                except OSError as exc:
                    stats["errors"] += 1
                    if callback:
                        callback(f"Error: Failed to copy {source_path}: {exc}")
                continue

            stats["total"] += 1

            try:
                changed, leftovers, unsafe_mixed = process_file(
                    str(source_path),
                    str(destination_path),
                    patterns,
                    direction,
                    profile,
                    str(relative_path).replace("\\", "/"),
                )
                if unsafe_mixed:
                    stats["unsafe_skipped"] += 1
                    if callback:
                        callback(
                            f"Warning: {destination_path} produced mixed QB/ESX symbols; kept original content."
                        )

                if changed:
                    stats["converted"] += 1
                    if callback:
                        callback(f"Converted: {destination_path}")
                else:
                    stats["skipped"] += 1
                    if callback:
                        callback(f"Skipped: {destination_path}")
                if leftovers:
                    if unsafe_mixed:
                        hits = []
                    else:
                        try:
                            hits = find_marker_hits(
                                destination_path.read_text(encoding="utf-8"),
                                direction,
                                profile,
                            )
                        except OSError:
                            hits = []
                    stats["flagged"] += 1
                    if hits:
                        hint = f"{destination_path}: " + ", ".join(
                            [f"L{line} {marker}" for line, marker in hits]
                        )
                    else:
                        hint = f"{destination_path}: " + ", ".join(leftovers)
                    stats["review_hints"].append(hint)
                    if callback:
                        callback(f"Warning: {hint}")
            except RuntimeError as exc:
                stats["errors"] += 1
                if callback:
                    callback(f"Error: {exc}")

    try:
        created = write_profile_extras(destination_root, direction, profile)
        if callback:
            for path in created:
                callback(f"Converted: {path}")
    except OSError as exc:
        stats["errors"] += 1
        if callback:
            callback(f"Error: Failed to write profile extras: {exc}")

    return stats
