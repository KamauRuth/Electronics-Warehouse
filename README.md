# Warehouse Management System for X Electronics

A custom warehouse management system built with **Frappe Framework** for the **X Electronics** exercise.

This project handles stock movement, inventory valuation, warehouse-level stock visibility, and reporting using a ledger-based inventory model.

---

## Features

### Core DocTypes
- **Item**
- **Warehouse**
- **Stock Entry**
- **Stock Entry Item**
- **Stock Ledger Entry**

### Stock Operations
- **Receipt** → adds stock into a target warehouse
- **Consume** → removes stock from a source warehouse
- **Transfer** → moves stock from a source warehouse to a target warehouse
- **Opening Stock** → loads initial stock into a target warehouse

### Inventory Logic
- Ledger-based inventory model
- Dynamic stock movement tracking
- Moving average valuation
- Negative stock prevention
- Warehouse-level stock balances

### Reports
- **Stock Ledger Report**
  - Shows all stock movements line by line
- **Stock Balance Report**
  - Shows summarized stock balance per item and warehouse

### Validation & Controls
- Quantity validation
- Warehouse validation by transaction type
- Transfer source/target mismatch prevention
- Server-side business logic in Python

### Tests
The project includes tests for:
- Item creation
- Warehouse creation
- Receipt flow
- Consume flow
- Negative stock blocking
- Moving average valuation
- Stock Ledger report
- Stock Balance report

---

## Project Structure

```text
mywarehouse/
├── mywarehouse/
│   ├── doctype/
│   │   ├── item/
│   │   ├── warehouse/
│   │   ├── stock_entry/
│   │   ├── stock_entry_item/
│   │   └── stock_ledger_entry/
│   └── report/
│       ├── stock_ledger/
│       └── stock_balance/
└── README.md