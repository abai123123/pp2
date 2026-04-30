import csv
import json
from connect import connect


def get_group_id(cur, group_name):
    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) ON CONFLICT(name) DO NOTHING",
        (group_name,)
    )
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def add_contact(name, email, birthday, group_name):
    conn = connect()
    cur = conn.cursor()

    try:
        group_id = get_group_id(cur, group_name)

        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT(name)
            DO UPDATE SET
                email = EXCLUDED.email,
                birthday = EXCLUDED.birthday,
                group_id = EXCLUDED.group_id
        """, (name, email, birthday, group_id))

        conn.commit()
        print("Contact added/updated")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def show_all_contacts():
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                c.name,
                c.email,
                c.birthday,
                g.name,
                STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, c.name, c.email, c.birthday, g.name
            ORDER BY c.name
        """)

        rows = cur.fetchall()

        print("\n--- ALL CONTACTS ---")
        if not rows:
            print("No contacts found")
        else:
            for row in rows:
                print("Name:", row[0])
                print("Email:", row[1])
                print("Birthday:", row[2])
                print("Group:", row[3])
                print("Phones:", row[4])
                print("--------------------")

    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()


def insert_from_console():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group_name = input("Group: ")

    add_contact(name, email, birthday, group_name)

    phone = input("Phone: ")
    phone_type = input("Type(home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        conn.commit()
        print("Phone added")
    except Exception as e:
        conn.rollback()
        print("Phone error:", e)

    cur.close()
    conn.close()


def add_phone_menu():
    name = input("Contact name: ")
    phone = input("Phone: ")
    phone_type = input("Type(home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        conn.commit()
        print("Phone added")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["name"]
                email = row["email"]
                birthday = row["birthday"]
                group_name = row["group"]
                phone = row["phone"]
                phone_type = row["type"]

                group_id = get_group_id(cur, group_name)

                cur.execute("""
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT(name)
                    DO UPDATE SET
                        email = EXCLUDED.email,
                        birthday = EXCLUDED.birthday,
                        group_id = EXCLUDED.group_id
                """, (name, email, birthday, group_id))

                cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

        conn.commit()
        print("CSV imported")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def search_contacts_menu():
    print("1. Search by name / phone / email / group")
    print("2. Search ONLY by email")

    choice = input("Choose: ")
    query = input("Enter search text: ")

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "2":
            cur.execute("""
                SELECT 
                    c.name,
                    c.email,
                    c.birthday,
                    g.name,
                    STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                WHERE c.email ILIKE %s
                GROUP BY c.id, c.name, c.email, c.birthday, g.name
                ORDER BY c.name
            """, ("%" + query + "%",))
        else:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))

        rows = cur.fetchall()

        print("\n--- SEARCH RESULTS ---")
        if not rows:
            print("No contacts found")
        else:
            for row in rows:
                print("Name:", row[0])
                print("Email:", row[1])
                print("Birthday:", row[2])
                print("Group:", row[3])
                print("Phones:", row[4])
                print("--------------------")

    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()


