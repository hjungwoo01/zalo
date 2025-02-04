# Zalo-Msg-App

## Overview

This FastAPI application provides an API for managing SMS templates and flows. It includes endpoints for adding, retrieving, and deleting templates, as well as creating and retrieving flows. Additionally, it features a cron job system to automatically send SMS messages based on the defined schedules in the flows. A specific flow can also be triggered manually.

## Setup and Running the Project

### Clone the repository

```bash
git clone https://github.com/shahzaib-1997/Zalo-Msg-App
cd Zalo-Msg-App
```

### Install dependencies

First install Python from its official website:

[https://www.python.org/downloads/](https://www.python.org/downloads/)

Now install dependencies using:

```bash
pip install -r requirements.txt
```

### Run the FastAPI application

```bash
uvicorn app:app --reload
```

The application will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Endpoints

### Template Management

#### Add a Template
- **Endpoint:** `/add-template/`
- **Method:** POST
- **Status Code:** 201 (Created)
- **Description:** Adds a new template to the system.
- **Request Body:** 
  - `name` (str): The name of the template.
  - `text` (str): The text content of the template.
- **Response:** 
  - `msg` (str): Confirmation message indicating the template was added successfully.

#### Get All Templates
- **Endpoint:** `/get-templates/`
- **Method:** GET
- **Description:** Retrieves all templates stored in the system.
- **Response:** A list of templates, each with the following fields:
  - `id` (int): The ID of the template.
  - `name` (str): The name of the template.
  - `text` (str): The text content of the template.

#### Delete a Template
- **Endpoint:** `/delete-template/`
- **Method:** DELETE
- **Description:** Deletes a template based on the given ID.
- **Query Parameter:**
  - `id` (int): The ID of the template to be deleted.
- **Responses:**
  - **204 (No Content):** Template deleted successfully.
  - **404 (Not Found):** No template found with the given ID.

### Flow Management

#### Create a Flow
- **Endpoint:** `/create-flow/`
- **Method:** POST
- **Status Code:** 201 (Created)
- **Description:** Creates a new flow in the system.
- **Request Body:**
  - `numbers` (List[str]): A list of recipient's user_id*.
  - `template` (int): The ID of the template to be used in the flow.
  - `auto_run` (bool): Indicates whether the flow should run automatically based on the schedule.
  - `schedule` (dict | None): A dictionary defining the schedule for automatic execution.
- **Response:**
  - `msg` (str): Confirmation message indicating the flow was added successfully.

*user_id = To get the user_id of a user, first open its chat in your official account. Now, the value of uid in the URL is the user_id.

#### Get All Flows
- **Endpoint:** `/get-flows/`
- **Method:** GET
- **Description:** Retrieves all flows stored in the system.
- **Response:** A list of flows, each with the following fields:
  - `id` (int): The ID of the flow.
  - `numbers` (List[str]): A list of recipient phone numbers.
  - `template` (int): The ID of the template used in the flow.
  - `auto_run` (bool): Indicates whether the flow runs automatically.
  - `schedule` (dict | None): The schedule for automatic execution.

#### Run a Flow
- **Endpoint:** `/run-flow/`
- **Method:** POST
- **Description:** Manually trigger the execution of a specific flow.
- **Query Parameter:**
  - `id` (int): The ID of the flow to be run.
- **Responses:**
  - **200 (OK):** Messages sent successfully.
  - **404 (Not Found):** No flow found with the given ID.

#### Delete a Flow
- **Endpoint:** `/delete-flow/`
- **Method:** DELETE
- **Description:** Deletes a flow based on the given ID.
- **Query Parameter:**
  - `id` (int): The ID of the flow to be deleted.
- **Responses:**
  - **204 (No Content):** Flow deleted successfully.
  - **404 (Not Found):** No Flow found with the given ID.

This README provides instructions on setting up and running the project, as well as details on the available API endpoints.