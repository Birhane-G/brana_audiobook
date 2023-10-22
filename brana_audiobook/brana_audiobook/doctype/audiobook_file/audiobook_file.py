# Copyright (c) 2023, Birhane Gebrial and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from pydub import AudioSegment
from frappe.utils.file_manager import get_file_url
import os
from werkzeug.utils import secure_filename

class AudiobookFile(Document):
	def validate(self):
		if self.audio_file:
			file_path = frappe.get_site_path("public", self.audio_file[1:])
			abso_file_path = os.path.abspath(file_path)
			# frappe.msgprint(file_path)

			fileName = os.path.basename(abso_file_path)
			self.audio_base_name = fileName

			# Set file type
			file_format = os.path.splitext(self.audio_file)[1][1:]
			self.type = file_format

			# Set file size
			file_size = os.path.getsize(abso_file_path)
			self.size = f"{file_size} byte"

			self.file_url = abso_file_path

			audio = AudioSegment.from_file(abso_file_path)
			duration_sec = len(audio) / 1000
			self.duration = duration_sec