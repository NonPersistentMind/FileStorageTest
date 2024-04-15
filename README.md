# FastAPI File Storage and Report Generator

## Introduction
This project is a FastAPI application for storing files and generating Excel reports based on uploaded files. It provides endpoints for uploading and downloading files, generating reports, and retrieving top files from the database. It also contains a `test_report_file.py` used to generate random reports in the predetermined format. Check `Random report.txt` to see.

## Installation
### Prerequisites
- `Python 3.10`
- `pipenv`

### Installation Steps
1. Clone the repository:
    ```
    git clone https://github.com/NonPersistentMind/FileStorageTest.git
    ```
2. Navigate to the project directory:
    ```
    cd FileStorageTest
    ```
3. Install dependencies using pipenv:
    ```
    pipenv install
    ```

## Usage
### Development
To run the application in development mode with auto-reload:
```
pipenv run uvicorn main:app --reload
```
> This starts the FastAPI server on http://localhost:8000.

### Deployment
To run the application in production mode:
```
pipenv run uvicorn main:app --host 0.0.0.0 --port 8000
```
> Replace 0.0.0.0 with your server's IP address if needed. This will start the FastAPI server on port 8000.


## Endpoints

### Upload File
* **Method:** POST
* **URL:** `/files`
* **Description:** Uploads a file to the root directory in the database.
* **URL:** `/files/{dir_name}`
* **Description:** Uploads a file to the specified directory in the database.

### Retrieves File
* **Method:** GET
* **URL:** `/files/{id}`
* **Description:** Retrieves the file from the database by its id

### Retrieve Top Files Info
* **Method:** GET
* **URL:** `/top`
* **Description:** Retrieves info about the top 10 files in descending order from all directories.
* **Method:** GET
* **URL:** `/top/{dir_name}`
* **Description:** Retrieves info about the top 10 files in descending order from the specified directory.

### Generate Report
* **Method:** GET
* **URL:** `/report/{id}`
* **Description:** Generates an Excel report based on the specified file ID.

### Get File's Metadata
* **Method:** HEAD
* **URL:** `/files/{id}`
* **Description:** Retrieves the specified file's metadata: name, size, last modified
