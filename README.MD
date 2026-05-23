# CoinGrep

A terminal-based cryptocurrency market and portfolio tracker built with Python. Fetch real-time prices, monitor global trends, track the Fear & Greed Index, and manage local wallet portfolios — all from the command line.

---

## Features

- Live cryptocurrency prices with market cap, volume, and 24h change
- Trending coins from CoinGecko
- Global crypto market statistics
- Fear & Greed Index
- Local wallet portfolio management (add, remove, list)
- Blockchain address validation
- Multi-wallet balance checking across chains
- SQLite-based local storage

---

## Requirements

### Python 3.9 or higher

```bash
python --version
```

If not installed:

**Linux (Ubuntu/Debian)**
```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv
```

**Arch Linux**
```bash
sudo pacman -S python
```

**Fedora**
```bash
sudo dnf install python3
```

**macOS**
```bash
brew install python
```

**Windows** — Download from python.org. During installation, enable **Add Python to PATH**.

### Git

```bash
git --version
```

If not installed: `sudo apt install git` (Linux), `brew install git` (macOS), or download Git for Windows.

---

## API Key

CoinGrep uses the CoinStats API for wallet balance tracking and address validation. Create a free API key at [coinstats.app](https://coinstats.app) before using wallet commands.

---

## Installation

**Clone the repository**
```bash
git clone https://github.com/MAhmadAhsan/coingrep.git
cd coingrep
```

**Create and activate a virtual environment**

Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (CMD):
```cmd
python -m venv venv
venv\Scripts\activate
```

Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Install dependencies**
```bash
pip install --upgrade pip
pip install .
```

For development mode:
```bash
pip install -e .
```

**Create the environment file**

Create a `.env` file in the project root:
```
coingrep/
├── .env
├── README.md
├── pyproject.toml
└── ...
```

Add your CoinStats API key:
```env
COINSTATS_API_KEY=your_api_key_here
```

---

## Commands

### Market Data

**Coin prices** — price, market cap, volume, and 24h change for one or more coins:
```bash
coingrep coins bitcoin ethereum solana
```

**Trending coins** — today's top trending coins on CoinGecko:
```bash
coingrep trending
```

**Global market overview** — active cryptocurrencies, total market cap, BTC/ETH dominance:
```bash
coingrep market
```

**Fear & Greed Index** — current value and classification:
```bash
coingrep fear-greed
```

**Supported blockchains** — list all blockchains supported by CoinStats:
```bash
coingrep blockchains
```

---

### Wallet Management

**Add a wallet**
```bash
coingrep wallet add --label "Main ETH" --address 0x123...abc --blockchain ethereum
```
The `--blockchain` flag is optional. When provided, the address is validated against that chain before saving.

**List saved wallets**
```bash
coingrep wallet list
```

**Check wallet balances**

By saved label:
```bash
coingrep wallet balance --label "Main ETH" --blockchain ethereum
```

By raw address:
```bash
coingrep wallet balance --address 0x123...abc --blockchain ethereum --blockchain polygon
```

Combined, across all chains:
```bash
coingrep wallet balance --label "Main ETH" --address 0xdef... --blockchain all
```

**Validate a wallet address**
```bash
coingrep wallet validate 0x123...abc --blockchain ethereum
```

**Remove a wallet**

By label:
```bash
coingrep wallet remove --label "Main ETH"
```

By address:
```bash
coingrep wallet remove --address 0x123...abc
```

---

## Local Storage

All data is stored locally using SQLite. Nothing is uploaded.

| Platform | Path |
|----------|------|
| Linux/macOS | `~/.coingrep/db/coingrep.db` |
| Windows | `C:\Users\YourUsername\.coingrep\` |

Logs are written to `~/.coingrep/logs/` on Linux/macOS.

---

## Privacy

Wallet addresses are stored locally only. No private keys are ever stored or transmitted. CoinGrep does not upload your local database.

---

## Technologies

- Python
- SQLite
- CoinGecko API
- CoinStats API

---

## License

MIT License