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

## Keywords

FiveM scripting tutorials, ESX to QB-Core guide, FiveM modding tools, Lua to Lua script converter, Server migration tools, ESX QB-Core bridge, FiveM resource converter, ESX QB-Core toolkit, FiveM development environment, ESX QB-Core script bridge, FiveM server management, ESX QB-Core integration tools, FiveM scripting resources, ESX to QB-Core transition, QB-Core to ESX migration guide, FiveM scripting framework, ESX QB-Core adaptation, FiveM custom scripts, ESX QB-Core compatibility tools, FiveM Lua tools, ESX to QB-Core scripts, QB-Core to ESX scripts, FiveM resource optimization, ESX QB-Core script editor, FiveM development suite, ESX QB-Core converter tool, FiveM scripting APIs, ESX QB-Core interoperability, FiveM modding scripts, ESX QB-Core sync, FiveM server frameworks, ESX QB-Core plugin, FiveM script compatibility, ESX QB-Core code converter, FiveM server scripts conversion, ESX QB-Core bridge scripts, FiveM development tools suite, ESX QB-Core script tools, FiveM resource management tools, ESX QB-Core automated scripts, FiveM Lua converter, ESX QB-Core script migration, FiveM scripting platform, ESX QB-Core integration scripts, FiveM resource editing, ESX QB-Core code compatibility, FiveM custom resource converter, ESX QB-Core development, FiveM script migration tools, ESX QB-Core script compatibility, FiveM resource conversion tools, ESX QB-Core framework tools, FiveM Lua script tools, ESX QB-Core server integration, FiveM community script converter, ESX QB-Core migration tools, FiveM scripting conversion, ESX QB-Core script bridge, FiveM resource editing tools, ESX QB-Core automated migration, FiveM Lua resource converter, ESX QB-Core integration toolkit, FiveM script editing tools, ESX QB-Core script integration, FiveM server resource converter, ESX QB-Core code tools, FiveM framework conversion, ESX QB-Core scripting toolkit, FiveM server script tools, ESX QB-Core development tools, FiveM script management, ESX QB-Core resource editing, FiveM Lua conversion tools, ESX QB-Core script optimization, FiveM server script migration, ESX QB-Core compatibility converter, FiveM resource development tools, ESX QB-Core script development, FiveM framework tools, ESX QB-Core migration scripts, FiveM Lua script editor, ESX QB-Core conversion toolkit, FiveM resource compatibility, ESX QB-Core integration development, FiveM script development tools, ESX QB-Core framework integration, FiveM resource bridge, ESX QB-Core script optimization, FiveM server development tools, ESX QB-Core resource converter, FiveM Lua resource management, ESX QB-Core code migration, FiveM scripting framework tools, ESX QB-Core script compatibility tools, FiveM resource scripting, ESX QB-Core server scripts, FiveM Lua framework converter, ESX QB-Core resource management, FiveM script compatibility converter, ESX QB-Core resource bridge, FiveM automated scripting, ESX QB-Core integration modules, FiveM Lua debugging tools, ESX QB-Core server setup, FiveM resource loader, ESX QB-Core script tester, FiveM deployment tools, ESX QB-Core performance optimization, FiveM version control integration, ESX QB-Core dependency management, FiveM real-time script editing, ESX QB-Core user interface tools, FiveM script versioning, ESX QB-Core error handling, FiveM collaborative scripting, ESX QB-Core documentation tools, FiveM script repository, ESX QB-Core update manager, FiveM resource backup tools, ESX QB-Core customization tools, FiveM script benchmarking, ESX QB-Core localization tools, FiveM API integration, ESX QB-Core security tools, FiveM multi-framework support, ESX QB-Core scalability tools, FiveM automated testing tools, ESX QB-Core logging tools, FiveM script packaging, ESX QB-Core deployment scripts, FiveM continuous integration, ESX QB-Core automation scripts, esx to qb, qb to esx, esx to qb-core, qb-core to esx
