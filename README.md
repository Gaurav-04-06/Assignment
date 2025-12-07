# Local Setup & Run Guide

## Prerequisites

- Python 3.7 or higher
- OpenAI API key
- MongoDB (local or Atlas)

## Installation

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Create `.env` file in project root:**

```
OPENAI_API_KEY=your_openai_api_key
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=liaplus_chatbot
```

## Running Locally

### Option 1: CLI Interface

```bash
python app.py
```

Then follow the prompts to chat with the bot.

### Option 2: Web Interface (Streamlit)

```bash
streamlit run app.py
```

Opens at `http://localhost:8500`

## Database Setup

If using MongoDB Atlas:

- Create a cluster at [mongodb.com/cloud](https://mongodb.com/cloud)
- Update `MONGODB_URI` in `.env` with your connection string
