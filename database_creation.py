from models import (
    engine,
    db_session, 
    Base, 
    ClassUp, 
    Class, 
    Assignment, 
    Candidate, 
    MedicalProfile, 
    Education, 
    PersonalProfile, 
    Sports, 
    SportsProfile, 
    EmergencyContactRelationship, 
    EmergencyContact, 
    Rank, 
    Mos, 
    MilitaryAttributes, 
    Assessment, 
    Event, 
    AssessmentBaselines, 
    Graduation, 
    Transition, 
    DropReason, 
    DropOrigin, 
    Drop
)


Base.metadata.create_all(bind=engine)

# # Fill the tables with some data
# engineering = Department(name='Engineering')
# db_session.add(engineering)
# hr = Department(name='Human Resources')
# db_session.add(hr)

# peter = Employee(name='Peter', department=engineering)
# db_session.add(peter)
# roy = Employee(name='Roy', department=engineering)
# db_session.add(roy)
# tracy = Employee(name='Tracy', department=hr)
# db_session.add(tracy)
# db_session.commit()
