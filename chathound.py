#!env/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import re
import csv
import argparse
import logtools
from urllib.parse import urlparse

LOGGER = logtools.set_up_logging(__name__, logtools.INFO)

# parse command line arguments and options
def parse_commands():
	description = "Find discord and telegram invites using keyword searching."
	parser = argparse.ArgumentParser(description=description)
	subparsers = parser.add_subparsers(dest="command")
	subparsers.required = True

	sub_parser = subparsers.add_parser("telegram", description="Find telegram invites using keyword searching.")
	sub_parser.add_argument("-o", "--output", metavar="<filename>", dest="output_file", help="Name of the output file (CSV)", default="telegram-links.csv")
	sub_parser.add_argument("-n", "--number", metavar="<number>", dest="num_links", help="Number of links to find (default 100)", type=int, default=100)
	sub_parser.add_argument("-s", "--search-engine", metavar="<search-engine>", dest="search_engine", help="Search engine to use (default Google)", choices=["Google", "DuckDuckGo"], default="Google")
	sub_parser.add_argument("-k", "--key-word", metavar="<keyword>", dest="keyword", help="keyword to use when searching for links", required=True)
	sub_parser.set_defaults(func=search_telegram)

	sub_parser = subparsers.add_parser("discord", description="Find discord invites using keyword searching.")
	sub_parser.add_argument("-o", "--output", metavar="<file>", dest="output_file", help="Name of the output file (CSV)", default="discord-links.csv")
	sub_parser.add_argument("-n", "--number", metavar="<number>", dest="num_links", help="Number of links to find (default 100)", type=int, default=100)
	sub_parser.add_argument("-k", "--key-word", metavar="<keyword>", dest="keyword", help="keyword to use when searching for links", required=True)
	sub_parser.add_argument("-s", "--search-engine", metavar="<search-engine>", dest="search_engine", help="Search engine to use (default Google)", choices=["Google", "DuckDuckGo"], default="Google")
	sub_parser.set_defaults(func=search_discord)

	args = parser.parse_args()
	return args

# used to validate a URL before requesting it.
def url_check(url):
	pat=re.compile(r"^(?:http(s)?:\/\/)[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")
	if not pat.match(url):
		LOGGER.error(f"{url} is not a valid URL.")
		return False
	return True

# search google for links + keyword, returns parsed links
def ask_google(keyword, num_links, site):
	all_links = set()
	offset = 0
	while len(all_links) < num_links:
		search = f"https://www.google.com/search?q=site:{site}+{keyword}&filter=0&start={offset}"
		bs = getpage(search)
		results = parse_google_results(bs, site)
		all_links.update(results)
		LOGGER.info(f"Number of links found so far: {len(all_links)}")
		offset += 10
	return all_links

# avoid duplicates by cleaning links
def clean_link(link, site):
	# remove query string
	link = link.replace(urlparse(link).query, "")
	if "?" in link:
		link = link.replace("?", "")
	# telegram specific problems
	if site == "t.me":
		# remove /s/ url path and query parameters
		link = link.replace("/s/", "/")
		# no need for any additional paths after the group name
		if link.count("/") > 3:
			link = link.rsplit('/', 1)[0]
		# discord links are case-sensitive, only do this to telegram
		link = link.lower()
	return link

# takes google search results and parses out relevant links
def parse_google_results(page, site):
	result_links = set()
	regex = f"^https://{site}/"
	for link in page.find_all("a", href=re.compile(regex)):
			if 'href' in link.attrs:
				href = clean_link(link.attrs['href'], site)
				if href not in result_links:
					LOGGER.debug(f"Candidate found: {href}")
					result_links.add(href)
	return result_links
	
# note yet implemented
def ask_DDG(keyword, num_links, site): 
	LOGGER.error("\n\tStill have to implement DuckDuckGo functionality :) Exiting!")
	exit(1)

