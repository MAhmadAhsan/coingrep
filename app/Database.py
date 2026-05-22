import sqlite3
from logger import get_logger

class Database:
    def __init__(self):
        self.logger = get_logger(__name__)

    def _get_connection(self, db_path):
        self.logger.info(
            f"Opening database connection: {db_path}"
        )

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        return conn

    def init_db(self, db_path):
        self.logger.info(
            "Initializing database..."
        )

        with self._get_connection(db_path) as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS wallets (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    label       TEXT NOT NULL UNIQUE,
                    address     TEXT NOT NULL UNIQUE,
                    added_at    TEXT NOT NULL DEFAULT (datetime('now'))
                );
                """
            )

        self.logger.info(
            "Database initialized successfully."
        )

    def add_wallet(self, label, address, db_path):
        self.logger.info(
            f"Adding wallet: label={label}, address={address}"
        )

        try:
            with self._get_connection(db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO wallets (label, address)
                    VALUES (?, ?)
                    """,
                    (label.strip(), address.strip()),
                )

            self.logger.info(
                f"Wallet added successfully: {label}"
            )

        except sqlite3.IntegrityError as e:
            self.logger.warning(
                f"Integrity error while adding wallet: {e}"
            )

            if "label" in str(e):
                raise ValueError(
                    f"Label '{label}' already exists."
                )

            if "address" in str(e):
                raise ValueError(
                    f"Address '{address}' is already in your portfolio."
                )

            raise

        except Exception as e:
            self.logger.exception(
                f"Unexpected error while adding wallet: {e}"
            )
            raise

    def remove_wallet_by_address(self, address, db_path):
        self.logger.info(
            f"Removing wallet by address: {address}"
        )

        with self._get_connection(db_path) as conn:
            cur = conn.execute(
                "DELETE FROM wallets WHERE address = ?",
                (address.strip(),),
            )

            if cur.rowcount > 0:
                self.logger.info(
                    "Wallet removed successfully."
                )
                return True

            self.logger.warning(
                "No wallet found with given address."
            )

            return False

    def remove_wallet_by_label(self, label, db_path):
        self.logger.info(
            f"Removing wallet by label: {label}"
        )

        with self._get_connection(db_path) as conn:
            cur = conn.execute(
                "DELETE FROM wallets WHERE label = ?",
                (label.strip(),),
            )

            if cur.rowcount > 0:
                self.logger.info(
                    "Wallet removed successfully."
                )
                return True

            self.logger.warning(
                "No wallet found with given label."
            )

            return False

    def list_wallets(self, db_path):
        self.logger.info(
            "Fetching wallet list..."
        )

        with self._get_connection(db_path) as conn:
            wallets = conn.execute(
                "SELECT * FROM wallets ORDER BY label"
            ).fetchall()

        self.logger.info(
            f"Fetched {len(wallets)} wallet(s)."
        )

        return wallets