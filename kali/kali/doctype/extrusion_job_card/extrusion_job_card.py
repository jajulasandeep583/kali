import frappe
from frappe import _
from frappe.model.document import Document

class ExtrusionJobCard(Document):
    def validate(self):
        self.validate_output_weight()
        self.calculate_output_metrics()

    def validate_output_weight(self):
        billet_weight = self.billet_weight_used_kg or 0
        net_output = self.net_output_kg or 0

        if net_output > billet_weight:
            frappe.throw(_("Net Output (Kg) cannot exceed Billet Weight Used (Kg)."))

    def calculate_output_metrics(self):
        billet_weight = self.billet_weight_used_kg or 0
        net_output = self.net_output_kg or 0

        self.scrap_weight = billet_weight - net_output if billet_weight else 0
        self.scrap_percentage = (self.scrap_weight / billet_weight * 100) if billet_weight else 0
        self.yield_percentage = (net_output / billet_weight * 100) if billet_weight else 0
        self.recovery_percentage = self.yield_percentage
