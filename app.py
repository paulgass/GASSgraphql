from flask import Flask 
from flask_graphql import GraphQLView
from flask_cors import CORS
from flask_graphql_auth import GraphQLAuth
from models import db_session
from schema import schema

app = Flask(__name__)
auth = GraphQLAuth(app)
CORS(app)
app.debug = True

app.config["JWT_SECRET_KEY"] = "something"  # change this!
app.config["REFRESH_EXP_LENGTH"] = 30
app.config["ACCESS_EXP_LENGTH"] = 10

app.add_url_rule(
    '/',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema, 
        graphiql=True
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()
