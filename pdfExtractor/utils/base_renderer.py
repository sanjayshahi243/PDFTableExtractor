from flask import jsonify

class CustomRenderer:
    def render(self, data, code, headers):
        # Add extra data to the response
        response_data = {'status_code': code, 'data': data}
        return jsonify(response_data)
    
    def __call__(self, data, code, headers):
        return self.render(data, code, headers)

