# Import external modules
import fitz
import sys
import os
import pdfkit
import fitz
import tkinter as tk

# Import internal modules
import zoresearch.gui

class Source:
	"""
	Class Source used for each source in dataset. 
	Used to update annotations, notes, and create tkinter labels
	"""
	def __init__(self, metadata):
		"""Creates Source object. Initializes with information passed from metadata dictionary"""

		# Set initial values
		self.title= ''
		self.short_title = ''
		self.url = ''
		self.attachment = ''
		self.date_added = ''
		self.collections = []
		self.annots = []
		self.all_notes = ''
		self.read = False
		self.starred = False

		# Add any passed data as attributes
		for key in metadata:
		 	setattr(self, key, metadata[key])


	def _describe(self):
		"""Prints Source object metadata"""
		print(f'SOURCE DESCRIPTION\nTitle: {self.title}\nKey: {self.key}\nURL: {self.url}\nAll notes: {self.all_notes}')


	def _create_label(self, frame):
		"""Creates tkinter label based on Source data
		Binds label to 2 functions: zoresearch.gui_hover & zoresearch.gui_leave
		"""

		if self.short_title is not None:
			text = self.short_title

		elif self.title is not None:
			text = self.title

		else:
			text = 'Title unavailable'

		if self.starred:
			text =u'\u2605 ' +  text

		if len(text) > 80:
			text = text[ :80] + '...'

		self.label = tk.Label(
						frame, 
						text=text,
						width=30,
						font=('open sans',10),
                        wraplength=200, 
                        bg='#E5E5E5', 
                        justify=tk.LEFT,
                        anchor='w',
                        pady=10,
                        cursor='hand2'
						)
		if self.read == False:
			self.label.config(font=('open sans', 10, 'bold'))

		self.label.bind('<Enter>', zoresearch.gui._hover)
		self.label.bind('<Leave>', zoresearch.gui._leave)
		

	def _html_to_pdf(self, html):
		"""Converts Source attachment from HTML to PDF"""
		print(f'\t\tConverting HTML file to PDF: {html}')
		html = self.attachment + html
		# print(html)
		pdf_path = html[ : -4] + 'pdf'
		# print(pdf_path)
		
		try:
			# Sometimes wkhtml works better if a path to its .exe is included
			if os.path.exists(r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"):
				config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
				pdfkit.from_file(html, pdf_path, verbose=False, configuration=config, options=(
						{
						'disable-javascript': True
						, 'load-error-handling': 'skip'
						}
					)
				)
			else:
				pdfkit.from_file(html, pdf_path, verbose=False, options=(
						{
						'disable-javascript': True
						, 'load-error-handling': 'skip'
						}
					)
				)

		except OSError:
			# print('\t\t\tWKHTML is complaining')
			pass
		
		if os.path.exists(pdf_path):
			print('\t\tCreated PDF')
			self.attachment = pdf_path
		else:
			print('\t\tFailed to create PDF')


	def _get_attachment(self):
		""""If a Source doesn't have a PDF attachment already, searches folder for PDF or HTML to convert to PDF """

		# Return if PDF is already located or if no attachment exists
		if self.attachment is None:
			return

		if self.attachment.endswith('.pdf'):
			# print('\t\tPDF already exists or no attachment: {}'.format(self.attachment))
			return

		# Otherwise, attachment points to directory. Convert HTML to PDF if needed
		else:
			try:
				directory = os.listdir(self.attachment)
				pdf = [match for match in directory if '.pdf' in match]
				if pdf:
					# print('\t\tPDF found in source folder: {}'.format(pdf[0]))
					self.attachment = self.attachment + pdf[0]

				else:
					html = [match for match in directory if '.html' in match]
					if html:
						# print(f'found html: {html[0]}')
						self._html_to_pdf(html[0])
						
					else:
						# print('\t\tNo attachment found in folder; return none')
						self.attachment = None
			
			except FileNotFoundError:
				return


	def _check_contain(self, rect_annot, rect_reference, threshold=0.75):
	    '''Check if word rectangle overlaps with annotation rectangle'''
	    x_a1, y_a1, x_a2, y_a2 = rect_annot
	    x_b1, y_b1, x_b2, y_b2 = rect_reference

	    if x_a1 >= x_b2 or x_b1 >= x_a2:
	        return False
	    elif y_a1 >= y_b2 or y_b1 >= y_a2:
	        return False
	    else:
	        b_area = (y_b2 - y_b1) * (x_b2 - x_b1)
	        overlap_area = (
	                        (min(y_a2, y_b2) - max(y_a1, y_b1))
	                        * (min(x_a2, x_b2) - max(x_a1, x_b1))
	                       )
	        return (overlap_area / b_area) > threshold


	def _iterate_words(self, page):
	    '''Iterate through all words in a page and return word'''
	    for wb in sorted(page.get_text('words'), key=lambda w: (w[1], w[0])):
	        yield(wb)


	def _get_highlight_text(self, annot):
	    '''Get highlighted text'''
	    annot_text_raw = ''
	    rect_counts = len(annot.vertices) // 4
	    for i in range(rect_counts):
	        for word in self._iterate_words(annot.parent):
	            if self._check_contain(
	                              annot.vertices[i * 4]
	                              + annot.vertices[(i * 4) + 3],
	                              word[:4],
	                             ):
	                annot_text_raw = annot_text_raw + ' ' + word[4]
	    return annot_text_raw


	def _create_annot(self, annot):
	    '''Create annot entry in source_entry dict
	       for sticky comments and highlights
	    '''
	    # Get text from sticky comment
	    if(annot.type[0] == 0):
	        annot_text_raw = annot.info['content']

	    # Get text from highlight
	    elif(annot.type[0] == 8):
	        annot_text_raw = self._get_highlight_text(annot)

	    else:
	        annot_text_raw = 'None'

	    # Create annot entry
	    annot_text = ('PAGE '
	                  + str(annot.parent.number + 1)
	                  + ' ('
	                  + annot.type[1]
	                  + '): '
	                  + annot_text_raw
	                  )
	    annot_entry = {
	                       'page': annot.parent.number + 1,
	                       'type': annot.type[1],
	                       'text': annot_text
	                       }

	    # Append annot entry if not already present
	    if annot_entry not in self.annots:
	        self.annots.append(annot_entry)
	        self.all_notes += '\n\n' + annot_text 


	def _get_annots(self):
		"""Runs through PDF pages and extracts annotation"""
		if self.attachment == None:
			return
		try:
			file_path = os.path.normpath(self.attachment)
			doc = fitz.open(file_path)

			for page in doc.pages():
				for annot in page.annots():
					self._create_annot(annot)
	   
		except RuntimeError:
		    self.attachment = None 
	        