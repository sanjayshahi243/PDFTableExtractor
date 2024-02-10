# PDFExtractor

PDFExtractor is a Flask-based web application that extracts tables from PDF files. It utilizes Camelot and Celery for PDF processing and asynchronous task execution.

## Table of Contents
- [PDFExtractor](#pdfextractor)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Configuration](#configuration)
    - [Usage](#usage)
    - [Access](#access)

## Features

- Extract tables from PDF files.
- Asynchronous PDF processing using Celery.
- RESTful API for uploading PDF files.

## Getting Started

### Prerequisites

- Python 3.10
- Docker (optional, for containerized deployment)
- Redis (for Celery)
- Ghostscript (for extraction of tables)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/PDFExtractor.git
   ```

### Configuration
Environment variables can be configured in the .env file. A sample of environment variables is available on `env.example`

### Usage

   1. Using virtual-env
       #### Install Prerequisites
       ```bash 
       apt install ghostscript redis-server
       ```
       
       #### All necessary commands are available in run.sh script file.
       ```bash
       sh run.sh
       ```    

       #### Terminate the process
       ```bash 
       sh terminate.sh
       ```
       #### Note: This will kill the process running in port 5000 and 5555 i.e. Flask Application and flower

   2. Using Docker-Compose
      #### Make sure you have docker and Docker-Compose installed. If not, install it using:
      ```bash
       sudo apt-get install docker.io docker-compose
       ```

       #### Create the docker images using the following command
       ```bash
       docker-compose build
       ```
       #### Start the docker containers using the following command
       ```bash
       docker-compose up -d
       ```

       #### Note: The above steps can be done in one step using the following command
       ```bash
       docker-compose up --build -d
       ```

### Access
   - Flask application at http://localhost:5000
   - Flower (Celery monitoring tool) at http://localhost:5555

