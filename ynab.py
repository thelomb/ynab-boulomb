from application import db, create_app
from application.models import (Budget,
                                Account,
                                Category,
                                Transaction,
                                )

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Budget': Budget,
            'Account': Account,
            'Category': Category,
            'Transaction': Transaction
            }
