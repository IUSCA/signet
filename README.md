<p align="center">
<img src="docs/assets/signet-logo.png" alt="signet-logo" width="50%"/>
</p>


### Set Flask and Authlib environment variables:

```bash
# disable check https (DO NOT SET THIS IN PRODUCTION)
$ export AUTHLIB_INSECURE_TRANSPORT=1
```

### Create Database and run the development server:

```bash
$ docker compose up -d
$ flask run
```

### Create a new client

- replace $APP with app name. Ex: `client_name: app_download`
- replace $APP_HOSTNAME with hostname of where app is deployed. Ex: `client_uri: app.company.com`
- run the below command in the host where Signet is running. Adjust the IP to the ip of the docker container running the Signet server

```bash
curl --request POST \
  --url http://172.19.1.2:5001/create_client \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data client_name=$APP_download \
  --data scope=scope1\ scope2 \
  --data client_uri=$APP_HOSTNAME \
  --data token_endpoint_auth_method=client_secret_basic \
  --data grant_type=client_credentials
```


### Get Token Signing Public Keys (JWKS)

```bash
curl --request GET \
  --url https://<hostname>/oauth/jwks
```