from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from commerce import create_app, db

app = create_app()

if app.config['ENV'] == 'production':
    app.config.from_object('config.Production')
    
else:
    app.config.from_object('config.Development')


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()