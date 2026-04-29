frappe.query_reports["Stock Balance"] = {
  filters: [
    {
      fieldname: "to_date",
      label: __("Balance Date"),
      fieldtype: "Date",
      default: frappe.datetime.get_today(),
      reqd: 1
    },
    {
      fieldname: "item",
      label: __("Item"),
      fieldtype: "Link",
      options: "Item"
    },
    {
      fieldname: "warehouse",
      label: __("Warehouse"),
      fieldtype: "Link",
      options: "Warehouse"
    }
  ]
};