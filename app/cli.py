import sys
import click
from datetime import datetime

from .config import DB_PATH
from .CryptoClient import CryptoClient, CryptoClientError
from .Database import Database
from .logger import setup_logging

client = CryptoClient()
db = Database(DB_PATH)
setup_logging()

def _ensure_db():
    db.init_db()


def _error(msg: str) -> None:
    click.echo(click.style(f"  error  {msg}", fg="red"), err=True)
    sys.exit(1)

def _ok(msg: str) -> None:
    click.echo(click.style(f"  ok     {msg}", fg="green"))

def _info(msg: str) -> None:
    click.echo(click.style(f"  info   {msg}", fg="cyan"))

def _warn(msg: str) -> None:
    click.echo(click.style(f"  warn   {msg}", fg="yellow"))

def _draw_table(headers: list[str], rows: list[list[str]]) -> None:
    """Print a Unicode box-drawing table from plain lists."""
    from .TerminalTable import TerminalTable

    if not rows:
        _warn("No data to display.")
        return

    total_rows = len(rows) + 1          # +1 for the header row
    total_cols = len(headers)

    t = TerminalTable(total_rows, total_cols)

    for j, h in enumerate(headers):
        t.insert(h.upper(), 0, j)

    for i, row in enumerate(rows, start=1):
        for j, cell in enumerate(row):
            t.insert(cell, i, j)

    click.echo()
    t.draw()
    click.echo()


@click.group()
def cli():
    """Crypto portfolio tracker — market data, wallets, and more."""


@cli.command("coins")
@click.argument("ids", nargs=-1, required=True)
def cmd_coins(ids):
    """
    Show price, market cap, volume, and 24 h change for COIN IDs.

    \b
    Examples:
        python cli.py coins bitcoin ethereum solana
    """
    try:
        data = client.get_coins(list(ids))
    except CryptoClientError as e:
        _error(str(e))

    if not data:
        _warn("No data returned for the given IDs.")
        return

    headers = ["coin", "price (usd)", "mkt cap (usd)", "vol 24h (usd)", "chg 24h (%)"]
    rows = []
    for coin_id, stats in data.items():
        rows.append([
            coin_id,
            f"${stats.get('usd', 'n/a'):,.6f}" if isinstance(stats.get('usd'), float) else str(stats.get('usd', 'n/a')),
            f"${stats.get('usd_market_cap', 0):,.0f}",
            f"${stats.get('usd_24h_vol', 0):,.0f}",
            f"{stats.get('usd_24h_change', 0):+.2f}%",
        ])

    _draw_table(headers, rows)


@cli.command("trending")
def cmd_trending():
    """Show today's top trending coins on CoinGecko."""
    try:
        coins = client.get_trending_coins()
    except CryptoClientError as e:
        _error(str(e))

    headers = ["rank", "name", "symbol", "price (usd)", "mkt cap (usd)", "chg 24h (%)"]
    rows = [
        [
            str(c["market_cap_rank"] or "—"),
            c["name"],
            c["symbol"].upper(),
            str(c["price_usd"]),
            c["market_cap_usd"],
            f"{c['price_change_percentage_24h']:+.2f}%",
        ]
        for c in coins
    ]
    _draw_table(headers, rows)


@cli.command("market")
def cmd_market():
    """Show global crypto market overview."""
    try:
        data = client.get_global_market_data()
    except CryptoClientError as e:
        _error(str(e))

    fields = [
        ("Active cryptocurrencies",  str(data.get("active_cryptocurrencies", "n/a"))),
        ("Active markets",           str(data.get("markets", "n/a"))),
        ("Total market cap (USD)",   f"${data.get('total_market_cap', {}).get('usd', 0):,.0f}"),
        ("Total volume 24h (USD)",   f"${data.get('total_volume', {}).get('usd', 0):,.0f}"),
        ("BTC dominance",            f"{data.get('market_cap_percentage', {}).get('btc', 0):.2f}%"),
        ("ETH dominance",            f"{data.get('market_cap_percentage', {}).get('eth', 0):.2f}%"),
        ("Mkt cap change 24h",       f"{data.get('market_cap_change_percentage_24h_usd', 0):+.2f}%"),
    ]

    _draw_table(["metric", "value"], [[k, v] for k, v in fields])

