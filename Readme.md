# ETF Constituents

This tool enables you to inform yourself about the constituents in all your etf‘s. So it helps you to build a diversified portfolio with ETF.

# Installation

```bash
git clone https://github.com/Heiss/ETF-Constituents.git
pip install -r requirements.txt
chmod +x starter.sh
./starter.sh
```

# Configuration

The `config.txt` holds all indices, which should be tracked with the software. The syntax per line: `INSTITUTION INDEXNAME`. E.g. `MSCI WORLD`. Take a look into the file of your needed institution in `src/institutions/data` to find out, which indexname you have to enter.

# current supported index institutions

- MSCI

# Upcoming features

- friendly user interface in qt
- more institutions supported
