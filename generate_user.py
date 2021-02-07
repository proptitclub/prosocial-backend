import requests
import csv

with open('prosocial_user.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        username = row[0]
        password = row[1]
        last_name = row[2]
        first_name = row[3]
        dob = row[4]
        display_name = row[5]
        user_gender = row[6]
        class_name = row[7]
        email = row[8]
        phone_number = row[9]
        
        content = {
            "username": username,
            "password": password,
            "last_name": last_name,
            "first_name": first_name,
            "dob": dob,
            "display_name": display_name,
            "user_gender": user_gender,
            "class_name": class_name,
            "email": email,
            "phone_number": phone_number,
        }

        response = requests.post("http://127.0.0.1:8000/users/create/", data=content)
        print(response)