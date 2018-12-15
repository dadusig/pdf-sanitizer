import os
from os import path
from glob import glob
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import NameObject, createStringObject

#find in given path all files of an extension
def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))

def main():
	# path of all pdf all_pdf_files
	# very bad implemenation. todo: use getopt
	my_path="." #default path is the current folder
	if len(sys.argv) == 2:
		my_path=sys.argv[1]
	elif len(sys.argv) > 2:
		print("Something went wrong. Check your arguments.")
		exit(-1)

	# create results directory if not exists
	os.makedirs(my_path + "/results" , exist_ok=True)

	print("Path given: ", my_path, "\n")

	# get all pdf files from specified folder
	all_pdf_files = find_ext(my_path,"pdf")

	# create metadata patch
	output = PdfFileWriter()
	infoDict = output._info.getObject()
	infoDict.update({
		NameObject('/Title'): createStringObject(u'title removed'),
		NameObject('/Author'): createStringObject(u'author removed'),
		NameObject('/Subject'): createStringObject(u'subject removed'),
		NameObject('/Creator'): createStringObject(u'software quality script'),
		NameObject('/Producer'): createStringObject(u'software quality script'),
		NameObject('/Keywords'): createStringObject(u'software, quality, sanitized')
	})

	c = 0
	for pdf in all_pdf_files:
		inputPdf = PdfFileReader(open(pdf, "rb"), strict=False) # strict=False for Windows support - PdfReadWarning: Superfluous whitespace found in object header
		docInfo = inputPdf.getDocumentInfo()

		c += 1

		# get filename from path
		filename = os.path.basename(pdf)
		# remove the extension
		filename_noext = os.path.splitext(filename)[0]

		#print some information
		print(c, ". Processing file: ", pdf)
		print("filename: ", filename)
		print("Title: ", docInfo.title)
		print("Author: ", docInfo.author)
		print("Subject: ", docInfo.subject)
		print("Producer: ", docInfo.producer)
		print("Creator: ", docInfo.creator)

		#create new pdf
		for page in range(inputPdf.getNumPages()):
			output.addPage(inputPdf.getPage(page))

		print("\n")

		# write new file in results subfolder
		# the new file name will be the old one extended with "-sanitized.pdf"
		outputStream = open(my_path+"/results/"+filename_noext+"-sanitized.pdf", 'wb')
		output.write(outputStream)
		outputStream.close()

if __name__ == '__main__':
    main()
