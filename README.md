# REST API in Python Flask implementing JWT access token checks

This is a minimal Python Flask application that implements a REST API that is protected by an JWT access token.

The code builds on Robert Prevato's code on how you validate a JWT from Azure AD

## Reading list

- My [blog post that explains the app](http://www.redbaronofazure.com/?p=7648)
- How do you build a [REST API in Python Flask](http://blog.luisrei.com/articles/flaskrest.html)
- How do I [validate a JWT from Azure AD in Python](https://robertoprevato.github.io/Validating-JWT-Bearer-tokens-from-Azure-AD-in-Python/)
- How do you [define scopes scopes in Azure AD](https://joonasw.net/view/defining-permissions-and-roles-in-aad)

## Debugging the app with VSCode

Install extension Python by Microsoft

## Running the app

Make sure you are running it with Python 3 and not 2

## Deploying

### Deploy to Azure App Services on Linux

Note that the Python support for App Services on Windows is pulled, so you should really use Linux. I've successfully managed to deploy not using containers on App Services. You can either use local git push or pull from github and it is described here - [Deploy to Azure App Service on Linux](https://code.visualstudio.com/docs/python/tutorial-deploy-app-service-on-linux)

### Deploy to Azure Kubernetes Services

I've included a Dockerfile in the repo which I've used to build and run the app as a container on my local laptop. Deploying it to Azure Kubernetes Services would be easy as long as you remember to put AZTENANTID and AZAPPID in a configMap.

## Testing the app

### Azure AD

#### Create an app for the REST API

Register an Azure AD app for the REST API. Edit the Manifest and do the following changes
- Change the oauth2AllowImplicitFlow value to true
- add two entries under oauth2Permissions. Make sure to generate two new guids for the Id values.

  {
      "adminConsentDescription": "Allow write access to REST API",
      "adminConsentDisplayName": "Write access to REST API",
      "id": "32c36471-df47-4df9-8416-69f6f66529ca",
      "isEnabled": true,
      "type": "User",
      "userConsentDescription": "Allow write access to REST API",
      "userConsentDisplayName": "Write access to REST API",
      "value": "Api.Write"
    },
    {
      "adminConsentDescription": "Allow read access to REST API",
      "adminConsentDisplayName": "Read access to REST API",
      "id": "4ea0f2d4-fab2-4268-a682-ed6a22712777",
      "isEnabled": true,
      "type": "User",
      "userConsentDescription": "Allow read access to REST API",
      "userConsentDisplayName": "Read access to REST API",
      "value": "Api.Read"
    }

#### Create an app for the caller

Register a seconds Azur AD application to represent the caller. In the Required permisions section, press +Add and in Select an API and select your REST API and add the Api.Read/Api.Write.
Make sure you press "Grant Permissions" before you close out.

In the Reply URLs, add an entry for https://www.getpostman.com/oauth2/callback

In the Keys section, generate a key

### Test with Postman

In Authorization > Get New Access Token, add the following values

Grant Type = Authorization Code
Callback = https://www.getpostman.com/oauth2/callback
Auth URL = https://login.microsoftonline.com/your-azuread-tenant-guid/oauth2/authorize?resource=appid-of-restapi
Access Token URL = https://login.microsoftonline.com/your-azuread-tenant-guid/oauth2/token
Client ID = appid-of-your-caller-app
Client Secret = key from caller app
Scope = openid
State = any random goo
Client Authentication = Send as Basic Auth header
