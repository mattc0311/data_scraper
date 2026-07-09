from urllib.request import urlopen
import json
from json import dumps
import os

url = "https://boards-api.greenhouse.io/v1/boards/spacex/jobs"


## Open URL, decode HTML (if any) then read with json for convenience

page = urlopen(url)
html_bytes = page.read()
raw_string = html_bytes.decode("utf-8")

data = json.loads(raw_string)
jobs_list = data["jobs"]


## Test information in different jobs 

#print(len(data["jobs"]))
#print(list(jobs_list[0].keys()))
#for i in range(6):
#    print(jobs_list[i*10]["metadata"])

matches = []

## work with one sample , type type(job_test[0]) = dict, 
# dict_keys(['id', 'name', 'value', 'value_type'])


job_test = jobs_list[10]["metadata"]
print(job_test[1]["value"])  # gives discipline 

with open("tracker.md","r") as file:
    text = file.read()

for job in jobs_list:

    title = job.get("title", "")
    url = job.get("absolute_url", "")
    
    # Safely access the nested location dictionary
    location_dict = job.get("location", {})
    location = location_dict.get("name", "") if location_dict else ""
    meta = job["metadata"]

    for item in meta:
        field = item.get("name")
        if field == "Discipline":
            disc = item.get("value")
        if field == "Employment Type":
            empl_type = item.get("value")

    if "Sr." not in title:
        # Note: Added safety check to ensure disc and empl_type are not None
        if disc and ("engineering" in disc.lower() or "physics" in disc.lower()):
            if "fl" in location.lower():  # e.g., Florida
                if empl_type and ("regular" in empl_type.lower() or "intern" in empl_type.lower()):
                    print(title)
                    print(url)

                    job_dict = {
                        "title": title,
                        "discipline": disc,
                        "location": location,
                        "type": empl_type,
                        "URL": url
                    }
                    matches.append(job_dict)

                    if url in text:
                        print("Job already tracked.")
                    else: 
                        print("Adding new job.")
                        with open("tracker.md","a") as file:
                            file.write(f"| {title} | {disc} | {location} | {empl_type} | {url} |\n")


                
print(matches)

'''    
with open("tracker.md", "a") as file:
    file.write(matches)    

'''



# Employment types: "Regular", "Temporary"
# ['absolute_url', 'data_compliance', 'education', 'internal_job_id', 
# 'location', 'metadata', 'id', 'updated_at', 'requisition_id', 'title', 
# 'company_name', 'first_published', 'language', 'application_deadline']


# " , 'title': --- ', "
# " , 'application_deadline': --- } "
# " {'absolute_url': '---', "

