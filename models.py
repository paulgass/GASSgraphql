from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, 
                            backref)
from sqlalchemy.ext.declarative import declarative_base
from config import db_connection_string

#connection_string = 'postgresql://brandiadmin:qnHQJT2FZpKG4KqV@lionscale.live:5999/brandidb'
connection_string = db_connection_string()
# print(connection_string)
#engine = create_engine(connection_string, convert_unicode=True)
engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)

#if not engine.has_table('candidate'):
#    raise Exception('Could not connect to database')

db_session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class ClassUp(Base):
    __tablename__ = 'class_up'
    class_up_id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('class.class_id'))
    roster_number = Column(String)
    class_up_ts = Column(DateTime, default=func.now())
    class_details = relationship("Class")

class Class(Base):
    __tablename__ = 'class'
    class_id = Column(Integer, primary_key=True)
    phase = Column(String)
    date_code = Column(String)

class Assignment(Base):
    __tablename__ = 'assignment'
    assign_code = Column(String, primary_key=True)
    description = Column(String)


class Candidate(Base):
    __tablename__ = 'candidate'
    brandi_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_initial = Column(String)
    social_security_number = Column(String)
    phone_number = Column(String)
    home_of_record = Column(String)
    dob = Column(DateTime)
    sex = Column(String)
    class_up_id = Column(Integer, ForeignKey('class_up.class_up_id'))
    assignment_code = Column(String, ForeignKey('assignment.assign_code'))
    arrived_from = Column(String)
    arrival_date = Column(DateTime, default=func.now())
    departed_date = Column(DateTime)
    assignment = relationship("Assignment")
    classup = relationship("ClassUp")
    personal_profile = relationship('PersonalProfile')
    medical_profile = relationship('MedicalProfile')
    military_profile = relationship('MilitaryAttributes')
    emergency_contact = relationship('EmergencyContact')
    events = relationship('Event')
    drop_info = relationship('Drop')
    graduation_info = relationship('Graduation')
    transition_info = relationship('Transition')

class MedicalProfile(Base):
    __tablename__ = 'medical_profile'
    med_id = Column(Integer, primary_key=True)
    brandi_id = Column(Integer, ForeignKey('candidate.brandi_id'))
    hot_weather_injury = Column(Boolean)
    cold_weather_injury = Column(Boolean)
    physical = Column(Boolean)
    glasses = Column(Boolean)
    candidate = relationship("Candidate")

class Education(Base):
    __tablename__ = 'education'
    edu_code = Column(String, primary_key=True)
    edu_name = Column(String)

class PersonalProfile(Base):
    __tablename__ = 'personal_profile'
    per_id = Column(Integer, primary_key=True)
    brandi_id = Column(Integer, ForeignKey('candidate.brandi_id'))
    edu_code = Column(String, ForeignKey('education.edu_code'))
    pov = Column(Boolean)
    gt_score = Column(String)
    success_factors = Column(String)
    success_motivators = Column(String)
    bad_habits = Column(String)
    dependents = Column(Boolean)
    ranger_regiment_discover = Column(String)
    played_sports = Column(Boolean)
    education = relationship('Education')
    sports = relationship('SportsProfile')

class Sports(Base):
    __tablename__ = 'sports'
    sport_code = Column(String, primary_key=True)
    sport_name = Column(String)


class SportsProfile(Base):
    __tablename__ = 'sports_profile'
    sports_played_id = Column(Integer, primary_key=True)
    per_id = Column(Integer, ForeignKey('personal_profile.per_id'))
    sport_code = Column(String, ForeignKey('sports.sport_code'))
    personal_profile = relationship('PersonalProfile')
    sport = relationship('Sports')

class EmergencyContactRelationship(Base):
    __tablename__ = 'emergency_contact_relationship'
    ec_code = Column(String, primary_key=True)
    description = Column(String)

