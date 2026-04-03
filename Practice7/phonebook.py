import csv
from connect import connect

# INSERT FROM CSV
def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted!")


# INSERT FROM CONSOLE
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added!")


# UPDATE CONTACT
def update_contact():
    old_phone = input("Enter phone of contact to update: ")
    new_name = input("Enter new name (or press Enter to skip): ")
    new_phone = input("Enter new phone (or press Enter to skip): ")

    conn = connect()
    cur = conn.cursor()

    if new_name:
        cur.execute(
            "UPDATE phonebook SET first_name = %s WHERE phone = %s",
            (new_name, old_phone)
        )

    if new_phone:
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE phone = %s",
            (new_phone, old_phone)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated!")


# QUERY WITH FILTERS
def query_contacts():
    print("1 - Show all")
    print("2 - Search by name")
    print("3 - Search by phone prefix")

    choice = input("Choose: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")

    elif choice == "2":
        name = input("Enter name: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE first_name ILIKE %s",
            ('%' + name + '%',)
        )

    elif choice == "3":
        prefix = input("Enter prefix: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s",
            (prefix + '%',)
        )

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# DELETE CONTACT
def delete_contact():
    choice = input("Delete by (1) name or (2) phone: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute(
            "DELETE FROM phonebook WHERE first_name = %s",
            (name,)
        )

    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute(
            "DELETE FROM phonebook WHERE phone = %s",
            (phone,)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted!")

while True:
    print("\n1. Insert from CSV")
    print("2. Add contact")
    print("3. Update contact")
    print("4. Query contacts")
    print("5. Delete contact")
    print("0. Exit")

    choice = input("Choose: ")

    if choice == "1":
        insert_from_csv("C:/Users/kossh/OneDrive/Документы/GitHub/PP2/Practice7/contacts.csv")
    elif choice == "2":
        insert_from_console()
    elif choice == "3":
        update_contact()
    elif choice == "4":
        query_contacts()
    elif choice == "5":
        delete_contact()
    elif choice == "0":
        break