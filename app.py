from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leads.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Float, nullable=False)
    last_scanned = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/submit_url', methods=['POST'])
def submit_url():
    data = request.get_json()
    url = data.get("url")
    # Logic to analyze the URL and generate leads
    leads = generate_leads(url)
    # Save leads to database
    for lead in leads:
        new_lead = Lead(business_name=lead["business_name"], url=lead["url"], score=lead["score"])
        db.session.add(new_lead)
    db.session.commit()
    return jsonify({"message": "Leads processed successfully", "leads": leads})

def generate_leads(url):
    # Simulate lead generation and scoring
    leads = []
    for _ in range(5):  # Generate 5 mock leads
        lead = {
            "business_name": f"Business {random.randint(1, 100)}",
            "url": f"{url}/lead{random.randint(1, 100)}",
            "score": random.uniform(50, 100)
        }
        leads.append(lead)
    return leads

@app.route('/get_leads', methods=['GET'])
def get_leads():
    leads = Lead.query.all()
    return jsonify([{"business_name": lead.business_name, "url": lead.url, "score": lead.score} for lead in leads])

if __name__ == "__main__":
    db.create_all()  # Creates the database tables
    app.run(debug=True)
