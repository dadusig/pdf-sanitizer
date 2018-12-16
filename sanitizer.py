#software-quality-script
import os
from os import path
from glob import glob
import sys, random, csv
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import NameObject, createStringObject

#find in given path all files of an extension
def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))

def makeList(path, id):
	inputPdf = PdfFileReader(open(path, "rb"), strict=False)
	docInfo = inputPdf.getDocumentInfo()
	return [id, os.path.basename(path), docInfo.title, docInfo.author, docInfo.subject, docInfo.producer, docInfo.creator, path]

def sanitizePDFs(dict, path):
	# create results directory if not exists
	os.makedirs(path + "/results" , exist_ok=True)
	print("Path given: ", path, "\n")

	c = 0
	for file in dict:
		inputPdf = PdfFileReader(open(dict[file][7], "rb"), strict=False) # strict=False for Windows support - PdfReadWarning: Superfluous whitespace found in object header
		docInfo = inputPdf.getDocumentInfo()

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

		c += 1
		#print some information
		print(c, ". Processing file: ", dict[file][1], "->", str(dict[file][0])+".pdf")
		#create new pdf
		for page in range(inputPdf.getNumPages()):
			output.addPage(inputPdf.getPage(page))

		# write new file in results subfolder
		outputStream = open(path+"/results/"+str(dict[file][0])+".pdf", 'wb')
		output.write(outputStream)
		outputStream.close()

	print("Removed metadata from", c, "files")

def createCSV(N, K, filesDict, csv_name):
	with open(csv_name, 'w', newline='') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		fieldnames=['id','filename','title','author','subject','producer','creator','path']
		wr.writerow(fieldnames)
		for i in range(N, N+K):
			wr.writerow(filesDict[i])

def main():
	my_path="./input_files"
	all_pdf_files = find_ext(my_path,"pdf")

	# N = random.randint(100,200)
	N = 100 #random base number
	K = len(all_pdf_files) # count of pdf files

	filesDict = {}
	for i in range(N, N+K):
		filesDict[i] = makeList(all_pdf_files[i-N], i)

	createCSV(N, K, filesDict, "demo.csv")
	sanitizePDFs(filesDict, my_path)

if __name__ == '__main__':
    main()
