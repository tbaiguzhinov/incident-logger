import os
import requests
import time

from dotenv import load_dotenv
from hs_incidents.models import SimpLogin


def authentication():
    logins = SimpLogin.objects.all()
    login = logins[0] if logins else None
    if login:
        current_time = time.time()
        if login.expiration > (current_time + 60*5):
            return login.token
    load_dotenv()
    simp_login = os.getenv('SIMP_LOGIN')
    simp_pass = os.getenv('SIMP_PASS')
    response = requests.post(
        'https://eu.core.resolver.com/user/authenticate',
        json={
            'email': simp_login,
            'password': simp_pass,
            'selectedOrg': 166,
            'client': 'core-client'
        }
    )
    response.raise_for_status()
    token = response.json()['token']
    expiration = int(response.json()['expiresAt'])
    if login:
        login.token = token
        login.expiration = expiration
        login.save()
    else:
        SimpLogin.objects.create(
            token = token,
            expiration = expiration,
        )
    return token


def get_trigger(id):
    token = authentication()
    response = requests.get(
        f'https://eu.core.resolver.com/data/object/{id}/triggers',
        headers={'Authorization': f'bearer {token}'},
    )
    response.raise_for_status()
    triggers = response.json()['data']
    for trigger in triggers:
        if trigger['name'].lower() == 'report incident':
            return trigger['id']


