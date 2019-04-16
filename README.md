# REST API in Python Flask implementing JWT access token checks

This is a minimal Python Flask application that implements a REST API that is protected by an JWT access token.

The code builds on Robert Prevato's code on how you validate a JWT from Azure AD

# Reading list

- My [blog post that explains the app](http://www.redbaronofazure.com/?p=7648)
- How do you build a [REST API in Python Flask](http://blog.luisrei.com/articles/flaskrest.html)
- How do I [validate a JWT from Azure AD in Python](https://robertoprevato.github.io/Validating-JWT-Bearer-tokens-from-Azure-AD-in-Python/)
- How do you [define scopes scopes in Azure AD](https://joonasw.net/view/defining-permissions-and-roles-in-aad)

# Debugging the app with VSCode

Install extension Python by Microsoft

# Running the app

Make sure you are running it with Python 3 and not 2

# Deploying

## Deploy to Azure App Services on Linux

Note that the Python support for App Services on Windows is pulled, so you should really use Linux. I've successfully managed to deploy not using containers on App Services. You can either use local git push or pull from github and it is described here - [Deploy to Azure App Service on Linux](https://code.visualstudio.com/docs/python/tutorial-deploy-app-service-on-linux)

## Deploy to Azure Kubernetes Services

I've included a Dockerfile in the repo which I've used to build and run the app as a container on my local laptop. Deploying it to Azure Kubernetes Services would be easy as long as you remember to put AZTENANTID and AZAPPID in a configMap.
