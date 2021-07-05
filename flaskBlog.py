from flaskBlog.config import DevConfig
from flaskBlog import create_app

app=create_app(DevConfig)

if __name__=='__main__':
    app.run()