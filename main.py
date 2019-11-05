import os
from project import app

if __name__ == "__main__":
    print("Running main block")
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=True, port=port)
