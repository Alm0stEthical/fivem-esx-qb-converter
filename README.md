![FiveM Converter - ESX to QB-Core and QB-Core to ESX converter tool for FiveM resources](https://github.com/Alm0stEthical/esx-qb-converter/assets/136627966/a223d9a2-dff2-4f80-88f2-1fe1a0f77f68)

# FiveM ESX/QB-Core Converter

Convert FiveM Lua resource scripts between ESX and QB-Core frameworks. Web UI powered by NiceGUI.

## Quick Start

```bash
git clone https://github.com/Alm0stEthical/fivem-esx-qb-converter.git
cd fivem-esx-qb-converter
pip install .
python main.py
```

Opens a browser UI where you pick a folder of `.lua` files, choose a direction, and hit Convert.

## Requirements

- Python 3.9+

## Project Structure

```
main.py              Entry point
src/
  core/
    converter.py     File walking + string replacement
    patterns.py      ESX <-> QB-Core mapping tables
  ui/
    components.py    NiceGUI UI widgets
```

## Versioning

This project uses [Semantic Versioning](https://semver.org/). See [CHANGELOG.md](CHANGELOG.md) for release history.

## License

MIT - see [LICENSE](LICENSE).

## Credits

Original creators: dFuZe & densuz
