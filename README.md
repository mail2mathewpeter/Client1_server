# Shree Bharatraj Corporation – Flask Server

This folder contains a self-contained Flask backend ready for deployment.

## Requirements

- Python 3.10+

## Setup

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with your SMTP credentials and recipient email
```

## Run (Development)

```bash
python app.py
```

## Run (Production)

Use any WSGI server (e.g., gunicorn, waitress, uWSGI):

```bash
# example with waitress on Windows
pip install waitress
waitress-serve --listen=0.0.0.0:5000 wsgi:application
```

Or with gunicorn (Linux):

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5000 wsgi:application
```

## API

- POST `/api/send-email`
- GET `/api/health`
- POST `/api/test-email` (disabled in production)

## Environment Variables (`.env`)

```
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASS=
RECIPIENT_EMAIL=
PORT=5000
NODE_ENV=production
```


