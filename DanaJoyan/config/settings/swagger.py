SPECTACULAR_SETTINGS = {
    'TITLE': 'DanaJoyan API',
    'DESCRIPTION': 'Transport Management System API',

    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True, 
        'displayRequestDuration': True,
    },
   'SECURITY_DEFINITIONS': {
        'BearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': 'Enter your access token',
        }
    },
    
    # این خط مهمه - باید حتماً باشه
    'SECURITY': [{'BearerAuth': []}],
}