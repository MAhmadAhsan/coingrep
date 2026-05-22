# COINGREP

A command-line crypto portfolio tracker that aggregates live market data, wallet balances, and global market statistics into a single terminal interface. Built with Python and Click, COINGREP connects to CoinGecko and CoinStats APIs to deliver real-time information without requiring a graphical interface or a web browser.

---

## Table of Contents

- [COINGREP](#coingrep)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Market Commands](#market-commands)
    - [Wallet Commands](#wallet-commands)
  - [Command Reference](#command-reference)
  - [Environment Variables](#environment-variables)
  - [Notes and Limitations](#notes-and-limitations)

---

## Overview

COINGREP is a terminal-first tool designed for users who prefer working in the command line and want quick access to cryptocurrency data without navigating dashboards or browser tabs. It stores wallet addresses locally in a SQLite database, fetches live prices and balances on demand, and renders all output as formatted tables directly in the terminal.

The tool is intentionally stateless at runtime — no background processes, no daemons, no scheduled polling. Every command makes a direct API call and returns immediately.

---

## Features

- Live price lookup for any coin by CoinGecko ID, including market cap, 24-hour volume, and percentage change
- Trending coins list pulled directly from CoinGecko's daily trending index
- Global crypto market overview covering total market cap, volume, BTC and ETH dominance, and active markets
- Crypto Fear and Greed Index from the Alternative.me API
- Blockchain network listing from CoinStats
- Local wallet portfolio management with add, remove, and list operations
- Live wallet balance fetching across any CoinStats-supported blockchain
- Address validation against a specific blockchain before saving
- All output rendered as Unicode box-drawing tables in the terminal

---

## Project Structure

```
COINGREP/
    app/
        cli.py            Entry point and all Click command definitions
        config.py         Configuration values, including DB_PATH
        CryptoClient.py   API client wrapping CoinGecko and CoinStats
        Database.py       SQLite wallet persistence layer
        logger.py         Logging setup
        TerminalTable.py  Unicode table renderer for terminal output
    .env                  Environment variables (API keys, not committed)
    .gitignore
    pyproject.toml
    README.md
```

---

## Requirements

- Python 3.10 or higher
- pip

The following third-party packages are installed automatically:

- `click` — CLI framework
- `requests` — HTTP client for API calls
- `python-dotenv` — loads environment variables from `.env`

---

## Installation

Clone the repository and install the package. It is recommended to use a virtual environment.

```bash
git clone https://github.com/your-username/coingrep.git
cd coingrep
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install .
```

After installation, the `coingrep` command becomes available in your environment.

## Configuration

COINGREP reads API keys from a `.env` file in the project root. Create the file before running any commands:

```
COINSTATS_API_KEY=your_coinstats_api_key_here
```

The local wallet database is created automatically on first use. Its path is defined in `config.py` via the `DB_PATH` variable. By default it writes to a file inside the project directory.

---

## Usage

All commands follow this structure:

```
coingrep [COMMAND] [SUBCOMMAND] [OPTIONS] [ARGUMENTS]
```

To see available commands:

```bash
coingrep --help
```

To see help for a specific command:

```bash
coingrep coins --help
coingrep wallet --help
```

---

### Market Commands

**Look up one or more coins by CoinGecko ID:**

```bash
coingrep coins bitcoin
coingrep coins bitcoin ethereum solana cardano
```

Output includes current price in USD, market cap, 24-hour trading volume, and 24-hour price change percentage.

**Show today's trending coins:**

```bash
coingrep trending
```

Displays the coins currently trending on CoinGecko, ranked by market cap, with price and 24-hour change.

**Show global market overview:**

```bash
coingrep market
```

Displays total market cap, total 24-hour volume, number of active cryptocurrencies and markets, BTC dominance, ETH dominance, and market cap change over the past 24 hours.

**Show the Fear and Greed Index:**

```bash
coingrep fear-greed
```

Returns the current index value, its classification (Extreme Fear, Fear, Neutral, Greed, Extreme Greed), and the timestamp of the reading.

**List supported blockchains:**

```bash
coingrep blockchains
```

Returns all blockchain networks supported by CoinStats, along with their connection IDs. These IDs are used as arguments to wallet commands.

---

### Wallet Commands

All wallet commands operate under the `wallet` subgroup:

```bash
coingrep wallet [SUBCOMMAND] [OPTIONS]
```

**Add a wallet:**

```bash
coingrep wallet add --label "My ETH Wallet" --address 0xabc123... --blockchain ethereum
coingrep wallet add --label "Cold Storage BTC" --address 1A1zP1...
```

The `--blockchain` flag is optional. When provided, COINGREP validates the address against that blockchain via the CoinStats API before saving. If validation fails, the wallet is not saved.

**List saved wallets:**

```bash
coingrep wallet list
```

Displays all wallets stored in the local database, including their ID, label, address, and the date they were added.

**Remove a wallet:**

```bash
coingrep wallet remove --address 0xabc123...
coingrep wallet remove --label "My ETH Wallet"
```

Either the address or the label can be used to identify the wallet to remove.

**Fetch live balances:**

```bash
coingrep wallet balances --blockchain ethereum
```

Queries the CoinStats API for live balances of all saved wallets on the specified blockchain. Returns USD balance and native token balance for each address.

**Validate an address:**

```bash
coingrep wallet validate 0xabc123... --blockchain ethereum
```

Checks whether a given address is valid on the specified blockchain without saving it. Exits with a non-zero status code if the address is invalid, making it usable in shell scripts.

---

## Command Reference

| Command | Description |
|---|---|
| `coingrep coins [IDS...]` | Price, market cap, volume, and 24h change for one or more coins |
| `coingrep trending` | Today's trending coins on CoinGecko |
| `coingrep market` | Global crypto market overview |
| `coingrep fear-greed` | Current Fear and Greed Index |
| `coingrep blockchains` | All blockchains supported by CoinStats |
| `coingrep wallet add` | Add a wallet to the local portfolio |
| `coingrep wallet remove` | Remove a wallet by address or label |
| `coingrep wallet list` | List all saved wallets |
| `coingrep wallet balances` | Fetch live balances for all saved wallets |
| `coingrep wallet validate` | Validate a wallet address against a blockchain |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `COINSTATS_API_KEY` | Yes | API key for CoinStats wallet and blockchain endpoints |

Place these in a `.env` file at the project root. The file is loaded automatically at startup via `python-dotenv`. Never commit `.env` to version control — it is included in `.gitignore`.

---

## Notes and Limitations

- Coin IDs passed to `coingrep coins` must be CoinGecko slugs (e.g., `bitcoin`, `ethereum`, `solana`), not ticker symbols. To find the correct ID, visit the CoinGecko website or search their coin list.
- Wallet balance queries depend on CoinStats API availability and may not return data for every blockchain or address format.
- The local database is a plain SQLite file. It is not encrypted. Do not store sensitive information in wallet labels.
- COINGREP does not execute any transactions and has no write access to any blockchain. It is a read-only data tool.
- Rate limits on the free CoinGecko API tier may apply under heavy use. If you encounter HTTP 429 responses, wait before retrying.