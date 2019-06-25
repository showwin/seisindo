from app import create_app

app = create_app()
# app.config.from_object('config.BaseConfig')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
