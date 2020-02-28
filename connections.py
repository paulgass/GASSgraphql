from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyObjectType
from graphene import relay
from models import (db_session, engine,
                    Class as ClassModel,
                    ClassUp as ClassUpModel,
                    Candidate as CandidateModel,
                    Assignment as AssignmentModel,
                    MedicalProfile as MedicalProfileModel,
                    PersonalProfile as PersonalProfileModel,
                    Graduation as GraduationModel,
                    EmergencyContact as EmergencyContactModel,
                    EmergencyContactRelationship as EmergencyContactRelationshipModel,
                    MilitaryAttributes as MilitaryAttributesModel,
                    Mos as MosModel,
                    Rank as RankModel,
                    Education as EducationModel,
                    Sports as SportsModel,
                    SportsProfile as SportsProfileModel,
                    Event as EventModel,
                    Assessment as AssessmentModel,
                    AssessmentBaselines as AssessmentBaselinesModel,
                    Transition as TransitionModel,
                    Drop as DropModel,
                    DropReason as DropReasonModel,
                    DropOrigin as DropOriginModel)


class Candidate(SQLAlchemyObjectType):
    class Meta:
        model = CandidateModel
        interfaces = (relay.Node, )

class CandidateConnection(relay.Connection):
    class Meta:
        node = Candidate

class ClassUp(SQLAlchemyObjectType):
    class Meta:
        model = ClassUpModel
        interfaces = (relay.Node, )

class ClassUpConnection(relay.Connection):
    class Meta:
        node = ClassUp

class Class(SQLAlchemyObjectType):
    class Meta:
        model = ClassModel
        interfaces = (relay.Node, )

class ClassConnection(relay.Connection):
    class Meta:
        node = Class

class Assignment(SQLAlchemyObjectType):
    class Meta:
        model = AssignmentModel
        interfaces = (relay.Node, )

class AssignmentConnection(relay.Connection):
    class Meta:
        node = Assignment

class MedicalProfile(SQLAlchemyObjectType):
    class Meta:
        model = MedicalProfileModel
        interfaces = (relay.Node, )

class MedicalProfileConnection(relay.Connection):
    class Meta:
        node = MedicalProfile

class PersonalProfile(SQLAlchemyObjectType):
    class Meta:
        model = PersonalProfileModel
        interfaces = (relay.Node, )

class PersonalProfileConnection(relay.Connection):
    class Meta:
        node = PersonalProfile

class Graduation(SQLAlchemyObjectType):
    class Meta:
        model = GraduationModel
        interfaces = (relay.Node, )

class GraduationConnection(relay.Connection):
    class Meta:
        node = Graduation

class EmergencyContact(SQLAlchemyObjectType):
    class Meta:
        model = EmergencyContactModel
        interfaces = (relay.Node, )

class EmergencyContactConnection(relay.Connection):
    class Meta:
        node = EmergencyContact

class EmergencyContactRelationship(SQLAlchemyObjectType):
    class Meta: 
        model = EmergencyContactRelationshipModel
        interfaces = (relay.Node, )

class EmergencyContactRelationshipConnection(relay.Connection):
    class Meta:
        node = EmergencyContactRelationship

class MilitaryAttributes(SQLAlchemyObjectType):
    class Meta:
        model = MilitaryAttributesModel
        interfaces = (relay.Node, )

class MilitaryAttributesConnection(relay.Connection):
    class Meta:
        node = MilitaryAttributes

class Mos(SQLAlchemyObjectType):
    class Meta: 
        model = MosModel
        interfaces = (relay.Node, )

class MosConnection(relay.Connection):
    class Meta:
        node = Mos

class Rank(SQLAlchemyObjectType):
    class Meta:
        model = RankModel
        interfaces = (relay.Node, )

class RankConnection(relay.Connection):
    class Meta:
        node = Rank

class Education(SQLAlchemyObjectType):
    class Meta: 
        model = EducationModel
        interfaces = (relay.Node, )

class EducationConnection(relay.Connection):
    class Meta:
        node = Education

class Sports(SQLAlchemyObjectType):
    class Meta:
        model = SportsModel
        interfaces = (relay.Node, )

class SportsConnection(relay.Connection):
    class Meta:
        node = Sports

class SportsProfile(SQLAlchemyObjectType):
    class Meta: 
        model = SportsProfileModel
        interfaces = (relay.Node, )

class SportsProfileConnection(relay.Connection):
    class Meta: 
        node = SportsProfile

class Event(SQLAlchemyObjectType):
    class Meta: 
        model = EventModel
        interfaces = (relay.Node, )

class EventConnection(relay.Connection):
    class Meta:
        node = Event

class Assessment(SQLAlchemyObjectType):
    class Meta: 
        model = AssessmentModel
        interfaces = (relay.Node, )

class AssessmentConnection(relay.Connection):
    class Meta: 
        node = Assessment

class AssessmentBaselines(SQLAlchemyObjectType):
    class Meta:
        model = AssessmentBaselinesModel
        interfaces = (relay.Node, )

class AssessmentBaselinesConnection(relay.Connection):
    class Meta: 
        node = AssessmentBaselines

class Transition(SQLAlchemyObjectType):
    class Meta:
        model = TransitionModel
        interfaces = (relay.Node, )

class TransitionConnection(relay.Connection):
    class Meta:
        node = Transition

class Drop(SQLAlchemyObjectType):
    class Meta: 
        model = DropModel
        interfaces = (relay.Node, )

class DropConnection(relay.Connection):
    class Meta:
        node = Drop

class DropReason(SQLAlchemyObjectType):
    class Meta: 
        model = DropReasonModel
        interfaces = (relay.Node, )

class DropReasonConnection(relay.Connection):
    class Meta:
        node = DropReason

class DropOrigin(SQLAlchemyObjectType):
    class Meta: 
        model = DropOriginModel
        interfaces = (relay.Node, )

class DropOriginConnection(relay.Connection):
    class Meta: 
        node = DropOrigin
