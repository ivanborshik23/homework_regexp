import re
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

def process_contacts(contacts):
    new_contacts_list = []
    header = contacts[0]
    new_contacts_list.append(header)
    
    contacts_dict = {}

    for row in contacts[1:]:
        full_name = " ".join(row[:3]).split()
        lastname = full_name[0] if len(full_name) > 0 else ""
        firstname = full_name[1] if len(full_name) > 1 else ""
        surname = full_name[2] if len(full_name) > 2 else ""
        
        phone_pattern = re.compile(
            r"(\+7|8)[\s-]*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s*\(?(доб\.)?\s*(\d+)\)?)?"
        )
        
        raw_phone = row[5]
        phone = phone_pattern.sub(r"+7(\2)\3-\4-\5", raw_phone)
        
        match = phone_pattern.search(raw_phone)
        if match and match.group(8):
            phone += f" доб.{match.group(8)}"

        current_data = [lastname, firstname, surname, row[3], row[4], phone, row[6]]
        
        person_key = (lastname, firstname)
        
        if person_key not in contacts_dict:
            contacts_dict[person_key] = current_data
        else:
            for i in range(len(current_data)):
                if not contacts_dict[person_key][i]:
                    contacts_dict[person_key][i] = current_data[i]

    for contact in contacts_dict.values():
        new_contacts_list.append(contact)
        
    return new_contacts_list

cleaned_contacts = process_contacts(contacts_list)

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(cleaned_contacts)