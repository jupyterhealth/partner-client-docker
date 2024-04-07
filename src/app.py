import argparse
import logging
from sqlite_delegate import SQLiteDelegate
from client import CHClient
from errors import UserNotConsented, DelegateStateError, HTTPError
from settings import (PATH_TO_DB_FILE, DB_PASSPHRASE, DB_PASSPHRASE_SALT,
                      AUTH_URL, SERVER_HOST, SERVER_PORT, SERVER_SCHEME, 
                      PARTNER_ID, CLIENT_ID, CLIENT_SECRET, PARTNER_NAME,
                      PARTNER_LOGO, DEFAULT_SCOPE, DEFAULT_EXPIRATION_TIME)

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 
handler = logging.StreamHandler()
logger.addHandler(handler)

class AppInitializer:
    def __init__(self):
        self.delegate = SQLiteDelegate(
            path_to_db_file=PATH_TO_DB_FILE,
            db_passphrase=DB_PASSPHRASE,
            db_passphrase_salt=DB_PASSPHRASE_SALT,
            logger=logger
        )
        self.delegate.initialize()
        logger.info("SQLiteDelegate initialized successfully.")

        self.ch_client = CHClient(
            CLIENT_ID,
            CLIENT_SECRET,
            PARTNER_ID,
            self.delegate,
            AUTH_URL,
            SERVER_HOST,
            SERVER_PORT,
            SERVER_SCHEME
        )
        
    def perform_initialization(self,partner_name, partner_logo,clear_existing_signing_keys):
        self.ch_client.perform_initialization(partner_name, partner_logo,clear_existing_signing_keys)
        logger.info("CHClient initialized successfully.")

    def create_deeplink(self, patient_id: str) -> str:
        deeplink = self.ch_client.construct_authorization_request_deeplink(
            patient_id, DEFAULT_SCOPE, DEFAULT_EXPIRATION_TIME)
        logger.info(f"Deeplink: {deeplink}")

    def fetch_patient_data(self, patient_id):
        try:
            patient_data = self.ch_client.fetch_data(patient_id)
            logger.info(f"Patient first record: {patient_data[0].json_content}")
        except UserNotConsented:
            logger.info("Patient not consented.")
        except DelegateStateError:
            logger.warning("Delegate state error.")
        except HTTPError as e:
            logger.error(f"HTTP error with status code: {e.status_code}")
        except Exception as e:
            logger.error(f"Error fetching patient data: {e}")


def main():
    parser = argparse.ArgumentParser(description="Partner Client Command Line Interface")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create subparser for each command
    parser_initialize = subparsers.add_parser('initialize', help='Initialize the system')
    parser_deeplink = subparsers.add_parser('create-deeplink', help='Create a deeplink')
    parser_fetch = subparsers.add_parser('fetch-data', help='Fetch patient data')

    # Clearing and Creating New Signing Keys (Debug purposes only)
    parser_initialize.add_argument('--clear-keys', type=bool, default=False, required=False, help='Clear and create new signing keys')
    
    # Update Name and Logo
    parser_initialize.add_argument('--update-logo', type=str, required=False, help='Update partner logo')
    parser_initialize.add_argument('--update-name', type=str, required=False, help='Update partner name')

    # Adding patient-id as required for specific commands
    parser_deeplink.add_argument('--patient-id', type=str, required=True, help='Patient ID for creating a deeplink')
    parser_fetch.add_argument('--patient-id', type=str, required=True, help='Patient ID for fetching data')

    args = parser.parse_args()
    initializer = AppInitializer()
    try:
        if args.command == 'initialize':
            # Use the provided arguments or default settings
            partner_name = args.update_name if args.update_name else PARTNER_NAME
            partner_logo = args.update_logo if args.update_logo else PARTNER_LOGO
            clear_keys = args.clear_keys if args.clear_keys else False
            initializer.perform_initialization(partner_name, partner_logo, clear_keys)
        elif args.command == 'create-deeplink':
            initializer.create_deeplink(args.patient_id)
        elif args.command == 'fetch-data':
            initializer.fetch_patient_data(args.patient_id)
        else:
            parser.print_help()
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
