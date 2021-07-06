from Blogg.config import DevConfig
from Blogg import create_app

app=create_app(DevConfig)

if __name__=='__main__':
    app.run()