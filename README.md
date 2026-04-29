# Warehouse Management System

A professional-grade warehouse management system built with **Frappe Framework**. Handles stock movement, inventory valuation, warehouse organization, and comprehensive reporting using a ledger-based inventory model.

## Overview

This system provides complete inventory control for multi-warehouse operations with real-time stock tracking, moving average valuation, and detailed audit trails.

---

## Features

### Core Functionality
- **Multi-warehouse support** — Organize inventory across multiple physical locations
- **Stock operations** — Receipt, Consume, Transfer, and Opening Stock transactions
- **Ledger-based tracking** — Complete audit trail of all inventory movements
- **Moving average valuation** — Accurate cost tracking for inventory
- **Negative stock prevention** — Built-in validation to prevent overselling
- **Real-time balances** — Instant visibility into warehouse stock levels

### DocTypes
- **Item** — Product catalog with identifiers and metadata
- **Warehouse** — Physical or logical storage locations
- **Stock Entry** — Transaction document recording inventory movement
- **Stock Entry Item** — Line items within a Stock Entry
- **Stock Ledger Entry** — Elementary record of each stock movement

### Reports
- **Stock Ledger Report** — Complete transaction history line by line
- **Stock Balance Report** — Current stock levels summarized by item and warehouse

### Data Integrity
- Comprehensive validation rules
- Warehouse-specific transaction controls
- Transfer validation (source/target matching)
- Server-side business logic in Python
- Full test coverage

---

## Technical Architecture

### Project Structure
```
mywarehouse/
├── mywarehouse/
│   ├── doctype/              # DocType definitions
│   │   ├── item/
│   │   ├── warehouse/
│   │   ├── stock_entry/
│   │   ├── stock_entry_item/
│   │   └── stock_ledger_entry/
│   ├── report/               # Reports
│   │   ├── stock_ledger/
│   │   └── stock_balance/
│   ├── config/
│   ├── patches/              # Database migrations
│   ├── public/               # CSS/JS assets
│   └── templates/            # UI templates
├── pyproject.toml
├── hooks.py
└── README.md
```

### Inventory Model

#### Stock Entry Types

| Type | Source | Target | Result |
|------|--------|--------|--------|
| **Receipt** | — | Warehouse | ➕ Positive ledger entry |
| **Consume** | Warehouse | — | ➖ Negative ledger entry |
| **Transfer** | Warehouse | Warehouse | ➖ & ➕ Paired ledger entries |
| **Opening Stock** | — | Warehouse | ➕ Positive ledger entry |

#### Stock Ledger Entry

The foundational record for all inventory tracking:
- **Item** & **Warehouse** — Identifies the stock location
- **Quantity & Valuation Rate** — Qty moved and cost per unit
- **Stock Value** — Total cost of transaction
- **Posting Date/Time** — When the movement occurred
- **Voucher Reference** — Links to Stock Entry

#### Valuation Method

**Moving Average Costing:**
- **Inbound:** New average = (Current Stock Value + Incoming Stock Value) ÷ (Current Qty + Incoming Qty)
- **Outbound:** Uses current average cost rate

---

## Installation

### Prerequisites
- Frappe Framework v16 (or compatible version)
- Python 3.8+
- Existing Frappe bench setup

### Setup Steps

1. **Navigate to your bench directory:**
   ```bash
   cd frappe-v16-bench
   ```

2. **Install the app:**
   ```bash
   bench --site warehouse install-app mywarehouse
   ```

3. **Run migrations:**
   ```bash
   bench --site warehouse migrate
   ```

4. **Start the development server:**
   ```bash
   bench start
   ```

5. **Access the application:**
   ```
   Open http://localhost:8000 in your browser
   ```

---

## Usage

### Creating Stock Movements

1. Navigate to **Stock Entry** list
2. Click **+ New Stock Entry**
3. Select transaction **Type** (Receipt, Consume, Transfer, Opening Stock)
4. Fill in **Item**, **Quantity**, and **Warehouse** details
5. Click **Save** and then **Submit**
6. Stock Ledger entries are created automatically

### Viewing Reports

- **Stock Ledger Report:** Complete record of all transactions
- **Stock Balance Report:** Current inventory by item and warehouse

---

## Testing

Run the full test suite:
```bash
bench --site warehouse run-tests --app mywarehouse --verbose
```

