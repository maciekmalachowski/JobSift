from flask import request, jsonify
from config import app, db
from sqlalchemy import or_, and_
from models import JobOffer

@app.route('/jobs', methods=['GET'])
def get_jobs():
    job_offers = JobOffer.query.all()
    job_list = [job.to_json() for job in job_offers]
    return jsonify(job_list)

@app.route('/search-jobs', methods=['POST'])
def search_jobs():
    data = request.json
    job_level = data.get('job_level', '').lower()
    location = data.get('location', '').lower()
    skills = data.get('skills', '').lower()

    query = JobOffer.query

    if job_level:
        query = query.filter(JobOffer.job_level.ilike(f"%{job_level}%"))

    if location:
        query = query.filter(JobOffer.location.ilike(f"%{location}%"))

    if skills:
        query = query.filter(
            or_(
                JobOffer.title.ilike(f"%{skills}%"),
                JobOffer.skills.ilike(f"%{skills}%")
            )
        )

    jobs = query.all()

    job_list = [{
        'title': job.title,
        'company': job.company,
        'job_level': job.job_level,
        'location': job.location,
    } for job in jobs]

    return jsonify(job_list)

if __name__ == "__main__":
    app.run(debug=True)