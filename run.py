import os
from tracker import create_app

app = create_app()
app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)
