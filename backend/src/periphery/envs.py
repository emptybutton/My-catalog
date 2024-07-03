import typenv


_env = typenv.Env()


class Env:
    mongo_username = _env.str("MONGO_USERNAME")
    mongo_password = _env.str("MONGO_PASSWORD")
    mongo_connecion_uri = _env.str("MONGO_CONNECION_URI")
    kafka_host = _env.str("KAFKA_HOST")
    kafka_port = _env.int("KAFKA_PORT")
