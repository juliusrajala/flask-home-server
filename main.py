import os
from project import app

if __name__ == "__main__":
    port = int(os.environ.get("APP_PORT", 5000))
    secret_key = str(os.environ.get("SECRET_KEY", ''))
    if secret_key == '':
        raise Exception('Bad key')
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # Temp
    print(f' *** Starting Flask Server in port {port} *** ')
    app.run(host='0.0.0.0', debug=True, port=port)
