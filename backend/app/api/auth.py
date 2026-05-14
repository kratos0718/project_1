import httpx
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config.settings import get_settings

security = HTTPBearer(auto_error=False)

# Simple cache for JWKS to avoid fetching on every request
_jwks_cache = {}

async def fetch_jwks(issuer_url: str) -> dict:
    if issuer_url in _jwks_cache:
        return _jwks_cache[issuer_url]
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{issuer_url}/.well-known/jwks.json")
        response.raise_for_status()
        jwks = response.json()
        _jwks_cache[issuer_url] = jwks
        return jwks

async def verify_token(credentials: HTTPAuthorizationCredentials | None = Security(security)) -> dict:
    settings = get_settings()
    
    if not settings.clerk_issuer_url:
        # Fallback for local development if Clerk is not configured
        return {"sub": "local_mock_user", "role": "admin"}

    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = credentials.credentials
    try:
        unverified_header = jwt.get_unverified_header(token)
        jwks = await fetch_jwks(settings.clerk_issuer_url)
        
        rsa_key = {}
        for key in jwks.get("keys", []):
            if key["kid"] == unverified_header.get("kid"):
                rsa_key = key
                break
        
        if rsa_key:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(rsa_key)
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                issuer=settings.clerk_issuer_url
            )
            return payload
        else:
            raise HTTPException(status_code=401, detail="Invalid JWT signature key")
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Could not validate credentials: {str(e)}")
