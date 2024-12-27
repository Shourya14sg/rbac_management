from fastapi import FastAPI
import uvicorn
from app.auth.router_auth import router_auth
from app.routes.router_dashboard import router_dashboard
from app.routes.router_admin import router_admin
from app.routes.router_viewer import router_view
from fastapi.responses import HTMLResponse

app = FastAPI()
app.include_router(router_auth,prefix="/auth",tags=["Authentication"])
#app.include_router(router_dashboard)
app.include_router(router_dashboard,prefix="/dashboard")
app.include_router(router_admin,prefix="/admin",tags=["Admin"])
app.include_router(router_view,prefix="/viewer",tags=["Viewer"])
@app.get("/",response_class=HTMLResponse)
def index():
    return """<html>
            <body style="background-color: #f0f0f0; font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1>RBAC-project</h1>
            <a href="/docs">Open SwaggerUI</a>
            </body>
        </html>"""

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
