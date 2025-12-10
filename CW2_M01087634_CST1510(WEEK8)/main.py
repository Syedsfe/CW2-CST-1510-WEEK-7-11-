from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_services import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents, get_incident_by_id,update_incident,delete_incident,load_cyber_incidents_csv 
from app.data.datasets import get_all_datasets, load_datasets_metadata_csv
from app.data.tickets import  get_all_tickets, load_it_tickets_csv

def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)
    
    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
    
    # 2. Migrating users from users.txt
    migrated=migrate_users_from_file()
    print(f"Migrated {migrated} users from DATA/users.txt")
    
    # 3. Testing authentication
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)

    success, msg = login_user("alice", "SecurePass123!")
    print(msg)
    
    #4a. Load CSV data into cyber_incidents (after fixing loader)
    conn = connect_database()
    loaded_rows = load_cyber_incidents_csv(conn)
    print(f"Loaded {loaded_rows} cyber incidents from CSV")

    # 4. Testing CRUD
    conn = connect_database()

    incident_id = insert_incident(
        conn,
        "Phishing",     # title
        "High",         # severity
        "open",         # status
        "2024-11-05"    # date
    )
    print(f"Created incident #{incident_id}")
    
    #4b updating incident 
    updated = update_incident(conn, incident_id, status="Closed")
    after_update = get_incident_by_id(conn, incident_id)
    print("Update worked:", updated)
    print("Incident after update:", after_update)

    #4c deleting incident 
    deleted_rows = delete_incident(conn, incident_id)
    after_delete = get_incident_by_id(conn, incident_id)
    print("Deleted rows:", deleted_rows)
    print("Incident after delete (should be None):", after_delete)

    #5a. loading datasets csv 
    loaded_datasets = load_datasets_metadata_csv(conn)
    print(f"Loaded {loaded_datasets} datasets from CSV")

    #5b. loading tickets csv 
    loaded_tickets = load_it_tickets_csv(conn)
    print(f"Loaded {loaded_tickets} IT tickets from CSV")

    # 5. Query data
    incidents= get_all_incidents(conn)
    print(f"Total incidents: {len(incidents)}")

    datasets=get_all_datasets()
    print(f"Toatal datasets: {len(datasets)}")

    tickets=get_all_tickets(conn)
    print(f"Total tickets: {len(tickets)}")
    conn.close()

if __name__ == "__main__":
    main()