import hashlib
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import urllib.parse


# كلمة المرور المشفرة (تأكد من تشفير كلمة "moksha1999" باستخدام SHA-256)
correct_password_hash = "f10f7a82bce244e8e340bd8bde5cbd04"  # كلمة "moksha1999" مشفرة

# إعدادات السيرفر
PORT = 8080
HOST = "localhost"

# صفحة HTML الخاصة بك
login_page = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dark Web Login</title>
    <style>
        body {
            background-color: #121212;
            color: #0f0;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
            height: 100vh;
            margin: 0;
        }

        #password-container {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 20px;
            border: 3px solid #0f0;
            background-color: #000;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
        }

        h1 {
            color: #ff0000;
            font-size: 30px;
            font-weight: bold;
        }

        input[type="password"] {
            background-color: #1c1c1c;
            border: 1px solid #0f0;
            color: #0f0;
            padding: 10px;
            font-size: 18px;
            width: 200px;
            border-radius: 5px;
        }

        button {
            background-color: #0f0;
            border: none;
            padding: 10px 20px;
            font-size: 18px;
            color: #000;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #00ff00;
        }

        #content {
            display: none;
            padding: 50px;
            text-align: left;
            font-size: 18px;
            line-height: 1.6;
        }

        .error {
            color: #ff0000;
        }

    </style>
    <script>
        function checkPassword() {
            var userPassword = document.getElementById("password").value;
            var correctHash = "''' + correct_password_hash + '''";

            // تشفير كلمة المرور المدخلة باستخدام SHA-256
            var hash = CryptoJS.SHA256(userPassword).toString(CryptoJS.enc.Hex);

            if (hash === correctHash) {
                window.location.href = "/content";  // إعادة توجيه للمحتوى المحمي
            } else {
                alert("Incorrect password!");
            }
        }
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9-1-crypto-js.js"></script>
</head>
<body>
    <div id="password-container">
        <h1>Dark Web Login</h1>
        <p>Enter the password to access the site:</p>
        <input type="password" id="password" placeholder="Enter password" />
        <button onclick="checkPassword()">Submit</button>
        <p id="error-message" class="error"></p>
    </div>
</body>
</html>'''

# صفحة المحتوى المحمي
content_page = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hidden Content</title>
</head>
<body>
    <h1>Welcome to the Hidden Website</h1>
    <p>Access granted. This is the hidden content of the dark web.</p>
    <p>Stay safe online.</p>
</body>
</html>'''


# معالج للطلبات
class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # إذا كان المسار هو /login، قم بإرسال صفحة تسجيل الدخول
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(login_page.encode())

        # إذا كان المسار هو /content، قم بإرسال المحتوى المحمي
        elif self.path == "/content":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content_page.encode())

        else:
            self.send_response(404)
            self.end_headers()

# بدء السيرفر
def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Starting server on http://{HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
