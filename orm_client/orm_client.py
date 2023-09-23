import uuid
import json
import allure
import structlog
import datetime
from sqlalchemy import create_engine


def allure_attach(fn):
    def wrapper(*args, **kwargs):
        def datetime_serializer(o):
            if isinstance(o, datetime.datetime):
                return o.isoformat()
            raise TypeError("Object not serializable")

        query = kwargs.get('query') if 'query' in kwargs else args[1]
        if query is None:
            raise ValueError("Parameter 'query' is missing or is None.")
        compiled_query_str = str(query.compile(compile_kwargs={"literal_binds": True}))

        allure.attach(
            compiled_query_str,
            name='SQL query',
            attachment_type=allure.attachment_type.TEXT
        )
        result = fn(*args, **kwargs)

        if result:
            formatted_results = [dict(row) for row in result]
            allure.attach(
                json.dumps(formatted_results, indent=4, ensure_ascii=False, default=datetime_serializer),
                name='Query result',
                attachment_type=allure.attachment_type.JSON
            )

        return result

    return wrapper


class OrmClient:
    def __init__(self, user, password, host, database, isolation_level='AUTOCOMMIT'):
        connection_string = f"postgresql://{user}:{password}@{host}/{database}"
        self.engine = create_engine(connection_string, isolation_level=isolation_level)
        self.db = self.engine.connect()
        self.log = structlog.getLogger(self.__class__.__name__).bind(service='db')

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
