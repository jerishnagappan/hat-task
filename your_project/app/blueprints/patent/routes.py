
from flask import Blueprint, request, jsonify,current_app
from your_project.app.extensions import db
from your_project.app.models.patent import Patent
from your_project.app.schemas import PatentSchema
from marshmallow import ValidationError
import json
import logging
from your_project.test import scrape_patent_data, store_patent_in_db ,get_pat_data 

from datetime import datetime, timedelta


from your_project.app.service_update import update_patent_details









logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  

file_handler = logging.FileHandler('flask_app.log')
file_handler.setLevel(logging.DEBUG)  

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)

patent_schema = PatentSchema()
patents_bp = Blueprint('patents', __name__)


@patents_bp.route('/get_patent_details', methods=['GET'])
def get_patent_details():
    with current_app.app_context():
        patnum = request.args.get('patnum')

        if not patnum:
            logger.error("No patnum provided in GET request")
            return jsonify({"error": "No patnum provided"}), 400

        try:
            patent = Patent.query.filter_by(patnum=patnum).first()

            if patent:
                logger.info(f"Patent {patnum} found in the database")
                return jsonify(patent.to_dict()), 200
            else:
                patent_data = get_pat_data(patnum)
                store_patent_in_db(patnum, patent_data)
                logger.info(f"Scraped and stored patent data for {patnum}")
                return jsonify(patent_data), 200

        except Exception as e:
            logger.error(f"Error fetching or storing patent {patnum}: {str(e)}")
            return jsonify({"error": f"Failed to fetch or store patent: {str(e)}"}), 500




@patents_bp.route('/delete_patents_details/<int:patent_id>', methods=['DELETE'])




