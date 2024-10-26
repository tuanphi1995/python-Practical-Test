# library_system.py
import mysql.connector
from datetime import datetime

# Kết nối với cơ sở dữ liệu
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Thay 'root' bằng tên người dùng MySQL của bạn
        password="phi",  # Thay 'password' bằng mật khẩu MySQL của bạn
        database="library_system"
    )

# Hàm thêm sách vào cơ sở dữ liệu
def add_book(title, author):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Đã thêm sách '{title}' của tác giả {author} vào cơ sở dữ liệu.")

# Hàm thêm thành viên vào cơ sở dữ liệu
def add_member(name, dob, address):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO members (name, dob, address) VALUES (%s, %s, %s)", (name, dob, address))
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Đã thêm thành viên '{name}' vào cơ sở dữ liệu.")

# Hàm thêm giao dịch mượn sách
def add_transaction(member_id, book_id, borrow_date, status='Đang mượn'):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO transactions (member_id, book_id, borrow_date, status) VALUES (%s, %s, %s, %s)",
        (member_id, book_id, borrow_date, status)
    )
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Đã thêm giao dịch mượn sách cho thành viên ID {member_id} với sách ID {book_id}.")

# Hàm tạo báo cáo và hiển thị lên màn hình
def generate_report():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT members.name, members.dob, members.address, books.title, transactions.borrow_date, transactions.status
        FROM transactions
        JOIN members ON transactions.member_id = members.id
        JOIN books ON transactions.book_id = books.id
    """)

    results = cursor.fetchall()
    print(f"{'STT':<5}{'Tên Thành Viên':<20}{'Ngày Sinh':<15}{'Địa Chỉ':<20}{'Tên Sách':<20}{'Ngày Mượn':<15}{'Trạng Thái':<10}")
    for index, (name, dob, address, title, borrow_date, status) in enumerate(results, start=1):
        print(f"{index:<5}{name:<20}{dob:<15}{address:<20}{title:<20}{borrow_date:<15}{status:<10}")

    cursor.close()
    connection.close()

# Hàm hiển thị các giao dịch trong ngày hôm nay
def show_today_transactions():
    today = datetime.now().date()
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT members.name, books.title, transactions.borrow_date, transactions.status
        FROM transactions
        JOIN members ON transactions.member_id = members.id
        JOIN books ON transactions.book_id = books.id
        WHERE transactions.borrow_date = %s
    """, (today,))

    results = cursor.fetchall()
    print(f"{'STT':<5}{'Tên Thành Viên':<20}{'Tên Sách':<20}{'Ngày Mượn':<15}{'Trạng Thái':<10}")
    for index, (name, title, borrow_date, status) in enumerate(results, start=1):
        print(f"{index:<5}{name:<20}{title:<20}{borrow_date:<15}{status:<10}")

    cursor.close()
    connection.close()

# Hàm hiển thị menu và xử lý lựa chọn
def menu():
    while True:
        print("\n--- Quản Lý Thư Viện ---")
        print("1. Thêm Sách")
        print("2. Thêm Thành Viên")
        print("3. Thêm Giao Dịch Mượn Sách")
        print("4. Xem Báo Cáo Mượn Sách")
        print("5. Xem Giao Dịch Hôm Nay")
        print("0. Thoát")

        choice = input("Chọn một chức năng: ")

        if choice == '1':
            title = input("Nhập tên sách: ")
            author = input("Nhập tên tác giả: ")
            add_book(title, author)

        elif choice == '2':
            name = input("Nhập tên thành viên: ")
            dob = input("Nhập ngày sinh (YYYY-MM-DD): ")
            address = input("Nhập địa chỉ: ")
            add_member(name, dob, address)

        elif choice == '3':
            member_id = int(input("Nhập ID thành viên: "))
            book_id = int(input("Nhập ID sách: "))
            borrow_date = input("Nhập ngày mượn (YYYY-MM-DD): ")
            status = input("Nhập trạng thái (Đang mượn / Đã trả): ")
            add_transaction(member_id, book_id, borrow_date, status)

        elif choice == '4':
            print("\nBáo cáo mượn sách:")
            generate_report()

        elif choice == '5':
            print("\nGiao dịch mượn sách hôm nay:")
            show_today_transactions()

        elif choice == '0':
            print("Thoát chương trình.")
            break

        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

# Khởi chạy menu
if __name__ == "__main__":
    menu()
