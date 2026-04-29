import frappe
from frappe.model.document import Document


class StockEntry(Document):

    def validate(self):
        self.validate_items_exist()
        self.validate_warehouses()
        self.validate_quantities()

    def on_submit(self):
        self.create_stock_ledger_entries()

    def validate_items_exist(self):
        if not self.item:
            frappe.throw("At least one item is required")

    def validate_warehouses(self):
        for row in self.item:
            if self.purpose in ["Receipt", "Opening"]:
                if not row.target_warehouse:
                    frappe.throw(
                        f"Row {row.idx}: Target Warehouse is required for {self.purpose}"
                    )

            elif self.purpose == "Consume":
                if not row.source_warehouse:
                    frappe.throw(
                        f"Row {row.idx}: Source Warehouse is required for Consume"
                    )

            elif self.purpose == "Transfer":
                if not row.source_warehouse or not row.target_warehouse:
                    frappe.throw(
                        f"Row {row.idx}: Source and Target Warehouse are required for Transfer"
                    )

                if row.source_warehouse == row.target_warehouse:
                    frappe.throw(
                        f"Row {row.idx}: Source and Target Warehouse cannot be the same"
                    )

    def validate_quantities(self):
        for row in self.item:
            if row.quantity is None or row.quantity <= 0:
                frappe.throw(f"Row {row.idx}: Quantity must be greater than zero")

    def create_stock_ledger_entries(self):
        for row in self.item:

            if self.purpose in ["Receipt", "Opening"]:
                self.create_sle(
                    item=row.item,
                    warehouse=row.target_warehouse,
                    qty=row.quantity,
                    rate=row.rate
                )

            elif self.purpose == "Consume":
                self.create_sle(
                    item=row.item,
                    warehouse=row.source_warehouse,
                    qty=-row.quantity,
                    rate=row.rate
                )

            elif self.purpose == "Transfer":
                self.create_sle(
                    item=row.item,
                    warehouse=row.source_warehouse,
                    qty=-row.quantity,
                    rate=row.rate
                )

                self.create_sle(
                    item=row.item,
                    warehouse=row.target_warehouse,
                    qty=row.quantity,
                    rate=row.rate
                )

    def create_sle(self, item, warehouse, qty, rate):
        current_qty, current_value = self.get_current_stock(item, warehouse)

        if qty < 0 and current_qty + qty < 0:
            frappe.throw(
                f"Insufficient stock for item {item} in warehouse {warehouse}",
                frappe.ValidationError
            )

        if qty > 0:
            new_value = current_value + (qty * rate)
            new_qty = current_qty + qty
            valuation_rate = new_value / new_qty if new_qty else 0
            qty_after_transaction = new_qty
        else:
            valuation_rate = current_value / current_qty if current_qty else 0
            qty_after_transaction = current_qty + qty

        stock_value = qty * valuation_rate

        frappe.get_doc({
            "doctype": "Stock Ledger Entry",
            "item": item,
            "warehouse": warehouse,
            "posting_date": self.posting_date,
            "posting_time": self.posting_time,
            "actual_qty": qty,
            "qty_after_transaction": qty_after_transaction,
            "valuation_rate": valuation_rate,
            "stock_value": stock_value,
            "voucher_type": "Stock Entry",
            "voucher_no": self.name
        }).insert(ignore_permissions=True)

    def get_current_stock(self, item, warehouse):
        result = frappe.db.sql("""
            SELECT
                SUM(actual_qty) AS qty,
                SUM(stock_value) AS value
            FROM `tabStock Ledger Entry`
            WHERE item = %s AND warehouse = %s
        """, (item, warehouse), as_dict=True)

        qty = result[0].qty or 0
        value = result[0].value or 0

        return qty, value