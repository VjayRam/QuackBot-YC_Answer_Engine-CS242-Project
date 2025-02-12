# PyElastic Setup

## Overview
This project involves setting up an Elastic server using Docker Compose, connecting to the server, indexing and loading data, and making general queries to retrieve data.

## Prerequisites
- Docker and Docker Compose installed on your machine.

## Getting Started

### Launch Elastic Server
To launch the Elastic server, use the provided Docker Compose file. Run the following command in your terminal:
```sh
docker-compose up -d
```

### Install Dependencies
Make sure you have all the necessary Python dependencies installed. Run the following command in your terminal:
```sh
pip install -r requirements.txt
```

### Sample Output of `SearchQuery.py` file:

```json
{
    "company_id": 30338,
    "company_name": "CopyCat",
    "short_description": "Screen recordings to automated workflows.",
    "long_description": "CopyCat allows you to record your screen and turn that task into an automation using AI.",
    "batch": "W25",
    "status": "Active",
    "tags": ["b2b", "workflow-automation", "ai"],
    "location": "Seattle, WA",
    "country": "US",
    "year_founded": 2024,
    "num_founders": 3,
    "founders_names": ["Abhi Balijepalli", "Zyad Elgohary", "Graham Sabin"],
    "team_size": 3,
    "website": "https://runcopycat.com",
    "cb_url": "",
    "linkedin_url": "https://www.linkedin.com/company/copycat-ai/",
    "image_urls": ["URL1", "URL2", "URL3"]
}
