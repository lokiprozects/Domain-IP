# tlclookup.py

from flask import Flask, request, render_template
import socket

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('tlclookup.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    query = request.form['query']
    try:
        # Try to resolve the input as an IP address
        ip = socket.gethostbyname(query)
        # If successful, return IP address and domain name
        domain = socket.gethostbyaddr(ip)[0]
        return f'IP Address: {ip}, Domain Name: {domain}'
    except socket.error:
        try:
            # Try to resolve the input as a domain name
            domain = query
            ip = socket.gethostbyname(query)
            # If successful, return IP address and domain name
            return f'Domain Name: {domain}, IP Address: {ip}'
        except socket.error:
            return 'Invalid input'

if __name__ == '__main__':
    app.run(debug=True)
