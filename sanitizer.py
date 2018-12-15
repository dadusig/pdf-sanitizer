from os import path
from glob import glob

def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))

def main():
	all_pdf_files = find_ext(".","pdf")

	for pdf in all_pdf_files:
		print(pdf)

if __name__ == '__main__':
    main()
