# Client Interface Service

A Flask web interface for the Smart Grid microservices project.

This service provides a browser-based interface for:

- Viewing meters
- Creating meters
- Updating meters
- Deleting meters
- Triggering reading simulations
- Viewing readings
- Viewing analysis results such as averages, peaks, and usage categories

This app does not store data directly. It communicates with other backend services through HTTP APIs.

---

## Project Structure

```text
.
├── app.py
├── config.py
├── services.py
├── requirements.txt
├── startup.sh
├── templates/
│   └── index.html
├── static/
│   └── styles.css
├── .env.example
├── .gitignore
└── README.md
