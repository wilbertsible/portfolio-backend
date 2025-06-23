from flask_restful import Resource
from flask import request, jsonify, current_app
from app.db_helpers import get_mongo_db
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


class ContactMessages(Resource):

    def post(self):
        try:
            data = request.get_json()

            if not data:
                current_app.logger.warning("No JSON data provided in the request.")
                return {"message": "Invalid JSON: Request body must be JSON."}, 400
            required_fields = ['name', 'message']
            for field in required_fields:
                if field not in data or not data[field]:
                    current_app.logger.warning(f"Missing or empty required field:{field}")
                    return {"message":f"Missing or empty required field:'{field}'"}, 400
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')
            if email  is not None and not isinstance(email, str) :
                current_app.logger.warning("Invalid data type for email. Must be a string.")
                return {"message": "Invalid data type for email. Must be a string."}, 400
            if not isinstance(message, str):
                current_app.logger.warning("Invalid data type for message. Must be a string.")
                return {"message": "Invalid data type for message. Must be a string."}, 400
            if not isinstance(name, str):
                current_app.logger.warning("Invalid data type for name. Must be a string or omitted.")
                return {"message": "Invalid data type for name. Must be a string or omitted."}, 400
            
            db = get_mongo_db()
            messages_collection = db.messages

            message_entry = {
                "name": name,
                "message": message,
                "timestamp": datetime.utcnow() # Store creation time
            }
            if email: # Only add name if it was provided and not empty
                message_entry["email"] = email


            result = messages_collection.insert_one(message_entry)
            message_id = str(result.inserted_id)
            current_app.logger.info(f"Message inserted with ID: {message_id}")

            # --- Twilio SMS Notification ---
            try:
                # Retrieve Twilio credentials from environment variables
                account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
                auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
                twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
                my_phone_number = os.environ.get("MY_PHONE_NUMBER") # The number to send the SMS to
                if not all([account_sid, auth_token, twilio_phone_number, my_phone_number]):
                    current_app.logger.warning(
                        "Twilio credentials or recipient number not fully configured. SMS not sent."
                        " Ensure TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, "
                        "and YOUR_PHONE_NUMBER environment variables are set."
                    )
                else:
                    client = Client(account_sid, auth_token)
                    sms_body = f"New Contact Message!\nFrom: {name}\nEmail: {email if email else 'N/A'}\nMessage: {message[:100]}..." # Truncate long messages

                    message_sms = client.messages.create(
                        to=my_phone_number,
                        from_=twilio_phone_number,
                        body=sms_body
                    )
                    current_app.logger.info(f"SMS sent successfully! SID: {message_sms.sid}")

            except TwilioRestException as twilio_e:
                current_app.logger.error(f"Twilio SMS error: {twilio_e}", exc_info=True)
                # You might choose to return an error here, or just log it
                # depending on whether SMS notification is critical for the API call success.
                # For now, we'll log and continue to return 201 for the main operation.
            except Exception as sms_e:
                current_app.logger.error(f"General SMS sending error: {sms_e}", exc_info=True)


            # 6. Return a success response for the API call
            return {
                "message": "Message received successfully!",
                "id": message_id
            }, 201

        except Exception as e:
            current_app.logger.error(f"Error processing contact message: {e}", exc_info=True)
            return {"message": "An internal server error occurred."}, 500