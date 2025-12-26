Personal Expense Tracker (CLI)
A robust, terminal-based expense manager built with Python and SQLite. This project focuses on data integrity, precise financial calculations, and clean CLI design.

🚀 Features
Persistent Storage: Uses SQLite to ensure your data stays safe between sessions.

Financial Precision: Uses the Decimal library to avoid floating-point errors (stores money as integers in cents).

Data Validation: Strict checking for dates (YYYY-MM-DD) and amounts to prevent database corruption.

Smart Aggregation: Categorized monthly summaries using SQL GROUP BY logic.

🛠️ Technical Stack
Language: Python 3.11+

Database: SQLite3

Libraries: * argparse: For professional command-line argument parsing.

pathlib: For cross-platform file path management.

decimal: For "half-up" rounding and monetary accuracy.

💻 How to Use
1. Initialize the Database
Bash

python -m expense_tracker init
2. Add an Expense
Bash

python -m expense_tracker add --amount 15.50 --category "Food" --date 2024-05-20 --note "Lunch with team"
3. View Recent History
Bash

python -m expense_tracker list --limit 10
4. Get a Monthly Summary
Bash

python -m expense_tracker summary --month 2024-05
🧠 What I Learned
The "State" Problem: Moving from temporary variables to permanent disk storage using SQL.

Defensive Programming: Implementing try/except blocks to handle user errors gracefully without crashing.

Package Structure: Organizing code into __init__.py and __main__.py for proper Python modularity.

Git Workflow: Using feature branches and .gitignore to maintain a clean production main branch.
