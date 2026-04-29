import frappe
from frappe import _


def execute(filters=None):
    filters = frappe._dict(filters or {})

    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():
    return [
        {
            "label": _("Item"),
            "fieldname": "item",
            "fieldtype": "Link",
            "options": "Item",
            "width": 200,
        },
        {
            "label": _("Warehouse"),
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 200,
        },
        {
            "label": _("Actual Qty"),
            "fieldname": "actual_qty",
            "fieldtype": "Float",
            "width": 140,
        },
        {
            "label": _("Stock Value"),
            "fieldname": "stock_value",
            "fieldtype": "Currency",
            "width": 140,
        },
        {
            "label": _("Valuation Rate"),
            "fieldname": "valuation_rate",
            "fieldtype": "Currency",
            "width": 140,
        },
    ]


def get_data(filters):
    conditions = []
    values = {}

    if filters.get("to_date"):
        conditions.append("posting_date <= %(to_date)s")
        values["to_date"] = filters.to_date

    if filters.get("item"):
        conditions.append("item = %(item)s")
        values["item"] = filters.item

    if filters.get("warehouse"):
        conditions.append("warehouse = %(warehouse)s")
        values["warehouse"] = filters.warehouse

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    data = frappe.db.sql(
        f"""
        SELECT
            item,
            warehouse,
            SUM(actual_qty) AS actual_qty,
            CASE
                WHEN SUM(actual_qty) <= 0 THEN 0
                ELSE SUM(actual_qty * valuation_rate) / SUM(actual_qty)
            END AS valuation_rate,
            SUM(actual_qty * valuation_rate) AS stock_value
        FROM `tabStock Ledger Entry`
        {where_clause}
        GROUP BY item, warehouse
        HAVING SUM(actual_qty) > 0
        ORDER BY item, warehouse
        """,
        values,
        as_dict=True,
    )

    return data

  