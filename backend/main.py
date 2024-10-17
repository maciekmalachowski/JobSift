from flask import request, jsonify
from config import app, db
from models import JobOffers

@app.route("/", methods=["GET"])
def get_job_offers():
    job_offers = JobOffers.query.all()
    json_job_offers = list(map(lambda x: x.to_json(), job_offers))
    return jsonify({"job_offers": json_job_offers})

@app.route("/scrape", methods=["POST"])
def create_job_offer():
    name1 = request.json.get("name1")
    name2 = request.json.get("name2")
    name3 = request.json.get("name3")

    if not name1 or not name2 or not name3:
        return (jsonify({"message": "enter values"}), 400)
    
    new_job_offer = JobOffers(name1=name1, name2=name2, name3=name3)
    try:
        db.session.add(new_job_offer)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}, 400)
    
    return jsonify({"message": "Job offer created"}, 200)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)