from django.core.management import call_command

call_command('loaddata', 'tipo_respuestas')
call_command('loaddata', 'preguntas')
call_command('loaddata', 'sintomas_categorias')
call_command('loaddata', 'sintomas')
