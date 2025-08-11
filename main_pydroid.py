import os
import glob
from processors.WalletProcessor import WalletProcessor
from utils.LoggingStream import setup_logger

def get_most_recent_file(directory):
    files = glob.glob(os.path.join(directory, '*'))
    if not files:
        return None  # No files in the directory
    most_recent = max(files, key=os.path.getmtime)
    return most_recent

setup_logger()

directory_path = "C:\\Users\\Stefano\\Documents\\MEGA\\MegaSync_Pixel"
most_recent_file = get_most_recent_file(directory_path)
print(f"Most recent file: {most_recent_file}")
main_wallet_selection = True  # False

start_date = "2016-01-01"
end_date = "2025-06-30"

wallet_processor = WalletProcessor(input_filename=most_recent_file,
                                   main_wallet_selection=main_wallet_selection,
                                   start_date=start_date,
                                   end_date=end_date
                                   )
wallet_processor.execute()
