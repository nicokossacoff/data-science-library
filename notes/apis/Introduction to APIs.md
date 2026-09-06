2026-04-24 18:48

Status: #Ongoing 

Tags: [[MLOps]]
***
# Introduction

An **API** (an abbreviation for **Application Programming Interface**) is a set of protocols (i.e., rules) and definitions that applications can use to communicate with one another.
The API defines *what* information can be requested, *how* it should be requested, and which output structure to expect, effectively **standardizing** connections between apps and services.
# Components

1. **API Client.** Responsible for starting the conversation by sending a request to the API. There are multiple ways an API can be trigger. Let's say we are developing a weather app. When the user types a location (via the frontend), it's effectively sending a request to fetch the weather information.
2. **API Request.** An API request can vary depending of the type of API but it always have:
	- **Endpoint.** A dedicated URL that provides access to a specific resource. For example, the `/temperature` endpoint will only provide information about temperature in the specified location, if we want to know the humidity, we might need to send a request to the `/humidity` endpoint.
	- **Method.** Defines the operation the client wants to perform on the resource. The most common type of API, the REST API protocol, uses the HTTP protocol to access information, enabling the client to perform actions like retreiving (`GET`), sharing (`POST`), updating (`PUT`) and deleting (`DELETE`).
	- **Parameters.** Variables passed to an API endpoint for providing specific instructions for the API process. For example, the `/temperature` endpoint might accept a `location` parameter, which could be used to extract the temperature in the user-defined location.
	- **Request Headers.** Key-value pairs used to provide extra details to a request, such as authentication.
	- **Body.** The body is the main part of a request, and includes the data needed to retieve, share, update or delete a resource.
3. **Service.** The API sends the request information to the server, which is in charge of processing and sharing data.
4. **API response.** Finally, the Server sends a response to the Client through the API. An API response usually have:
	- **HTTP Status Code.** A three-digit code that indicates the outcome of an API request.
	- **Response Headers.** Similar to the request headers, but they are used to provide information about the APIs response.
	- **Response Body.** Contains the actual data the Client asked for (or an error message if something went wrong).

Ever single API call has:
- A **request** sent by the user (or app) to another service, asking for information.
- An **endpoint**, which defines a URL path that tells the API which information or action is being requested.
- A **method**, which specifies the type of the request. Usually, there are only four types of requests:
	- `PUT`: used to send data to another application.
	- `GET`: used to fetch data from another application.
	- `PUT`: used to update data in another application.
	- `DELETE`: used to deleter data in another application.
- A **response** containing the result of the request. It usually come in JSON or XML format.
# Benefits

1. APIs define clear and consistent rules on how different systems interact. This makes developing and deploying an application faster.
2. APIs help developers prototype, experiment, and deploy new features by reutilizing services.
3. Improve scalability by splitting an application into smaller, independent services. This makes it easier to scale parts of an app or add new features without compromising the whole system with possible new bugs.
4. They bridge the cap between new and old tech stacks, which helps companies to transform faster and easier.

# Types

1. Based on availability:
	- **Public APIs.** Available to developers outside an organization.
	- **Internal APIs.** Restricted to developers within an organization. Used by organizations to manage data flows and interactions between services.
	- **Partner APIs.** Internal APIs available to some extend to external developers. They often need authentication and have usage limits.
	- **Composite APIs.** This APIs allow to call multiple services at the same time.
2. Based on location:
	- **Web APIs.** Design to work over the internet via the HTTP protocol, these are the most common APIs.
	- **Remote APIs.** Design to communicate software located in different machines or networks.
3. Based on protocols:
	- **REST**. It's a lightweight and flexible protocol that uses the standard HTTP method. This makes REST (Representational State Transfer) the most common API protocol.
	- **SOAP.** It has strict standards for sharing information, and supports more advanced security and controls.
	- **GraphQL.** A query language that enable clients to ask for the data that they need (no more, no less), reducing the amount of information to fetch.

# References