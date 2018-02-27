import os
from iota.json import JsonEncoder
from flask_script import Manager, Server, prompt_bool
from permanode import init
from permanode.models import db
from permanode.store import Store

app = init('development')
app.json_encoder = JsonEncoder

flask_server = Manager(app)

port = os.getenv('PORT', '9080')
flask_server.add_command('dev', Server(host='0.0.0.0', port=int(port)))


@flask_server.command
def sync():
    db.sync_db()

    if os.getenv('WITH_DUMPS') == 'yes':
        Store()


if __name__ == '__main__':
    flask_server.run()
