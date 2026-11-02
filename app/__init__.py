from pathlib import Path
from flask import Flask, render_template
from .cli import register_cli
from .config import Config
from .extensions import csrf, db, limiter, login_manager

def create_app(config_class=Config):
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_object(config_class)
    Path(app.instance_path).mkdir(parents=True,exist_ok=True)
    for key in ("UPLOAD_FOLDER","GENERATED_FOLDER","TEMP_FOLDER"):
        Path(app.config[key]).mkdir(parents=True,exist_ok=True)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        try: return User.from_row(db.fetchone("SELECT * FROM users WHERE id=%s LIMIT 1",(int(user_id),)))
        except (TypeError,ValueError): return None
    from .main import main
    from .auth import auth
    from .dashboard import dashboard
    from .certificates import certificates
    from .users import users
    from .colleges import colleges
    from .profile import profile
    app.register_blueprint(main); app.register_blueprint(auth,url_prefix="/auth"); app.register_blueprint(dashboard,url_prefix="/dashboard")
    app.register_blueprint(certificates,url_prefix="/certificates"); app.register_blueprint(users,url_prefix="/users"); app.register_blueprint(colleges,url_prefix="/colleges"); app.register_blueprint(profile,url_prefix="/profile")
    register_cli(app)
    @app.context_processor
    def inject_company():
        return {"company_name":app.config["COMPANY_NAME"],"company_email":app.config["COMPANY_EMAIL"],"company_phone":app.config["COMPANY_PHONE"],"company_address":app.config["COMPANY_ADDRESS"]}
    @app.errorhandler(400)
    def bad_request(error): return render_template("errors/400.html"),400
    @app.errorhandler(403)
    def forbidden(error): return render_template("errors/403.html"),403
    @app.errorhandler(404)
    def not_found(error): return render_template("errors/404.html"),404
    @app.errorhandler(413)
    def request_too_large(error): return render_template("errors/400.html"),413
    @app.errorhandler(429)
    def too_many_requests(error): return render_template("errors/429.html"),429
    @app.errorhandler(500)
    def internal_server_error(error): return render_template("errors/500.html"),500
    return app
