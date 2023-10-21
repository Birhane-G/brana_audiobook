# Copyright (c) 2023, Birhane Gebrial and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

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
                    "item_code": self.naming_series,
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


	# def after_insert(self):
	# 	stock_account = frappe.get_doc("Account", "Stock in Hand - BRA")
	# 	stock_account.balance += float(self.licensing_cost)
	# 	stock_account.save()

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