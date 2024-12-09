<div align="center">
  <h1><b>NOVA MICROSERVICE BASE ARCHITECTURE</b></h1>
  <h4>A base architecture for building microservice using fastapi</h4>
</div>

## 📗 Table of Contents

- [📖 About the Project](#about-project)
  - Repository structure for building microservice using fastapi for the nova project.
    - [👀 Overview](#overview)
      - The repository is already integrated with redis, kafka and postgres.
    - [🛠 Built With](#built-with)
      - Python
      - Poetry
      - Docker
      - Docker Compose
      - [🔥 Tech Stack](#tech-stack)
        - FastApi
        - Postgres
        - Redis
        - Kafka
      - [🔑 Key Features](#key-features)
        - Factory Design Pattern
        - Decorator Pattern
        - Clean Code Approach
        - Model View Controller (MVC) Design Pattern
- [💻 Getting Started](#getting-started)
  - [📜 Prerequisites](#prerequisites)
    - python3
    - python3-venv
    - poetry
    - postgres
    - redis
    - kafka
    - docker
    - docker-compose
    - git
  - [⚓ Install](#setup)
    - install the various tools listed under prerequisite on your local machine
    - for instructions on how to install and set up these tools, please check their websites for directions
  - [⚙️ Setup](#install)
    - from your terminal, navigate to your preferred directory location on your machine
    - clone the repository into a directory of your choice
    - navigate into this directory
  - [▶️ Run Application](#run-application)
    - without docker:
      - create a virtual environment and activate it by executing below commands
        - for linux, run
          1. `python3 -m venv venv`
          2. `source venv/bin/activate`
        - for windows, run
          1. `python3 -m venv venv`
          2. `venv\Scripts\activate`
      - with the virtual environment activated, run blow commands to install dependencies
          1. `poetry install`
      - after installing dependencies, run below command to start application
          1. `  `
    - with docker:
      - run below command:
        - `docker-compose up`
  - [🕹️ Usage](#usage)
    - access application on http://localhost:8000
    - test endpoint from swagger documentation
  - [💯 Run tests](#run-tests)
    - To run the unit tests cases
      - set env variable FASTAPI_CONFIG to 'testing'
    - run below command
      - `pytest -v`
  - [🚀 Deployment](#triangular_flag_on_post-deployment)
    - TODO
- [👥 Author](#author)
  - Michael Asumadu
    - email ✉️ : michaelasumadu10@gmail.com
    - country 🌍 : Ghana 🇬🇭
