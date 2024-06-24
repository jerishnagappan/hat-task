
from your_project.app.models.patent import Patent
from your_project.app.extensions import db
from your_project.app.schemas import PatentSchema
from marshmallow import ValidationError
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('flask_app.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

patent_schema = PatentSchema()

def update_patent_details(patent_id, data):
    schema = PatentSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as e:
        logger.error(f"Validation error in updating patent {patent_id}: {str(e.messages)}")
        return {'error': 'Validation error', 'messages': e.messages}, 400

    patent = Patent.query.get(patent_id)
    if not patent:
        logger.info(f"Patent with id {patent_id} not found for update")
        return {'message': f'Patent with id {patent_id} not found'}, 404

    patent.title = validated_data.get('title', patent.title)
    patent.inventor_name = json.dumps(validated_data.get('inventor_name', []))
    patent.assignee_name_current = json.dumps(validated_data.get('assignee_name_current', []))
    patent.application_number = json.dumps(validated_data.get('application_number', patent.application_number))
    patent.backward_cites_no_family = json.dumps(validated_data.get('backward_cites_no_family', []))
    patent.forward_cites_no_family = json.dumps(validated_data.get('forward_cites_no_family', []))
    patent.pub_date = validated_data.get('pub_date', patent.pub_date)
    patent.grant_date = validated_data.get('grant_date', patent.grant_date)

    try:
        db.session.commit()
        logger.info(f"Patent with id {patent_id} updated successfully")
        return {'message': f'Patent with id {patent_id} updated successfully'}, 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating patent {patent_id}: {str(e)}")
        return {'message': f'Failed to update patent {patent_id}: {str(e)}'}, 500
