from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from .auth_config import idp, require_roles, ROLES, SAML_SETTINGS
from python3_saml import OneLogin_Saml2_Auth
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
import json

app = FastAPI(title="AppInventory API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Keycloak authentication
idp.add_swagger_config(app)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/auth/login")
async def login():
    """Redirect to Keycloak login page"""
    return RedirectResponse(url=idp.login_uri)

@app.get("/auth/callback")
async def callback(session_state: str, code: str):
    """Handle OAuth callback"""
    return await idp.process_callback(session_state=session_state, code=code)

@app.get("/auth/logout")
async def logout():
    """Handle logout"""
    return RedirectResponse(url=idp.logout_uri)

# SAML routes
@app.get("/saml/metadata")
async def saml_metadata():
    """Serve SAML metadata"""
    auth = OneLogin_Saml2_Auth(request, SAML_SETTINGS)
    metadata = auth.get_settings().get_sp_metadata()
    return JSONResponse(
        content=metadata,
        headers={"Content-Type": "application/xml"},
    )

@app.post("/saml/acs")
async def saml_acs(request: Request):
    """Handle SAML Assertion Consumer Service"""
    auth = OneLogin_Saml2_Auth(request, SAML_SETTINGS)
    auth.process_response()
    errors = auth.get_errors()
    
    if errors:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"SAML Authentication failed: {', '.join(errors)}"
        )
    
    if not auth.is_authenticated():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="SAML Authentication failed"
        )
    
    # Get user attributes from SAML assertion
    attributes = auth.get_attributes()
    
    return {
        "message": "Successfully authenticated",
        "attributes": attributes
    }

# Protected routes example
@app.get("/api/protected")
@require_roles([ROLES["user"]])
async def protected_route(user=Depends(idp.get_current_user)):
    """Example protected route"""
    return {"message": "This is a protected route", "user": user}

@app.get("/api/admin")
@require_roles([ROLES["admin"]])
async def admin_route(user=Depends(idp.get_current_user)):
    """Example admin route"""
    return {"message": "This is an admin route", "user": user}
