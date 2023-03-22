import requests as r
import math
from tqdm import tqdm
from colorama import Fore, Back, Style

print(Fore.BLUE + """
██╗   ██╗███╗   ██╗ █████╗  ██████╗ █████╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗     ██████╗ ██╗     
██║   ██║████╗  ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝████╗ ████║╚██╗ ██╔╝     ██╔══██╗██║     
██║   ██║██╔██╗ ██║███████║██║     ███████║██║  ██║█████╗  ██╔████╔██║ ╚████╔╝█████╗██║  ██║██║     
██║   ██║██║╚██╗██║██╔══██║██║     ██╔══██║██║  ██║██╔══╝  ██║╚██╔╝██║  ╚██╔╝ ╚════╝██║  ██║██║     
╚██████╔╝██║ ╚████║██║  ██║╚██████╗██║  ██║██████╔╝███████╗██║ ╚═╝ ██║   ██║        ██████╔╝███████╗
 ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝   ╚═╝        ╚═════╝ ╚══════╝
                                                                                                    
""")

print(Fore.MAGENTA + "Report issues: https://github.com/w3Abhishek/uadl"+ Style.RESET_ALL)

headers = {"User-Agent": "Abhishek ka bot 1.0"}

tutor_link = input(Fore.CYAN + "Enter the profile URL of Unacademy Tutor (For Example https://unacademy.com/@nishant91-1003): "+ Style.RESET_ALL)
tutor_username = tutor_link.split("/")[3].replace("@","")


def downloadPdf(pdf_url):
	filename = pdf_url.split('/')[5]
	pdf = r.get(pdf_url, stream=True, headers=headers)
	total_size = int(pdf.headers.get('content-length', 0))
	block_size = 1024
	progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
	with open(filename, 'wb') as f:
	    for data in pdf.iter_content(block_size):
	        progress_bar.update(len(data))
	        f.write(data)
	progress_bar.close()
	print(Fore.GREEN + f"Downloaded {filename}\n\n"+ Style.RESET_ALL)

def showCourses(courses):
	for course in courses:
		print(Fore.YELLOW + course['programme']['next_session']['properties']['name']+ Style.RESET_ALL)

def listCourses(tutor_username):
	course_url = f"https://unacademy.com/api/v1/search_v3/educators/{tutor_username}/courses/v2/?limit=12000&filters_applied=%7B%22topic%22%3A%7B%22id%22%3A%22%22%7D%2C%22show_only%22%3A%7B%22id%22%3A%22%22%7D%2C%22goal%22%3A%7B%22id%22%3A%22all%22%7D%2C%22language%22%3A%7B%22id%22%3A%22%22%7D%2C%22filter_by%22%3A%7B%22id%22%3A%22special%22%7D%7D"
	re = r.get(course_url, headers=headers).json()
	courses = re['results']
	print("\n\nList of courses by {tutor_username}\n\n")
	showCourses(courses)
	for course in courses:
		path = f"{course['programme']['next_session']['properties']['slug']}/{course['programme']['next_session']['properties']['uid']}"
		course_url = f'https://unacademy.com/_next/data/EyjMTWv8hUY8s-istyI_w/class/{path}.json'
		print(f"Subscripting {course['programme']['next_session']['properties']['name']}")
		course_info = r.get(course_url, headers=headers).json()
		if course_info['pageProps']['classFallbackData']['slidesPdf']:
			print(f"Downloading {course['programme']['next_session']['properties']['name']}")
			downloadPdf(course_info['pageProps']['classFallbackData']['slidesPdf']['noAnnotation'])
		else:
			print(Fore.RED + f"\n\nNo PDF was provided by Tutor in {path}\n\n"+ Style.RESET_ALL)
listCourses(tutor_username)
