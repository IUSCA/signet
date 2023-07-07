<p align="center">
<img src="docs/assets/signet-logo.png" alt="signet-logo" width="50%"/>
</p>


Set Flask and Authlib environment variables:

```bash
# disable check https (DO NOT SET THIS IN PRODUCTION)
$ export AUTHLIB_INSECURE_TRANSPORT=1
```

Create Database and run the development server:

```bash
$ docker compose up -d
$ flask run
```