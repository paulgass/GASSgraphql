import graphene
from connections import *
from enums import (SexEnum, AssignmentCodeEnum, RankEnum,
                    EducationEnum, AssessmentCodeEnum, SportsEnum)
from attributes import (CandidateInput, AssignmentInput,
        MedicalProfileInput, PersonalProfileInput, SportsProfileInput, EventInput,
        AssessmentBaselinesInput, GraduationInput, TransitionInput, DropInput, MilitaryAttributeInput)
import utils
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

class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def mutate(cls, _, info, username, password):
        user_is_valid = True
        if not user_is_valid:
            return None

        return AuthMutation(
            access_token=create_access_token(username),
            refresh_token=create_refresh_token(username),
        )

class ProtectedMutation(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()

    message = graphene.Field(ProtectedUnion)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info):
        return ProtectedMutation(
            message=MessageField(message="Protected mutation works")
        )


class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _):
        current_user = get_jwt_identity()
        return RefreshMutation(new_token=create_access_token(identity=current_user))


class CreateCandidate(graphene.Mutation):
    class Arguments:
        input = CandidateInput(required=True)

    candidate = graphene.Field(lambda: Candidate)

    def validate(self, data):
        is_valid = True
        if not data['firstName']:
            is_valid = False

        return is_valid

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        #data['edited'] = datetime.utcnow()
        errors = utils.validate('Candidate', data)
        if bool(errors):
            raise Exception(' | '.join(errors.values()))
        else:
            """ add try except """
            data = utils.clean(data)
            candidate = CandidateModel(**data)

            #! Create and add the candidate to the database
            db_session.add(candidate)
            db_session.commit()
            return CreateCandidate(candidate=candidate)

class UpdateCandidate(graphene.Mutation):
    """Update a person."""
    candidate = graphene.Field(lambda: Candidate, description="Candidate updated by this mutation.")
    class Arguments:
        brandi_id = graphene.Int(required=True)
        input = CandidateInput(required=False)

    def mutate(self, info, brandi_id, input):
        data = utils.input_to_dictionary(input)
        #data['edited'] = datetime.utcnow()
        data = utils.clean(data)
        exists = db_session.query(
            db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).exists()
        ).scalar()
        if exists:
            candidate = db_session.query(CandidateModel).filter_by(brandi_id=brandi_id)
            candidate.update(data)
            db_session.commit()
            candidate = db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).first()
            return UpdateCandidate(candidate=candidate)
        else:
            raise Exception(f'Unable to find candidate with brandi_id: {brandi_id}')

class CreateClassUp(graphene.Mutation):
    class_up = graphene.Field(lambda: ClassUp)

    class Arguments:
        brandi_id = graphene.Int(required=True)
        class_id = graphene.Int(required=True)
        roster_number = graphene.Int(required=True)

    def mutate(self, info, brandi_id, class_id, roster_number):
        # 1 - get the candidate
        candidate_exists = db_session.query(
            db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).exists()
        ).scalar()
        class_exists = db_session.query(
            db_session.query(ClassModel).filter_by(class_id=class_id).exists()
        ).scalar()
        if candidate_exists and class_exists:
            _candidate = db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).first()
            _class = db_session.query(ClassModel).filter_by(class_id=class_id).first()
            # create Class Up
            _class_up = ClassUpModel(roster_number=roster_number)
            _class_up.class_details = _class
            _class_up.class_id = _class.class_id
            db_session.add(_class_up)
            db_session.commit()
            _candidate.class_up = _class_up
            _candidate.class_up_id = _class.class_id
            db_session.commit()
            return CreateClassUp(class_up=_class_up)
        else:
            raise Exception('Unable to locate Candidate or Class')

class CreateAssignmentForCandidate(graphene.Mutation):
    assignment = graphene.Field(lambda: Assignment)

    class Arguments:
        input = AssignmentInput(required=True)

    def mutate(self, info, brandi_id, assign_code):
        candidate_exists = db_session.query(
            db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).exists()
        ).scalar()
        assignment_exists = db_session.query(
            db_session.query(AssignmentModel).filter_by(assign_code=assign_code).exists()
        ).scalar()
        if candidate_exists and assignment_exists:
            candidate = db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).first()
            assignment = db_session.query(AssignmentModel).filter_by(assign_code=assign_code).first()
            candidate.assignment = assignment
            candidate.assignment_code = assign_code
            db_session.commit()
            return CreateAssignmentForCandidate(assignment=assignment)
        else:
            raise Exception(f'Unable to locate Candidate{candidate_exists} or Assignment {assignment_exists}')

