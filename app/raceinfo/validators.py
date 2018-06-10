from .models import JuryType
from wtforms import ValidationError

def FunctionAllowed(form, field):
    type= JuryType.query.filter(JuryType.id==field.data).first()
    print("type.is_member_allowed", type.is_member_allowed)
    print("form.is_member.data", form.is_member.data)
    print(type.is_member_allowed is False)
    print(form.is_member.data == 1)
    print(type.is_member_allowed is False and form.is_member.data == 1)
    if type.is_member_allowed is False and form.is_member.data == 1:
        raise ValidationError('Тип TechnicalDelegate не  допустим для типа Member')
