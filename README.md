# StarkAdvisor
# StarkAdvisor Backend

This README explains how to install and configure the Django backend `StarkAdvisorBackend` in both development and production environments, following the multi-settings structure located in `starkadvisorbackend/settings/`.

## Quick Overview
- Project: Django (multi-settings structure: `base.py`, `local.py`, `production.py`).
- Default configuration in `manage.py` points to `starkadvisorbackend.settings.local`.
- The project uses environment variables managed with `django-environ`.
- The repository includes a `Pipfile`/`Pipfile.lock`, but `requirements.txt` may also be used.

## Prerequisites
- Python 3.11+
- Git
- (Optional) Docker / Docker Compose for services such as PostgreSQL and Redis

## Configuration Files
- `starkadvisorbackend/settings/base.py` — common settings (environment, MONGO, DRF, installed apps, etc.).
- `starkadvisorbackend/settings/local.py` — development settings (DEBUG=True, default local DB, open CORS, dev middleware).
- `starkadvisorbackend/settings/production.py` — production settings (DEBUG=False, HTTPS, PostgreSQL, Redis, logging, `STATIC_ROOT`, `MEDIA_ROOT`).

These settings read environment variables via `environ.Env()`.  
Key variables (define them in a `.env` file or in the system environment):

- `SECRET_KEY` (required in production)
- `DEBUG` (True/False)
- `ALLOWED_HOSTS` (comma-separated)
- Database (Postgres): `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- Redis: `REDIS_URL` or `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`
- Mongo: `MONGO_URI` or `MONGO_NAME`, `MONGO_HOST`, `MONGO_PORT` (if `MONGO_URI` exists, it takes precedence)
- Optional chatbot variables: `FAQ_PATH`, `FAQ_MODEL_PATH`, `FINANCIAL_NEWS_SOURCES`


## Installation (Development – Option A: Pipenv)
If you prefer using Pipenv (a `Pipfile` is provided):

```powershell
# Install pipenv (if you don't have it)
pip install --user pipenv

# From the root of the repository
cd C:\Users\ASUS\Desktop\X\StarkAdvisorBackend
pipenv install --dev

# Activate pipenv shell
pipenv shell

```
Generate requirements.txt from Pipfile.lock (if needed):

```powershell
pipenv lock -r > requirements.txt
pipenv lock -r -d > requirements-dev.txt

```

## Instalación (Desarrollo - opción B: venv y pip)
```powershell
cd C:\Users\ASUS\Desktop\X\StarkAdvisorBackend
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

```

## Environment Variables (.env)
Create a .env file in the project root with at least the required variables.
Minimal example for development (adjust values as needed):

```
# .env
SECRET_KEY=django-insecure-dev-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=starkadvisorbd
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
# Mongo (elige MONGO_URI o las variables individuales)
MONGO_URI=
# o
MONGO_NAME=starkadvisor
MONGO_HOST=localhost
MONGO_PORT=27017
```
The project uses `environ.Env.read_env()` inside `base.py`, so if the `.env` file is located in the root directory, it will be loaded automatically.

## Starting Services (Local Docker Compose)
If you prefer using Docker for PostgreSQL and Redis, a `docker-compose.local.yml` file is included.

```powershell
# Start services
docker-compose -f docker-compose.local.yml up -d

# Check containers
docker ps

```

## Migrations, Superuser, and Tests
```powershell
# Activate virtualenv/pipenv if applicable
. .\.venv\Scripts\Activate.ps1
# or: pipenv shell

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

```

## Run Development Server
By default, `manage.py` loads `starkadvisorbackend.settings.local`.

```powershell
python manage.py runserver

```

## Collect Static Files & Basic Production Deployment
In production, make sure to set `DJANGO_SETTINGS_MODULE=starkadvisorbackend.settings.production`and configure a WSGI server (gunicorn/uWSGI) plus a reverse proxy (nginx).

```powershell
# Example environment variables (PowerShell)
$env:DJANGO_SETTINGS_MODULE = "starkadvisorbackend.settings.production"
$env:SECRET_KEY = "<tu-secret>"
# Other DB and Redis variables...

# Collect static files
python manage.py collectstatic --noinput

# Run with gunicorn (install it first)

gunicorn starkadvisorbackend.wsgi:application --bind 0.0.0.0:8000
```
## Logs, Static, and Media

- `STATIC_ROOT` in production points to `<BASE_DIR>/staticfiles`.
- `MEDIA_ROOT` points to `<BASE_DIR>/media`.
- Error logs are stored in `logs/django_errors.log` according to the `production.py` configuration.

Make sure the process user has write permissions for these directories.

---

## Recommendations

- Commit your `Pipfile.lock` or `requirements.txt` to ensure others install the exact same versions.
- Do not upload your `.env` file to the repository.
- If you want better dependency management, use `pip-tools` (`pip-compile`) to separate:
  - `requirements.in` → Declared (top-level) dependencies.
  - `requirements.txt` → Fully resolved and locked dependencies.

---

## How to quickly generate `requirements.txt`

With your virtual environment activated:

```bash
pip freeze > requirements.txt


