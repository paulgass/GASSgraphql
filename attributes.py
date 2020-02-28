import graphene
from enums import *

''' Attributes '''
#! Remove all required attributes, handle vlidation in query/mutation

class CandidateAttribute:
    brandi_id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    phone_number = graphene.String()
    home_of_record = graphene.String()
    sex = graphene.Argument(graphene.Enum.from_enum(SexEnum))
    arrival_date = graphene.types.datetime.DateTime()
    middle_initial = graphene.String()
    social_security_number = graphene.String()
    dob = graphene.types.datetime.Date()
    rank_id = graphene.Argument(graphene.Enum.from_enum(RankEnum))
    arrived_from = graphene.String()

class AssignmentAttribute:
    assign_code = graphene.Argument(graphene.Enum.from_enum(AssignmentCodeEnum))
    brandi_id = graphene.Int(required=True)

class MedicalProfileAttribute:
    hot_weather_injury = graphene.Boolean()
    cold_weather_injury = graphene.Boolean()
    physical = graphene.Boolean()
    glasses = graphene.Boolean()

class PersonalProfileAttribute:
    brandi_id = graphene.Int(required=True)
    #edu_code = graphene.String(required=False) #Column(String, ForeignKey('education.edu_code'))
    edu_code = graphene.Argument(graphene.Enum.from_enum(EducationEnum))
    pov = graphene.Boolean() #Column(Boolean)
    gt_score = graphene.String() #Column(String)
    success_factors = graphene.String() # Column(String)
    success_motivators = graphene.String() #Column(String)
    bad_habits = graphene.String() #Column(String)
    dependents = graphene.Boolean()
    ranger_regiment_discover = graphene.String()
    played_sports = graphene.Boolean()

class SportsProfileAttribute:
    brandi_id = graphene.Int()
    per_id = graphene.Int()
    sport_code = graphene.Argument(graphene.Enum.from_enum(SportsEnum)) #graphene.String()

class EmergencyContactAttibute:
    brandi_id = graphene.Int(required=True)
    contact_first_name = graphene.String()
    contact_last_name = graphene.String()
    contact_phone_number = graphene.String() #! add clean/validation!
    contact_ec_code = graphene.String()

class MilitaryAttribute:
    mil_id = graphene.Int()
    brandi_id = graphene.Int()
    rank_code = graphene.String()
    mos_code = graphene.String()
    dod_id = graphene.String()
    is_tdy = graphene.Boolean()
    airborne = graphene.Boolean()

class EventAttribute:
    event_id = graphene.Int()
    brandi_id = graphene.Int()
    asmnt_code = graphene.Enum.from_enum(AssessmentCodeEnum)
    score = graphene.Int()
    modifier = graphene.String()
    retest = graphene.Boolean()
    grader = graphene.String()
    event_timestamp = graphene.types.DateTime()

class AssessmentBaselinesAttribute:
    asment_code = graphene.String()
    pass_score = graphene.Int()
    timed = graphene.Boolean()

class GraduationAttribute:
    brandi_id = graphene.Int()
    grad_date = graphene.types.DateTime()

class TransitionAttribute:
    brandi_id = graphene.Int()
    assignment_submitted = graphene.types.DateTime()
    orders_submitted = graphene.types.DateTime()
    duty_station = graphene.String()
    exit_interview_date = graphene.types.DateTime()
    travel_date = graphene.types.DateTime()

class DropAttribute:
    brandi_id = graphene.Int()
    drop_code = graphene.String()
    drop_origin_code = graphene.String()
    recycled = graphene.Boolean()
    drop_descr = graphene.String()
    drop_ts = graphene.types.DateTime()


''' Input '''
class CreateCandidateInput(graphene.InputObjectType, CandidateAttribute):
    """Arguments to create a candidate."""
    pass

class UpdateCandidateInput(graphene.InputObjectType, CandidateAttribute):
    """Arguments to update a person."""
    pass

class CandidateInput(graphene.InputObjectType, CandidateAttribute):
    pass

class AssignmentInput(graphene.InputObjectType, AssignmentAttribute):
    pass

class MedicalProfileInput(graphene.InputObjectType, MedicalProfileAttribute):
    pass

class PersonalProfileInput(graphene.InputObjectType, PersonalProfileAttribute):
    pass

class SportsProfileInput(graphene.InputObjectType, SportsProfileAttribute):
    pass

class MilitaryAttributeInput(graphene.InputObjectType, MilitaryAttribute):
    pass

class EventInput(graphene.InputObjectType, EventAttribute):
    pass

class AssessmentBaselinesInput(graphene.InputObjectType, AssessmentBaselinesAttribute):
    pass

class GraduationInput(graphene.InputObjectType, GraduationAttribute):
    pass

class TransitionInput(graphene.InputObjectType, TransitionAttribute):
    pass

class DropInput(graphene.InputObjectType, DropAttribute):
    pass

class CandidateQueryInput(CandidateInput):
    class_up_id = graphene.Int()
    assignment_code = graphene.String()
    departed_date = graphene.types.Date()

class EventQueryInput(EventInput):
    min_score = graphene.Int()
    max_score = graphene.Int()
    start_date = graphene.types.Date()
    end_date = graphene.types.Date()
