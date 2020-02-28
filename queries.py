import graphene
from connections import *
from datetime import timedelta
from enums import *
import utils
from sqlalchemy.sql import text, and_, desc
from attributes import (CandidateQueryInput, MilitaryAttributeInput, EventQueryInput)
from datetime import datetime
from sqlalchemy import func
from flask_graphql_auth import (
    AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    get_raw_jwt,
    create_access_token,
    create_refresh_token,
    query_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
)
from fga import MessageField, ProtectedUnion

"""
    Queries
"""
class Query(graphene.ObjectType):
    node = relay.Node.Field()

    '''
        Versatile endpoint: can take in JSON object of all Candidate attributes
        and perform an innder join on whatever is passed in. Also option is limit.
        Always sorts by last name.
    '''
    get_candidates = graphene.Field(lambda: graphene.List(Candidate),
                                            limit = graphene.Int(),
                                            input=CandidateQueryInput())

    ''' Get all Queries '''
    get_all_assignments = graphene.List(Assignment)
    get_all_class_ups = graphene.List(ClassUp)
    get_all_medical = graphene.List(MedicalProfile)
    get_all_ranks = graphene.List(Rank)
    get_all_sports = graphene.List(Sports)
    get_all_mos = graphene.List(Mos)
    get_all_assessments = graphene. List(Assessment)
    get_all_education = graphene.List(Education)
    get_all_military_profile = graphene.Field(lambda: MilitaryAttributes,
                                                    limit = graphene.Int())
    get_all_military_attributes = graphene.Field(lambda: graphene.List(MilitaryAttributes),
                                    input=MilitaryAttributeInput(required=False))
    get_all_emergency_contact_relationships = graphene.List(EmergencyContactRelationship)
    get_all_drop_reasons = graphene.List(DropReason)
    get_all_drop_origins = graphene.List(DropOrigin)

    get_sports_profile = graphene.Field(lambda: SportsProfile,
                                        brandi_id = graphene.Int(),
                                        sports_played_id = graphene.Int())
    get_personal_profile = graphene.Field(lambda: PersonalProfile,
                                        brandi_id = graphene.Int(),
                                        per_id = graphene.Int())



    # add a query for searching by arrival date range
    get_candidates_by_arrival_date = graphene.Field(lambda: graphene.List(Candidate),
                                        arrival_date=graphene.types.DateTime(),
                                        window = graphene.Int())
    get_candidates_by_arrival_date_range = graphene.Field(lambda: graphene.List(Candidate),
                                            start_date=graphene.types.datetime.Date(),
                                            end_date=graphene.types.datetime.Date())
    get_events = graphene.Field(lambda: graphene.List(Event),
                                                token=graphene.String(),
						limit = graphene.Int(),
                                                input=EventQueryInput())
    get_candidates_who_scored = graphene.Field(lambda: graphene.List(Candidate),
                                                    min_score=graphene.Float(),
                                                    max_score=graphene.Float())

    """ Return Candidates from database

        [Arguments]:
            - limit<optional>: the maximum number of events to return
            - input<optional>:
                - brandi_id<int>: unique identifier, if provided a single candidate will be returned
                - first_name<string>: First name of candidate
                - last_name<string>: Last name of candidate
                - phone_number<string>: String of candidate phone number, on the
                                        backend this will be converted to an integer
                - home_of_record<string>:
                - sex<Enum<string>>: Male or Female, SexEnum enforces value in database
                - arrival_date: <DateTime>: The date and timestamp of arrival
                - middle_initial<string>: String of middle initial, 1 character
                - social_security_number<string>: String consisting of social security
                                                    number on the backend this will be
                                                    converted to an integer
                - dob<Date>: Date of birth
                - arrived_from<string>: The location where the candidate arrived from
                - limit<int>: the maximum number of candidates to return, after sorting
                - class_up_id<int>: 
                - assignment_code<string>: 
                - departed_date<Date>: 
        [Return]:
            List of candidates, sorted by last_name (ascending, a-z)
                * if no input/limit argument is provided, then all candidates are returned
    """
    def resolve_get_candidates(self, info,limit=None, input=None):
        query = Candidate.get_query(info)

        if input:
            data = utils.input_to_dictionary(input)

            if data.get('brandi_id'):
                query = query.filter_by(brandi_id=data.get('brandi_id'))
            if data.get('first_name'):
                query = query.filter_by(first_name=data.get('first_name'))
            if data.get('last_name'):
                query = query.filter_by(last_name=data.get('last_name'))
            if data.get('phone_number'):
                query = query.filter_by(phone_number=data.get('phone_number'))
            if data.get('home_of_record'):
                query = query.filter_by(home_of_record=data.get('home_of_record'))
            if data.get('sex'):
                query = query.filter_by(sex=data.get('sex'))
            if data.get('arrival_date'):
                query = query.filter_by(arrival_date=data.get('arrival_date'))
            if data.get('middle_initial'):
                query = query.filter_by(middle_initial=data.get('middle_initial'))
            if data.get('social_security_number'):
                query = query.filter_by(social_security_number=data.get('social_security_number'))
            if data.get('dob'):
                query = query.filter_by(dob=data.get('dob'))
            if data.get('arrived_from'):
                query = query.filter_by(arrived_from=data.get('arrived_from'))
            if data.get('class_up_id'):
                query = query.filter_by(class_up_id=data.get('class_up_id'))
            if data.get('assignment_code'):
                query = query.filter_by(assignment_code=data.get('assignment_code'))
            if data.get('departed_date'):
                query = query.filter_by(departed_date=data.get('departed_date'))
        if limit:
            # which limit Candidates to get? sort first?
            return query.order_by('last_name').limit(limit)
        query = query.order_by('last_name')
        return query.all()


    """ Return events from database

        [Arguments]:
            - limit<optional>: the maximum number of events to return
            - input<optional>:
                - event_id<Int>: The unique identifier of the event
                - brandi_id<Int>: The ID of the Candidate for this event
                - asmnt_code<Enum<String>>: The type of the event
                - score<Int>: The score for this event for the given candidate
                - modifier<String>: 
                - retest<Bool>: Was this event a retest?
                - grader<String>: The cadre conducting this event
                - event_timestamp<DateTime>: When the event took plac
                - min_score<Int>: If supplied, return those candidates 
                - max_score<Int>: 
                - start_date<Date>: 
                - end_date<Date>: 

        [Return]: List of events
            * if no input/limit argument is provided, then all events are returned
    """
    @query_jwt_required
    def resolve_get_events(self, info, limit=None, input=None):
        query = Event.get_query(info)
        if input:
            data = utils.input_to_dictionary(input)
            if data.get('event_id'):
                query = query.filter_by(event_id=data.get('event_id'))
            if data.get('brandi_id'):
                query = query.filter_by(brandi_id=data.get('brandi_id'))
            if data.get('asmnt_code'):
                query = query.filter_by(asmnt_code='asmnt_code')
            if data.get('score'):
                query = query.filter_by(score='score')
            if data.get('modifier'):
                query = query.filter_by(modifier='modifier')
            if data.get('retest'):
                query = query.filter_by(retest='retest')
            if data.get('grader'):
                query = query.filter_by(grader='grader')
            if data.get('event_timestamp'):
                query = query.filter_by(event_timestamp='event_timestamp')
            if data.get('min_score'):
                query = query.filter_by(score >= data.get('min_score'))
            if data.get('max_score'):
                query = query.filter_by(score <= data.get('max_score'))
            #! what about getting all those candidates with an above average score?
            ''' select all candidates who have scored (on average) higher than a certain value
            SELECT * FROM candidate AS c LEFT JOIN event as e ON e.brandi_id = c.brandi_id
            '''
            # if data.get('average'):
            #     query = query(func.avg(Event.score).label('avg_score'))
            if data.get('start_date'):
                start_date = datetime.strptime(data.get('start_date') , '%Y-%m-%d')
                query = query.filter_by(event_timestamp>=start_date)
            if data.get('end_date'):
                end_date = datetime.strptime(data.get('end_date') , '%Y-%m-%d')
                query = query.filter_by(event_timestamp<=end_date)
        if limit:
            query = query.limit(limit)
        return query.all()


    """ Return those candidates who scored (on average) higher or lower than a given score

        [Arguments]:
            - min_score<Int>: the lowest average score a Candidate must have
            - max_score<Int>: the highest average score a Candidate must have

        [Return]: List of candidates meeting constraint

    """
    def resolve_get_candidates_who_scored(self, info, min_score=None, max_score=None):
        def create_candidates(results):
            candidates = []
            for result in results:
                data = {}
                for key in result.keys():
                    data[key] = result[key]
                candidate = Candidate(**data)
                candidates.append(candidate)
            return candidates

        base_sql = "SELECT c.* FROM candidate AS c LEFT JOIN event as e ON e.brandi_id = c.brandi_id GROUP BY c.brandi_id HAVING AVG(e.score)"
        if min_score:
            sql = f'{base_sql} >= {min_score}'
        if max_score:
            sql = f'{base_sql} <= {max_score}'
        if sql:
            results = engine.execute(sql)
            return create_candidates(results)
        return []


    def resolve_get_all_military_attributes(self, info, limit=None):
        query = MilitaryAttributes.get_query(info)
        if limit:
            return query.limit(limit)
        return query.all()

    """ Return all assignments

        [Return]:
            - List of assignments
    """
    def resolve_get_all_assignments(self, info, **kwargs):
        query = Assignment.get_query(info)
        return query.all()


    """ Return all Class Ups

        [Return]:
            - List of Class Ups
    """
    def resolve_get_all_class_ups(self, info, **kwargs):
        query = ClassUp.get_query(info)
        return query.all()


    """ Return all Medical Profiles

        [Return]:
            - List of medical profiles
    """
    def resolve_get_all_medical(self, info, **kwargs):
        query = MedicalProfile.get_query(info)
        return query.all()


    """ Get all ranks

        [Return]:
            - List of all ranks
    """
    def resolve_get_all_ranks(self, info):
        query = Rank.get_query(info)
        return query.all()


    """ Get all sports

        [Return]:
            - List of all sports
    """
    def resolve_get_all_sports(self, info):
        query = Sports.get_query(info)
        return query.all()

    """ Get all MOS

        [Return]:
            - List of all MOS
    """
    def resolve_get_all_mos(self, info):
        query = Mos.get_query(info)
        return query.all()

    """ Get all Assessments

        [Return]:
            - List of all assessments
    """
    def resolve_get_all_assessments(self, info):
        query = Assessment.get_query(info)
        return query.all()

    """ Get all education

        [Return]:
            - List of all education
    """
    def resolve_get_all_education(self, info):
        query = Education.get_query(info)
        return query.all()

    """ Get all Emergency Contact Relationships

        [Return]:
            - List of all Emergency Contact Relationships
    """
    def resolve_get_all_emergency_contact_relationships(self, info):
        return EmergencyContactRelationship.get_query(info).all()

    """ Get all drop reasons

        [Return]:
            - List of all drop reasons
    """
    def resolve_get_all_drop_reasons(self, info):
        return DropReason.get_query(info).all()

    """ Get all drop origins

        [Return]:
            - List of all drop origins
    """
    def resolve_get_all_drop_origins(self, info):
        return DropOrigin.get_query(info).all()

    """ Get all candidates who arrived on a certain date

        [Arguments]:
            - arrival_date<DateTime>: The date a candidate arrived on
            - window<Optional<Int>>: If specified, include those candidates who
                                        arrived plus or minus the arrival date
                                        provided.
        [Return]:
            - List of all ranks
    """
    def resolve_get_candidates_by_arrival_date(self, info, arrival_date, window=0):
        if window < 0:
            raise Exception('Window must be a positive value')
        end_date = arrival_date + timedelta(days = window)
        start_date = arrival_date - timedelta(days = window)
        query = Candidate.get_query(info)
        return query.filter(and_(CandidateModel.arrival_date >= start_date, CandidateModel.arrival_date <= end_date)).all()

    """Get all candidates who have an arrival date within a range

        [Arugments]:
            - start_date<Date>: date following the iso8601 format
            - end_date<Date>: date following the iso8601 format

        [Raises]:
            - Exception: End date must occur on or after start date

        [Return]:
            - List of candidates falling within an arrival date range
    """
    def resolve_get_candidates_by_arrival_date_range(self, info, start_date, end_date):
        if end_date < start_date:
            raise Exception('End date must occur on or after the start date')
        query = Candidate.get_query(info)
        return query.filter(and_(CandidateModel.arrival_date >= start_date, CandidateModel.arrival_date <= end_date)).all()

    def resolve_get_candidates_by_arrived_from(self, info, arrived_from):
        query = Candidate.get_query(info)
        return query.filter(CandidateModel.arrived_from == arrived_from).all()

    #! I would like to require this be of type AssignmentCodeEnum
    #! would also like to return count, [candidate]
    # def resolve_get_candidates_by_assignent_code(self, info, assignment_code):
    #     candidates = db_session.query(CandidateModel).filter_by(assignment_code=assignment_code).all()
    #     return candidates

    def resolve_get_sports_profile(self, info, brandi_id=None, sports_played_id=None):
        if not brandi_id and not sports_played_id:
            raise Exception('Either brandi_id or sports_played_id needs to be specified')
        if sports_played_id:
            return db_session.query(SportsProfileModel).filter_by(sports_played_id=sports_played_id).first()
        elif brandi_id:
            exists = db_session.query(
                db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).exists()
            ).scalar()
            if not exists:
                raise Exception('Candidate not found for given brandi_id')
            candidate = db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).first()
            if not candidate.personal_profile:
                raise Exception('Candidate has no personal profile')
            print('return sport for candidate', candidate.personal_profile[0].sports[0].sport_code)
            return candidate.personal_profile[0].sports[0]

    """ Get the personal profile of a candidate

        [Arguments]:
            - brandi_id<Optional<Int>>: the candidate ID
            - per_id<Optional<Int>>: the personal profile ID

        [Raises]:
            - Exception: brandi_id or per_id not given
            - Exception: Candidate does not exist with given brandi_id
            - Exception: Candidate has no personal profile
            - Exception: Personal profile does not exist with given per_id

        [Return]:
            - Candidate
    """
    def resolve_get_personal_profile(self, info, brandi_id=None, per_id=None):
        if not brandi_id and not per_id:
            raise Exception('Either brandi_id or per_id needs to be specified')
        if per_id:
            exists = db_session.query(
                db_session.query(PersonalProfileModel).filter_by(per_id=per_id).exists()
            ).scalar()
            if not exists:
                raise Exception('Personal profile does not exist with given per_id')
            return db_session.query(PersonalProfileModel).filter_by(per_id=per_id).first()
        elif brandi_id:
            exists = db_session.query(
                db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).exists()
            ).scalar()
            if not exists:
                raise Exception('Candidate not found for given brandi_id')
            candidate = db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).first()
            if not candidate.personal_profile:
                raise Exception('Candidate has no personal profile')
            return candidate.personal_profile[0]

    """ Get a military profile

        [Arguments]:
            - mil_id<Int>: 
            - brandi_id<Int>: 
            - rank_code<String>: 
            - mos_code<String>: 
            - dod_id<String>: 
            - is_tdy<Bool>: 
            - airborne<Bool>: 

        [Raises]:
            - Exception: Military profile does not exist with given mil_id

        [Return]:
            - Military Profile
    """
    def resolve_get_military_attributes(self, info, input):
        data = utils.input_to_dictionary(input)

        return db_session.query(MilitaryAttributesModel).filter()

        if data.get('mil_id'):
            exists = db_session.query(
                db_session.query(MilitaryAttributesModel).filter_by(mil_id=data.get('mil_id')).exists()
            ).scalar()
            if not exists:
                raise Exception('Military profile does not exist with given mil_id')
            db_session.query(MilitaryAttributesModel).filter_by(mil_id=data.get('mil_id')).all()
        elif data.get('brandi_id'):
            return db_session.query(MilitaryAttributesModel).filter_by(brandi_id=data.get('brandi_id')).all()
        elif data.get('rank_code'):
            return db_session.query(MilitaryAttributesModel).filter(rank_code=data.get('rank_code')).all()
        elif data.get('mos_code'):
            return db_session.query(MilitaryAttributesModel).filter(mos_code=data.get('mos_code')).all()
        elif data.get('dod_id'):
            return db_session.query(MilitaryAttributesModel).filter_by(dod_id=data.get('dod_id'))
        elif data.get('is_tdy'):
            return db_session.query(MilitaryAttributesModel).filter(is_tdy=data.get('is_tdy'))
        elif data.get('airborne'):
            return db_session.query(MilitaryAttributesModel).filter(airborne=data.get('airborne'))
