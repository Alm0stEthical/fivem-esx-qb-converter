![FiveM Converter - ESX to QB-Core and QB-Core to ESX converter tool for FiveM resources](https://github.com/Alm0stEthical/esx-qb-converter/assets/136627966/a223d9a2-dff2-4f80-88f2-1fe1a0f77f68)
# FiveM ESX/QB-Core Converter
The ESX/QB-Core Converter is a Python script that helps you convert FiveM resource scripts between the ESX and QB-Core frameworks. It provides an easy-to-use graphical user interface (GUI) built with the `customtkinter` library.

## Features

- Converts FiveM resource scripts from ESX to QB-Core and vice versa.
- Supports a wide range of conversion patterns for client-side and server-side code.
- Processes all `.lua` files in the selected folder and its subfolders.
- Provides a user-friendly GUI for selecting the folder and conversion direction.
- Displays the conversion progress and results in a text output area.

## Requirements

- Python 3.x
- `customtkinter` library

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Alm0stEthical/esx-qb-converter.git
   ```

2. Install the required dependencies:
   ```
   pip install customtkinter
   ```

## Usage

1. Run the script:
   ```
   python main.py
   ```

2. In the GUI:
   - Click the "Browse" button to select the folder containing the FiveM resource scripts you want to convert.
   - Choose the conversion direction: "ESX to QB-Core" or "QB-Core to ESX".
   - Click the "Convert" button to start the conversion process.
    
3. The script will process all `.lua` files in the selected folder and its subfolders, applying the appropriate conversion patterns based on the selected direction.

4. The conversion progress and results will be displayed in the GUI.

5. Once the conversion is completed, the modified files will be saved in their origina; locations.

## Customization

- You can add or modify the conversion patterns in the `load_conversion_patterns()` function to adapt the script to your specific needs.
- The `manual_replace()` function allows you to define custom replacements that are applied before the pattern-based replacements.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- The script uses the [customtkinter](https://github.com/TomSchimansky/CustomTkinter) library for creating the GUI.
- The conversion patterns source are from https://github.com/DeffoN0tSt3/ESX-QBCore-Convert-Functions.

## Disclaimer

This script is provided as-is and may not cover all possible conversion scenarios. Please review the converted files manually to make sure the wanted results are achieved.
