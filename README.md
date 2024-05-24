# Website Parsing Project

This project is designed for parsing a website and downloading data in various formats. The scripts are written in Python 3.

## Description

The project contains two scripts:
1. **download_mp4.py** - for downloading video files in MP4 format.
2. **download_csv.py** - for downloading data in CSV format.

## Requirements

Before running the scripts, you need to install the dependencies listed in `requirements.txt`.


## Installation and Using

1. Clone the repository:
   ```bash
   git clone https://github.com/Dasifue/VideoParsing
   ```
2. Go into project folder
   ```bash
   cd VideoParsing
   ```
3. Install all requirements

    ```bash
    pip install -r requirements.txt
    ```
4. Type command for creating `motionelements.csv`. In this file will be all links for each video.
    ```bash
    python download_csv.py
    ```
5. Type command for downloading mp4 files (before type command create folder named `media` in project folder)
    ```bash
    python download_mp4.py
    ```

## Requirements
* aiohttp
* aiofiles
* aiocsv