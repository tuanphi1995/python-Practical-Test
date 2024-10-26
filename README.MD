CODE SQL TẠO DATABASE

CREATE DATABASE library_system;
USE library_system;

-- Tạo bảng members để lưu thông tin thành viên
CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    address VARCHAR(100)
);

-- Tạo bảng books để lưu thông tin sách
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100)
);

-- Tạo bảng transactions để lưu thông tin mượn trả sách
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    book_id INT,
    borrow_date DATE,
    return_date DATE,
    status ENUM('Đang mượn', 'Đã trả'),
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);
