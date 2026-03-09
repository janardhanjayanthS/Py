# Toggling Log Levels

## Overview
This document explains how to change the logging level in your application using environment variables.

## What are Log Levels?
Log levels control how much detail your application logs. From most to least verbose:

| Level | Purpose | When to Use |
|-------|---------|-------------|
| `DEBUG` | Detailed diagnostic info | Development & troubleshooting |
| `INFO` | General informational messages | Normal operation (default) |
| `WARNING` | Warning messages for potential issues | Production monitoring |
| `ERROR` | Error messages | Production |
| `CRITICAL` | Critical failures | Production |
| `NOTSET` | No filtering | Special cases only |

## How to Change Log Level

### Step 1: Locate your `.env` file
The `.env` file is in your project root directory.

### Step 2: Add or Update the LOG_LEVEL variable
Open the `.env` file and add or modify this line:

```env
LOG_LEVEL=DEBUG
```

Replace `DEBUG` with any valid level from the table above.

### Step 3: Restart your application
The log level is loaded when the application starts, so you need to restart for changes to take effect.

## Examples

### Development Mode (See Everything)
```env
LOG_LEVEL=DEBUG
```
Shows all log messages including detailed debug information.

### Production Mode (Only Important Stuff)
```env
LOG_LEVEL=WARNING
```
Only shows warnings, errors, and critical messages.

### Default Mode
```env
LOG_LEVEL=INFO
```
Balanced logging suitable for most use cases. This is the default if you don't specify a level.

## How It Works

1. The `.env` file stores the `LOG_LEVEL` configuration
2. `LogSettings` class (in `src/core/log.py`) reads this value using Pydantic
3. The `setup_logging()` function applies this level to structlog
4. All loggers in your application respect this level

## Code Reference

See `src/core/log.py`:
- Line 11-19: `LogLevel` enum defines available levels
- Line 26: `LOG_LEVEL` field with default value `INFO`
- Line 59: Log level is retrieved from settings
- Line 84: Applied to structlog configuration

## Quick Tips

- **Missing LOG_LEVEL in .env?** → Application uses `INFO` by default
- **Changes not working?** → Remember to restart the application
- **Too many logs?** → Increase the level (e.g., from DEBUG to INFO)
- **Missing important info?** → Decrease the level (e.g., from WARNING to INFO)

## Common Use Cases

| Scenario | Recommended Level |
|----------|------------------|
| Local development | `DEBUG` |
| Running tests | `INFO` or `WARNING` |
| Staging environment | `INFO` |
| Production | `WARNING` or `ERROR` |
| Investigating a bug | `DEBUG` |
