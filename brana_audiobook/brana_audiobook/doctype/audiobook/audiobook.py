# Copyright (c) 2023, Birhane Gebrial and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Audiobook(Document):
	def after_insert(self):
		stock_account = frappe.get_doc("Account", "Stock In Hand")
		stock_account.balance += float(self.cost)
		stock_account.save()
