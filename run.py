from app import create_app
from app.routes.auth_routes import auth_routes
from app.routes.manager_routes import manager_routes
from app.routes.user_routes import user_routes
from app.routes.admin_routes import admin_routes
# Create the Flask app using the application factory
app = create_app()

# Registering the route
app.register_blueprint(auth_routes)
app.register_blueprint(manager_routes)
app.register_blueprint(user_routes)
app.register_blueprint(admin_routes)

if __name__ == '__main__':
    # Run the development server
    app.run(host="0.0.0.0", port=5000, debug=True)
