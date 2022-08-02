from django.core.management import call_command

# symptoms
call_command('loaddata', 'tipo_respuestas')
call_command('loaddata', 'preguntas')
call_command('loaddata', 'sintomas_categorias')
call_command('loaddata', 'sintomas')

# pollens
call_command('loaddata', 'grupos_polinicos')
call_command('loaddata', 'polens')

# information
call_command('loaddata', 'notificaciones')
call_command('loaddata', 'terminos_condiciones')