@patents_bp.route('/delete_patents_details', methods=['DELETE'])
def delete_patent_details():
    try:
        data = request.get_json()
        patnum_list = data.get('patnum', [])

        if not isinstance(patnum_list, list):
            return jsonify({'error': 'Input should be a list of patnum'}), 400

        for patnum in patnum_list:
            patent = Patent.query.filter_by(patnum=patnum).first()

            if patent:
                db.session.delete(patent)
                db.session.commit()
                logger.info(f"Deleted patent with patnum {patnum}")
            else:
                logger.info(f"Patent with patnum {patnum} not found")

        return jsonify({'message': 'Patents deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting patents: {str(e)}")
        return jsonify({'error': str(e)}), 500
    





# @patents_bp.route('/delete_patents_details/<int:patent_id>', methods=['DELETE'])
# def delete_patent_details(patent_id):
#     try:
#         patent = Patent.query.get_or_404(patent_id)

        
#         logger.info(f"Deleting patent with id {patent_id}")

        
#         patent.title = None

    
#         db.session.commit()

    
#         logger.info(f"Patent with id {patent_id} title deleted successfully")

#         return jsonify({'message': 'Title deleted successfully'}), 200

#     except Exception as e:
#         db.session.rollback()

        
#         logger.error(f"Error deleting patent with id {patent_id}: {str(e)}")

#         return jsonify({'error': str(e)}), 500

# @patents_bp.route('/update_patent_details/<int:patent_id>', methods=['PUT'])



# def update_patent_details(patent_id):
#     if request.method == 'PUT':
#         data = request.get_json()

#         schema = PatentSchema()
#         try:
#             validated_data = schema.load(data)
#         except ValidationError as e:
#             logger.error(f"Validation error in updating patent {patent_id}: {str(e.messages)}")
#             return jsonify({'message': 'Validation error', 'errors': e.messages}), 400

    
#         patent = Patent.query.get(patent_id)
#         if not patent:
#             logger.info(f"Patent with id {patent_id} not found for update")
#             return jsonify({'message': f'Patent with id {patent_id} not found'}), 404

        
#         patent.title = validated_data.get('title', patent.title)
#         patent.inventor_name = json.dumps(validated_data.get('inventor_name', []))
#         patent.assignee_name_current = json.dumps(validated_data.get('assignee_name_current', []))
#         patent.application_number = json.dumps(validated_data.get('application_number', patent.application_number))
#         patent.backward_cites_no_family = json.dumps(validated_data.get('backward_cites_no_family', []))
#         patent.forward_cites_no_family = json.dumps(validated_data.get('forward_cites_no_family', []))
#         patent.pub_date = (validated_data.get('pub_date', patent.pub_date))
#         patent.grant_date = (validated_data.get('grant_date',patent.grant_date))

#         try:
#             db.session.commit()
#             logger.info(f"Patent with id {patent_id} updated successfully")
#             return jsonify({'message': f'Patent with id {patent_id} updated successfully'}), 200
#         except Exception as e:
#             db.session.rollback()
#             logger.error(f"Error updating patent {patent_id}: {str(e)}")
#             return jsonify({'message': f'Failed to update patent {patent_id}: {str(e)}'}), 500

#     else:
#         logger.warning('Use PUT method to update patent details')
#         return jsonify({'message': 'Use PUT method to update patent details'}), 405
    
@patents_bp.route('/update_patent_details/<int:patent_id>', methods=['PUT'])
def update_patent_details_route(patent_id):
    data = request.get_json()
    return update_patent_details(patent_id, data)







# def update_patent_details(patent_id):
#     if request.method == 'PUT':
#         data = request.get_json()

        
#         schema = PatentSchema()
#         try:
#             validated_data = schema.load(data)
#         except ValidationError as e:
#             return jsonify({'message': 'Validation error', 'errors': e.messages}), 400

        
#         patent = Patent.query.get(patent_id)
#         if not patent:
#             return jsonify({'message': f'Patent with id {patent_id} not found'}), 404

#         patent.title = validated_data.get('title', patent.title)
#         patent.inventor_name = json.dumps(validated_data.get('inventor_name', []))
#         patent.assignee_name_current = json.dumps(validated_data.get('assignee_name_current', []))
#         patent.application_number = json.dumps(validated_data.get('application_number',patent.application_number))
#         patent.backward_cites_no_family = json.dumps(validated_data.get('backward_cites_no_family',[]))
#         patent.forward_cites_no_family = json.dumps(validated_data.get('forward_cites_no_family',[]))
#         patent.pub_date = json.dumps(validated_data.get('pub_date',patent.pub_date))
        
#         db.session.commit()

#         return jsonify({'message': f'Patent with id {patent_id} updated successfully'}), 200

#     else:
#         return jsonify({'message': 'Use PUT method to update patent details'}), 405



    


# def delete_patent(patnum):
#     try:
#         patent = Patent.query.filter_by(patnum=patnum).first()  
#         if not patent:
#             logger.info(f"Patent with title '{patnum}' not found for delete")
#             return jsonify({'message': f'Patent with title "{patnum}" not found'}), 404

#         db.session.delete(patent)
#         db.session.commit()
#         logger.info(f"Patent with title '{patnum}' deleted successfully")
#         return jsonify({'message': f'Patent with title "{patnum}" deleted successfully'}), 200

#     except Exception as e:
#         logger.error(f"Error deleting patent with title '{patnum}': {str(e)}")
#         return jsonify({'message': f'Failed to delete patent with title "{patnum}": {str(e)}'}), 500


#     else:
#         logger.warning('Use PUT method to update patent details')
#         return jsonify({'message': 'Use PUT method to update patent details'}), 405


    
        
# def delete_patent_details(patent_id):
#     try:
#         patent = Patent.query.get_or_404(patent_id)

#         # Check request data to determine which fields to delete
#         data = request.get_json()
#         if data:
#             if 'title' in data and data['title']:
#                 patent.title = None
#             if 'application_number' in data and data['application_number']:
#                 patent.application_number = None
#             if 'inventor_name' in data and data['inventor_name']:
#                 patent.inventor_name = None

#         db.session.commit()
#         return jsonify({'message': 'Fields deleted successfully'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500    








