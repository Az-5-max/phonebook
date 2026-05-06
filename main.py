import csv
import re
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

print("Было:")
pprint(contacts_list)

new_contacts = []
headers = ["lastname", "firstname", "surname", "organization", "position", "phone", "email"]
new_contacts.append(headers)

for row in contacts_list[1:]:
    while len(row) < 12:
        row.append("")

    organization = row[0]
    email = row[7]
    phone = row[9]
    full_name = row[5]

    name_parts = full_name.split()

    lastname = name_parts[0] if len(name_parts) > 0 else ""
    firstname = name_parts[1] if len(name_parts) > 1 else ""
    surname = name_parts[2] if len(name_parts) > 2 else ""

    new_row = [lastname, firstname, surname, organization, "", phone, email]
    new_contacts.append(new_row)


def format_phone(phone):
    if not phone:
        return ""

    ext = ""
    if "доб" in phone.lower():
        ext_match = re.search(r"(\d+)", phone.split("доб")[1])
        if ext_match:
            ext = f" доб.{ext_match.group(1)}"

    digits = ""
    for ch in phone:
        if ch.isdigit():
            digits += ch

    if len(digits) >= 10:
        code = digits[-10:-7]
        part1 = digits[-7:-4]
        part2 = digits[-4:]
        return f"+7({code}){part1}-{part2}{ext}"

    return phone


for contact in new_contacts[1:]:
    contact[5] = format_phone(contact[5])

unique = {}
for contact in new_contacts[1:]:
    key = (contact[0], contact[1])

    if key not in unique:
        unique[key] = contact
    else:
        old = unique[key]
        for i in range(len(contact)):
            if not old[i] and contact[i]:
                old[i] = contact[i]

result = [headers] + list(unique.values())

print("\nСтало:")
pprint(result)

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(result)

print("\nГотово! Результат в phonebook.csv")
