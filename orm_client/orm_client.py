import structlog
from sqlalchemy import create_engine
import uuid
import allure


def allure_attach(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        query = kwargs['query'] if kwargs else None
        statement = str(query.compile(compile_kwargs={"literal_binds": True}))
        report_content = (
            f"Query: {statement}\n"
            f"Result: {result}\n"
        )
        allure.attach(
            report_content,
            name="query",
            attachment_type=allure.attachment_type.TEXT
        )

        return result

    return wrapper


class OrmClient:
    def __init__(self, user, password, host, database, isolation_level='AUTOCOMMIT'):
        connection_string = f"postgresql://{user}:{password}@{host}:5432/{database}"
        self.engine = create_engine(connection_string, isolation_level=isolation_level)
        self.db = self.engine.connect()
        self.log = structlog.get_logger(__class__.__name__).bind(service='orm')

    def close_connection(self):
        self.db.close()

    @allure_attach
    def send_query(self, query):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=str(query)
        )
        dataset = self.db.execute(statement=query)
        result = [row for row in dataset]
        log.msg(
            event='response',
            dataset=[dict(row) for row in result]
        )
        return result

    @allure_attach
    def send_bulk_query(self, query):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=str(query)
        )
        self.db.execute(statement=query)
