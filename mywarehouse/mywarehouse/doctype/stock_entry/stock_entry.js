frappe.ui.form.on("Stock Entry", {
  refresh(frm) {
    toggle_warehouse_fields(frm);
  },

  purpose(frm) {
    toggle_warehouse_fields(frm);
  }
});

function toggle_warehouse_fields(frm) {
  const purpose = frm.doc.purpose;

  const show_source = ["Consume", "Transfer"].includes(purpose);
  const show_target = ["Receipt", "Opening", "Transfer"].includes(purpose);

  frm.fields_dict.item.grid.update_docfield_property(
    "source_warehouse",
    "hidden",
    !show_source
  );

  frm.fields_dict.item.grid.update_docfield_property(
    "target_warehouse",
    "hidden",
    !show_target
  );

  frm.refresh_field("item");
}