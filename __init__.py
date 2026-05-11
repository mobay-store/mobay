from flask import Flask

def create_app():
app = Flask(**name**)

```
# config
app.config.from_object("config.Config")

# routes
from app.routes.product_routes import product_bp
app.register_blueprint(product_bp)

return app
```
