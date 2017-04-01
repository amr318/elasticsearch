from elastic_init import initialize_elasticsearch
from app import app

initialize_elasticsearch()
if __name__ == '__main__':
    app.run(debug=True)