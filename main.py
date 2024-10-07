import argparse
import logging
import os
from smart_extract import main as download_all_chapters  # Importing the main function as download_all_chapters

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def main_wrapper():
    # Default values for URL and destination directory
    default_url = "https://vyvymanga.net/manga/hundred-ghost-stories-of-my-own-death"
    default_directory = os.path.expanduser("~/Desktop/100_Ghost_Stories")

    # Argument parser setup
    parser = argparse.ArgumentParser(description="Script to download manga images.")
    parser.add_argument(
        "-u", "--url", 
        default=default_url,
        help=f"URL of the manga page. (Default: {default_url})"
    )
    parser.add_argument(
        "-d", "--directory", 
        default=default_directory,
        help=f"Directory where images will be saved. (Default: {default_directory})"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level to display."
    )

    # Parse arguments
    args = parser.parse_args()

    # Set log level
    logging.getLogger().setLevel(args.log_level)

    # Execute the function to download all chapters
    download_all_chapters(args.directory)

if __name__ == "__main__":
    main_wrapper()
