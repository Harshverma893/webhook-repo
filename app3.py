from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson import ObjectId
import datetime

app = Flask(__name__)

# Connect to MongoDB
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['github_events']
    collection = db['events']
    print("Connected to MongoDB successfully")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/github', methods=['POST'])
def listen_github():
    payload = request.json
    event_type = request.headers.get('X-GitHub-Event', 'unknown')
    
    if not payload:
        print("No payload received")
        return 'No payload received', 400

    # Log payload for debugging
    print(f"Received payload: {payload}")
    
    try:
        event_data = {
            'request_id': request.headers.get('X-GitHub-Delivery', ''),
            'timestamp': datetime.datetime.now(datetime.UTC).isoformat()
        }

        if event_type == 'push':
            event_data.update({
                'author': payload.get('pusher', {}).get('name', payload.get('sender', {}).get('login', 'Unknown')),
                'action': 'PUSH',
                'to_branch': payload.get('ref', '').replace('refs/heads/', ''),
                'request_id': payload.get('head_commit', {}).get('id', request.headers.get('X-GitHub-Delivery', ''))
            })
        elif event_type == 'pull_request':
            pr_action = payload.get('action', '')
            pr_data = payload.get('pull_request', {})
            from_branch = pr_data.get('head', {}).get('ref', 'unknown')
            to_branch = pr_data.get('base', {}).get('ref', 'unknown')
            if pr_action == 'opened':
                if from_branch == 'unknown' or to_branch == 'unknown':
                    print(f"Warning: Missing branch info - from_branch: {from_branch}, to_branch: {to_branch}")
                event_data.update({
                    'author': pr_data.get('user', {}).get('login', 'Unknown'),
                    'action': 'PULL_REQUEST',
                    'from_branch': from_branch,
                    'to_branch': to_branch,
                    'request_id': str(pr_data.get('id', request.headers.get('X-GitHub-Delivery', '')))
                })
            elif pr_action == 'closed' and pr_data.get('merged', False):
                if from_branch == 'unknown' or to_branch == 'unknown':
                    print(f"Warning: Missing branch info - from_branch: {from_branch}, to_branch: {to_branch}")
                event_data.update({
                    'author': pr_data.get('merged_by', {}).get('login', pr_data.get('user', {}).get('login', 'Unknown')),
                    'action': 'MERGE',
                    'from_branch': from_branch,
                    'to_branch': to_branch,
                    'request_id': str(pr_data.get('id', request.headers.get('X-GitHub-Delivery', ''))),
                    'timestamp': pr_data.get('merged_at', datetime.datetime.now(datetime.UTC).isoformat())
                })
            else:
                print(f"Unsupported pull_request action: {pr_action}")
                return 'Pull Request action not handled', 200
        else:
            print(f"Unsupported event type: {event_type}")
            return 'Event not handled', 200

        # Insert into MongoDB
        inserted_event = collection.insert_one(event_data)
        # Convert ObjectId to string for JSON serialization
        event_data['_id'] = str(inserted_event.inserted_id)
        print(f"Stored event: {event_data}")
        return jsonify(event_data), 200
    except Exception as e:
        print(f"Error inserting into MongoDB: {e}")
        return 'Failed to store event', 500

@app.route('/events', methods=['GET'])
def get_events():
    try:
        # Fetch events sorted by timestamp (newest first)
        events = list(collection.find().sort('timestamp', -1))
        # Convert ObjectId to string for each event
        for event in events:
            event['_id'] = str(event['_id'])
        return jsonify(events), 200
    except Exception as e:
        print(f"Error fetching events: {e}")
        return jsonify([]), 500

if __name__ == '__main__':
    app.run(debug=True)