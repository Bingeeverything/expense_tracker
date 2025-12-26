import argparse
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="expense_tracker",
        description="Personal expense tracker (CLI + SQL Lite)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="Initialize the database.")

    add = sub.add_parser("add", help="Add a new expense.")
    add.add_argument("--amount", required=True, help="Amount like 12.50")
    add.add_argument("--category", required=True, help="Category like food, transport or Rent")
    add.add_argument("--date", required=True, help="Date YYYY-MM-DD")
    add.add_argument("--note", default="", help="Optional note")

    lst = sub.add_parser("list", help="List Recent Expenses.")
    lst.add_argument("--limit",type=int,default=20)

    summ = sub.add_parser("summary", help="Monthly Summary by Category")
    summ.add_argument("--month", required=True, help="Month YYYY-MM")
    return parser

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.cmd == "init":
        db_path = Path.cwd() / "expenses.db"

        conn = sqlite3.connect(db_path)
        try:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount_cents INTEGER NOT NULL,
                currency TEXT NOT NULL DEFAULT 'AUD',
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                note TEXT,
                created_at TEXT NOT NULL
            );
            """)
            conn.commit()
        finally:
            conn.close()
        
        print(f"Database intitialized at {db_path}")
        return 0

    elif args.cmd == "add":

        db_path = Path.cwd() / "expenses.db"
        if not db_path.exists():
            print("Error: database not found. Run: python -m expense_tracker init")
            return 2
        conn = sqlite3.connect(db_path)
        
        try:
            amount = Decimal(args.amount)
        except InvalidOperation:
            print("Error: --amount must be a number like 12.50")
            return 2
        
        if amount <= 0:
            print("Error: --amount must be > 0")
            return 2
        
        amount_cents = int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        
        try:
            datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("Error: --date must be a real date in YYYY-MM-DD format")
            return 2

        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

        try:
            conn.execute(
                """
                INSERT INTO expenses (amount_cents, currency, category, date, note, created_at)
                VALUES (?, 'AUD', ?, ?, ?, ?)
                """,
                (amount_cents, args.category, args.date, args.note, created_at)
            )
            conn.commit()
        finally:
            conn.close()

        print(f"Added: {args.amount} AUD {args.category} {args.date}")
        return 0      

    elif args.cmd == 'list':
        db_path = Path.cwd() / "expenses.db"
        if not db_path.exists():
            print("Error: database not found. Run: python -m expense_tracker init")
            return 2
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.execute(
                """
                SELECT id, amount_cents, currency, category, date, note, created_at
                FROM expenses
                ORDER BY id DESC
                LIMIT ?;
                """,
                (args.limit,)
            )
            rows = cursor.fetchall()
        finally:
            conn.close()

        if not rows:
            print(f"There are no expenses yet")
            return 0
        
        print("ID   Date     Category    Amount  Note")
        for row in rows:
            id_, amount_cents, currency, category, date, note, created_at = row
            amount_str = f"{amount_cents / 100:.2f}"
            print(f"{id_:<3} {date:<10} {category:<10} {amount_str:<7} {note}")
        return 0
    
    elif args.cmd == "summary":
        db_path = Path.cwd() / "expenses.db"
        if not db_path.exists():
            print("Error: database not found. Run: python -m expense_tracker init")
            return 2
        try:
            datetime.strptime(args.month, "%Y-%m")
        except ValueError:
            print("Error: --month must be in YYYY-MM format")
            return 2
        
        conn = sqlite3.connect(db_path)
        try:
            cursor =  conn.execute(
                """
                SELECT category, SUM(amount_cents)
                FROM expenses
                WHERE date LIKE ?
                GROUP BY category
                ORDER BY category;
                """,
                (args.month + "%",)
            )
            rows = cursor.fetchall()
        finally:
            conn.close()
        
        if not rows:
            print(f"No expenses for {args.month}")
            return 0
        
        print(f"Summary for {args.month}:")
        total_cents = 0
        for category, sum_cents in rows:
            amount = sum_cents/100
            total_cents += sum_cents
            print(f"{category:<12}{amount:.2f}")

        print("-" * 17)
        print(f"{'Total':<12}{total_cents / 100:.2f}")
        return 0

    else:
        print("not found try again")
if __name__ == "__main__":
    raise SystemExit(main())
