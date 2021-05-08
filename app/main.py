from flask import Flask, jsonify, request

from invalid_usage import InvalidUsage
from validation import validate_message

app = Flask(__name__)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

#create post method to send json values
@app.route("/api/v1", methods=['POST'])
def api() -> str:
    errors = validate_message(request)
    if errors is not None:
        print(errors)
        raise InvalidUsage(errors)
    activities = request.json.get("activities")
    response = {"activities": activities}
    return jsonify(response)

# These two lines are used only while developing.
# In production this code will be run as a module.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

