You’re right — I did include those sections, but the way they were formatted with extra block markers made them look broken and easy to miss.

Here is the **full clean README** again, with the **Setup Instructions** and **Screenshots** sections clearly included and properly formatted.

````markdown
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


