# subdomainchecker

Script written to "quickly" and easily check the results from the "subfinder" script.

Example usage is as follows:

subfinder -d youtube.com >> ytsubdomains.txt
./subdomainchecker.py -i ytsubdomains.txt -o output.txt
cat output.txt


Future updates plan to:
Include all protocols (such as HTTP and HTTPS)
Include many common ports (80, 443, 8080, 443)
More..