def create_incident(incident):
    token = authentication()
    business_activity_options = {
        'Manufacturing': 207767,
        'Leaf': 207768,
        'Market': 207769,
        'R&D': 210806,
        'GBS': 210808,
        'CSS': 210807,
    }
    incident_classification_options = {
        'Safety': 207765,
        'Health': 207766,
    }
    work_related_options = {
        'Yes': 207772,
        'No': 207773,
    }
    auth_notified_options = {
        'Yes': 207770,
        'No': 207771,
    }
    location_options = {
        'Onsite': 167213,
        'Offsite': 167214,
    }
    data={
        'objectTypeId': 14692, #H&S Incident
        'evaluations': [
            {'fieldId': 69605, 'value': business_activity_options[incident.business_activity]}, # Business Activity
            {'fieldId': 69604, 'value': incident_classification_options[incident.incident_classification]}, # Incident Classification
            {'fieldId': 69607, 'value': work_related_options[incident.work_related]},
            {'fieldId': 69606, 'value': auth_notified_options[incident.auth_notified]}, # Ext. Auth. notification?
            {'fieldId': 51553, 'value': incident.description}, # Incident Description
            {'fieldId': 56759, 'value': location_options[incident.location]}, # Incident Location
            {'fieldId': 37129, 'value': time.mktime(incident.date_occurred.timetuple())}, # Date Occurred
            {'fieldId': 69608, 'value': time.mktime(incident.date_reported.timetuple())}, # Date Reported to Local H&S
        ],
        'relationships': [
            {'relationshipId': 24815, 'value': [71339]} # Country, obviously, Iran
        ],
        'triggerId': 60456, # Add Injury / Illness details
    }
    if incident.business_activity == 'Manufacturing' or incident.business_activity == 'Leaf':
        data['relationships'].append(
            {'relationshipId': 25280, 'value': [1337297]} # Reporting Factory Code
        )
    if incident.location == 'Onsite' and incident.jti_site:
        jti_sites = {
            '1419': 303106,
            '934': 230631,
            '933': 230630,
            '932': 230629,
            '931': 230628,
            '930': 230627,
            '929': 230626,
            '928': 230625,
            '927': 230624,
            '926': 230623,
            '925': 230622,
            '924': 230621,
            '923': 230620,
            '922': 230619,
            '921': 230618,
            '920': 230617,
            '919': 230616,
            '918': 230615,
            '917': 230614,
            '916': 230613,
            '915': 230612,
            '914': 230611,
            '913': 230610,
            '912': 230609,
            '911': 230608,
            '910': 230607,
            '908': 230605,
            '907': 230604,
            '906': 230603,
            '904': 230601,
            '903': 230600,
            '902': 230599,
            '901': 230598,
            '900': 230597,
            '898': 230595,
            '897': 230594,
            '896': 230593,
            '895': 230592,
            '401': 109845,
            '399': 109843,
            '92': 109536,
            '28': 109472,
        }
        data['relationships'].append(
            {'relationshipId': 24814, 'value': [jti_sites[incident.jti_site]]} # JTI Site(s)
        )
    elif incident.location == 'Offsite' and incident.latitude and incident.longitude:
        data['geolocation'] = {
            'geo': {
                'type': 'point',
                'coordinates': [incident.latitude, incident.longitude]
                },
        }
    response = requests.post(
        'https://eu.core.resolver.com/creation/creation',
        headers={'Authorization': f'bearer {token}'},
        json=data,
    )
    response.raise_for_status()
    payload = response.json()
    incident_id = payload['id']
    unique_id = payload['uniqueId']
    severity_options = {
        'Fatality': 207775,
        'LTI': 207776,
        'RWC': 207777,
        'MTC': 207778,
        'First aid': 207779,
    }
    relation_to_business_options = {
        'JTI Employee': 207797,
        'Outsourced': 207798,
        'Contractor': 207799,
        'Public': 207800,
    }
    if incident.incident_classification == 'Health' and incident.illnesses:
        consequence_options = {
            '1': 207880,
            '2': 207881,
            '3': 207882,
            '4': 207883,
            '5': 207884,
            '6': 207885,
        }
        immediate_cause_options = {
            '1': 207886,
            '2': 207887,
            '3': 207888,
            '4': 207889,
            '5': 207890,
            '6': 207891,
        }
        gender_options = {
            '1': 98592,
            '2': 97768,
        }
        for illness in incident.illnesses.all():
            data = {
            'objectTypeId': 14705, # Illness
            'evaluations': [
                {'fieldId': 69610, 'value': severity_options[illness.severity]}, # Severity
                {'fieldId': 69612, 'value': relation_to_business_options[illness.relation_to_business]}, # Relation to Business
                {'fieldId': 69646, 'value': consequence_options[illness.consequence]}, # Consequence
                {'fieldId': 69647, 'value': immediate_cause_options[illness.immediate_cause]}, # Immediate Cause - Occ. Health
                {'fieldId': 69648, 'value': illness.age}, # Age
                {'fieldId': 37097, 'value': gender_options[illness.gender]}, # Gender
            ],
            'parent': 
                {
                    'inverse': False,
                    'objectId': incident_id,
                    'relationshipTypeId': 24830
                }, # Linking back to Incident
            'triggerId': 60537, # Create
            }
            token = authentication()
            response = requests.post(
                'https://eu.core.resolver.com/creation/creation',
                headers={'Authorization': f'bearer {token}'},
                json=data,
            )
            response.raise_for_status()
    if incident.incident_classification == 'Safety' and incident.injuries:
        immediate_cause_options = {
            '1': 207780,
            '2': 207781,
            '3': 207782,
            '4': 207783,
            '5': 207784,
            '6': 207785,
            '7': 207786,
            '8': 207787,
            '9': 207788,
            '10': 207789,
            '11': 207790,
            '12': 207791,
            '13': 207792,
            '14': 207793,
            '15': 207794,
            '16': 207795,
            '17': 207796,
        }
        for injury in incident.injuries.all():
            data = {
            'objectTypeId': 14693, # Injury
            'evaluations': [
                {'fieldId': 69610, 'value': severity_options[injury.severity]}, # Severity
                {'fieldId': 69611, 'value': immediate_cause_options[injury.immediate_cause]}, # Immediate Cause - Safety
                {'fieldId': 69612, 'value': relation_to_business_options[injury.relation_to_business]}, # Relation to Business
            ],
            'parent': 
                {
                    'inverse': False,
                    'objectId': incident_id,
                    'relationshipTypeId': 24816
                }, # Linking back to Incident
            'triggerId': 60459, # Add Injury / Illness details
            }
            token = authentication()
            response = requests.post(
                'https://eu.core.resolver.com/creation/creation',
                headers={'Authorization': f'bearer {token}'},
                json=data,
            )
            response.raise_for_status()
    submission_trigger = get_trigger(incident_id)
    token = authentication()
    response = requests.post(
        f'https://eu.core.resolver.com/data/object/{incident_id}/trigger/{submission_trigger}/go',
        headers={'Authorization': f'bearer {token}'},
    )
    response.raise_for_status()
    return unique_id

def update_incident(incident):
    pass