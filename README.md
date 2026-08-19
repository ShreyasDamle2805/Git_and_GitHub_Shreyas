# Flask & MongoDB Integration

This is a Flask web application that stores user submissions in MongoDB Atlas and serves a JSON API endpoint.

## Features
- `/` - HTML form for user input
- `/success` - Confirmation page after database submission
- `/api` - Returns records from `data.json`
- `/health` - Health check route for container/monitoring status

## Prerequisites
- Python 3.x
- Docker & Docker Compose (optional for container run)

## Local Setup

1. Clone the repo:
   ```bash
   git clone [https://github.com/ShreyasDamle2805/Flask_and_MongoDB_Shreyas.git](https://github.com/ShreyasDamle2805/Flask_and_MongoDB_Shreyas.git)
   cd Flask_and_MongoDB_Shreyas