from app import app as application

# For local debug via: `python server/wsgi.py`
if __name__ == "__main__":
  application.run(host="0.0.0.0", port=5000)

