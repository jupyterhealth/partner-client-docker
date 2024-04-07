
# chcs-partner-client-docker

This repository hosts the Dockerized version of the `chcs-partner-client`, specifically designed to streamline testing and interaction with the CommonHealth Cloud Storage (CHCS) service. This tool is ideal for developers and testers looking for an easy way to integrate and interact with CHCS.

## Overview

The `chcs-partner-client` in Docker facilitates seamless integration with CHCS, leveraging a local SQLite-based delegate. This approach simplifies the management of encryption keys, patient ID mapping, and other essential metadata, ensuring a robust and secure interaction with CHCS.

## Full Package on Pypi
- For a broader integration into new or existing Python applications, consider using the [commonhealth-cloud-storage-client](https://pypi.org/project/commonhealth-cloud-storage-client/) Python package hosted on Pypi.org.
- This package is a comprehensive library designed to facilitate interaction with the CommonHealth Cloud Storage Service, allowing developers to seamlessly integrate CHCS functionalities into their Python applications. 

## Prerequisites

Before using the CHCS Partner Client, you need to ensure you have the following:

- **Partner ID**: A unique identifier for your organization, provided by CHCS upon registration.
- **API Client ID**: A unique identifier for your application, used to authenticate requests.
- **API Client Secret**: A secret key used alongside the API Client ID for secure authentication.

You must be registered with CHCS service to obtain these credentials.

## Setup and Configuration

### Environment Variables

Before starting the service, configure the necessary environment variables based on information received from CHCS service registration. These variables are crucial for setting up database connections, authentication details, and other required configurations. Refer to the `dev.env.sample` file for an example.

### Building and Running the Container

After cloning the repository, you can build and run the Docker container using the following commands:

```
docker build -t chcs-partner-client-docker:latest .
```

### Passing Environment Variables

When running the Docker container, use the `--env-file` option to pass the environment variables:

```
docker run -it --env-file dev.env --name chcs-partner-client-docker chcs-partner-client-docker:latest
```

## Usage

Once the service is running locally, you can execute the following sample CLI commands directly in the container's terminal:

### Initialization

```
python app.py initialize
```

### Generating a Deep Link
- Each deeplinks is specific to a given user adn should not be re-used with other users.
```
python app.py create-deeplink --patient-id "stable identifier for a given patient. This can be a hash of an actual patient ID"
```

Refer to `sample_deeplink.txt` for an example of a Deep Link.

### Fetching Encrypted Records
- The returned `patient_data` is a list of `ResourceHolder` objects. Access the raw, plaintext JSON through the `json_content` property on each `ResourceHolder`.
- The default is to visually logout the patient record in `patient_data`. This can be adjusted in the fetch_patient_data function of `src/app.py`.
```
python app.py fetch-data --patient-id "Patient_ID"
```

### Updating Partner Client Name and Logo
- After initialization is complete you can update the partner client name and logo that will be displayed in the CommonHealth app:

```
python app.py initialize --update-name "Partner Name" --update-logo "https://yourwebsite.com/logo.png"
```
## License

- This project is licensed under the terms of the LICENSE file located in the root directory. For more details, see [LICENSE](LICENSE).
