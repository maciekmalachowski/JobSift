from config import db

class JobOffers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    company = db.Column(db.String(80), unique=False, nullable=False)
    salary = db.Column(db.String(40), unique=False, nullable=False)
    localisation = db.Column(db.String(40), unique=False, nullable=False)
    type_of_work = db.Column(db.String(40), unique=False, nullable=False)
    experience = db.Column(db.String(40), unique=False, nullable=False)
    localisation = db.Column(db.String(40), unique=False, nullable=False)
    desc = db.Column(db.String(300), unique=False, nullable=False)
    employment_type = db.Column(db.String(40), unique=False, nullable=False)

    def to_json(self):
        return{
            "id": self.id,
            "name": self.name,
            "company": self.company,
            "salary": self.salary,
            "localisation": self.localisation,
            "type_of_work": self.type_of_work,
            "experience": self.experience,
            "localisation": self.localisation,
            "desc": self.desc,
            "employment_type": self.employment_type,
        }