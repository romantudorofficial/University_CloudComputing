from pydantic import BaseSettings



class Settings (BaseSettings):

    '''
        Configuration settings for the application.
    '''

    # JWT settings.
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str


    class Config:

        '''
            Configuration for the Pydantic settings.
            This specifies that the settings should be loaded from a .env file.
        '''

        env_file = ".env"



# Create an instance of the Settings class to load the configuration.
settings = Settings()