class UpdateAssignmentForCandidate(graphene.Mutation):
    assignment = graphene.Field(lambda: Assignment)

    class Arguments:
        input = AssignmentInput(required=True)

    def mutate(self, info, brandi_id, assign_code):
        candidate_exists = db_session.query(
            db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).exists()
        ).scalar()
        assignment_exists = db_session.query(
            db_session.query(AssignmentModel).filter_by(assign_code=assign_code).exists()
        ).scalar()
        if candidate_exists and assignment_exists:
            candidate = db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).first()
            assignment = db_session.query(AssignmentModel).filter_by(assign_code=assign_code).first()
            candidate.assignment = assignment
            candidate.assignment_code = assign_code
            db_session.commit()
            return UpdateAssignmentForCandidate(assignment=assignment)
        else:
            raise Exception(f'Unable to locate Candidate{candidate_exists} or Assignment {assignment_exists}')

class CreateMedicalProfile(graphene.Mutation):
    medical_profile = graphene.Field(lambda: MedicalProfile)

    class Arguments:
        brandi_id = graphene.Int(required=True)
        input = MedicalProfileInput(required=True)

    def mutate(self, info, brandi_id, input):
        # get candidate
        candidate_exists = db_session.query(
            db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).exists()
        ).scalar()
        if candidate_exists:
            candidate = db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).first()
            data = utils.input_to_dictionary(input)
            profile = MedicalProfileModel(**data)
            #print(profile)
            db_session.add(profile)
            profile.candidate = candidate
            profile.brandi_id = brandi_id
            db_session.commit()
            return CreateMedicalProfile(medical_profile=profile)
        else:
            raise Exception('Unable to find Candidate with given brandi_id')

class UpdateMedicalProfile(graphene.Mutation):
    medical_profile = graphene.Field(lambda: MedicalProfile, description="Medical Profile updated by this mutation.")
    class Arguments:
        med_id = graphene.Int(required=True)
        input = MedicalProfileInput(required=False)

    def mutate(self, info, med_id, input):
        data = utils.input_to_dictionary(input)
        if bool(data):
            data = utils.clean(data)
            exists = db_session.query(
                db_session.query(MedicalProfileModel).filter_by(med_id=med_id).exists()
            ).scalar()
            if exists:
                medical_profile = db_session.query(MedicalProfileModel).filter_by(med_id=med_id).first()
                for key, value in data.items():
                    setattr(medical_profile, key, value)
                db_session.commit()
                return UpdateMedicalProfile(medical_profile=medical_profile)
            else:
                raise Exception(f'Unable to find medical profile with med_id: {med_id}')
        raise Exception('No changes')

class CreatePersonalProfile(graphene.Mutation):
    personal_profile = graphene.Field(lambda: PersonalProfile, description="Mutation to create a personal profile")

    class Arguments:
        input = PersonalProfileInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        # 1 - check if candidate exists
        candidate_exists = db_session.query(
            db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).exists()
        ).scalar()
        if candidate_exists:
            personal_profile = PersonalProfileModel(**data)
            db_session.add(personal_profile)
            db_session.commit()
            return CreatePersonalProfile(personal_profile=personal_profile)
        else:
            raise Exception(f'Candidate with brandi_id: {data["brandi_id"]} does not exist.')

