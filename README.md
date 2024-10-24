# User-Migration-Script
The script is used for automating the migration of users in ArcGIS Enterprise. It only does viewers accounts, as creator accounts should be handled manually due to group ownership. You will run the scripts in order of the numbering in the title. Additionally, keep the csv files as placeholders for the script. 

---

### **Description:**
The script is used for automating the migration of users in ArcGIS Enterprise. It performs several tasks such as fetching users, identifying duplicates, checking for existing accounts, migrating users to the correct user type and groups, logging successful and failed migrations, and sending email notifications with CSV reports.

### **Key Features:**
- **User Migration**: Automatically identifies and migrates users from one domain to another (e.g., from "idpUsername" to "STATE").
- **Handling Duplicate Accounts**: Detects duplicate user accounts and processes them accordingly.
- **Logging**: Logs every migration or failure in CSV files for auditing and tracking.
- **Email Notifications**: Sends reports via email once migrations are completed.
- **Encryption**: Uses encryption to secure sensitive information like user passwords.

### **What the Script Can Do:**
1. **Fetch Users**: Retrieves ArcGIS users of specified types (e.g., Viewer, Editor, FieldWorker).
2. **Duplicate Handling**: Detects and processes duplicate accounts.
3. **Migration**: Migrates user accounts, including roles, licenses, and group memberships.
4. **Logging**: Logs successful and failed migrations in CSV files.
5. **Email Reports**: Sends out email reports with attached CSV logs of the migration process.

### **What the Script Can't Do:**
1. **Manual Handling for Creators**: The script only processes certain user types (e.g., Viewers, Editors) and does not handle Creators, which must be done manually.
2. **Non-Interactive Password Encryption**: Password encryption needs to be handled outside the script (using the `generate_key()` function once, and manually updating the encrypted password in the script).
3. **No Automatic Retry for Failures**: If a migration fails, the script logs the failure but doesn't retry automatically.

### **Prerequisites:**
- **ArcGIS Enterprise Access**: The script uses the `arcgis.gis` module to interact with ArcGIS Enterprise, so appropriate permissions are required.
- **Python Libraries**: Requires the `arcgis`, `cryptography`, `requests`, `logging
