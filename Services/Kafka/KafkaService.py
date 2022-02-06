from confluent_kafka import SerializingProducer
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer
import logging

class KafkaService:

    def __init__(self, bootstrap_server, schema_registry=None) -> None:
        self.bootstrap_server = bootstrap_server
        if schema_registry is not None:
            self.schema_registry_client = SchemaRegistryClient(
                {'url': schema_registry})

    def send_message_schema(self, objects, topic, subject):
        try:
            producer_configs = {'bootstrap.servers': self.bootstrap_server,
                                'key.serializer': StringSerializer('utf_8'),
                                'value.serializer': self.__get_serializer(subject)}

            producer = SerializingProducer(producer_configs)

            for object in objects:
                producer.produce(topic, value=object["payload"], key=object["key"], headers=object["header"], on_delivery=self.__delivery_report)

            producer.flush()
        except Exception as error:
            logging.error(f'Error sending messages: {error}')
            raise


    def send_message(self, objects, topic):
        try:
            producer = Producer({'bootstrap.servers': self.bootstrap_server})
            
            for object in objects:
                producer.produce(topic, value=str(object["payload"]).encode('utf-8'), key=object["key"], headers=object["header"], on_delivery=self.__delivery_report)
                producer.poll(0.1)
                producer.flush()
        except Exception as error:
            logging.error(f'Error on producing message {topic}. Error: {error}')

            

    def __get_serializer(self, subject):
        avro_str = self.__get_avro_schema(
            self.schema_registry_client, subject)

        return AvroSerializer(
            schema_registry_client=self.schema_registry_client,
            schema_str=avro_str,
            to_dict=self.__serialize_event)

    def __delivery_report(self, err, msg):
        if err is not None:
            logging.error(f'Message delivery failed: {err}')
        else:
            logging.info(f"Message Delivered - Key: {msg.key()} - Value: {msg.value()}")


    def __serialize_event(self, event: dict, memis):
        return event

    def __get_avro_schema(self, schema_registry_client, subject_name):
        return schema_registry_client.get_latest_version(subject_name).schema.schema_str