class UpdatePersonalProfile(graphene.Mutation):
    personal_profile = graphene.Field(lambda: PersonalProfile, description="Mutation to create a personal profile")

    class Arguments:
        # either (but not both) of these can be blank. 
        # You will either update a particular candidates' profile OR
        # update a profile given the per_id
        per_id = graphene.Int()
        input = PersonalProfileInput(required=True)

    def mutate(self, info, input, per_id=None):
        data = utils.input_to_dictionary(input)
        brandi_id = data.get('brandi_id')
        if not brandi_id and not per_id:
            raise Exception("At least one brandi_id of per_id must be passed in.")
        # 1 - check if candidate exists
        candidate_exists = db_session.query(
            db_session.query(CandidateModel).filter_by(brandi_id=brandi_id).exists()
        ).scalar()
        if candidate_exists:
        # get the profile
            if per_id:
                personal_profile = db_session.query(PersonalProfileModel).filter_by(per_id=per_id).first()
            elif brandi_id:
                personal_profile = db_session.query(PersonalProfileModel).filter_by(brandi_id=brandi_id).first()
                #personal_profile = db_session.query(PersonalProfileModel).filter_by(brandi_id=brandi_id).first()
            if not personal_profile:
                raise Exception("Could not get personal profile")
            print(personal_profile.success_motivators)
            data = utils.input_to_dictionary(input)
            print(dir(personal_profile))
            for key, value in data.items():
                setattr(personal_profile, key, value)
            db_session.commit()
            return CreatePersonalProfile(personal_profile=personal_profile)
        else:
            raise Exception(f'Candidate with brandi_id: {brandi_id} does not exist.')

class CreateSportsProfile(graphene.Mutation):
    sports_profile = graphene.Field(lambda: SportsProfile, description="Create sports profile.")

    class Arguments:
        input = SportsProfileInput(required=True)

    def mutate(self, info, input):
        # check input
        data = utils.input_to_dictionary(input)
        if data.get('per_id'):
            per_id = data.get('per_id')
            personal_profile = db_session.query(PersonalProfileModel).filter_by(per_id=per_id).first()
        elif data.get('brandi_id'):
            candidate_exists = db_session.query(
                db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).exists()
            ).scalar()
            # check if candidate exists
            if not candidate_exists:
                raise Exception('Candidate does not exist.')
            candidate = db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).first()
            personal_profile = candidate.personal_profile[0]
            per_id = personal_profile.per_id
        else:
            raise Exception('Either the brandi_id or per_id must be passed.')

        exists = db_session.query(
            db_session.query(PersonalProfileModel).filter_by(per_id=per_id).exists()
        ).scalar()
        if not exists:
            raise Exception(f'Personal profile with per_id{per_id} does not exist')
        sports_profile = SportsProfileModel(per_id=per_id, personal_profile=personal_profile)

        if data.get('sport_code'):
            sport = db_session.query(SportsModel).filter_by(sport_code=data.get('sport_code')).first()
            sports_profile.sport_code = data.get('sport_code')
            sports_profile.sport = sport
            db_session.add(sports_profile)
            db_session.commit()
        else:
            raise Exception('Sport code is required')

        #db_session.commit()
        return CreateSportsProfile(sports_profile=sports_profile)

class UpdateSportsProfile(graphene.Mutation):
    sports_profile = graphene.Field(lambda: SportsProfile, description="Update sports profile.")

    class Arguments:
       input = SportsProfileInput(required=True)

    def mutate(self, info, input):
        # need to get the sports profile
        data = utils.input_to_dictionary(input)
        if data.get('brandi_id'):
            candidate_exists = db_session.query(
                db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).exists()
            ).scalar()
            if not candidate_exists:
                raise Exception('Candidate does not exist')
            candidate = db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).first()
            if not candidate.personal_profile:
                raise Exception('Candidate has no personal profile')
            sports_profile = candidate.personal_profile[0].sports[0]
        elif data.get('per_id'):
            profile_exists = db_session.query(
                db_session.query(PersonalProfileModel).filter_by(per_id=data.get('per_id')).exists()
            ).scalar()
            if not profile_exists:
                raise Exception('Personal profile does not exist')
            sports_profile = db_session.query(PersonalProfileModel).filter_by(per_id=data.get('per_id')).first().sports[0]
        else:
            raise Exception('Must provide either a brandi_id or a per_id')
        if not data.get('sport_code'):
            raise Exception('You must provide a sport code')
        if sports_profile.sport_code != data.get('sport_code'):
            sport = db_session.query(SportsModel).filter_by(sport_code=data.get('sport_code'))
            sports_profile.sport_code = data.get('sport_code')
            sports_profile.sport = sport
        db_session.commit()
        return UpdateSportsProfile(sports_profile=sports_profile)

