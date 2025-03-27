import azure.functions as func
import fastapi_app

app = func.AsgiFunctionApp(
    app=fastapi_app.app,
    http_auth_level=func.AuthLevel.ANONYMOUS
)
