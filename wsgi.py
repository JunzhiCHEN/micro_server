#!/env/python
#import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)