class CreateEvent(graphene.Mutation):
    event = graphene.Field(lambda: Event, description='Create an event.')
    class Arguments:
        token = graphene.String()
        input = EventInput(required=True)
    
    @classmethod
    @mutation_jwt_required
    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        # cannot pass in an event_id
        if data.get('event_id'):
            del data['event_id']
        errors = utils.validate('Event', data)
        if bool(events):
            raise Exception(' | '.join(errors.values()))
        # need to get candidate and assessment
        candidate_exists = db_session.query(
            db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).exists()
        ).scalar()
        if not candidate_exists:
            raise Exception('Candidate does not exist')

        assessment_exists = db_session.query(
            db_session.query(AssessmentModel).filter_by(asmnt_code=data.get('asmnt_code')).exists()
        ).scalar()
        if not assessment_exists:
            raise Exception('Assessment does not exist')

        candidate = db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).first()
        assessment = db_session.query(AssessmentModel).filter_by(asmnt_code=data.get('asmnt_code')).first()
        event = EventModel(**data)
        event.candidate = candidate
        event.assessment = assessment
        db_session.add(event)
        db_session.commit()
        return CreateEvent(event=event)

class UpdateEvent(graphene.Mutation):
    event = graphene.Field(lambda: Event, description='Update event attributes')
    class Arguments:
        token = graphene.String()
        input = EventInput(required=True)
    
    @classmethod
    @mutation_jwt_required
    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        if not data.get('event_id'):
            raise Exception('Must pass in event_id')
        exists = db_session.query(
            db_session.query(EventModel).filter_by(event_id=data.get('event_id')).exists()
        ).scalar()
        if not exists:
            raise Exception('Event does not exist')
        event = db_session.query(EventModel).filter_by(event_id=data.get('event_id')),first()
        for key, value in data.items():
            if key == 'event_id':
                continue
            setattr(event, key, value)
        db_session.commit()
        return UpdateEvent(event=event)

class CreateAssessmentBaseline(graphene.Mutation):
    assessment_baseline = graphene.Field(lambda: AssessmentBaselines, description='Create assessment baseline for candidate')

    class Arguments:
        input = AssessmentBaselinesInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        if not data.get('asment_code'):
            raise Exception('Assessment Code is required.')
        exists = db_session.query(
            db_session.query(AssessmentModel).filter_by(asment_code=asment_code).exists()
        ).scalar()
        if not exists:
            raise Exception('Assessment not found.')
        assessment = db_session.query(AssessmentModel).filter_by(asment_code=asment_code)
        assessment_baseline = AssessmentBaselinesModel(**data)
        assessment_baseline.assessment = assessment
        return CreateAssessmentBaseline(assessment_baseline=assessment_baseline)

class UpdateAssessmentBaseline(graphene.Mutation):
    assessment_baseline = graphene.Field(lambda: AssessmentBaselines, description='Update an assessment baseline.')

    class Arguments:
        assessment_base_id = graphene.Int(required=True)
        input = AssessmentBaselinesInput(required=True)

    def mutate(self, info, assessment_base_id, input):
        exists = db_session.query(
            db_session.query(AssessmentBaselinesModel).filter_by(assessment_base_id=assessment_base_id).exists()
        ).scalar()
        if not exists:
            raise Exception('Assessment Baseline not found.')
        assessment_baseline = db_session.query(AssessmentBaselinesModel).filter_by(assessment_base_id=assessment_base_id).first()
        data = utils.input_to_dictionary(input)
        [setattr(assessment_baseline, key, value) for key, value in data.items()]
        db_session.commit()
        return UpdateAssessmentBaseline(assessment_baseline=assessment_baseline)

