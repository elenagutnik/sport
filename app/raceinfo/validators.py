from .models import JuryType
from wtforms import ValidationError

def FunctionAllowed(form, field):
    type= JuryType.query.filter(JuryType.id==field.data).first()
    if type.is_member_allowed is not True and form.is_member.data is True:
        raise ValidationError('Тип TechnicalDelegate не  допустим для типа Member')
