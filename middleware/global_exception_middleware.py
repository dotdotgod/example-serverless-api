from fastapi import Request
from fastapi.responses import JSONResponse


async def global_error_handler(request: Request, call_next):
    try:
        # 모든 요청을 처리하기 전에 실행할 코드
        response = await call_next(request)
        return response
    except Exception as e:
        # 예외가 발생한 경우 처리
        return JSONResponse(status_code=500, content={"detail": str(e)})
