# Copyright (c) 2023, Birhane Gebrial and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Podcast(Document):
    def after_insert(self):
        company = frappe.defaults.get_user_default("Company")
        posting_date = self.get("posting_date") or frappe.utils.nowdate()
        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.posting_date = posting_date
        stock_entry.stock_entry_type = "Material Receipt"
        stock_entry.company = company
        stock_entry.append(
            "items",{
            "item_code": "Brana - Podcast",
            "qty": 1,
            # "valuation_rate": self.licensing_cost,
            # If Their is another calculation will be here
            # * self.production_cost,
            "basic_rate": (self.licensing_cost or 0) * (self.production_cost or 0), 
            "cost_center": frappe.defaults.get_user_default("Cost Center"),
            "t_warehouse": "Stores - BRA", 
            })
        stock_entry.save()
        stock_entry.submit()

    def validate(self):
        if self.episodes:
            self.total_episode_duration = 0
            for data in self.episodes:
                chapter_audio_file_doc = frappe.get_doc("Audiobook File", data.audio_file)
                data.duration = chapter_audio_file_doc.duration
                self.total_episode_duration += data.duration

    def on_submit(self):
        self.save()
        self.reload()
