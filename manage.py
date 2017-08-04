# -*- coding: utf-8 -*-
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from application import db, app, config
from sms.models.core import Sms, SmsRecord, Provider


def make_shell_context():
    return dict(app=app, db=db, config=config, Sms=Sms, SmsRecord=SmsRecord, Provider=Provider)


migrate = Migrate(app, db)


manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
