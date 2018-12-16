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
	return [id, path, os.path.basename(path), docInfo.title, docInfo.author, docInfo.subject, docInfo.producer, docInfo.creator]

def main():
	my_path="./input_files"
	# N = random.randint(100,200)
	N = 100

	all_pdf_files = find_ext(my_path,"pdf")
	K = int(len(all_pdf_files))

	filesDict = {}

	for i in range(N, N+K):
		filesDict[i] = makeList(all_pdf_files[i-N], i)

	# print(filesDict)

	for i in range(N, N+K):
		print(i, filesDict[i][1])

	with open('demo.csv', 'w', newline='') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		wr.writerow(filesDict[100])


if __name__ == '__main__':
    main()
