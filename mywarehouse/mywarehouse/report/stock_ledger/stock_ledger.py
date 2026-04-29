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
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": _("Posting Time"),
            "fieldname": "posting_time",
            "fieldtype": "Time",
            "width": 100,
        },
        {
            "label": _("Item"),
            "fieldname": "item",
            "fieldtype": "Link",
            "options": "Item",
            "width": 180,
        },
        {
            "label": _("Warehouse"),
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 180,
        },
        {
            "label": _("Voucher Type"),
            "fieldname": "voucher_type",
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "label": _("Voucher No"),
            "fieldname": "voucher_no",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Actual Qty"),
            "fieldname": "actual_qty",
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "label": _("Valuation Rate"),
            "fieldname": "valuation_rate",
            "fieldtype": "Currency",
            "width": 130,
        },
        {
            "label": _("Stock Value"),
            "fieldname": "stock_value",
            "fieldtype": "Currency",
            "width": 130,
        },
    ]


def get_data(filters):
    conditions = []
    values = {}

    if filters.get("from_date"):
        conditions.append("posting_date >= %(from_date)s")
        values["from_date"] = filters.from_date

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

    return frappe.db.sql(
        f"""
        SELECT
            posting_date,
            posting_time,
            item,
            warehouse,
            voucher_type,
            voucher_no,
            actual_qty,
            valuation_rate,
            stock_value
        FROM `tabStock Ledger Entry`
        {where_clause}
        ORDER BY posting_date, posting_time, creation
        """,
        values,
        as_dict=True,
    )