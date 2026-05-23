# Submission Questions
## 1. How to run

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

# How to Run the Project

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

---

## 2. Stack Choice

**Why did you pick this stack/language/framework for this task? What would have been a worse choice and why?**

I used Python to build this tool because it has many useful libraries that make development easier and faster. These libraries handle a lot of complex work automatically, so I didn’t have to deal with low-level details or write everything from scratch.

The tool could also be built in C or C++, but that would require much more boilerplate code for basic tasks. Python’s ecosystem made the development process simpler, cleaner, and more efficient.

---

## 3. One Real Edge Case

**Describe one specific edge case your code handles correctly. Point to the file and line number. Explain what would happen without that handling.**

### Edge Case: Consistent Exception Handling (`app/CryptoClient.py`, line 20)

I implemented a `_get()` helper function to send GET requests. Inside it, I wrapped Python's base `Exception` class into a custom `CryptoClientError` exception. This ensures that all errors thrown at the class level are consistent and predictable. `_get()` raises appropriate exceptions whenever something goes wrong.

CoinStats does not provide a direct boolean endpoint to check whether a wallet address is valid against a blockchain. To work around this, I used the `/wallet/status` route inside `is_valid_wallet_address()`:

- If the GET request returns a proper response → return `True`
- If the response has a status code of `400 Bad Request`, `404 Not Found`, or `422 Unprocessable Entity` → return `False`
- For other failures (e.g. request timeout, rate limit exceeded) → raise an exception

**Why I didn't use `_get()` here:** `_get()` would have raised an exception for `400`, `404`, and `422` responses, but in this context, those status codes are _expected_ and meaningful (they indicate an invalid wallet), not errors. Bypassing `_get()` and calling `requests.get()` directly gives me full control over how those status codes are interpreted.

---

## 4. AI Usage

**List every place you used AI. For at least one, describe something you changed about the AI output and why.**

### Brainstorming

Used Gemini to brainstorm ideas and decide what to build:

- [Conversation 1](https://gemini.google.com/share/a1aadec6f88e)
- [Conversation 2](https://gemini.google.com/share/9a217b34a1c0)

### TOML Build File & CLI (Click Library)

I had limited prior knowledge of TOML build files and the Click library for building CLI interfaces, so I used AI to generate the code for both:

- TOML file: [Gemini conversation](https://gemini.google.com/share/64935edad6f5)
- Click CLI: [Claude conversation](https://claude.ai/share/dcd387ce-6091-4c51-87fb-d6f5e46dfbee)

I also used Google Search for syntax guidance and related reference material.

### What I Changed

I used Claude to understand the professional approach to logging: [Claude conversation](https://claude.ai/share/ca002ed1-1205-43ef-8a12-5d18e1fa00c2).

Claude's response suggested using handlers, but I felt that was overkill for an application of this scale. I reverted to a basic logging setup simpler, more appropriate, and easier to maintain for a small CLI tool.

I also used AI to properly format this file :)

---

## 5. Honest Gap

**What's one thing in your submission that isn't good enough, and what would you do to fix it given another day?**

Rigorous testing is missing. I only tested the application manually throughout development.

Given another day, I would write a proper test cases to ensure the app behaves consistently across inputs, edge cases, and failure modes covering things like invalid wallet addresses, network timeouts, and unexpected API responses.