# flake8: noqa

# VALIDATIONS
passwords_should_match = 'Las contraseñas no coinciden'
email_already_created = 'Ya existe un usuario registrado con esa dirección de correo electrónico.'
valid_email = 'Introduzca una dirección de correo electrónico válida.'
valid_neighboor = 'El barrio no puede ser vacío.'
empty_field = 'Este campo es requerido.'

# SYMPTOMS
low_critical_alert = 'Te sugerimos iniciar el tratamiento recetado e ingresar tus síntomas en el diario al menos una vez al día, por una semana.'
medium_critical_alert = 'Te sugerimos iniciar el tratamiento recetado y consultar con tu médico.'
high_critical_alert = 'Por favor, agendá una consulta con tu médico.'

# NOTIFICATIONS
diary_reminder = {'title': 'Recordatorio', 'body': 'No olvides agregar una nueva entrada en el diario de síntomas!'}
critical_reports = {'title': 'Nuevo reporte', 'body': 'Hay un nuevo reporte de pólen en el aire, visitá la app para más información.'}


# EMAILS
email_confirmation = {'subject': '[MIA] Por favor confirmar dirección de correo electrónico', 'body': 'Bienvenido a MIA! \n\nEstás recibiendo este correo electrónico porque se creó una cuenta con el mail {} \n\nPara confirmar que esto es correcto, clickea desde el celular en el siguiente link: \n {} \n\nGracias!'}
reset_password = {'subject': '[MIA] Cambiar contraseña', 'body': 'Le enviamos este email porque Ud. ha solicitado que se reestablezca la contraseña para su cuenta de usuario en MIA. \n\nPor favor visite la página que se muestra a continuación y elija una nueva contraseña: \n\n{}\n\nGracias!'}