import os
from project import app

if __name__ == "__main__":
    port = int(os.environ.get("APP_PORT", 5000))
    print(f' *** Starting Flask Server in port {port} *** ')
    app.run(debug=True, port=port)