@cli.command("fear-greed")
def cmd_fear_greed():
    """Show the latest Crypto Fear & Greed Index."""
    try:
        entry = client.get_fear_and_greed_index()
    except CryptoClientError as e:
        _error(str(e))
    timestampUnix = int(entry.get("timestamp"))
    timestamp = datetime.fromtimestamp(timestampUnix)
    
    rows = [
        ["Value",       entry.get("value", "n/a")],
        ["Rating",      entry.get("value_classification", "n/a")],
        ["Timestamp",   timestamp],
    ]
    _draw_table(["metric", "value"], rows)


@cli.command("blockchains")
def cmd_blockchains():
    """List all blockchains supported by CoinStats."""
    try:
        chains = client.get_blockchains()
    except CryptoClientError as e:
        _error(str(e))

    headers = ["id", "name"]
    rows = [[c.get("connectionId", ""), c.get("name", "")] for c in chains]
    _draw_table(headers, rows)

@cli.group("wallet")
def wallet_group():
    """Manage and query your wallet portfolio."""


@wallet_group.command("add")
@click.option("--label",   "-l", required=True, help="Human-readable name for the wallet.")
@click.option("--address", "-a", required=True, help="Blockchain wallet address.")
@click.option(
    "--blockchain", "-b",
    default=None,
    help="CoinStats connectionId (e.g. ethereum). If given, the address is validated before saving.",
)
def wallet_add(label, address, blockchain):
    """
    Add a wallet to your local portfolio.

    \b
    Examples:
        python cli.py wallet add -l "My ETH" -a 0xabc... -b ethereum
        python cli.py wallet add -l "Cold BTC" -a 1A1zP1... 
    """
    _ensure_db()

    if blockchain:
        _info(f"Validating address on {blockchain}…")
        try:
            valid = client.is_valid_wallet_address(address, blockchain)
        except CryptoClientError as e:
            _error(f"Validation failed: {e}")

        if not valid:
            _error(f"Address '{address}' is not valid for blockchain '{blockchain}'.")

        _ok("Address validated.")

    try:
        db.add_wallet(label, address)
        _ok(f"Wallet '{label}' added successfully.")
    except ValueError as e:
        _error(str(e))
    except Exception as e:
        _error(f"Unexpected error: {e}")


@wallet_group.command("remove")
@click.option("--address", "-a", default=None, help="Remove by wallet address.")
@click.option("--label",   "-l", default=None, help="Remove by wallet label.")
def wallet_remove(address, label):
    """
    Remove a wallet from your local portfolio.

    \b
    Examples:
        python cli.py wallet remove -a 0xabc...
        python cli.py wallet remove -l "My ETH"
    """
    if not address and not label:
        _error("Provide either --address or --label.")

    _ensure_db()

    if address:
        removed = db.remove_wallet_by_address(address)
        if removed:
            _ok(f"Wallet with address '{address}' removed.")
        else:
            _warn(f"No wallet found with address '{address}'.")

    elif label:
        removed = db.remove_wallet_by_label(label)
        if removed:
            _ok(f"Wallet '{label}' removed.")
        else:
            _warn(f"No wallet found with label '{label}'.")


@wallet_group.command("list")
def wallet_list():
    """List all wallets in your local portfolio."""
    _ensure_db()
    wallets = db.list_wallets()

    if not wallets:
        _warn("No wallets in portfolio. Use 'wallet add' to add one.")
        return

    headers = ["id", "label", "address", "added at"]
    rows = [
        [str(w["id"]), w["label"], w["address"], w["added_at"]]
        for w in wallets
    ]
    _draw_table(headers, rows)


