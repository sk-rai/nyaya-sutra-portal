"""Gunicorn configuration for production deployment."""

import multiprocessing
import os

# Server socket
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:5000")

# Worker processes
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")

# Process naming
proc_name = "nyaya-sutra-api"

# Server mechanics
preload_app = True
daemon = False

# Restart workers after this many requests (prevents memory leaks)
max_requests = 1000
max_requests_jitter = 50
