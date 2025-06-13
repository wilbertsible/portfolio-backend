# Wilbert Backend API

This is the backend API for my website at

[https://www.wilbertsible.com/]

## Table of Contents

- [About](#about)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage (API Endpoints)](#usage-api-endpoints)
- [Development](#development)
- [Contact](#contact)

## About

This API supports my website. It contains some of the content mapping and project data.


## Features

List the key features and capabilities of your API.

- CRUD operations 
- Data validation
- Error handling with meaningful responses
- MongoDB integration

## Technologies Used

List the main technologies, libraries, and frameworks used in your project.

- Python 3
- Flask
- Flask-restful
- Blueprint
- python-dotenv (for environment variables)
- MongoDB


## Installation

Detailed steps on how to get the development environment set up.

1.  **Prerequisites:**
    * Python 3.8+
    * `pip` (Python package installer)

2.  **Clone the repository:**
    ```bash
    git clone [git@github.com:wilbertsible/portfolio-backend.git]
    cd your-flask-api
    ```

3.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Explain how to configure the API, especially environment variables.

1.  **Create a `.env` file:**
    In the root directory of your project, create a file named `.env`.

    ```dotenv
    # .env example
    MONGO_URI=<your mongo connection uri>
    ```

## Usage (API Endpoints)

This is a crucial section for an API. Document your endpoints clearly.

### Base URL

`http://127.0.0.1:5000/api/v1` (during development)


### User Endpoints (Website)

-   **`GET /api/v1/website/projects`**
    * **Description:** Website project mapping
    * **Success Response (200 OK):**
        ```json
        [
            {
                "_id": {
                    "$oid": "<Mongo-generated id 1>"
                },
                "contentId": 1,
                "title": "My Project 1",
                "bannerImage": "<image link>>",
                "fileName": "MyProject1",
                "is_active": false,
                "tags": [],
                "dateUploaded": "<datetime>",
                "url": "myproject1"
            },
            {
                "_id": {
                    "$oid": "<Mongo-generated id 2>"
                },
                "contentId": 2,
                "title": "My Project 2",
                "bannerImage": "<image link>>",
                "fileName": "MyProject2",
                "is_active": false,
                "tags": [],
                "dateUploaded": "<datetime>",
                "url": "myproject2"
            }
        ]
        ```
-   **`GET /api/v1/website/projects/<url>`**
    * **Description:** Get Specific Project
    * **Success Response (200 OK):**
        ```json
        [
          {
            "_id": {
                "$oid": "<Mongo-generated id>"
            },
            "contentId": 1,
            "title": "My Project 1",
            "bannerImage": "<image link>>",
            "fileName": "MyProject1",
            "is_active": false,
            "tags": [],
            "dateUploaded": "<datetime>",
            "url": "myproject1"
            }
        ]
        ```
-   **`GET /api/v1/social/`**
    * **Description:** Retrieves a specific user by ID.
    * **Path Parameters:** `user_id` (string, UUID)
    * **Success Response (200 OK):**
        ```json
        [
            {
                "_id":"<Mongo-generated id>",
                "name":"Instagram",
                "icon":"Instagram",
                "link": "<Instagram_Link>",
                "is_active":true,
                "socialId":1
            }
        ]
        ```

### User Endpoints (Zinny Plant Monitoring System)

-   **`GET /api/v1/zinny/zinny-data/latest`**
    * **Description:** Zinny Latest Data
    * **Success Response (200 OK):**
        ```json
        [
            {
                "_id": {
                    "$oid": "<Mongo-generated id>"
                },
                "sunlight_level": 0.8670588235294118,
                "temperature": 20.8,
                "humidity": 61,
                "soil_moisture": 63.492063492063494,
                "total_daily_dispensed_water": 0,
                "current_datetime": "2025-06-08 23:20:09.529136"
            }
          
        ]
        ```

-   **`GET /api/v1/zinny/zinny-data`**
    * **Description:** Zinny All Data
    * **Success Response (200 OK):**
        ```json
        [
             {
                "_id": {
                    "$oid": "<Mongo-generated id>"
                },
                "sunlight_level": 0.8670588235294118,
                "temperature": 20.8,
                "humidity": 61,
                "soil_moisture": 63.492063492063494,
                "total_daily_dispensed_water": 0,
                "current_datetime": "2025-06-08 23:20:09.529136"
            }, 
            {
                "_id": {
                    "$oid": "<Mongo-generated id>"
                },
                "sunlight_level": 0.8670588235294118,
                "temperature": 20.8,
                "humidity": 62,
                "soil_moisture": 63.492063492063494,
                "total_daily_dispensed_water": 0,
                "current_datetime": "2025-06-08 23:21:09.708301"
            }
        ]
        ```

-   **`GET /api/v1/zinny/zinny-calibration/latest`**
    * **Description:** Zinny Latest Calibration
    * **Success Response (200 OK):**
        ```json
        [
            {
            "_id": {
                "$oid": "68463339be9bbca139c38e95"
            },
            "date": {
                "$date": "2025-06-08T18:04:57.006Z"
            },
            "slope": -61.32756132756136,
            "y_intercept": 168.2539682539683
            }
        ]
        ```


### Development

```bash
# Ensure your virtual environment is active
flask run
```

### Contact

wilbertsible@gmail.com