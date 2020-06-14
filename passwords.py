import requests
import hashlib
import sys

def request_api(query_char):
	url='https://api.pwnedpasswords.com/range/'+ query_char
	req=requests.get(url)
	if req.status_code!=200:
		raise RuntimeError(f'Error fetching: {req.status_code}.Authentication error or bad API')
	return req

def match_hash(hashes,actual_hash):
	hashes=(line.split(':') for line in hashes.text.splitlines())
	for found,count in hashes:
		if found==actual_hash:
			return count
	return 0

def pwned_api(password):
	sha1password=(hashlib.sha1(password.encode('utf-8')).hexdigest()).upper()
	first_five,tail=sha1password[:5],sha1password[5:]
	response=request_api(first_five)
	return match_hash(response,tail)

def main(argv):
	for passwords in argv:
		hacked_count=pwned_api(passwords)
		if hacked_count:
			print(f"Your {passwords} have been hacked {hacked_count} times.Use a stronger password!")
		else:
			print(f"Your {passwords} have been hacked {hacked_count} times.It's a pretty strong password!")
	return 0

main(sys.argv[1:])