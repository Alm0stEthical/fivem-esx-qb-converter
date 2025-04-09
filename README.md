![FiveM Converter - ESX to QB-Core and QB-Core to ESX converter tool for FiveM resources](https://github.com/Alm0stEthical/esx-qb-converter/assets/136627966/a223d9a2-dff2-4f80-88f2-1fe1a0f77f68)
# FiveM ESX/QB-Core Converter
The ESX/QB-Core Converter is a modern web-based application that helps you convert FiveM resource scripts between the ESX and QB-Core frameworks. It provides an intuitive user interface built with the `NiceGUI` library.

## Features

- Converts FiveM resource scripts from ESX to QB-Core and vice versa.
- Supports a wide range of conversion patterns for client-side and server-side code.
- Processes all `.lua` files in the selected folder and its subfolders.
- Provides a modern, responsive web interface for selecting the folder and conversion direction.
- Displays the conversion progress and results in real-time with color-coded output.
- Modular architecture for easy maintenance and extension.

## Requirements

- Python 3.x
- `nicegui` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Alm0stEthical/fivem-esx-qb-converter.git
   cd fivem-esx-qb-converter
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. The web interface will open in your default browser.

3. Select the folder containing the FiveM resource scripts you want to convert.

4. Choose the conversion direction (ESX to QB-Core or QB-Core to ESX).

5. Optionally, enable SQL pattern conversion.

6. Click the "Convert" button to start the conversion process.

7. View the conversion progress and results in the output console.

## Project Structure

The project follows a modular architecture for better organization and maintainability:

```
fivem-esx-qb-converter/
├── main.py                  # Entry point for the application
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── src/                     # Source code directory
    ├── core/                # Core functionality
    │   ├── converter.py     # Script conversion logic
    │   └── patterns.py      # Conversion patterns
    ├── ui/                  # User interface components
    │   ├── app.py           # Main application UI
    │   └── components.py    # Reusable UI components
    └── utils/               # Utility functions
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- Original creators: dFuZe & densuz
- Modernized version with NiceGUI: Alm0stEthical
