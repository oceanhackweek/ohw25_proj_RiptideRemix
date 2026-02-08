# Heroku Deployment Setup

## What was fixed

Your Django app wasn't running on Heroku due to:
1. **Hardcoded `DEBUG=True`** — causes static file serving errors and security issues
2. **Hardcoded `ALLOWED_HOSTS`** — your Heroku domain wasn't allowed
3. **SQLite database** — Heroku's filesystem is ephemeral (resets on redeploy)
4. **No database migrations on deploy** — tables weren't created
5. **Missing cache table** — audio processing cache wasn't working across requests

## Changes made

- ✅ `settings.py` now reads `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS` from environment variables
- ✅ Database switches to PostgreSQL when `DATABASE_URL` is set (Heroku), otherwise SQLite (local)
- ✅ `Procfile` now runs migrations and collects static files on deploy
- ✅ Cache configured to use database (shared across requests)
- ✅ Security settings enabled for production

## Heroku Configuration

### 1. Add Heroku Config Vars

Run these commands from your project root after installing [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli):

```bash
heroku login
heroku apps:list  # find your app name

# Set config vars
heroku config:set DEBUG=False --app YOUR_APP_NAME
heroku config:set SECRET_KEY="your-long-random-secret-key-here" --app YOUR_APP_NAME
heroku config:set ALLOWED_HOSTS="your-app.herokuapp.com,www.your-app.herokuapp.com" --app YOUR_APP_NAME
```

Replace `YOUR_APP_NAME` with your actual Heroku app name, and `your-app.herokuapp.com` with your actual domain.

### 2. Add PostgreSQL Addon

```bash
heroku addons:create heroku-postgresql:mini --app YOUR_APP_NAME
```

This automatically sets `DATABASE_URL`.

### 3. Add Buildpack for Python & Matplotlib

Matplotlib needs system libraries on Heroku. Add buildpacks:

```bash
heroku buildpacks:add --index 1 https://github.com/heroku-community/heroku-buildpack-apt --app YOUR_APP_NAME
heroku buildpacks:add --index 2 heroku/python --app YOUR_APP_NAME
```

Then create an `Aptfile` in your repo root with:

```
libpng-dev
libfreetype6-dev
libjpeg-dev
```

### 4. Deploy

```bash
git add -A
git commit -m "Fix Heroku compatibility"
git push heroku main  # or your branch name
```

### 5. Monitor the Deployment

```bash
heroku logs --tail --app YOUR_APP_NAME
```

## Local Development

To test locally with the new settings:

1. Create a `.env` file (copy from `.env.example`):
   ```
   DEBUG=True
   SECRET_KEY=dev-key
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

2. Install python-dotenv if not already in requirements:
   ```bash
   pip install python-dotenv
   ```

3. Load env vars in your shell or use `python-decouple`:
   ```bash
   # Linux/Mac:
   export $(cat .env | xargs)
   
   # Windows PowerShell:
   Get-Content .env | ForEach-Object { 
       if ($_ -match '^\s*[^#].*=') { 
           $_.Split('=')[0], $_.Split('=')[1] -join '=' | ForEach-Object { $env:$_ } 
       } 
   }
   ```

4. Run migrations locally (creates cache table):
   ```bash
   python manage.py migrate
   ```

5. Start dev server:
   ```bash
   python manage.py runserver
   ```

## Troubleshooting

**500 errors?** Check logs: `heroku logs --tail`

**Static files not loading?** Re-run: `heroku run python manage.py collectstatic --app YOUR_APP_NAME`

**Spectrogram generation timing out?** Heroku's free/mini dyno is slower. Consider scaling to Standard-1X (`heroku dyno:type -t standard-1x`).

**Audio processing is slow?** The optimizations from the previous PR should help. If still slow, consider using Redis for caching:
```bash
heroku addons:create heroku-redis:mini --app YOUR_APP_NAME
```
Then update CACHES in settings.py to use Redis backend.
