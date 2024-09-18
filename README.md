# Library Database Script

## Overview

This Python script interacts with a SQLite database to manage and query a library's data. It uses the `Faker` library to generate random data for authors and books, and it performs various queries to retrieve information from the database.

## Features

- **Create Tables:** Creates `author` and `book` tables if they do not exist.
- **Generate Data:** Inserts 500 authors and 1000 books into the database with random data.
- **Querying:**
  - Finds and prints the book with the maximum number of pages.
  - Calculates and prints the average number of pages across all books.
  - Finds and prints the youngest author.
  - Finds and prints authors who do not have any books.
  - Bonus: Finds and prints 5 authors who have more than 3 books.

## Prerequisites

- Python 3.x
- SQLite3 (comes with Python)
- `Faker` library

To install the `Faker` library, run:

```bash
pip install faker
