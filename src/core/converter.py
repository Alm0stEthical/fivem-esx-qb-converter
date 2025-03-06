"""
Core converter functionality for ESX to QB-Core and QB-Core to ESX conversions.
"""
import os
import re
from typing import List, Tuple, Dict, Optional, Callable


def manual_replace(script: str) -> str:
    """
    Perform manual replacements for specific code patterns.

    Args:
        script (str): The content of the script file.

    Returns:
        str: The modified script content.
    """
    replacements = {
        "local QBCore = exports['qb-core']:GetCoreObject()": "ESX = exports['es_extended']:getSharedObject()",
        "QBCore = exports['qb-core']:GetCoreObject()": "ESX = exports['es_extended']:getSharedObject()",
    }

    for old, new in replacements.items():
        script = script.replace(old, new)

    return script


def convert_script(
    script: str, 
    patterns: List[Tuple[str, str]], 
    include_sql: bool = False, 
    sql_patterns: Optional[List[Tuple[str, str]]] = None
) -> str:
    """
    Convert the script content based on the provided patterns.

    Args:
        script (str): The original script content.
        patterns (List[Tuple[str, str]]): List of tuples containing old and new patterns.
        include_sql (bool, optional): Flag to include SQL patterns. Defaults to False.
        sql_patterns (Optional[List[Tuple[str, str]]], optional): List of SQL pattern tuples. Defaults to None.

    Returns:
        str: The converted script content.
    """
    if sql_patterns is None:
        sql_patterns = []
        
    script = manual_replace(script)
    for old, new in patterns:
        script = script.replace(old, new)
    
    if include_sql:
        for old, new in sql_patterns:
            script = script.replace(old, new)
            
    return script


def process_file(
    file_path: str, 
    patterns: List[Tuple[str, str]], 
    direction: str, 
    include_sql: bool, 
    sql_patterns: List[Tuple[str, str]]
) -> bool:
    """
    Process a single Lua script file, converting its content based on the patterns.

    Args:
        file_path (str): Path to the Lua script file.
        patterns (List[Tuple[str, str]]): List of tuples containing old and new patterns.
        direction (str): Conversion direction ("ESX to QB-Core" or "QB-Core to ESX").
        include_sql (bool): Flag to include SQL patterns.
        sql_patterns (List[Tuple[str, str]]): List of SQL pattern tuples.

    Returns:
        bool: True if changes were made, False otherwise
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        converted = convert_script(content, patterns, include_sql, sql_patterns)

        if content != converted:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(converted)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False


def process_folder(
    folder_path: str, 
    patterns: List[Tuple[str, str]], 
    direction: str, 
    include_sql: bool, 
    sql_patterns: List[Tuple[str, str]],
    callback: Optional[Callable[[str], None]] = None
) -> Dict[str, int]:
    """
    Recursively process all Lua script files in the specified folder.

    Args:
        folder_path (str): Path to the folder containing Lua script files.
        patterns (List[Tuple[str, str]]): List of tuples containing old and new patterns.
        direction (str): Conversion direction ("ESX to QB-Core" or "QB-Core to ESX").
        include_sql (bool): Flag to include SQL patterns.
        sql_patterns (List[Tuple[str, str]]): List of SQL pattern tuples.
        callback (Optional[Callable[[str], None]], optional): Callback function for progress updates. Defaults to None.

    Returns:
        Dict[str, int]: Statistics about the conversion process
    """
    stats = {
        "total_files": 0,
        "converted_files": 0,
        "skipped_files": 0,
        "error_files": 0
    }
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".lua"):
                file_path = os.path.join(root, file)
                stats["total_files"] += 1
                
                try:
                    was_converted = process_file(file_path, patterns, direction, include_sql, sql_patterns)
                    if was_converted:
                        stats["converted_files"] += 1
                        if callback:
                            callback(f"Converted: {file_path}")
                    else:
                        stats["skipped_files"] += 1
                        if callback:
                            callback(f"No changes needed: {file_path}")
                except Exception as e:
                    stats["error_files"] += 1
                    if callback:
                        callback(f"Error processing {file_path}: {str(e)}")
                        
    return stats