```bash
pip freeze > requirements.txt


```powershell
pip freeze > requirements.txt
```

- O, si usas pip-tools:

```powershell
pip install --user pip-tools
pip-compile --output-file=requirements.txt requirements.in
```

## Specific Notes About the `starkadvisorbackend/settings` Folder

- `local.py` includes the middleware `starkadvisorbackend.middleware.DisableCSRFMiddleware` for development (make sure you enable CSRF in any non-local/open environment).
- `production.py` enforces HTTPS (`SECURE_SSL_REDIRECT = True`) and secure cookies; ensure all required environment variables are set before enabling production mode.
- MongoDB is configured in `base.py` through `MONGO_DB` / `MONGO_URI`.
- FAQ files and chatbot models rely on relative paths, so update `FAQ_PATH` and `FAQ_MODEL_PATH` if you change the project’s folder structure.

---

### Changing Which Settings Django Uses (manage.py / wsgi / asgi)

In this project `manage.py`, `wsgi.py`, and `asgi.py` load `starkadvisorbackend.settings.local` by default.  
If you want to switch to production or another settings module, you must update the `DJANGO_SETTINGS_MODULE` environment variable in all three entry points (or define it globally in the process environment).

**Examples:**

```powershell
#  Define for the current session (PowerShell)
$env:DJANGO_SETTINGS_MODULE = "starkadvisorbackend.settings.production"

# For WSGI/ASGI in deployment (systemd example), export the variable in the service that starts gunicorn/uvicorn
```

You can also directly edit wsgi.py and asgi.py if you need a different default value during deployment (not recommended — it’s better to set DJANGO_SETTINGS_MODULE from the system environment):

```python
# example in wsgi.py/asgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starkadvisorbackend.settings.production')
```
### Mongo and Redis: `*_URI` vs individual variables (precedence)

The settings for Mongo and Redis in this project accept two styles:

- Full URI (e.g., `MONGO_URI`, `REDIS_URL`) — a compact format that includes scheme, host, port, database, and credentials.
- Individual variables (e.g., `MONGO_HOST`, `MONGO_PORT`, `MONGO_NAME` or `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`).

Behavior and recommendation:

- If `MONGO_URI` is provided in the environment (non-null), the project will use that URI to connect to Mongo, and the individual Mongo variables will be ignored.
- Similarly, if `REDIS_URL` is present, that URL will be used and the variables `REDIS_HOST`/`REDIS_PORT`/`REDIS_DB` will not be considered.
- This provides flexibility: locally you can use individual variables, and in production you can use a single URI provided by your hosting provider (e.g., `mongodb+srv://...` or `rediss://...`).

Examples of `.env` using full URI:


```
MONGO_URI=mongodb://user:pass@mongo-host:27017/starkadvisor
REDIS_URL=redis://:password@redis-host:6379/0
```

If you are not using URIs, define the individual variables documented in  
`starkadvisorbackend/settings/base.py` and `local.py`.

## Contributing
1. Fork the repo and create a feature branch.  
2. Run tests locally.  
3. Open a PR to `main` with a clear description.

---

If you want, I can:
- Create a `.env.example` with the most important variables.  
- Update `requirements.txt` automatically from your current environment (I saw you ran `pip freeze > requirements.txt`).  
- Add specific Docker/Nginx instructions for production.

Tell me what you prefer and I’ll do it.

## Useful Commands and Recommended Periodic Execution
Below is a list of CLI scripts available in the project and recommendations for running them periodically (crontab).  
All commands assume you are in the repo root and have your virtual environment active (or are using pipenv).

- Update "Trade of the Day":


```powershell
python -m stocks.scripts.update_trade_of_the_day_data
```

**Description:** Fetches the “trade of the day” information and saves/updates the corresponding document in Mongo (collection `trade_of_the_day`).  
**Recommendation:** Schedule it in cron every 8 hours (for example: `0 */8 * * *`) to keep the information fresh without overloading the APIs.


- News Scraping :

```powershell
python -m news.scripts.scraping_job
```

**Description:** Runs the category-based news scraper, performs sentiment analysis, and stores the results in the database.  
**Recommendation:** Run it once every two days (for example in cron: `0 3 */2 * *`). This job may consume rate limits from external sources, so a low execution frequency is recommended.

- **Market Pipeline (all-in-one):**

```powershell
python -m stocks.scripts.market_pipeline_cli run_all --period 5d --interval 1d
```

**Description:** `run_all` downloads and updates metrics and time series for stocks, ETFs, and currencies. It includes both historical time series and computed metrics.

**Recommendations:**

- **First run:** if this is your first time running it, fetch the last 5 years (`--period 5y`) with `--interval 1d` to populate the full historical database.
- **Daily run:** for maintenance, schedule a daily cron job that updates metrics and time series for the last 3 days with a 1-day interval (e.g., `--period 3d --interval 1d`).

**Crontab examples** (edit them with `crontab -e` on Linux; on Windows use Task Scheduler):


```cron
# Every 8 hours -> update_trade_of_the_day_data
0 */8 * * * cd /path/to/StarkAdvisorBackend && . .venv/bin/activate && python -m stocks.scripts.update_trade_of_the_day_data

# Every 2 days at 03:00 -> scraping_job
0 3 */2 * * cd /path/to/StarkAdvisorBackend && . .venv/bin/activate && python -m news.scripts.scraping_job

# Daily at 02:00 -> market pipeline (update last 3 days)
0 2 * * * cd /path/to/StarkAdvisorBackend && . .venv/bin/activate && python -m stocks.scripts.market_pipeline_cli run_all --period 3d --interval 1d
```

**Notes:**
- Adjust paths and the virtual environment activation command according to your OS (Windows PowerShell uses `. .\.venv\Scripts\Activate.ps1` or `venv\Scripts\activate`).
- If you run inside containers (Docker), adapt the commands to run inside the container or use scheduled tasks in the orchestrator.
- Monitor logs and external API rate limits. For heavy scraping, consider using backoff and retries (the job already implements basic retries).

