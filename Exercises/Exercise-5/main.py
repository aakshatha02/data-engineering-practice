import psycopg2


def main():
    host = "postgres"
    database = "postgres"
    user = "postgres"
    pas = "postgres"
    conn = psycopg2.connect(host=host, database=database, user=user, password=pas)
    # your code here
    cur = conn.cursor()

    # ------------------------
    # CREATE TABLES & INDEX
    # ------------------------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
                customer_id	INT PRIMARY KEY,
                first_name	VARCHAR(40),
                last_name	VARCHAR(40),
                address_1	VARCHAR(40),
                address_2 	VARCHAR(40),
                city	    VARCHAR(20),
                state	    VARCHAR(20),
                zip_code	VARCHAR(10),
                join_date   DATE
            )
        """)
    cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_accounts_city ON accounts(city)
        """)
    

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
                product_id INT PRIMARY KEY,
                product_code INT,
                product_description VARCHAR(255))
         """)
    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_product_code ON products(product_code)
        """)
    
    cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions(
                transaction_id VARCHAR(50)  PRIMARY KEY,
                transaction_date    DATE,
                product_id  INT,
                product_code VARCHAR(50),
                product_description VARCHAR(255),
                quantity INT,
                account_id INT,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            """)

    # -----------------
    # LOAD DATA
    # -----------------

    with open ('data/accounts.csv', 'r') as f:
        next(f)
        cur.copy_from(f, 'accounts', sep=',', null="")

    with open('data/products.csv', 'r') as f:
        next(f)
        cur.copy_expert('COPY products FROM STDIN WITH CSV', f)

    with open('data/transactions.csv', 'r') as f:
        next(f)
        cur.copy_expert('COPY transactions FROM STDIN WITH CSV', f)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
