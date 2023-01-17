"""
Flask app to serve a fibonnaci request
"""

from flask import Flask, jsonify
from flask_api import status
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def calculate_nth_fibonacci_term(n) -> int:
    """
    Calculate the nth fibonacci term.

    :param n: the required term
    :return: fibonacci term at the given index
    """
    if n <= 1:
        return n
    return calculate_nth_fibonacci_term(n-1) + calculate_nth_fibonacci_term(n-2)    


@app.route('/fibonacci/<n>')
def get_nth_fibonacci_term(n: int):
    """
    Handle requests to get the nth fibonacci term
    """
    try:
        nth_term = calculate_nth_fibonacci_term(int(n))
        return jsonify({"term":nth_term}), status.HTTP_200_OK
    except Exception as e:
        return f"error at server for processing {n} : {e}", status.HTTP_500_INTERNAL_SERVER_ERROR   


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False, port=5005)