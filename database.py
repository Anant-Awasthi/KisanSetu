import sqlite3

def init_db():
    conn = sqlite3.connect("kisansetu.db")
    cursor = conn.cursor()
    
    # Create farmers mock table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mock_aadhaar_token TEXT UNIQUE,
            phone_number TEXT,
            farmer_name TEXT,
            state TEXT,
            land_holding_acres REAL,
            pm_kisan_status TEXT,
            last_installment_date TEXT,
            pending_reason TEXT
        )
    ''')
    
    # Insert synthetic demo data (No real personal numbers)
    cursor.execute('''
        INSERT OR IGNORE INTO farmers 
        (mock_aadhaar_token, phone_number, farmer_name, state, land_holding_acres, pm_kisan_status, last_installment_date, pending_reason)
        VALUES 
        ('MOCK-AADHAAR-1001', '9876543210', 'Ramesh Kumar', 'Uttar Pradesh', 2.5, 'Active - 12th Installment Credited', '2026-07-15', 'None'),
        ('MOCK-AADHAAR-1002', '9123456789', 'Sita Devi', 'Bihar', 1.8, 'Pending e-KYC Verification', '2026-01-10', 'Aadhaar-Bank linking pending')
    ''')
    
    conn.commit()
    conn.close()

def query_farmer_by_token(identifier: str):
    conn = sqlite3.connect("kisansetu.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT farmer_name, state, pm_kisan_status, last_installment_date, pending_reason 
        FROM farmers 
        WHERE mock_aadhaar_token = ? OR phone_number = ?
    ''', (identifier, identifier))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "name": row[0],
            "state": row[1],
            "status": row[2],
            "last_payment": row[3],
            "pending_reason": row[4]
        }
    return None

if __name__ == "__main__":
    init_db()
    print("KisanSetu mock SQLite database created successfully.")