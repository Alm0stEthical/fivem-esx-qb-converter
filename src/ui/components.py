"""
UI components for the ESX/QB-Core Converter application.
"""
from typing import Callable, Dict, List, Optional, Tuple, Any
from nicegui import ui
from tkinter import filedialog
import os


class FolderSelector:
    """A component for selecting a folder from the file system."""
    
    def __init__(self, label: str = "Select Folder:"):
        """Initialize the folder selector component.
        
        Args:
            label (str, optional): Label text for the component. Defaults to "Select Folder:".
        """
        self.container = ui.card().classes('w-full p-4 shadow-md')
        with self.container:
            with ui.row().classes('w-full items-center'):
                ui.label(label).classes('text-lg font-medium')
                self.path_input = ui.input(placeholder='Path to folder...').classes('flex-grow mx-2')
                ui.button('Browse', on_click=self._browse_folder).classes(
                    'bg-primary text-white hover:bg-primary-dark'
                )
    
    def _browse_folder(self):
        """Open a dialog to select a folder."""
        folder = filedialog.askdirectory()
        if folder:
            self.path_input.value = folder
    
    @property
    def value(self) -> str:
        """Get the selected folder path.
        
        Returns:
            str: The selected folder path.
        """
        return self.path_input.value or ""
    
    @value.setter
    def value(self, path: str):
        """Set the folder path.
        
        Args:
            path (str): The folder path to set.
        """
        self.path_input.value = path


class ConversionOptions:
    """A component for selecting conversion options."""
    
    def __init__(self):
        """Initialize the conversion options component."""
        self.container = ui.card().classes('w-full p-4 mt-4 shadow-md')
        with self.container:
            ui.label('Conversion Options').classes('text-xl font-bold mb-4')
            
            with ui.row().classes('w-full items-center mb-4'):
                ui.label('Direction:').classes('text-lg font-medium mr-4')
                self.direction = ui.select(
                    options=['ESX to QB-Core', 'QB-Core to ESX'],
                    value='ESX to QB-Core'
                ).classes('flex-grow')
            
            with ui.row().classes('w-full items-center'):
                ui.label('Include SQL Patterns:').classes('text-lg font-medium mr-4')
                self.include_sql = ui.switch(value=False)
    
    @property
    def conversion_direction(self) -> str:
        """Get the selected conversion direction.
        
        Returns:
            str: The selected conversion direction.
        """
        return self.direction.value
    
    @property
    def include_sql_patterns(self) -> bool:
        """Get whether to include SQL patterns.
        
        Returns:
            bool: Whether to include SQL patterns.
        """
        return self.include_sql.value


class OutputConsole:
    """A component for displaying output messages."""
    
    def __init__(self):
        """Initialize the output console component."""
        self.container = ui.card().classes('w-full p-4 mt-4 shadow-md')
        with self.container:
            ui.label('Conversion Output').classes('text-xl font-bold mb-2')
            
            # Create a scrollable container for the output
            self.output_area = ui.scroll_area().classes('h-64 w-full border border-gray-300 rounded p-2 bg-gray-100')
            with self.output_area:
                self.output_text = ui.html().classes('font-mono text-sm whitespace-pre-wrap')
            
            # Add clear button
            with ui.row().classes('w-full justify-end mt-2'):
                ui.button('Clear Output', on_click=self.clear).classes(
                    'bg-red-500 text-white hover:bg-red-600'
                )
            
        self._messages = []
    
    def add_message(self, message: str, message_type: str = 'info'):
        """Add a message to the output console.
        
        Args:
            message (str): The message to add.
            message_type (str, optional): The type of message ('info', 'success', 'error', 'warning'). 
                                         Defaults to 'info'.
        """
        # Define colors for different message types
        colors = {
            'info': 'text-blue-600',
            'success': 'text-green-600',
            'error': 'text-red-600',
            'warning': 'text-yellow-600'
        }
        
        color_class = colors.get(message_type, colors['info'])
        timestamp = ui.get_time().strftime('%H:%M:%S')
        
        self._messages.append(f'<div class="{color_class}">[{timestamp}] {message}</div>')
        self.output_text.content = '\n'.join(self._messages)
        
        # Auto-scroll to bottom
        self.output_area.scroll_to(percent=1.0)
    
    def clear(self):
        """Clear all messages from the output console."""
        self._messages = []
        self.output_text.content = ''
    
    @property
    def value(self) -> str:
        """Get the current output text.
        
        Returns:
            str: The current output text.
        """
        return '\n'.join(self._messages)
    
    @value.setter
    def value(self, text: str):
        """Set the output text.
        
        Args:
            text (str): The text to set.
        """
        self._messages = [text]
        self.output_text.content = text


class ActionButtons:
    """A component for action buttons."""
    
    def __init__(self, convert_callback: Callable[[], None], quit_callback: Callable[[], None]):
        """Initialize the action buttons component.
        
        Args:
            convert_callback (Callable[[], None]): Callback function for the Convert button.
            quit_callback (Callable[[], None]): Callback function for the Exit button.
        """
        self.container = ui.card().classes('w-full p-4 mt-4 shadow-md')
        with self.container:
            with ui.row().classes('w-full justify-between'):
                ui.button('Convert', on_click=convert_callback).classes(
                    'bg-green-500 text-white hover:bg-green-600 px-6 py-2'
                )
                ui.button('Exit', on_click=quit_callback).classes(
                    'bg-gray-500 text-white hover:bg-gray-600 px-6 py-2'
                )
