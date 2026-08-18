import os
import sqlite3
import pandas as pd

from database import get_connection


# ==========================================
# CSV FILE LOCATION
# ==========================================

CSV_FOLDER = "csv files"


# ==========================================
# DATABASE TABLE COLUMNS
# ==========================================

def get_table_columns(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    return [column[1] for column in columns]


# ==========================================
# GET PRIMARY KEY
# ==========================================

def get_primary_key(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    for column in columns:
        # column[5] = primary key indicator
        if column[5] == 1:
            return column[1]

    return None


# ==========================================
# MIGRATE ONE CSV FILE
# ==========================================

def migrate_table(csv_file, table_name, conn):

    file_path = os.path.join(CSV_FOLDER, csv_file)

    if not os.path.exists(file_path):
        print(f"⚠️ {csv_file} not found. Skipping {table_name}.")
        return

    try:
        df = pd.read_csv(file_path)

        # Remove completely empty rows
        df = df.dropna(how="all")

        if df.empty:
            print(f"⚠️ {csv_file} is empty. Skipping.")
            return

        cursor = conn.cursor()

        # Get database columns
        db_columns = get_table_columns(cursor, table_name)

        if not db_columns:
            print(f"❌ Table '{table_name}' not found in database.")
            return

        # Keep only columns that exist in both CSV and database
        csv_columns = [
            column for column in df.columns
            if column in db_columns
        ]

        if not csv_columns:
            print(
                f"❌ No matching columns found between "
                f"{csv_file} and {table_name}."
            )
            return

        # Primary key
        primary_key = get_primary_key(cursor, table_name)

        count = 0

        for _, row in df.iterrows():

            columns = csv_columns

            values = []

            for column in columns:

                value = row[column]

                # Convert pandas NaN to None
                if pd.isna(value):
                    value = None

                values.append(value)

            column_names = ", ".join(columns)
            placeholders = ", ".join(["?"] * len(columns))

            # ==========================================
            # INSERT / UPDATE
            # ==========================================

            if primary_key and primary_key in columns:

                query = f"""
                    INSERT OR REPLACE INTO {table_name}
                    ({column_names})
                    VALUES ({placeholders})
                """

            else:

                query = f"""
                    INSERT INTO {table_name}
                    ({column_names})
                    VALUES ({placeholders})
                """

            try:
                cursor.execute(query, values)
                count += 1

            except sqlite3.Error as e:
                print(
                    f"⚠️ Could not migrate row in {csv_file}: {e}"
                )

        conn.commit()

        print(
            f"✅ {table_name.capitalize()} migrated: {count}"
        )

    except Exception as e:
        print(
            f"❌ Error migrating {csv_file}: {e}"
        )


# ==========================================
# MAIN MIGRATION
# ==========================================

def migrate_all():

    print("\n===================================")
    print(" CSV → SQLite Migration")
    print("===================================\n")

    # Check CSV folder
    if not os.path.exists(CSV_FOLDER):
        print(f"❌ Folder '{CSV_FOLDER}' not found.")
        return

    # Connect to database
    conn = get_connection()

    try:

        # ------------------------------------------
        # PRODUCTS
        # ------------------------------------------

        migrate_table(
            "products.csv",
            "products",
            conn
        )

        # ------------------------------------------
        # SALES
        # ------------------------------------------

        migrate_table(
            "sales.csv",
            "sales",
            conn
        )

        # ------------------------------------------
        # CUSTOMERS
        # ------------------------------------------

        migrate_table(
            "customers.csv",
            "customers",
            conn
        )

        # ------------------------------------------
        # SUPPLIERS
        # ------------------------------------------

        migrate_table(
            "suppliers.csv",
            "suppliers",
            conn
        )

    finally:
        conn.close()

    print("\n===================================")
    print("✅ Migration Completed")
    print("===================================\n")


# ==========================================
# RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    migrate_all()