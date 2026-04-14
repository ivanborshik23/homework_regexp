import re
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

def format_phone(raw_phone):
    if not raw_phone:
        return ""
    
    digits = re.sub(r"\D", "", raw_phone)
    
    if len(digits) >= 10:
        main_part = digits[-10:]
        formatted = f"+7({main_part[:3]}){main_part[3:6]}-{main_part[6:8]}-{main_part[8:10]}"
        
        ext_match = re.search(r"доб\.?\s*(\d+)", raw_phone)
        if ext_match:
            formatted += f" доб.{ext_match.group(1)}"
        
        return formatted
    return raw_phone

def process_contacts(contacts):
    header = contacts[0]
    contacts_dict = {}

    for row in contacts[1:]:
        full_name_raw = " ".join(row[:3]).split()
        lastname = full_name_raw[0] if len(full_name_raw) > 0 else ""
        firstname = full_name_raw[1] if len(full_name_raw) > 1 else ""
        surname = full_name_raw[2] if len(full_name_raw) > 2 else ""
        
        organization = row[3]
        position = row[4]
        email = row[6]
        phone = format_phone(row[5])

        current_data = [lastname, firstname, surname, organization, position, phone, email]
        
        person_key = (lastname, firstname)
        
        if person_key not in contacts_dict:
            contacts_dict[person_key] = current_data
        else:
            for i in range(len(current_data)):
                if not contacts_dict[person_key][i]:
                    contacts_dict[person_key][i] = current_data[i]

    return [header] + list(contacts_dict.values())

cleaned_contacts = process_contacts(contacts_list)

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(cleaned_contacts)