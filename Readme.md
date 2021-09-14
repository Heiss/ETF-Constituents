# ETF Constituents

This tool enables you to inform yourself about the constituents in all your etf‘s. So it helps you to build a diversified portfolio with ETF.

# Installation

```bash
git clone https://github.com/Heiss/ETF-Constituents.git
pip install -r requirements.txt
chmod +x starter.sh
```

# Start the application

```bash
./starter.sh
```

# Configuration

The `config.txt` holds all indices, which should be tracked with the software. The syntax per line: `INSTITUTION INDEXNAME`. E.g. `MSCI WORLD`.

You can take a look into the settings in the gui (shortcut CTRL+O) to see all ETF's. You have to reload (shortcut CTRL+R) manually the list of all shares in the main window, after you change the used ETF's.

# current supported index institutions

- MSCI
- Solactive

# Upcoming features

- more institutions supported
- unittests for institutions
- using github actions
- executable file for windows