# fetches a link and returns a beautiful soup object
def getpage(url):
	if not url_check(url):
		print(f" invalid URL: {url}... skipping.")
		return None
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	try:
		LOGGER.debug(f"requesting {url}")
		driver = webdriver.Chrome(
			executable_path='/usr/local/bin/chromedriver', options=chrome_options)
		driver.get(url)
		time.sleep(2)
		html = driver.page_source
		bs = BeautifulSoup(html, 'html.parser')
		driver.close()
		return bs
	except Exception as e:
		LOGGER.error(f"Couldn't request {url}\n Received exception {e}")
		exit(1)


def search_telegram(args):
	telegram_links = set()
	LOGGER.info(f"Searching for Telegram channels on {args.search_engine} using keyword {args.keyword}")
	site = "t.me"
	if args.search_engine == "Google":
		telegram_links = ask_google(args.keyword, args.num_links, site)
	elif args.search_engine == "DuckDuckGo":
		telegram_links = ask_DDG(args.keyword, args.num_links, site)
	return telegram_links



def search_discord(args):
	discord_links = set()
	LOGGER.info(f"Searching for Discord channels on {args.search_engine} using keyword {args.keyword}")
	site = "discord.com/invite"
	if args.search_engine == "Google":
		discord_links = ask_google(args.keyword, args.num_links, site)
	elif args.search_engine == "DuckDuckGo":
		discord_links = ask_DDG(args.keyword, args.num_links, site)
	return discord_links


def get_telegram_room_info(links):
	invite_links = dict()
	for invite in links:
		bs = getpage(invite)
		if bs is None:
			continue
		text = bs.find('div', class_="tgme_page_title")
		if text is not None:
			server_text = text.span.get_text().replace("\n", " ").replace(",", " ")
		else:
			server_text = "N/A"
		text = bs.find('div', class_="tgme_page_description")
		if text is not None:
			info_text = text.get_text().replace("\n", " ").replace(",", " ")
		else:
			info_text = "N/A"
		text = bs.find('div', class_="tgme_page_extra")
		if text is not None:
			member_text = text.get_text().strip()
		else:
			member_text = "N/A"
		invite_links[invite] = {"Room": server_text, "Description": info_text, "Member Count": member_text, "Link": invite}
		LOGGER.debug(f"Found: {server_text} : {info_text} : {member_text}")
	return invite_links


def get_discord_server_info(links):
	invite_links = dict()
	for invite in links:
		bs = getpage(invite)
		if bs is None:
			continue
		text = bs.select_one(".colorHeaderPrimary-26Jzh-")
		if text is None:
			continue
		server_text = text.get_text()
		info_text = text.next_sibling.get_text()
		info_text = info_text.replace("Online", "Online ")
		if "Invite Invalid" not in server_text and "Opening Discord App" not in server_text:
			invite_links[invite] = {"Room": server_text, "Description": "N/A", "Member Count": info_text, "Link": invite}
			LOGGER.debug(f"Found: {server_text} : {info_text} : {info_text}")
		else:
			LOGGER.info(f"Invalid invite link: {invite}")	
	return invite_links


def write_file(invite_links, outfile):
	if ".csv" not in outfile:
		outfile += ".csv"
	LOGGER.info(f"Writing {len(invite_links)} links to {outfile}")
	with open(outfile, 'w', newline='') as csvfile:
		headers = ["Room", "Member Count", "Description", "Link"]
		writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore', restval='')
		writer.writeheader()
		for info in invite_links.values():
			writer.writerow(info)

def main():
	args = parse_commands()
	links = args.func(args)	
	LOGGER.info(f"Done finding links, now parsing info about each. Be patient, this takes time.")
	if args.command == "telegram":
		invite_links = get_telegram_room_info(links)
	elif args.command == "discord":
		invite_links = get_discord_server_info(links)
	write_file(invite_links, args.output_file)

	
if __name__ == "__main__":
	main()