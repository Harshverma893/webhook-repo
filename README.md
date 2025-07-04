# 📡 Webhook Repository

This repository contains a **Flask application** that receives GitHub webhook events (Push, Pull Request, Merge) from the [Action Repository](https://github.com/your-username/action-repo), stores them in **MongoDB**, and displays them on a real-time web UI.

---

## ✨ Features

- **Webhook Receiver:** Handles GitHub webhook events (Push, PR, Merge).
- **MongoDB Integration:** Stores structured event data.
- **Live Dashboard:** UI auto-refreshes every 15 seconds to display new events.
- **Easy Integration:** Use with GitHub + Ngrok to test locally.

---

## 🛠️ Technologies Used

- **Backend:** Python, Flask  
- **Database:** MongoDB  
- **Frontend:** HTML + JavaScript (AJAX polling)  
- **Others:** GitHub Webhooks, Ngrok

---

## 🔧 Full Setup Guide

### 📁 Clone the Repository

```bash
git clone https://github.com/Harshverma893/webhook-repo.git
cd webhook-repo
```

#🧪 Install Python Dependencies

First, ensure Python 3.8+ and pip are installed. Then run:

```bash
pip install -r requirements.txt
```

### 🗄️ Setup and Start MongoDB

```bash
Program Files\MongoDB\Server\8.0\bin> mongod
```
Make sure MongoDB is running on mongodb://localhost:27017.

### ▶️ Run the Flask Application

```bash
python app3.py
```
Flask server will start at:

```bash
http://localhost:5000/
```

### 🌐 Expose Flask Locally with Ngrok

```bash
ngrok http 5000
```

Copy the HTTPS forwarding URL (e.g., https://abcd1234.ngrok.io)

### 🔗 Connect with GitHub Webhook

Go to your action-repo on GitHub

Navigate to:
Settings → Webhooks → Add webhook

Fill the form:

Payload URL: https://your-ngrok-url.ngrok.io/github

Content type: application/json

Events: Choose Push, Pull requests, or Send me everything

Click Add webhook

✅ Now your webhook-repo is ready to receive and display events.

### 🖥️ UI - How Events Are Shown

The Flask app polls /events every 15 seconds and shows logs like:

Push:
"{author} pushed to {to_branch} on {day}{suffix} {month} {year} - {hour}:{minute} {AM/PM} IST"

Pull Request:
"{author} submitted a pull request from {from_branch} to {to_branch} on {day}{suffix} {month} {year} - {hour}:{minute} {AM/PM} IST"

Merge:
"{author} merged branch {from_branch} to {to_branch} on {day}{suffix} {month} {year} - {hour}:{minute} {AM/PM} IST"

### 🧾 MongoDB Schema

Each document in the github_events.events collection contains:

Field	Description
_id      	      MongoDB ObjectId
request_id     	Commit hash or PR ID
author	        GitHub username
action	        "PUSH", "PULL_REQUEST", "MERGE"
from_branch	    Source branch
to_branch	      Destination branch
timestamp	UTC   datetime string

### ✅ Final Test Checklist

✅ Run MongoDB

✅ Start Flask app (python app.py)

✅ Expose via Ngrok

✅ Set up webhook in action-repo

✅ Push or PR in action-repo

✅ See events in http://localhost:5000/ or Ngrok URL