Run tests for a specific module:
```bash
bench --site warehouse run-tests --app mywarehouse --module mywarehouse.mywarehouse.doctype.stock_entry.test_stock_entry --verbose
```

**Test Coverage:**
- Item and Warehouse creation
- Stock operations (Receipt, Consume, Transfer, Opening)
- Negative stock validation
- Moving average valuation accuracy
- Report data accuracy

---

## Example Data

### Sample Warehouses
- Main Warehouse (Primary distribution center)
- Thika Warehouse (Regional hub)
- Nairobi Warehouse (Customer fulfillment)

### Sample Items
- Dell Latitude 5420 Laptop
- Samsung 24" Monitor
- Logitech Wireless Mouse
- HP Laptop Charger
- Kingston 512GB SSD

---

## Development

### Key Files
- `mywarehouse/doctype/*/` — DocType Python and JSON definitions
- `mywarehouse/report/*/` — Report logic and configurations
- `hooks.py` — App hooks and fixture definitions

### Adding New Features
1. Create DocType in `mywarehouse/doctype/`
2. Add corresponding test file (`test_*.py`)
3. Run tests to verify functionality
4. Update documentation

---

## Notes

**Built for:** X Electronics Warehouse Management Exercise  
**Framework:** Frappe Framework  
**Language:** Python 3  
**Database:** MariaDB (via Frappe)

**Design Focus:**
- Clean separation of concerns
- ERP-style stock movement handling
- Precise inventory reporting
- Comprehensive test coverage
- Production-ready validation

---

## Author

**Kamau** — Software Engineer
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
````

---

## How the System Works

### 1. Stock Entry

A user creates a **Stock Entry** and submits it.

Depending on the purpose:

#### Receipt

Creates a **positive Stock Ledger Entry** in the **target warehouse**.

#### Consume

Creates a **negative Stock Ledger Entry** in the **source warehouse**.

#### Transfer

Creates:

* a **negative Stock Ledger Entry** in the **source warehouse**
* a **positive Stock Ledger Entry** in the **target warehouse**

#### Opening

Creates a **positive Stock Ledger Entry** in the **target warehouse**.

---

### 2. Stock Ledger Entry

This is the **source of truth** for inventory movement.

Each ledger row stores:

* item
* warehouse
* posting date
* posting time
* actual quantity moved
* valuation rate
* stock value
* voucher type
* voucher number

---

### 3. Valuation

The system uses **moving average valuation**.

For incoming stock:

* average cost is recalculated based on current stock value and incoming stock value

For outgoing stock:

* the current average cost is used

---

## Setup Instructions

### 1. Go to your bench

```bash
cd frappe-v16-bench
```

### 2. Install the custom app

```bash
bench --site warehouse install-app mywarehouse
```

### 3. Run migrations

```bash
bench --site warehouse migrate
```

### 4. Start bench

```bash
bench start
```

---

## Running Tests

Run all tests for this module:

```bash
bench --site warehouse run-tests --app mywarehouse --module mywarehouse.mywarehouse.doctype.stock_entry.test_stock_entry --verbose
```

---

## Demo Data

For demonstration, the system was tested using realistic warehouse and item data such as:

### Warehouses

* Main Warehouse
* Thika Warehouse
* Nairobi Warehouse

### Items

* Dell Latitude 5420 Laptop
* Samsung 24 Inch Monitor
* Logitech Wireless Mouse
* HP Laptop Charger
* Kingston 512GB SSD

---

## Screenshots

Below are some screenshots of the system:

### Item List

![Item List](screenshots/items.png)

### Warehouse List

![Warehouse List](screenshots/warehouses.png)

### Stock Entry Form

![Stock Entry Form](screenshots/stock-entry.png)

### Stock Ledger Report

![Stock Ledger Report](screenshots/stock-ledger.png)

### Stock Balance Report

![Stock Balance Report](screenshots/stock-balance.png)

### Example Screenshot Folder Structure

```text
screenshots/
├── items.png
├── warehouses.png
├── stock-entry.png
├── stock-ledger.png
└── stock-balance.png
```

---

## Notes

This project was built as part of the **Navari Limited Software Engineer Exercise**.

The focus was on:

* clean business logic
* ERP-style stock movement handling
* accurate reporting
* test coverage
* clarity of implementation

---

## Author

**Kamau**

````


