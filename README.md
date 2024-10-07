
# 100 Ghost Stories Manga Downloader

This project is a script designed to download all chapters of the manga "100 Ghost Stories of My Own Death" from VyvyManga. It uses `selenium` to navigate through the website, extract chapter URLs, and download images from each chapter.

## Features
- Downloads all chapters from the manga's page.
- Saves all images from each chapter to a local directory.
- Customisable logging level to track progress and debug issues.

## Important Note
Please note that Chapter 63 is missing, as well as Chapters 89 to 100. This is based on the content available on [VyvyManga](https://vyvymanga.net/manga/hundred-ghost-stories-of-my-own-death).

## Requirements

- Python 3.x
- Google Chrome browser
- `chromedriver` installed and added to your system's PATH.
- A UK VPN is recommended for accessing and extracting the manga content without restrictions.

## Installation

1. Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Make sure `chromedriver` is installed and accessible. You can download it from [here](https://sites.google.com/chromium.org/driver/).

## Usage

Run the main script to start downloading the manga images. You can specify the URL and directory to save the images or use the default values.

### Command

```bash
python3 main.py -d ~/Desktop/100_Ghost_Stories -u https://vyvymanga.net/manga/hundred-ghost-stories-of-my-own-death
```

This command will download all manga chapters to `~/Desktop/100_Ghost_Stories`.

## Project Structure

- `main.py`: The main wrapper script to handle command-line arguments and trigger the download process.
- `smart_extract.py`: Contains the logic for extracting and downloading the manga images from the provided URL.
- `requirements.txt`: List of required Python packages.

## License

This project is licensed under the MIT License.
