from datetime import datetime
import pytz
from flask_login import current_user

def turno_atual(return_int=False):
    tz = pytz.timezone('America/Sao_Paulo')
    hora_atual = datetime.now(tz).hour
    if 6 <= hora_atual < 12:
        return 'manha' if not return_int else 1
    elif 12 <= hora_atual < 18:
        return 'tarde' if not return_int else 2
    elif 18 <= hora_atual < 22:
        return 'noite' if not return_int else 3
    else:
        return 'madrugada' if not return_int else 0

def usuario_esta_logado():
    return current_user.is_authenticated