class CreateGraduation(graphene.Mutation):
    graduation = graphene.Field(lambda: Graduation, description='Create graduation record for candidate')

    class Arguments:
        input = GraduationInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        exists = db_session.query(
            db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).exists()
        ).scalar()
        if not exists:
            raise Exception('Candidate with brandi_id of {} not found.'.format(data.get('brandi_id')))
        candidate = db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id'))
        #! should add some validation for abnormal dates, also make sure a candidate exists with the provided brandi_id
        graduation = GraduationModel(**data)
        graduation.candidate = candidate
        db_session.add(graduation)
        db_session.commit()
        return CreateGraduation(graduation=graduation)

class UpdateGraduation(graphene.Mutation):
    graduation = graphene.Field(lambda: Graduation, description='Update a graduation record')

    class Arguments:
        grad_id = graphene.Int(required=True)
        input = GraduationInput(required=True)

    def mutate(self, info, grad_id, input):
        exists = db_session.query(
            db_session.query(GraduationModel).filter_by(grad_id=grad_id).exists()
        ).scalar()
        if not exists:
            raise Exception('Graduation record with ID of {} not found.'.format(grad_id))
        #! should add some validation for abnormal dates, also make sure a candidate exists with the provided brandi_id
        graduation = db_session.query(GraduationModel).filter_by(grad_igrad_id)
        [setattr(graduation, key, value) for key,value in data.items()]
        db_session.commit()
        return UpdateGraduation(graduation=graduation)

class CreateTransition(graphene.Mutation):
    transition = graphene.Field(lambda: Transition, description='Create a Transition record.')

    class Arguments:
        input = TransitionInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        exists = db_session.query(
            db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).exists()
        ).scalar()
        if not exists:
            raise Exception('Candidate with ID {} not found.'.format(data.get('brandi_id')))
        candidate = db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).first()
        transition = TransitionModel(**data)
        transition.candidate = candidate
        db_session.add(transition)
        db_session.commit()
        return CreateTransition(Transition=Transition)

class UpdateTransition(graphene.Mutation):
    Transition = graphene.Field(lambda: Transition, description='Update a transis')

    class Arguments:
        trans_id = graphene.Int(required=True)
        input = TransitionInput(required=True)

    def mutate(self, info, trans_id, input):
        exists = db_session.query(
            db_session.query(TransitionModel).filter_by(trans_id=trans_id).exists()
        ).scalar()
        if not exists:
            raise Exception('Transition with ID does not exist.'.format(trans_id))
        data = utils.input_to_dictionary(input)
        transition = db_session.query(TransitionModel).filter_by(trans_id=trans_id).first()
        [setattr(transition, key, value) for key, value in data.items()]
        db_session.commit()
        return UpdateTransition(transition=transition)

class CreateDrop(graphene.Mutation):
    drop = graphene.Field(lambda: Drop, description='Create a drop record for a particular candidate.')

    class Arguments:
        input = DropInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        candidate_exists = db_session.query(
            db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).exists()
        ).scalar()
        drop_reason_exists = db_session.query(
            db_session.query(DropReasonModel).filter_by(drop_code=data.get('drop_code')).exists()
        ).scalar()
        drop_reason_origin_exists = db_session.query(
            db_session.query(DropOriginModel).filter_by(drop_origin_code=data.get('drop_origin_code')).exists()
        ).scalar()
        errors = {}
        if not candidate_exists:
            errors['candidate'] = 'Candidate with ID {} was not found.'.format(data.get('brandi_id'))
        if not drop_reason_exists:
            errors['drop_reason'] = 'The given drop reason ({}) can not be found.'.format(data.get('drop_code'))
        if not drop_reason_origin_exists:
            errors['drop_reason_origin'] = 'The given drop reason ({}) origin can not be found.'.format(data.get('drop_origin_code'))
        if bool(errors):
            raise Exception(' '.join(errors.values()))

        candidate = db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).first()
        drop_reason = db_session.query(DropReasonModel).filter_by(drop_code=data.get('drop_code')).first()
        drop_origin = db_session.query(DropOriginModel).query(drop_origin_code=data.get('drop_origin_code')).first()

        drop = DropModel(**data)
        drop.candidate = candidate
        drop.drop_reason = drop_reason
        drop.drop_origin = drop_origin
        db_session.add(drop)
        db_session.commit()
        return CreateDrop(drop=drop)

