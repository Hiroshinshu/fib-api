from flask import Flask, request, jsonify
from collections import OrderedDict

app = Flask(__name__)

def fibo(n):
    if n == 1 or n == 2:
        return 1
    fib = [1, 1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib[n-1]

@app.route("/")
def home():
    return "Enter https://hmsample.f5.si/fib?n=<number> to get the nth fibonacci number."

@app.route('/fib', methods=['GET'])
def get_fibo():
    n = request.args.get('n', default=1)
    try:
        n = int(n)
    except ValueError:
        response = {"status":400, "message":"n must be an integer."}
        return jsonify(response)
    if n <= 0:
        response = {"status":400, "message":"n must be a positive integer."}
        return jsonify(response)
    result = fibo(n)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=443, ssl_context=('/etc/letsencrypt/live/hmsample.f5.si/fullchain.pem', '/etc/letsencrypt/live/hmsample.f5.si/privkey.pem'))