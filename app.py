import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from datetime import datetime
import logging
import sys

from authlib.integrations.flask_client import OAuth
from authlib.integrations.base_client.errors import OAuthError
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

# Explicit logging configuration (stdout)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
app.logger.handlers = []
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Explicit structured logging function as required
def log_event(event, user_id=None, email=None, route=None, severity="info"):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event,
        "user_id": user_id,
        "email": email,
        "route": route,
        "ip": request.remote_addr,
    }
    if severity == "info":
        app.logger.info(json.dumps(log_entry))
    else:
        app.logger.warning(json.dumps(log_entry))

@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    try:
        token = oauth.auth0.authorize_access_token()
        userinfo = token.get("userinfo")

        session["user"] = token

        # Explicit structured logging for EVERY successful login clearly defined as required
        log_event(
            event="login_success",
            user_id=userinfo.get("sub"),
            email=userinfo.get("email"),
            route="/callback",
            severity="info"
        )

        # Additionally providing the clear visual message you want 
        app.logger.info("✅ Successful login")

        return redirect("/")
    except OAuthError as e:
        # Structured logging for every failed login attempt
        log_event(
            event="login_failure",
            route="/callback",
            severity="warning"
        )
        # your requested clear visual message:
        app.logger.warning(f"⚠️ Failed login attempt: {str(e)}")
        return redirect("/")

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {"returnTo": url_for("home", _external=True), "client_id": env.get("AUTH0_CLIENT_ID")},
            quote_via=quote_plus,
        )
    )

@app.route("/protected")
def protected():
    user = session.get("user")
    if user and "userinfo" in user:
        # Explicit logs for each authorized access structured clearly
        log_event(
            event="protected_access",
            user_id=user["userinfo"].get("sub"),
            email=user["userinfo"].get("email"),
            route="/protected",
            severity="info"
        )
        # clearly labeled success for visual clarity
        app.logger.info("✅ Authorized access to protected route")
        return f"Hello {user['userinfo'].get('name')}! You are viewing a protected page."
    else:
        # Explicitly structured logs clearly present for unauthorized attempts
        log_event(
            event="unauthorized_access",
            route="/protected",
            severity="warning"
        )
        # your requested visual message clearly displayed
        app.logger.warning("⚠️ Unauthorized access attempt to protected route")
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(env.get("PORT", 3000)), debug=True)