class UpdateDrop(graphene.Mutation):
    drop = graphene.Field(lambda: Drop, description='Update a drop record.')

    class Arguments:
        drop_id = graphene.Int(required=True)
        input = DropInput(required=True)

    def mutate(self, info, drop_id, input):
        exists = db_session.query(
            db_session.query(DropModel).filter_by(drop_id=drop_id).exists()
        ).scalar()
        if not exists:
            raise Exception('Drop with given ID ({}) can not be found.'.format(drop_id))
        drop = db_session.query(DropModel).filter_by(drop_id=drop_id).first()
        [setattr(drop, key, value) for key, value in data.items()]
        db_session.commit()
        return UpdateDrop(drop=drop)

class CreateMilitaryProfile(graphene.Mutation):
    military_profile = graphene.Field(lambda: MilitaryAttributes, description='Create a military profile for a candidate')

    class Arguments:
        input = MilitaryAttributeInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        military_profile = MilitaryAttributesModel(**data)
        exists = db_session.query(
            db_session.query(RankModel).filter_by(rank_code=data.get('rank_code')).exists()
        ).scalar()
        if not exists:
            raise Exception('Supplied rank is invalid')
        military_profile.rank = db_session.query(RankModel).filter_by(rank_code=data.get('rank_code')).first()

        exists = db_session.query(
            db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).exists()
        ).scalar()
        if not exists:
            raise Exception('Supplied candidate does not exist')
        military_profile.candidate = db_session.query(CandidateModel).filter_by(brandi_id=data.get('brandi_id')).first()

        exists = db_session.query(
            db_session.query(MosModel).filter_by(mos_code=data.get('mos_code')).exists()
        ).scalar()
        if not exists:
            raise Exception('Supplied Mos code is not valid.')
        military_profile.mos = db_session.query(MosModel).filter_by(mos_code=data.get('mos_code')).first()

        db_session.add(military_profile)
        db_session.commit()
        return CreateMilitaryProfile(military_profile=military_profile)

class UpdateMilitaryProfile(graphene.Mutation):
    military_profile = graphene.Field(lambda: MilitaryAttributes, description='Update a military profile for a candidate')

    class Arguments:
        input = MilitaryAttributeInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        if data.get('mil_id'):
            exists = db_session.query(
                db_session.query(MilitaryAttributesModel).filter_by(mil_id=data.get('mil_id')).exists()
            ).scalar()
            if not exists:
                raise Exception('Military profile does not exist for milId: '.format(data.get('mil_id')))
            military_profile = db_session.query(MilitaryAttributesModel).filter_by(mil_id=data.get('mil_id')).first()
            [setattr(military_profile, key, value) for key, value in data.items()]
            db_session.commit()
            return UpdateMilitaryProfile(military_profile=military_profile)

        else:
            raise Exception('You must specifiy a brandi_id')




class Mutation(graphene.ObjectType):
    auth = AuthMutation.Field()
    refresh = RefreshMutation.Field()
    protected = ProtectedMutation.Field()
    create_candidate = CreateCandidate.Field()
    update_candidate = UpdateCandidate.Field()
    create_class_up = CreateClassUp.Field()
    create_assignment_for_candidate = CreateAssignmentForCandidate.Field()
    update_assignment_for_candidate = UpdateAssignmentForCandidate.Field()
    create_military_profile = CreateMilitaryProfile.Field()
    update_military_profile = UpdateMilitaryProfile.Field()
    create_medical_profile = CreateMedicalProfile.Field()
    update_medical_profile = UpdateMedicalProfile.Field()
    create_personal_profile = CreatePersonalProfile.Field()
    update_personal_profile = UpdatePersonalProfile.Field()
    create_sports_profile = CreateSportsProfile.Field()
    update_sports_profile = UpdateSportsProfile.Field()
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    create_assessment_baseline = CreateAssessmentBaseline.Field()
    update_assessment_baseline = UpdateAssessmentBaseline.Field()
    create_graduation = CreateGraduation.Field()
    update_graduation = UpdateGraduation.Field()
    create_transition = CreateTransition.Field()
    update_transition = UpdateTransition.Field()
    create_drop = CreateDrop.Field()
    update_drop = UpdateDrop.Field()
