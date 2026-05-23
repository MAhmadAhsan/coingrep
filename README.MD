# CoinGrep 🪙

A fast, terminal-based cryptocurrency market and portfolio tracker built with Python.

CoinGrep allows users to fetch real-time cryptocurrency market data, monitor global trends, track the Fear & Greed Index, and manage local wallet portfolios directly from the command line.

---

# ✨ Features

- Live cryptocurrency prices
- Market cap and trading volume data
- Trending coins
- Global crypto market statistics
- Fear & Greed Index
- Local wallet portfolio management
- Blockchain address validation
- SQLite-based local storage
- Multi-wallet balance checking

---

# Requirements

Before running CoinGrep, install the following dependencies on your machine.

---

## 1. Python 3.9 or Higher

Check if Python is installed:

```bash
python --version
```

or:

```bash
python3 --version
```

If Python is not installed:

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Arch Linux

```bash
sudo pacman -S python
```

### Fedora

```bash
sudo dnf install python3
```

### macOS

Install using Homebrew:

```bash
brew install python
```

### Windows

Download and install Python from the official installer.

IMPORTANT:
During installation, enable:

```text
Add Python to PATH
```

---

## 2. Git

Git is required to clone the repository.

Check installation:

```bash
git --version
```

If Git is not installed:

### Linux

```bash
sudo apt install git
```

### macOS

```bash
brew install git
```

### Windows

Install Git for Windows.

---

# 🔑 API Key Requirement

CoinGrep uses the CoinStats API for:

- Wallet balance tracking
- Blockchain validation

You must create a free CoinStats API key before using wallet-related commands.

---

# 🚀 How to Run the Project

The following instructions assume a completely fresh machine.

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/MAhmadAhsan/coingrep.git
cd coingrep
```

---

## Step 2 — Create a Virtual Environment

### Linux/macOS

```bash
python3 -m venv venv
```

### Windows

```cmd
python -m venv venv
```

---

## Step 3 — Activate the Virtual Environment

### Linux/macOS

```bash
source venv/bin/activate
```

### Windows (CMD)

```cmd
venv\Scripts\activate
```

### Windows (PowerShell)

```powershell
venv\Scripts\Activate.ps1
```

After activation, you should see:

```text
(venv)
```

at the beginning of your terminal prompt.

---

## Step 4 — Upgrade pip

```bash
pip install --upgrade pip
```

---

## Step 5 — Install the Project

```bash
pip install .
```

For development mode:

```bash
pip install -e .
```

---

## Step 6 — Create the Environment File

Create a file named:

```text
.env
```

inside the project root directory.

Example structure:

```text
coingrep/
│
├── .env
├── README.md
├── pyproject.toml
└── ...
```

---

## Step 7 — Add Your CoinStats API Key

Inside `.env`:

```env
COINSTATS_API_KEY=your_api_key_here
```

---

## Step 8 — Run the Application

Example commands:

### View trending coins

```bash
coingrep trending
```

### View global market statistics

```bash
coingrep market
```

### Check coin information

```bash
coingrep coins bitcoin ethereum solana
```

### View Fear & Greed Index

```bash
coingrep fear-greed
```

---

# 💼 Wallet Commands

## Add a Wallet

```bash
coingrep wallet add \
  --label "Main ETH" \
  --address 0x123...abc \
  --blockchain ethereum
```

---

## List Saved Wallets

```bash
coingrep wallet list
```

---

## Check Wallet Balances

```bash
coingrep wallet balances --blockchain ethereum
```

---

## Validate a Wallet Address

```bash
coingrep wallet validate 0x123...abc --blockchain ethereum
```

---

## Remove a Wallet

By label:

```bash
coingrep wallet remove --label "Main ETH"
```

By address:

```bash
coingrep wallet remove --address 0x123...abc
```

---

# 🗄️ Local Storage

CoinGrep stores all data locally using SQLite.

Default storage locations:

## Linux/macOS

```text
~/.coingrep/db/coingrep.db
```

Logs:

```text
~/.coingrep/logs/
```

---

## Windows

```text
C:\Users\YourUsername\.coingrep\
```

---

# 🔒 Privacy

- Wallet addresses are stored locally only
- No private keys are stored
- CoinGrep does not upload local wallet databases

---

# 🛠️ Technologies Used

- Python
- SQLite
- CoinGecko API
- CoinStats API

---

# 📄 License

MIT License