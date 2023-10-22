# Copyright (c) 2023, Birhane Gebrial and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from pydub import AudioSegment
from frappe.utils.file_manager import get_file_url
import os
from werkzeug.utils import secure_filename
class Audiobook(Document):
      def after_insert(self):
              company = frappe.defaults.get_user_default("Company")
              posting_date = self.get("posting_date") or frappe.utils.nowdate()
              stock_entry = frappe.new_doc("Stock Entry")
              stock_entry.posting_date = posting_date
              stock_entry.stock_entry_type = "Material Receipt"
              stock_entry.company = company
              stock_entry.append(
                "items",{
                    "item_code": "Test",
                    "qty": 1,
                    # "valuation_rate": self.licensing_cost,
                    # If Their is Ant calculation will be here
                    "basic_rate": self.licensing_cost * self.production_cost,
                    "cost_center": frappe.defaults.get_user_default("Cost Center"),
                    "t_warehouse": "Stores - BRA", 
    })
              stock_entry.save()
              stock_entry.submit()
              self.reload()

      def validate(self):
        if self.audio_file:
            # audio_file_doc = frappe.get_doc("File", self.audio_file)
            # file_path = frappe.get_site_path("public", audio_file_doc.file_url[1:])
            file_path = frappe.get_site_path("public", self.audio_file[1:])
            abso_file_path = os.path.abspath(file_path)

            # frappe.msgprint(abso_file_path)
            audio = AudioSegment.from_file(abso_file_path)
            # frappe.msgprint(audio)
            duration_sec = len(audio) / 1000
            self.duration = duration_sec

	# def after_insert(self):
	# 	company = frappe.defaults.get_user_default("Company")
	# 	posting_date = self.get("posting_date") or frappe.utils.nowdate()
		
	# 	gl_entry = make_gl_entry(
    #     company=company,
    #     posting_date=posting_date,
    #     account="Stock In Hand",
    #     debit=0,
    #     credit=flt(self.licensing_cost),
    #     voucher_type=self.doctype,
    #     voucher_no=self.name,
    #     against_voucher_type=self.doctype,
    #     against_voucher=self.name,
    #     remarks="Update Stock In Hand balance",
    # )
	# 	gl_entry.insert()
	# 	gl_entry.submit()
		
	# 	self.reload()