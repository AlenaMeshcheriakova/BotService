# Bot Service

## Overview

This is a Bot Service, which part of telegram project - "DeutschLernen" designed for interacting with telegram chat bot. 
The application provides logic in bot which allowed communicate with user.

## Dependensy

This service provide data from another service: DataServive via grpc connection. 

## Features

/start: Start learning set.
/learn_standard_words: Learn standard words.
/learn_user_words: Learn the words you added.
/help: Get a list of available commands.
/registration: Start registration process.
/add_words: Add new words for learning.
/stop_add: Stop adding new words process.
/settings: Go to settings

## Prerequisites

- Python 3.8 or higher
- Use Poetry for a dependency installation from pyproject.toml:
(Install poetry and execute comand "poetry install")

## Environment

For enviroment installetion, you need to create you own .env and .test.env file
In cfg/config.py please write link to your cfg files
For a template use file: .template.env

## Installation

### Clone the Repository

https://github.com/AlenaMeshcheriakova/BotService.git
cd BotService

### Starting project

For start up project, use: /src/telegram/main_bot.py
