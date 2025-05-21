# Solar-Data-Discovery
Week 0 Challenge

Steps to Reproduce Environment Locally

Clone the repository

    git clone https://github.com/your-username/solar-challenge-week1.git
    cd solar-challenge-week1
Create and activate a virtual environment
Using venv (Python 3.6+):

    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
Install dependencies

        pip install -r requirements.txt
Run the project
(Instructions for running scripts/notebooks go here — update as needed.)
Continuous Integration

    GitHub Actions runs pip install -r requirements.txt on every push to ensure dependencies are installable.

Note: The data/ directory and any CSV files are excluded from the repository via .gitignore.
