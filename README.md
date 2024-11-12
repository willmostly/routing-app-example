# External Routing Group server for Trino Gateway

This gives a simple example of a Flask app for recieving routing information
from Trino Gateway and returning a response containing a Routing Group.

## Usage
First make sure you have Flask installed. For testing with the Flask
development server, run 
```
flask --app getrouting/views.py run
```
from the root of this repository. Do not use the development server in 
production - see Flask documentation for running with a WSGI server.

The devlopment server will expose the app on `localhost:5000`. Set
```
routingRules:
  rulesEngineEnabled: true
  rulesType: EXTERNAL
  rulesExternalConfiguration:
        urlPath: http://localhost:5000/debug-routing-info
```
in your trino gateway configuration to begin interacting with the 
application. If you are in k8s, create a service for the pod and
use the service name instead of `localhost`. The `debug-routing-info`
endpoint prints debug information to the console logs and optionally
saves input for offline testing. The `/get-routing-group` endpoint
will not print debug info.
