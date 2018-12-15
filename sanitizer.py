from os import path
from glob import glob
import sys

from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import NameObject, createStringObject

def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))

def main():
	all_pdf_files = find_ext(".","pdf")

	output = PdfFileWriter()

	infoDict = output._info.getObject()
	infoDict.update({
		NameObject('/Title'): createStringObject(u'title'),
		NameObject('/Author'): createStringObject(u'author'),
		NameObject('/Subject'): createStringObject(u'subject'),
		NameObject('/Creator'): createStringObject(u'a script')
	})

	c = 0

	for pdf in all_pdf_files:
		inputPdf = PdfFileReader(open(pdf, "rb"))
		docInfo = inputPdf.getDocumentInfo()

		c = c + 1

		print("Processing file: ", pdf)
		print("Title: ", docInfo.title)
		print("Author: ", docInfo.author)
		print("Subject: ", docInfo.subject)
		print("Producer: ", docInfo.producer)
		print("Creator: ", docInfo.creator)

		for page in range(inputPdf.getNumPages()):
			output.addPage(inputPdf.getPage(page))

		outputStream = open(str(c)+".pdf", 'wb')
		output.write(outputStream)
		outputStream.close()

		print("\n")



if __name__ == '__main__':
    main()
