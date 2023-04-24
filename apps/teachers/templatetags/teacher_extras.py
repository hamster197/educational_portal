from django import template

register = template.Library()

@register.simple_tag
def get_quize_rezult(rezult_queryset, user_pk, ):
    user_rezult = rezult_queryset.get(pk=user_pk)
    rezult_string = 'estimation ' + str(user_rezult.get_estimation())
    rezult_string += ' correct answers ' + str(user_rezult.get_correct_answers())
    rezult_string += ' percent ' + str(user_rezult.get_correct_answers_percent())

    return rezult_string