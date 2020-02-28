from graphql_relay.node.node import from_global_id
import re

def input_to_dictionary(input):
    """Method to convert Graphene inputs into dictionary"""
    dictionary = {}
    for key in input:
        # Convert GraphQL global id to database id
        # if key[-2:] == 'id':
        #     input[key] = from_global_id(input[key])[1]
        dictionary[key] = input[key]
    return dictionary

def validate(model, data):
    errors = {}
    if model == 'Candidate':
        if not data.get('first_name'):
            errors['firstName'] = "First name is required"
        if not data.get('last_name'):
            errors['lastName'] = 'Last name is required'
        if not data.get('phone_number'):
            errors['phoneNumber'] = 'Phone number is required'
        if not data.get('home_of_record'):
            errors['homeOfRecord'] = 'Home of record is required'
        if not data.get('sex'):
            errors['sex'] = 'Sex is required'
        if not data.get('arrival_date'):
            errors['arrivalDate'] = 'Arrival date is required'
    elif model == 'Event':
        if not data.get('brandi_id'):
            errors['brandi_id'] = 'Candidate ID is required.'
        if not data.get('assmt_code'):
            errors['assmt_code'] = 'Assessment code is required.'
        if not data.get('score'):
            errors['score'] = 'Event score is required'
        if not data.get('grader'):
            errors['grader'] = 'Grader is required'
    return errors

def clean(data):
    # *clean* data, strip - out of phone number and SSN
    if data.get('phone_number'):
        data['phone_number'] = re.sub('[^\d]','',data['phone_number'])
    if data.get('social_security_number'):
        data['social_security_number'] = re.sub('[^\d]','',data['social_security_number'])
    return data
