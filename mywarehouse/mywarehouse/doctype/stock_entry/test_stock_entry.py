# Copyright (c) 2026, kamau and Contributors
# See license.txt

import frappe
import unittest


class TestStockEntry(unittest.TestCase):

    def setUp(self):
        frappe.db.delete("Stock Ledger Entry")
        frappe.db.delete("Stock Entry")
        frappe.db.delete("Warehouse")
        frappe.db.delete("Item")

    def create_item(self):
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": "TEST-ITEM-001",
            "item_name": "Test Item 001",
            "description": "Test inventory item",
            "is_active": 1,
            "reorder_level": 5
        })
        item.insert()
        return item

    def create_warehouse(self, name="Test Warehouse"):
        warehouse = frappe.get_doc({
            "doctype": "Warehouse",
            "warehouse_name": name,
            "is_active": 1
        })
        warehouse.insert()
        return warehouse

    def create_receipt(self, item, warehouse, quantity, rate):
        doc = frappe.get_doc({
            "doctype": "Stock Entry",
            "purpose": "Receipt",
            "posting_date": frappe.utils.today(),
            "posting_time": frappe.utils.nowtime(),
            "item": [
                {
                    "item": item.name,
                    "quantity": quantity,
                    "target_warehouse": warehouse.name,
                    "rate": rate
                }
            ]
        })
        doc.insert()
        doc.submit()
        return doc

    def create_consume(self, item, warehouse, quantity, rate):
		doc = frappe.get_doc({
			"doctype": "Stock Entry",
			"purpose": "Consume",
			"posting_date": frappe.utils.today(),
			"posting_time": frappe.utils.nowtime(),
			"item": [
				{
					"item": item.name,
					"quantity": quantity,
					"source_warehouse": warehouse.name,
					"rate": rate
				}
			]
		})
		doc.insert()
		doc.submit()
		return doc

    def test_create_item(self):
        item = self.create_item()
        self.assertEqual(item.item_code, "TEST-ITEM-001")

    def test_create_warehouse(self):
        warehouse = self.create_warehouse()
        self.assertEqual(warehouse.warehouse_name, "Test Warehouse")

    def test_receipt_creates_stock_ledger(self):
        item = self.create_item()
        warehouse = self.create_warehouse()

        self.create_receipt(item, warehouse, 10, 100)

        entries = frappe.get_all(
            "Stock Ledger Entry",
            filters={
                "item": item.name,
                "warehouse": warehouse.name
            },
            fields=["actual_qty", "valuation_rate", "stock_value"]
        )

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["actual_qty"], 10)
        self.assertEqual(entries[0]["valuation_rate"], 100)
        self.assertEqual(entries[0]["stock_value"], 1000)

    def test_moving_average_valuation(self):
        item = self.create_item()
        warehouse = self.create_warehouse()

        self.create_receipt(item, warehouse, 10, 100)
        self.create_receipt(item, warehouse, 10, 200)

        latest_sle = frappe.get_all(
            "Stock Ledger Entry",
            filters={
                "item": item.name,
                "warehouse": warehouse.name
            },
            fields=["actual_qty", "valuation_rate", "stock_value"],
            order_by="creation desc",
            limit=1
        )[0]

        self.assertEqual(latest_sle["actual_qty"], 10)
        self.assertEqual(latest_sle["valuation_rate"], 150)
        self.assertEqual(latest_sle["stock_value"], 1500)

    def test_consume_reduces_stock(self):
        item = self.create_item()
        warehouse = self.create_warehouse()

        self.create_receipt(item, warehouse, 10, 100)
        self.create_consume(item, warehouse, 4, 100)

        balance = frappe.db.sql("""
            SELECT
                SUM(actual_qty) AS qty,
                SUM(stock_value) AS value
            FROM `tabStock Ledger Entry`
            WHERE item = %s AND warehouse = %s
        """, (item.name, warehouse.name), as_dict=True)[0]

        self.assertEqual(balance["qty"], 6)
        self.assertEqual(balance["value"], 600)

    def test_consume_cannot_make_stock_negative(self):
        item = self.create_item()
        warehouse = self.create_warehouse()

        self.create_receipt(item, warehouse, 5, 100)

        consume = frappe.get_doc({
            "doctype": "Stock Entry",
            "purpose": "Consume",
            "posting_date": frappe.utils.today(),
            "posting_time": frappe.utils.nowtime(),
            "item": [
                {
                    "item": item.name,
                    "quantity": 10,
                    "source_warehouse": warehouse.name,
                    "rate": 100
                }
            ]
        })
        consume.insert()

        with self.assertRaises(frappe.ValidationError):
            consume.submit()

    def test_stock_ledger_report(self):
        item = self.create_item()
        warehouse = self.create_warehouse()

        self.create_receipt(item, warehouse, 10, 100)
        self.create_consume(item, warehouse, 4, 100)

        from mywarehouse.mywarehouse.report.stock_ledger.stock_ledger import execute

        columns, data = execute({
            "from_date": frappe.utils.today(),
            "to_date": frappe.utils.today(),
            "item": item.name,
            "warehouse": warehouse.name
        })

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["actual_qty"], 10)
        self.assertEqual(data[1]["actual_qty"], -4)

    def test_stock_balance_report(self):
        item = self.create_item()
        warehouse = self.create_warehouse()

        self.create_receipt(item, warehouse, 10, 100)
        self.create_consume(item, warehouse, 4, 100)

        from mywarehouse.mywarehouse.report.stock_balance.stock_balance import execute

        columns, data = execute({
            "to_date": frappe.utils.today(),
            "item": item.name,
            "warehouse": warehouse.name
        })

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["balance_qty"], 6)
        self.assertEqual(data[0]["stock_value"], 600)
        self.assertEqual(data[0]["valuation_rate"], 100)