frappe.ui.form.on("Extrusion Job Card", {
	refresh(frm) {
		calculate_output_metrics(frm);
	},

	billet_weight_used_kg(frm) {
		calculate_output_metrics(frm);
	},

	net_output_kg(frm) {
		calculate_output_metrics(frm);
	},

	validate(frm) {
		validate_output_weight(frm);
		calculate_output_metrics(frm);
	}
});

function validate_output_weight(frm) {
	const billet_weight = flt(frm.doc.billet_weight_used_kg);
	const net_output = flt(frm.doc.net_output_kg);

	if (net_output > billet_weight) {
		frappe.throw(__("Net Output (Kg) cannot exceed Billet Weight Used (Kg)."));
	}
}

function calculate_output_metrics(frm) {
	const billet_weight = flt(frm.doc.billet_weight_used_kg);
	const net_output = flt(frm.doc.net_output_kg);
	const scrap_weight = billet_weight ? billet_weight - net_output : 0;
	const scrap_percentage = billet_weight ? (scrap_weight / billet_weight) * 100 : 0;
	const recovery_percentage = billet_weight ? (net_output / billet_weight) * 100 : 0;

	set_calculated_value(frm, "scrap_weight", scrap_weight);
	set_calculated_value(frm, "scrap_percentage", scrap_percentage);
	set_calculated_value(frm, "yield_percentage", recovery_percentage);
	set_calculated_value(frm, "recovery_percentage", recovery_percentage);
}

function set_calculated_value(frm, fieldname, value) {
	if (flt(frm.doc[fieldname]) !== flt(value)) {
		frm.set_value(fieldname, value);
	}
}
