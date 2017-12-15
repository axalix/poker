from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import poker, db


migrate = Migrate(poker, db)
manager = Manager(poker)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()