import os
from arcgis.gis import GIS, UserManager, Group
import requests
import csv
from urllib.parse import quote
import logging
import datetime
import shutil
from email.message import EmailMessage
import smtplib
from cryptography.fernet import Fernet

# Get current date-time group (DTG)
dtg = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Setup logging with DTG in filename
log_file = fr"/path/to/log/migration_log_{dtg}.txt"  # <--- Update this path
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Function to generate and store encryption key (run once and store the key securely)
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load the encryption key
def load_key():
    return open("/path/to/secret.key", "rb").read()  # <--- Update this path

# Function to encrypt the password (run once to store the encrypted password)
def encrypt_password(password):
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

# Function to decrypt the password
def decrypt_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Initialize GIS object and UserManager
gis = GIS("home")
um = UserManager(gis)

# Decrypt and use the password
my_pw_encrypted = b'your-encrypted-password'  # <--- Replace with your encrypted password
my_pw = decrypt_password(my_pw_encrypted)

# Function to get all users based on specified user types
def get_users(gis):
    um = UserManager(gis)
    viewers = um.search(user_type="Viewer", max_users=10000)
    editors = um.search(user_type="editorUT", max_users=10000)
    fieldworkers = um.search(user_type="fieldWorkerUT", max_users=10000)
    logging.info("Fetched all users")
    return viewers + editors + fieldworkers

# Function to extract username from different formats
def get_username(fqUsername):
    if fqUsername is None:
        return None
    if "\\" in fqUsername:
        return fqUsername.split("\\")[1]
    elif "@" in fqUsername:
        return fqUsername.split("@")[0]
    else:
        return fqUsername

# Function to find duplicate user accounts
def users_with_duplicate_accounts(all_users):
    duplicates = []
    for user in all_users:
        if user not in duplicates and all_users.count(user) > 1:
            duplicates.append(user)
    logging.info("Identified users with duplicate accounts")
    return duplicates

# Function to parse first and last names from a full name
def parse_first_last_names(fullName):
    try:
        first = fullName.split(', ')[1]
        last = fullName.split(', ')[0]
    except IndexError:
        return ['', '']
    return [first, last]

# Function to generate a portal token
def portal_token():
    my_user = r"your_username"  # <--- Update this with your username
    url = r"https://your-portal-url/arcgis/sharing/rest/generateToken"  # <--- Update this URL
    params = {'username': my_user, 'password': my_pw, 'client': 'referer', 'referer': r"https://your-referer-url", 'f': 'json'}  # <--- Update referer
    response = requests.post(url, params)
    logging.info("Generated portal token")
    return response.json()["token"]

# Function to log successful migrations
def log_migration(old_gs, new_gs, old_idp, new_idp):
    migration_csv = fr"/path/to/output/geostate_user_migration_{dtg}.csv"  # <--- Update this path
    with open(migration_csv, 'a', newline='') as log:
        writer = csv.writer(log)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([old_gs, new_gs, old_idp, new_idp, timestamp])
    logging.info(f"Logged migration for user {old_gs} to {new_gs} at {timestamp}")

# Function to log failed migrations
def log_failure(username, exception):
    failure_csv = fr"/path/to/output/failed_to_migrate_{dtg}.csv"  # <--- Update this path
    with open(failure_csv, 'a', newline='') as log:
        writer = csv.writer(log)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([username, exception, timestamp])
    logging.error(f"Logged failure for user {username}: {exception} at {timestamp}")

# Create folder and copy CSV files
def create_folder_and_copy_files():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    year = now.strftime("%Y")
    month_number = now.strftime("%m")
    month_name = now.strftime("%B")

    folder_path = fr"/path/to/output/User Migration/{year}/{month_number}. {month_name}/{date_str}"  # <--- Update this path
    os.makedirs(folder_path, exist_ok=True)

    source_files = [
        fr"/path/to/output/geostate_user_migration_{dtg}.csv",  # <--- Update this path
        fr"/path/to/output/failed_to_migrate_{dtg}.csv"  # <--- Update this path
    ]

    for file in source_files:
        shutil.copy(file, folder_path)

    logging.info(f"Created folder {folder_path} and copied files")

# Send email with attachments
def send_email():
    bodyLine1 = (
        "Attached are the most recent reports generated by the GeoState migration scripts. Please review the list and clean up old accounts.\n\n"
    )
    subjString = "GeoState User Migration Report"

    smmFrom = "your-email@example.com"  # <--- Update this email
    SMTPMailRecpts = [
        "recipient1@example.com",  # <--- Add recipients
        "recipient2@example.com"
    ]
    smmSvr = "your-smtp-server.com"  # <--- Update this SMTP server

    msg = EmailMessage()
    msg['From'] = smmFrom
    msg['To'] = ', '.join(SMTPMailRecpts)
    msg['Subject'] = subjString
    msg.set_content(bodyLine1)

    csv_files = [
        fr"/path/to/output/geostate_user_migration_{dtg}.csv",  # <--- Update this path
        fr"/path/to/output/failed_to_migrate_{dtg}.csv"  # <--- Update this path
    ]

    for file in csv_files:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(file)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP(smmSvr) as server:
        server.send_message(msg)
    print("Email sent successfully with attachments.")

# Send email after completing the main script operations
send_email()