def filter_by_group():
    group_name = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                c.name,
                c.email,
                c.birthday,
                g.name,
                STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE g.name = %s
            GROUP BY c.id, c.name, c.email, c.birthday, g.name
            ORDER BY c.name
        """, (group_name,))

        rows = cur.fetchall()

        print("\n--- GROUP RESULTS ---")
        if not rows:
            print("No contacts found")
        else:
            for row in rows:
                print("Name:", row[0])
                print("Email:", row[1])
                print("Birthday:", row[2])
                print("Group:", row[3])
                print("Phones:", row[4])
                print("--------------------")

    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()


def sort_contacts():
    print("1. name")
    print("2. birthday")
    print("3. created_at")

    choice = input("Choose: ")

    if choice == "1":
        order = "name"
    elif choice == "2":
        order = "birthday"
    elif choice == "3":
        order = "created_at"
    else:
        print("Invalid choice")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(f"""
            SELECT 
                c.name,
                c.email,
                c.birthday,
                g.name,
                c.created_at,
                STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
            ORDER BY c.{order}
        """)

        rows = cur.fetchall()

        print("\n--- SORTED CONTACTS ---")
        for row in rows:
            print("Name:", row[0])
            print("Email:", row[1])
            print("Birthday:", row[2])
            print("Group:", row[3])
            print("Created:", row[4])
            print("Phones:", row[5])
            print("--------------------")

    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()


def pagination_loop():
    try:
        limit = int(input("How many contacts per page: "))
    except ValueError:
        print("Please enter a number")
        return

    if limit <= 0:
        print("Limit must be greater than 0")
        return

    offset = 0
    page = 1

    while True:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                c.name,
                c.email,
                c.birthday,
                g.name,
                STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, c.name, c.email, c.birthday, g.name
            ORDER BY c.name
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        print("\n--- PAGE", page, "---")

        if not rows:
            print("No contacts on this page")
        else:
            for row in rows:
                print("Name:", row[0])
                print("Email:", row[1])
                print("Birthday:", row[2])
                print("Group:", row[3])
                print("Phones:", row[4])
                print("--------------------")

        cur.close()
        conn.close()

        cmd = input("next / prev / quit: ").strip().lower()

        if cmd == "next":
            if not rows:
                print("No next page")
            else:
                offset += limit
                page += 1

        elif cmd == "prev":
            if page > 1:
                offset -= limit
                page -= 1
            else:
                print("You are already on the first page")

        elif cmd == "quit":
            break
        else:
            print("Invalid command")


def export_json():
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT c.id, c.name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.name
        """)

        contacts = []

        for row in cur.fetchall():
            contact_id, name, email, birthday, group_name = row

            cur.execute(
                "SELECT phone, type FROM phones WHERE contact_id = %s",
                (contact_id,)
            )

            phones = []

            for phone_row in cur.fetchall():
                phones.append({
                    "phone": phone_row[0],
                    "type": phone_row[1]
                })

            contacts.append({
                "name": name,
                "email": email,
                "birthday": str(birthday),
                "group": group_name,
                "phones": phones
            })

        with open("contacts_export.json", "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4, ensure_ascii=False)

        print("Exported to contacts_export.json")

    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()


def import_json():
    filename = input("JSON filename: ")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            contacts = json.load(file)
    except Exception as e:
        print("File error:", e)
        return

    conn = connect()
    cur = conn.cursor()

    try:
        for contact in contacts:
            name = contact["name"]

            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            existing = cur.fetchone()

            if existing:
                answer = input(f"{name} exists. skip/overwrite: ")

                if answer == "skip":
                    continue

            group_id = get_group_id(cur, contact["group"])

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT(name)
                DO UPDATE SET
                    email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id
            """, (name, contact["email"], contact["birthday"], group_id))

            contact_id = cur.fetchone()[0]

            cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

            for phone in contact["phones"]:
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (contact_id, phone["phone"], phone["type"]))

        conn.commit()
        print("JSON imported")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def move_to_group_menu():
    name = input("Contact name: ")
    group_name = input("New group: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
        conn.commit()
        print("Moved")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def main():
    while True:
        print("\n--- PHONEBOOK TSIS1 ---")
        print("1. Insert from CSV")
        print("2. Add contact")
        print("3. Add phone")
        print("4. Search")
        print("5. Filter by group")
        print("6. Sort contacts")
        print("7. Pagination")
        print("8. Export JSON")
        print("9. Import JSON")
        print("10. Move to group")
        print("11. Show all contacts")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            add_phone_menu()
        elif choice == "4":
            search_contacts_menu()
        elif choice == "5":
            filter_by_group()
        elif choice == "6":
            sort_contacts()
        elif choice == "7":
            pagination_loop()
        elif choice == "8":
            export_json()
        elif choice == "9":
            import_json()
        elif choice == "10":
            move_to_group_menu()
        elif choice == "11":
            show_all_contacts()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()