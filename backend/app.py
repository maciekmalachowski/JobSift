from flask import request, jsonify
from config import app, db
from sqlalchemy import or_, and_
from models import JobOffer
from scrapers import justjoin_it, bulldogjob

def insert_jobs():
    jobs = justjoin_it.get_data()
    jobs.update(bulldogjob.get_data())

    for values in jobs.values():
        job_offer = JobOffer(
            link = values['link'],
            title = values['title'],
            salary = values['salary'],
            company = values['company'],
            location = values['location'],
            type_of_work = values['type_of_work'],
            job_level = values['job_level'],
            operating_mode = values['operating_mode'],
            skills = values['skills']
        )
        db.session.add(job_offer)

    db.session.commit()

@app.before_request
def before_first_request():
    insert_jobs()

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
        query = query.filter(JobOffer.title.ilike(f"%{skills}%"))
        #     or_(
        #         JobOffer.title.ilike(f"%{skills}%"),
        #         JobOffer.desc.ilike(f"%{skills}%")
        #     )
        # )

    jobs = query.all()

    job_list = [{
        'title': job.title,
        'company': job.company,
        'location': job.location,
    } for job in jobs]

    return jsonify(job_list)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)