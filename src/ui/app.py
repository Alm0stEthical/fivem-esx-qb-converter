"""
Main application UI for the ESX/QB-Core Converter.
"""
from typing import Dict, List, Tuple, Optional
from nicegui import ui
import sys
import os

from src.ui.components import FolderSelector, ConversionOptions, OutputConsole, ActionButtons
from src.core.patterns import load_conversion_patterns
from src.core.converter import process_folder


class ConverterApp:
    """Main application class for the ESX/QB-Core Converter."""
    
    def __init__(self):
        """Initialize the converter application."""
        # Set up the UI theme
        ui.colors(
            primary='#10b981',
            secondary='#3b82f6',
            accent='#8b5cf6',
            positive='#22c55e',
            negative='#ef4444',
            warning='#f59e0b',
            info='#3b82f6'
        )
        
        # Load conversion patterns
        self.patterns = load_conversion_patterns()
        
        # Set up the UI layout
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI layout."""
        # Set page title and favicon
        ui.page_title('ESX/QB-Core Converter')
        
        # Create the header
        with ui.header().classes('bg-primary text-white'):
            ui.label('ESX/QB-Core Converter').classes('text-2xl font-bold p-4')
        
        # Create the main content area
        with ui.column().classes('w-full max-w-3xl mx-auto p-4 gap-4'):
            # Add a brief description
            with ui.card().classes('w-full p-4 shadow-md'):
                ui.label('Convert FiveM scripts between ESX and QB-Core frameworks').classes('text-lg')
                ui.markdown('''
                This tool allows you to convert Lua scripts between ESX and QB-Core frameworks.
                Select a folder containing Lua scripts, choose the conversion direction, and click Convert.
                ''').classes('text-sm text-gray-600')
            
            # Add the folder selector
            self.folder_selector = FolderSelector()
            
            # Add conversion options
            self.conversion_options = ConversionOptions()
            
            # Add action buttons
            self.action_buttons = ActionButtons(
                convert_callback=self._convert,
                quit_callback=self._quit
            )
            
            # Add output console
            self.output_console = OutputConsole()
        
        # Add footer
        with ui.footer().classes('bg-gray-100 text-gray-600 p-4'):
            ui.label('ESX/QB-Core Converter by dFuZe & densuz').classes('text-sm')
    
    def _convert(self):
        """Start the conversion process based on user input."""
        folder = self.folder_selector.value
        if not folder:
            ui.notify('Please select a folder', type='negative')
            return
        
        if not os.path.isdir(folder):
            ui.notify('Selected path is not a valid directory', type='negative')
            return
        
        direction = self.conversion_options.conversion_direction
        include_sql = self.conversion_options.include_sql_patterns
        
        # Clear and update output console
        self.output_console.clear()
        self.output_console.add_message(f"Starting conversion: {direction}", 'info')
        self.output_console.add_message(f"Processing folder: {folder}", 'info')
        self.output_console.add_message(
            f"Include SQL Patterns: {'Yes' if include_sql else 'No'}", 'info'
        )
        
        # Select patterns based on direction
        if direction == "ESX to QB-Core":
            selected_patterns = self.patterns["ESX_to_QB_Core"]
        else:
            selected_patterns = self.patterns["QB_Core_to_ESX"]
        
        sql_patterns = self.patterns.get("SQL_patterns", [])
        
        # Define callback for progress updates
        def update_progress(message: str):
            if "Converted:" in message:
                self.output_console.add_message(message, 'success')
            elif "No changes needed:" in message:
                self.output_console.add_message(message, 'info')
            elif "Error" in message:
                self.output_console.add_message(message, 'error')
            else:
                self.output_console.add_message(message, 'info')
        
        try:
            # Process the folder
            stats = process_folder(
                folder,
                selected_patterns,
                direction,
                include_sql,
                sql_patterns,
                update_progress
            )
            
            # Display summary
            self.output_console.add_message("\n--- Conversion Summary ---", 'info')
            self.output_console.add_message(f"Total files processed: {stats['total_files']}", 'info')
            self.output_console.add_message(f"Files converted: {stats['converted_files']}", 'success')
            self.output_console.add_message(f"Files skipped (no changes needed): {stats['skipped_files']}", 'info')
            
            if stats['error_files'] > 0:
                self.output_console.add_message(f"Files with errors: {stats['error_files']}", 'error')
            
            self.output_console.add_message("\nConversion completed successfully!", 'success')
            
            # Show success notification
            ui.notify('Conversion completed successfully!', type='positive')
        except Exception as e:
            self.output_console.add_message(f"\nAn error occurred: {str(e)}", 'error')
            ui.notify(f'Error: {str(e)}', type='negative')
    
    def _quit(self):
        """Exit the application."""
        ui.notify('Exiting application...', type='info')
        sys.exit(0)
    
    def run(self):
        """Run the application."""
        ui.run(title="ESX/QB-Core Converter")
