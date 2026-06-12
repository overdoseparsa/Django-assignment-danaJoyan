from config.env import env

JWT_SECRET_KEY = env("JWT_SECRET_KEY", default="Your-secret-key")
