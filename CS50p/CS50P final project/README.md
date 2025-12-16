
## Smart Expense Tracker

#### Video Demo: https://youtu.be/DjGIIyj4JjU

#### Description:
Smart Expense Tracker is a full-fledged Python application designed to help users
record, store, and analyze personal expenses through both a command-line interface
and a modern web interface.

The project uses **SQLite** for persistent data storage and **Streamlit** to provide
an interactive web UI, while keeping all core business logic isolated and testable.

### Key Features:
- Persistent expense storage using SQLite
- Add expenses with strict input validation
- Monthly expense summaries
- Category-wise expense breakdown with charts
- Interactive Streamlit web interface
- Fully tested core logic using pytest
- Clean separation between UI layer and business logic

### Project Structure:

```
├── project.py        # Core logic (SQLite + business functions)
├── app.py            # Streamlit Web UI
├── test_project.py   # Pytest unit tests
├── requirements.txt
└── README.md
```
### Technologies Used:
- Python 3
- SQLite (built-in database)
- Streamlit (web UI)
- Pytest (testing)

### How to Run the Project:
1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the web application:
```
streamlit run app.py
```

3. (Optional) Run tests:
```
pytest
```

### Design Philosophy:
- **Business logic is independent of UI**
- **Database logic is centralized**
- **All critical functions are test-covered**
- **Easily extensible into REST APIs or SaaS products**

This project demonstrates real-world software engineering practices such as
database design, modular architecture, testing, and user-friendly interfaces.


