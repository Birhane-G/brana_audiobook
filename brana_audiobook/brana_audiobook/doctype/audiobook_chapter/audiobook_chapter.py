# Copyright (c) 2023, Birhane Gebrial and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class AudiobookChapter(Document):
    pass
	# def validate(self):
	# 	frappe.msgprint("test")
		# if self.audio_file:
		# 	audio_file_doc = frappe.get_doc("Audiobook File", self.audio_file)
		# 	self.duration = audio_file_doc.duration
		# else:
		# 	frappe.msgprint("not working")
