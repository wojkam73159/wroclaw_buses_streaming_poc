# wroclaw_buses_streaming_poc: Azure Function App for Real-Time Event Streaming
## Overview

This Azure Function App is designed to periodically download CSV data from a public API and publish the data to an Azure Event Hub for further processing. The function is triggered every 5 minutes using a timer trigger and uses Azure Key Vault to securely retrieve the Event Hub connection string. The CSV data is converted to JSON format and streamed to the Event Hub, enabling real-time event processing.
Steps:

    Download CSV Data:
        The function fetches the latest CSV data from a public API endpoint using an HTTP GET request.

    Convert CSV to JSON:
        The CSV content is parsed, converted into a list of JSON messages, and prepared for streaming.

    Secure Event Hub Connection:
        The connection string for Azure Event Hub is securely retrieved from Azure Key Vault using the DefaultAzureCredential for authentication.

    Stream Data to Event Hub:
        The JSON data is batched and sent to the specified Event Hub for real-time processing and integration into downstream systems.

    Function Scheduling:
        The Azure Function runs every 5 minutes using a cron-like schedule, ensuring that data is continuously ingested and processed.

## Tech Stack:

    Azure Functions: Serverless compute service that executes the function on a timer trigger.
    Azure Event Hub: Streaming platform used to ingest and distribute real-time data.
    Azure Key Vault: Securely stores sensitive information, such as the Event Hub connection string.
    Azure Identity: Provides authentication and authorization for accessing Key Vault secrets.
    Python AsyncIO: Handles asynchronous requests and streaming for efficient data processing.
    HTTP Requests: Retrieves CSV data from the public API.
