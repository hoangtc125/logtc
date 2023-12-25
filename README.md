# `logtc`: Python Logging Library

## Overview

`logtc` is a versatile Python logging library designed for modern web services. It provides advanced logging capabilities including context-aware logging for request and internal tasks, automatic file rotation based on time intervals, and socket-based logging with automatic Socket.IO support.

## Key Features

- **Context-Aware Logging**: Log messages are tagged with a unique context, making it easier to trace logs back to specific requests or internal tasks.
- **Automatic File Rotation**: Log files are automatically rotated based on configurable time intervals, helping manage log file sizes and organization.
- **Socket Logging**: Real-time logging through web sockets, with built-in support for Socket.IO.
- **Easy Integration with Web Frameworks**: Designed to be easily integrated with frameworks like FastAPI.

## Installation

You can install `logtc` via pip:

```bash
pip install logtc
```

## Setup and Configuration

### Basic Logger Setup

To set up the logger, import the `Logger` from `logtc` and configure it with your preferences:

```python
from logtc.logger import Logger

Logger().setup(
    name="test_service",
    log_path="E:\\logging\\log\\.log",
    when="M",
    interval=1,
    url="http://localhost:8000",
    handshake_path="/logtc/socket.io/",
)
```

Parameters:

- `name`: Name of the logging service.
- `log_path`: Path to the log file.
- `when` and `interval`: Controls the log file rotation. For instance, "M" and 1 means the file rotates every minute.
- `url`: URL for the socket logging server.
- `handshake_path`: Handshake path for the Socket.IO server.

### Context-Aware Logging

For logging with request or task-specific contexts:

```python
from logtc.logger import request_id_context

# Set a unique identifier for the current context
request_id_context.set(UNIQUE_ID)
```

Each log message will include this unique identifier, making it easier to correlate logs with specific requests or tasks.

### Socket Logging with FastAPI

To use socket logging with FastAPI, mount the `socket` from `logtc`:

```python
from fastapi import FastAPI
from logtc.logger import socket

app = FastAPI()

# Mount the socket logger
app.mount("/logtc", socket())
```

This sets up an endpoint for the Socket.IO server, enabling real-time log streaming.

## Usage

After setting up `logtc`, you can use its logger to log messages of different severities:

```python
from logtc.logger import Logger

# Logging an info message
Logger().logger.info("This is an info message.")

# Logging a warning message
Logger().logger.warning("This is a warning message.")

# Logging an error message
Logger().logger.error("This is an error message.")

# Logging a debug message
Logger().logger.debug("This is a debug message.")

# Logging a critical message
Logger().logger.critical("This is a critical message.")
```

## Contributing

Contributions to `logtc` are welcome! Please refer to the repository's contribution guidelines for more details.

## License

`logtc` is released under MIT License.