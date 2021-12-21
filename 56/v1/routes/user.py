from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

from dependency_injector.wiring import inject, Provide

from config import WEAK_PASS_LIST
from injector import MainContainer
from app.v1.models.user import UserService
from v1.schemas import UserRegisterSchema, UserLoginSchema
from v1 import templates

router = APIRouter(prefix='/user')


@router.get('/register', response_class=HTMLResponse)
async def register_html(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


@router.post('/register')
@inject
async def register_user(request: Request, form: UserRegisterSchema = Depends(UserRegisterSchema),
                        user_serv: UserService = Depends(Provide[MainContainer.v1.models.user])):
    if not 8 <= len(form.password) <= 64 or form.password in WEAK_PASS_LIST:
        return JSONResponse({'message': 'Your password is too weak'}, status_code=400)

    await user_serv.insert_with_encrypt(
        username=form.username,
        password=form.password,
        credit_card_number=form.credit_card_number,
        credit_card_pin=form.credit_card_pin,
        credit_card_cvv=form.credit_card_cvv
    )
    return RedirectResponse(url='/user/login')


@router.get('/login', response_class=HTMLResponse)
async def register_html(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/login')
@inject
async def login_user(request: Request, log_data: UserLoginSchema = Depends(UserLoginSchema),
                     user_serv: UserService = Depends(Provide[MainContainer.v1.models.user])):
    if not await user_serv.verify_user_access(log_data.username, log_data.password):
        return JSONResponse({'message': 'Incorrect password'}, status_code=403)
    user = await user_serv.get_decrypted_by_username(log_data.username)

    response_data = user.__dict__

    response_data.pop('_sa_instance_state')
    response_data.pop('password')
    response_data.pop('dek')
    response_data.pop('id')

    return templates.TemplateResponse('data.html', {
        'request': request,
        'username': user.username,
        'card_number': user.credit_card_number,
        'card_pin': user.credit_card_pin,
        'card_cvv': user.credit_card_cvv
    })
