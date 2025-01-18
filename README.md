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

Tags:
FiveM scripting tutorials, ESX to QB-Core guide, FiveM modding tools, Lua to Lua script converter, Server migration tools, ESX QB-Core bridge, FiveM resource converter, ESX QB-Core toolkit, FiveM development environment, ESX QB-Core script bridge, FiveM server management, ESX QB-Core integration tools, FiveM scripting resources, ESX to QB-Core transition, QB-Core to ESX migration guide, FiveM scripting framework, ESX QB-Core adaptation, FiveM custom scripts, ESX QB-Core compatibility tools, FiveM Lua tools, ESX to QB-Core scripts, QB-Core to ESX scripts, FiveM resource optimization, ESX QB-Core script editor, FiveM development suite, ESX QB-Core converter tool, FiveM scripting APIs, ESX QB-Core interoperability, FiveM modding scripts, ESX QB-Core sync, FiveM server frameworks, ESX QB-Core plugin, FiveM script compatibility, ESX QB-Core code converter, FiveM server scripts conversion, ESX QB-Core bridge scripts, FiveM development tools suite, ESX QB-Core script tools, FiveM resource management tools, ESX QB-Core automated scripts, FiveM Lua converter, ESX QB-Core script migration, FiveM scripting platform, ESX QB-Core integration scripts, FiveM resource editing, ESX QB-Core code compatibility, FiveM custom resource converter, ESX QB-Core development, FiveM script migration tools, ESX QB-Core script compatibility, FiveM resource conversion tools, ESX QB-Core framework tools, FiveM Lua script tools, ESX QB-Core server integration, FiveM community script converter, ESX QB-Core migration tools, FiveM scripting conversion, ESX QB-Core script bridge, FiveM resource editing tools, ESX QB-Core automated migration, FiveM Lua resource converter, ESX QB-Core integration toolkit, FiveM script editing tools, ESX QB-Core script integration, FiveM server resource converter, ESX QB-Core code tools, FiveM framework conversion, ESX QB-Core scripting toolkit, FiveM server script tools, ESX QB-Core development tools, FiveM script management, ESX QB-Core resource editing, FiveM Lua conversion tools, ESX QB-Core script optimization, FiveM server script migration, ESX QB-Core compatibility converter, FiveM resource development tools, ESX QB-Core script development, FiveM framework tools, ESX QB-Core migration scripts, FiveM Lua script editor, ESX QB-Core conversion toolkit, FiveM resource compatibility, ESX QB-Core integration development, FiveM script development tools, ESX QB-Core framework integration, FiveM resource bridge, ESX QB-Core script optimization, FiveM server development tools, ESX QB-Core resource converter, FiveM Lua resource management, ESX QB-Core code migration, FiveM scripting framework tools, ESX QB-Core script compatibility tools, FiveM resource scripting, ESX QB-Core server scripts, FiveM Lua framework converter, ESX QB-Core resource management, FiveM script compatibility converter, ESX QB-Core resource bridge, FiveM automated scripting, ESX QB-Core integration modules, FiveM Lua debugging tools, ESX QB-Core server setup, FiveM resource loader, ESX QB-Core script tester, FiveM deployment tools, ESX QB-Core performance optimization, FiveM version control integration, ESX QB-Core dependency management, FiveM real-time script editing, ESX QB-Core user interface tools, FiveM script versioning, ESX QB-Core error handling, FiveM collaborative scripting, ESX QB-Core documentation tools, FiveM script repository, ESX QB-Core update manager, FiveM resource backup tools, ESX QB-Core customization tools, FiveM script benchmarking, ESX QB-Core localization tools, FiveM API integration, ESX QB-Core security tools, FiveM multi-framework support, ESX QB-Core scalability tools, FiveM automated testing tools, ESX QB-Core logging tools, FiveM script packaging, ESX QB-Core deployment scripts, FiveM continuous integration, ESX QB-Core automation scripts, esx to qb, qb to esx, esx to qb-core, qb-core to esx
