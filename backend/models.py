from config import db

class JobOffer(db.Model):
    __tablename__ = 'joboffers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    company = db.Column(db.String(255), unique=False, nullable=False)
    salary = db.Column(db.String(255), unique=False, nullable=False)
    type_of_work = db.Column(db.String(255), unique=False, nullable=False)
    job_level = db.Column(db.String(255), unique=False, nullable=False)
    location = db.Column(db.String(255), unique=False, nullable=False)
    operating_mode = db.Column(db.String(255), unique=False, nullable=False)
    # desc = db.Column(db.Text, unique=False, nullable=False)
    skills = db.Column(db.String(255), unique=False, nullable=False)
    link = db.Column(db.String(255), unique=False, nullable=False)
    

    def to_json(self):
        return{
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "salary": self.salary,
            "location": self.location.split(','),
            "type_of_work": self.type_of_work,
            "job_level": self.job_level,
            "operating_mode": self.operating_mode,
            # "desc": self.desc,
            "skills": self.skills.split(','),
            "link": self.link
        }