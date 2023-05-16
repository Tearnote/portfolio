# Portfolio: a showcase and commission website

*Portfolio* is a dynamic website showcasing my projects, with commissioning functionality, made for [Code Institute](https://codeinstitute.net/)'s 5th submission project.

A live version is deployed and available [here](https://portfolio.tear.moe).

## Important notes

The documentation is split across three files:

-   [README.md](README.md) (this file): Overview of the project. Read this to get an idea of the basic concept, technologies used and project conventions.
-   [DESIGN.md](doc/DESIGN.md): UX design notes crafted during early stages of development. The design process is described entirely, from the concept and market research, through information structuring to visual design principles and color palettes.
-   [TESTING.md](doc/TESTING.md): Automated and manual testing procedures are described in detail, as well as their outcomes.

## Deployment

*Portfolio* is a Django web-app, and is deployed via the standard Django procedures. A number of settings is exposed via environment variables, some of which must be set for the app to load:

-   `PORTFOLIO_SECRET_KEY`: required. Must be set to any string, as long as it's kept secret. Make sure the key is not present in committed code, logs, etc.
-   `PORTFOLIO_STRIPE_PUBLISHABLE_KEY`, `PORTFOLIO_STRIPE_SECRET_KEY`, `PORTFOLIO_STRIPE_WEBHOOK_SECRET`: set of keys obtained from Stripe. The webhook must be configured under the `/account/webhook/` URL.
-   `PORTFOLIO_EMAIL_HOST`, `PORTFOLIO_EMAIL_USER`, `PORTFOLIO_EMAIL_PASSWORD`, `PORTFOLIO_EMAIL_PORT`: SMTP server details for sending emails through,
-   `PORTFOLIO_POSTGRES_PASSWORD`: password to the Postgres database.

### Deployment example

*Portfolio* can be deployed via a number of methods - to a dedicated server, application platform such as S3 or Heroku, a Docker container, etc. The instance [above](#portfolio-a-showcase-and-commission-website) was deployed to a virtual environment (venv) in a dedicated server. The procedure will be detailed below for reference. Creating accounts on email providers and Stripe are well documented on their own help pages, and outside of the scope of this section.

Prerequisites:

-   Server is running a Linux distribution with systemd,
-   Nginx is installed and running,
-   PostgreSQL is installed and running.

1. Navigate to the destination folder that will store the application, such as `/srv/http`,
2. Clone the repository:
    ```
    git clone https://github.com/Tearnote/portfolio
    ```
3. We need to set up a virtual environment for Python. Enter the cloned project, and create a fresh virtualenv:
    ```
    python -m venv venv
    ```
4. Activate the virtual environment in current shell. This should add `(venv)` to your visible command line:
    ```
    source venv/bin/activate
    ```
5. Dependencies can now be installed with the following command:
    ```
    pip install -r requirements.txt
    ```
6. The dependencies include Gunicorn and Psycopg2, which will be required for a production deployment. Gunicorn will need to be configured separately to match your deployment. An example configuration file is included [here](doc/gunicorn.conf.py). Copy this to the root folder of the project, and customize it with your server's paths.
7. We will now configure the database. *Portfolio* is by default configured to use a Sqlite database file, which is only suitable for a test deployment with few concurrent users. Configure your Postgres connection in `portfolio/settings.py`. An example commented-out configuration is included.
8. The database and user needs to be created on Postgres side. These example commands will configure the database for use, customize them to match your deployment:
    ```
    sudo -u postgres psql
    create database portfolio;
    create user portfolio with password 'portfolio';
    alter role portfolio set client_encoding to 'utf8';
    alter role portfolio set default_transaction_isolation to 'read committed';
    alter role portfolio set timezone to 'UTC';
    grant all privileges on database portfolio to portfolio;
    \q
    ```
9. You should now have all the prerequisites to get the webapp to run. To populate all the environment variables, the definitions can be inserted in the `.env` file in the root of the project.
10. Now, you should be able to connect to the database to create all the required tables. Navigate to the project folder, activate the venv again if needed (step 4.), and run the following commands:
     ```
     python manage.py makemigrations
     python manage.py migrate
     ```
11. Optionally, you might want to configure *Portfolio* as a systemd service so that it's started automatically. An example systemd unit file is available [here](doc/portfolio.service). Customize the file with your credentials and paths, drop it into `/etc/systemd/system/`, and run these commands to reload unit files and start *Portfolio*:
    ```
    sudo systemctl daemon-reload
    sudo systemctl start portfolio
    ```  
    If the unit doesn't start correctly, look for errors in the system journal and the Gunicorn log file as configured in `gunicorn.conf.py` (step 6.)
12. The app is now running, and it's time to expose it to the world via Nginx reverse proxy. This needs to be configured to match your domain name, serving methods and SSL setup, among others. You can find an example Nginx configuration file [here](doc/nginx-portfolio.conf), which needs to be customized with domain names and local paths. The file assumes the app is hosted on `localhost:8002`, which matches the example Gunicorn configuration file.
13. You should be able to view the app via its URL, but the styles and images will not work. For that, static files must be hosted via Nginx. Collect all static files by navigating to the project folder, activating the venv (step 4.), and running the following command:
    ```
    python manage.py portfoliotstatic
    ```  
    This will copy all static files into the `static` folder in the project. The default Nginx configuration will serve these files directly.
