# app.py
from aiohttp import web
from sqlalchemy.orm import Session
from database import get_db, init_db
from services import UserService

async def register_user(request):
    db: Session = next(get_db())
    user_data = await request.json()
    user_service = UserService(db)
    user = user_service.create_user(user_data)
    return web.json_response({"success": True, "user_id": user.du_nativeID})

async def get_user(request):
    db: Session = next(get_db())
    user_id = int(request.match_info['user_id'])
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if user:
        return web.json_response({"success": True, "user": user.__dict__})
    return web.json_response({"success": False, "message": "User not found"}, status=404)

app = web.Application()
app.router.add_post('/api/register', register_user)
app.router.add_get('/api/user/{user_id}', get_user)

if __name__ == '__main__':
    init_db()  # 初始化数据库
    web.run_app(app, host='0.0.0.0', port=8000)