#!/usr/bin/env python3

'''

Usage:

subfinder -d website.com >> results.txt
./subdomainchecker.py -i results.txt -o output.txt

'''

import sys, getopt, re, os, requests

def checkSubdomains(inputfile):

	dict = {}

	with open(inputfile) as f:
		subdomains = f.readlines()

		for subdomain in subdomains:

			prefixes = ['http://', 'https://']

			subdomain = "https://{}".format(subdomain.strip())

			try:
				response = requests.head(subdomain, timeout=.5)
			except Exception as e:
				pass
			else:

				if str(response.status_code)[0] == '2':
					if str(response.status_code)[0] in dict:
						string = "{} Success: Response code {}".format(subdomain, response.status_code)
						dict[str(response.status_code)[0]].append(string)
						print(string)
					else:
						string = "{} Success: Response code {}".format(subdomain, response.status_code)
						dict[str(response.status_code)[0]] = [string]
						print(string)
				elif str(response.status_code)[0] == '3':
					if str(response.status_code)[0] in dict:
						string = "{} Response code {}: Redirect to {}".format(subdomain, response.status_code, response.headers['Location'])
						dict[str(response.status_code)[0]].append(string)
						print(string)
					else:
						string = "{} Response code {}: Redirect to {}".format(subdomain, response.status_code, response.headers['Location'])
						dict[str(response.status_code)[0]] = [string]
				elif str(response.status_code)[0] == '4':
					if str(response.status_code)[0] in dict:
						string = "{} Failure: Response code {}".format(subdomain, response.status_code)
						dict[str(response.status_code)[0]].append(string)
						print(string)
					else:
						string = "{} Failure: Response code {}".format(subdomain, response.status_code)
						dict[str(response.status_code)[0]] = [string]
						print(string)

	return dict


def displayResults(results):

	exportList = []

	st = "\n\nFinal Results:\n\n"
	print(st)
	exportList.append(st)

	for key in results.keys():
		st = "\nResults for Response Code {}XX".format(key)
		print(st)
		exportList.append(st)
		for response in results[key]:
			st = response
			exportList.append(st)
			print(st)

	return exportList


def findEmail():
		emailDomain = ''
		site = emailDomain.split('.')[0]
		os.system('dig mx {} |grep MX |cut -d " " -f2 |cut -d "." -f 1,2 |grep {} |tr -d ";"'.format(emailDomain, site))


def writeFile(finalList, outputfile):
	if os.path.exists(outputfile):
		os.remove(outputfile)

	while "Response" not in finalList[0]:
		finalList.pop(0)
	finalList[0] = finalList[0].lstrip()
	with open(outputfile, 'w') as w:
		for item in finalList:
			w.write("{}\n".format(item))


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('subdomainchecker.py -i <domainlist_inputfile>.txt -o <results>.txt')
      sys.exit(2)
   for opt, arg in opts:
      if opt in ('-h', '--help'):
      	print('subdomainchecker.py -i <domainlist_inputfile>.txt -o <results>.txt')
      	sys.exit(0)
      elif opt == "-i":
         inputfile = arg
      elif opt == "-o":
         outputfile = arg

   results = checkSubdomains(inputfile)
   toFile = displayResults(results)
   writeFile(toFile, outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
