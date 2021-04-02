"""
1) add_argument() is we provide without - or -- => poisitional arguments aka required ones 
if we provide with those - or -- => positional => not required ones. 

2) 'type' in add_argument means which datatype should user input, like str or int etc

3) You can add 'required = True' in add_mutually_exclusive_group to make user input either of the options
or you can type 'reuired = True' in one of with -, but second will be without it, hence if
user puts that => it'll do some additional stuff

4) if you add 'action = store_true' to one of the two with -, then the one with it can be used
as True and another as False

5) metavar substitutes the name of the variable given in -- by name in metavar
"""

# 1
import argparse

def fib(n):
	a, b = 0, 1
	for x in range(n):
		a, b = b, a + b
	return a

def Main():
	parser = argparse.ArgumentParser()

	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-v', '--verbose', action='store_true')
	group.add_argument('-q', '--quiet', action='store_true')

	parser.add_argument('x', help='Fib to calculate', type=int)
	parser.add_argument('-o', '--output', help='Output result to file', action='store_true')

	args = parser.parse_args()

	results = fib(args.x)
	if args.verbose:
		print(f"The {str(args.x)}th fib number is {str(results)}")
	elif args.quiet:
		print(results)
	else:
		print(f"Fib = {str(args.x)} and result = {str(results)}")

	if args.output:
		f = open('fib.txt', 'a')
		f.write(str(results) + '\n')


if __name__ == '__main__':
	Main()


# 2
import argparse

parser = argparse.ArgumentParser(description='Just some program', 
									epilog="I'm watching",
									proq='Network scanner')

parser.add_argument('target', help='Provide IPv4 network range')
parser.add_argument('-v', '--verbose', help='Turn on verbose mode', action='store_true')
# another variant of the above line
parser.add_argument('-v', '--verbose', help='Turn on verbose mode', choices=[1,2,3], type=int)

args = parser.parse_args()

if args.verbose == 1:
	print('1st variant was chosen')
elif args.verbose == 2:
	print('2nd variant was chosen')
elif args.verbose == 3:
	print('3rd variant was chosen')

# if args.verbose:
# 	print('Verbose mode turned on')
# else:
# 	print('Quiet mode')

# print(args)
# print(args.verbose)
# print(args.target)


# 2-1
import argparse
import scapy.all as scapy
import os
import pandas as pd

def get_args():
	parser = argparse.ArgumentParser(proq='Network scanner',
									description="It'll scan based on ARP protoocl",
									epiloq='Super admin is watching')

	parser.add_argument('-v', '--verbose', action='store_true', help='Turn on verbose mode') 
	# verbose version
	parser.add_argument('-t', '--target', required=True, help='Provide IPv4 range') 
# short version

	parser.add_argument('-o', dest='fout', help='Save program output to the file')

	args = parser.parse_args()

	return args

def net_scan(net):
	arp_reg = scapy.ARP(pdst=net)
	broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
	arp_broad_req = broadcast/arp_reg
	ans, unans = scapy.srp(arp_broad_req, timeout=2, verbose=False)

	res_dict = {}
	ips = []
	macs = []

	for elem in ans:
		ips.append(elem[1].psrc)
		macs.append(elem[1].hwsrc)

	res_dict['IPAddress'] = ips
	res_dict['MACAddress'] = macs

	return ans, unans, res_dict

# verbose below depends whether user provided -v or not 
def print_results(results, verbose=False):
	ans = results[0]
	unans = results[1]

	print('MAC Address\t\tIPAddress')
	print(35 * '-')

	for elem in ans:
		print(elem[1].hwsrc + '\t' + elem[1].psrc)

	if verbose:
		print('\nPrinting unanswered summary')
		print(35 * '-')
		for elem in unans:
			print(elem.summary())

def main():
	args = get_args()
	results = net_scan(args.target)
	res_dict = results[2]

	if args.verbose:
		print_results(results, verbose=True)
	else:
		print_results(results)

	if args.fout:
		cwd = os.getcwd()
		df = pd.DataFrame(res_dict)
		df.to_csv(args.fout, index=False)
		print(f"Saved to {cwd}")


if __name__ == '__main__':
	main()
