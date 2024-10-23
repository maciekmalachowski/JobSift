from config import app, db
from models import JobOffer
from scrapers import justjoin_it, bulldogjob

def insert_jobs():
    jobs = {}
    jobs.update(justjoin_it.get_data())
    jobs.update(bulldogjob.get_data())

    for values in jobs.values():
        job_offer = JobOffer(
            link = values['link'],
            title = values['title'],
            salary = values['salary'],
            company = values['company'],
            location = ','.join(values['location']),
            type_of_work = values['type_of_work'],
            job_level = values['job_level'],
            operating_mode = values['operating_mode'],
            skills = ','.join(values['skills'])
        )
        db.session.add(job_offer)

    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        insert_jobs()
        print("Job data inserted successfully!")
