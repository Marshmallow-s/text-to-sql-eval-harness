# sqlite3 是 Python 内置库，不需要安装，直接用
# 它让 Python 能创建和操作 SQLite 数据库
import sqlite3

# os 是 Python 内置的操作系统库
# 让 Python 能处理文件路径
import os

# __file__ = 这个脚本自己的完整路径（不管从哪里运行都不变）
# os.path.dirname(__file__) = 取路径的"目录部分"，去掉文件名
#   例：/Users/emmasun/.../db/setup_db.py → /Users/emmasun/.../db/
# os.path.join(..., "ecommerce.db") = 把目录路径和文件名拼在一起
#   结果：/Users/emmasun/.../db/ecommerce.db
# 效果：ecommerce.db 永远建在跟这个脚本同一个文件夹里
#       不管你从项目根目录还是 db/ 里运行，位置都一样
DB_PATH = os.path.join(os.path.dirname(__file__), "ecommerce.db")


def create_database():
    # 连接数据库：如果 ecommerce.db 不存在就自动创建，存在就直接连上
    conn = sqlite3.connect(DB_PATH)

    # cursor 是"执行 SQL 的光标"，所有 SQL 命令都通过它来执行
    cursor = conn.cursor()

    # executescript 可以一次执行多条 SQL 语句
    # CREATE TABLE IF NOT EXISTS = 表不存在才建，存在就跳过（安全，可重复运行）
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            city        TEXT,
            age         INTEGER,
            gender      TEXT
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id  INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            price       REAL NOT NULL,
            category    TEXT
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id    INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date  TEXT,
            status      TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id      INTEGER NOT NULL,
            product_id    INTEGER NOT NULL,
            quantity      INTEGER NOT NULL,
            price         REAL NOT NULL,
            FOREIGN KEY (order_id)   REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    """)

    # INSERT OR IGNORE = 插入数据，如果 primary key 已经存在就跳过
    # 效果：脚本可以安全地运行多次，不会因为重复数据报错
    cursor.executescript("""
        INSERT OR IGNORE INTO customers VALUES
            (1, 'Alice Chen',  'New York',     28, 'F'),
            (2, 'Bob Smith',   'Chicago',      35, 'M'),
            (3, 'Carol Wang',  'New York',     42, 'F'),
            (4, 'David Lee',   'Los Angeles',  25, 'M'),
            (5, 'Emma Davis',  'Chicago',      31, 'F'),
            (6, 'Frank Kim',   'New York',     29, 'M'),
            (7, 'Grace Liu',   'Seattle',      38, 'F'),
            (8, 'Henry Park',  'Los Angeles',  45, 'M');

        INSERT OR IGNORE INTO products VALUES
            (1, 'Wireless Headphones', 79.99,  'Electronics'),
            (2, 'Running Shoes',       120.00, 'Sports'),
            (3, 'Coffee Maker',        49.99,  'Kitchen'),
            (4, 'Yoga Mat',            35.00,  'Sports'),
            (5, 'Laptop Stand',        45.00,  'Electronics'),
            (6, 'Water Bottle',        25.00,  'Sports'),
            (7, 'Desk Lamp',           39.99,  'Electronics'),
            (8, 'Blender',             65.00,  'Kitchen');

        INSERT OR IGNORE INTO orders VALUES
            (1,  1, '2024-01-15', 'completed'),
            (2,  2, '2024-01-18', 'completed'),
            (3,  1, '2024-02-03', 'cancelled'),
            (4,  3, '2024-02-10', 'completed'),
            (5,  4, '2024-02-14', 'completed'),
            (6,  5, '2024-03-01', 'completed'),
            (7,  2, '2024-03-05', 'refunded'),
            (8,  6, '2024-03-12', 'completed'),
            (9,  7, '2024-03-20', 'completed'),
            (10, 8, '2024-04-01', 'completed');

        INSERT OR IGNORE INTO order_items VALUES
            (1,  1, 1, 1, 79.99),
            (2,  1, 5, 1, 45.00),
            (3,  2, 2, 2, 120.00),
            (4,  3, 3, 1, 49.99),
            (5,  4, 4, 1, 35.00),
            (6,  4, 6, 2, 25.00),
            (7,  5, 7, 1, 39.99),
            (8,  6, 1, 1, 79.99),
            (9,  6, 3, 1, 49.99),
            (10, 7, 8, 1, 65.00),
            (11, 8, 2, 1, 120.00),
            (12, 9, 5, 2, 45.00),
            (13, 10, 4, 1, 35.00),
            (14, 10, 6, 3, 25.00);
    """)

    # commit = 把所有操作正式写入数据库（没有 commit 的话数据不会保存）
    conn.commit()

    # close = 关闭数据库连接，释放资源
    conn.close()

    print(f"Database created at: {DB_PATH}")


# 这一块的意思：只有直接运行这个脚本时才执行 create_database()
# 如果其他脚本 import 这个文件，create_database() 不会自动运行
if __name__ == "__main__":
    create_database()