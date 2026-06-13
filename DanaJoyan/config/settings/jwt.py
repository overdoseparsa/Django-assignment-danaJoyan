from config.env import env

JWT_SECRET_KEY = env("JWT_SECRET_KEY", default="Your-secret-key")

TOKEN_TYPE = env("TOKEN_TYPE", default="bearer")