@wallet_group.command("balance")
@click.option(
    "--label", "-l",
    multiple=True,
    help="Wallet label(s) saved in your local portfolio.",
)
@click.option(
    "--blockchain", "-b",
    multiple=True,
    default=("all",),
    show_default=True,
    help="CoinStats connectionId(s) to query (e.g. ethereum, bitcoin). Defaults to 'all'.",
)
@click.option(
    "--address", "-a",
    multiple=True,
    help="Raw wallet address(es) to query (not required to be saved).",
)
def wallet_balances(label, blockchain, address):
    """
    Show token balances for wallets, grouped by address and blockchain.

    \b
    Sources are combined — provide --label, --address, or both.

    \b
    Examples:
        python cli.py wallet balance -l "My ETH" -b ethereum
        python cli.py wallet balance -a 0xabc... -b ethereum -b polygon
        python cli.py wallet balance -l "My ETH" -a 0xdef... -b all
    """
    _ensure_db()

    labels_map: dict[str, str] = {}

    if label:
        db_wallets = db.get_wallet_by_labels(label)
        if not db_wallets:
            _warn(f"No saved wallets matched the given label(s): {', '.join(label)}")
        for w in db_wallets:
            labels_map[w["address"]] = w["label"]

    for raw_addr in address:
        if raw_addr not in labels_map:
            labels_map[raw_addr] = raw_addr[:10] + "…"

    if not labels_map:
        _error("No addresses to query. Provide --label and/or --address.")

    all_addresses = list(labels_map.keys())

    _info(
        f"Fetching balances for {len(all_addresses)} address(es) "
        f"on: {', '.join(blockchain)} …"
    )
    try:
        raw = client.get_wallet_balances(all_addresses, blockchain)
    except CryptoClientError as e:
        _error(str(e))
        return

    results: list[dict] = raw if isinstance(raw, list) else raw.get("wallets", [])

    if not results:
        _warn("No balance data returned.")
        return

    from collections import defaultdict
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)

    for entry in results:
        addr  = entry.get("address", "")
        chain = entry.get("blockchain") or entry.get("connectionId", "unknown")
        grouped[(addr, chain)].extend(entry.get("balances", []))

    if not grouped:
        _warn("Response contained no token balances.")
        return

    for (addr, chain), balances in sorted(grouped.items()):
        label_display = labels_map.get(addr, addr)
        click.echo(
            click.style(
                f"  ── {label_display}  ({addr})  [{chain}]",
                fg="cyan", bold=True,
            )
        )

        if not balances:
            _warn("  No tokens found on this chain.")
            continue

        headers = ["symbol", "name", "amount", "price (usd)", "value (usd)", "chg 24h (%)"]
        rows = []
        for token in balances:
            amount    = token.get("amount", 0)
            price     = token.get("price", 0)
            value_usd = amount * price
            rows.append([
                token.get("symbol", "").upper(),
                token.get("name", ""),
                f"{amount:,.6f}",
                f"${price:,.4f}",
                f"${value_usd:,.2f}",
                f"{token.get('pCh24h', 0):+.2f}%",
            ])

        rows.sort(key=lambda r: float(r[4].replace("$", "").replace(",", "")), reverse=True)
        _draw_table(headers, rows)

@wallet_group.command("validate")
@click.argument("address")
@click.option(
    "--blockchain", "-b",
    required=True,
    help="CoinStats connectionId (e.g. ethereum, bitcoin, solana).",
)
def wallet_validate(address, blockchain):
    """
    Validate a wallet ADDRESS against a blockchain via CoinStats.

    \b
    Example:
        python cli.py wallet validate 0xabc... -b ethereum
    """
    _info(f"Validating '{address}' on {blockchain}…")
    try:
        valid = client.is_valid_wallet_address(address, blockchain)
    except CryptoClientError as e:
        _error(str(e))

    if valid:
        _ok(f"Address is valid on {blockchain}.")
    else:
        click.echo(
            click.style(f"  invalid  '{address}' is not a valid {blockchain} address.", fg="red")
        )
        sys.exit(1)


if __name__ == "__main__":
    cli()