from faststream.kafka import KafkaBroker

from periphery.envs import Env


kafka_broker = KafkaBroker(f"{Env.kafka_host}:{Env.kafka_port}")