class EmergencyContact(Base):
    __tablename__ = 'emergency_contact'
    emer_con_id = Column(Integer, primary_key=True)
    brandi_id = Column(Integer, ForeignKey('candidate.brandi_id'))
    contact_first_name = Column(String)
    contact_last_name = Column(String)
    contact_phone_number = Column(String)
    contact_ec_code = Column(String, ForeignKey('emergency_contact_relationship.ec_code'))
    candidate = relationship('Candidate')
    contact_relationship = relationship('EmergencyContactRelationship')

class Rank(Base):
    __tablename__ = 'rank'
    rank_code = Column(String, primary_key=True)
    description = Column(String)

class Mos(Base):
    __tablename__ = 'mos'
    mos_code = Column(String, primary_key=True)
    description = Column(String)

class MilitaryAttributes(Base):
    __tablename__ = 'mil_attributes'
    mil_id = Column(Integer, primary_key=True)
    brandi_id = Column(Integer, ForeignKey('candidate.brandi_id'))
    rank_code = Column(String, ForeignKey('rank.rank_code'))
    mos_code = Column(String, ForeignKey('mos.mos_code'))
    dod_id = Column(String)
    active_service_date = Column(DateTime)
    is_tdy = Column(Boolean)
    tdy_unit = Column(String)
    airborne = Column(Boolean)
    ranger_sof_affiliations = Column(Boolean)
    candidate = relationship('Candidate')
    rank = relationship('Rank')
    mos = relationship('Mos')

class Assessment(Base):
    __tablename__ = 'assessment'
    asmnt_code = Column(String, primary_key=True)
    assessment_name = Column(String)

class Event(Base):
    __tablename__ = 'event'
    event_id = Column(Integer, primary_key=True)
    brandi_id = Column(Integer, ForeignKey('candidate.brandi_id'))
    asmnt_code = Column(String, ForeignKey('assessment.asmnt_code'))
    score = Column(Integer)
    modifier = Column(String)
    retest = Column(Boolean, default=False)
    grader = Column(String)
    event_timestamp = Column(DateTime, default=func.now())
    candidate = relationship('Candidate')
    assessment = relationship('Assessment')

class AssessmentBaselines(Base):
    __tablename__ = 'assessment_baselines'
    assessment_base_id = Column(Integer, primary_key=True)
    asment_code = Column(String, ForeignKey('assessment.asmnt_code'))
    pass_score = Column(Integer)
    timed = Column(Boolean)
    assessment = relationship('Assessment')

class Graduation(Base):
    __tablename__ = 'graduation'
    grad_id = Column(Integer, primary_key=True)
    brandi_id = Column(Integer, ForeignKey('candidate.brandi_id'))
    grad_date = Column(DateTime)
    candidate = relationship('Candidate')

class Transition(Base):
    __tablename__ = 'transition'
    trans_id = Column(Integer, primary_key=True)
    brandi_id = Column(Integer, ForeignKey('candidate.brandi_id'))
    assignment_submitted = Column(DateTime)
    orders_submitted = Column(DateTime)
    duty_station = Column(String)
    exit_interview_date = Column(DateTime)
    travel_date = Column(DateTime)
    candidate = relationship('Candidate')

class DropReason(Base):
    __tablename__ = 'drop_reason'
    drop_code = Column(String, primary_key=True)
    drop_description = Column(String)

class DropOrigin(Base):
    __tablename__ = 'drop_origin'
    drop_origin_code = Column(String, primary_key=True)
    drop_origin_description = Column(String)

class Drop(Base):
    __tablename__ = 'drop'
    drop_id = Column(Integer, primary_key=True)
    brandi_id = Column(Integer, ForeignKey('candidate.brandi_id'))
    drop_code = Column(String, ForeignKey('drop_reason.drop_code'))
    drop_origin_code = Column(String, ForeignKey('drop_origin.drop_origin_code'))
    recycled = Column(Boolean)
    drop_descr = Column(String)
    drop_ts = Column(DateTime)
    candidate = relationship('Candidate')
    drop_reason = relationship('DropReason')
    drop_origin = relationship('DropOrigin')
