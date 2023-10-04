from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
import json
import datetime
import os
from dateutil import parser
from prometheus_flask_exporter import PrometheusMetrics
from sqlalchemy.exc import OperationalError
import time

# Cria uma instância do aplicativo Flask
app = Flask(__name__)

# Inicializa o PrometheusMetrics para métricas
metrics = PrometheusMetrics(app)

# Configura a URI do banco de dados a partir de uma variável de ambiente
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# Inicializa o SQLAlchemy com o aplicativo Flask
db = SQLAlchemy(app)

# Configura o registro de logs em um arquivo chamado 'app.log'
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Define a estrutura da tabela no banco de dados usando uma classe SQLAlchemy
class HistoricoEnvio(db.Model):
    # Define as colunas da tabela
    id = db.Column(db.Integer, primary_key=True)
    shipment_order_volume_id = db.Column(db.Integer)
    shipment_order_volume_state = db.Column(db.String(255))
    tracking_state = db.Column(db.String(255))
    created_iso = db.Column(db.String(255))
    provider_message = db.Column(db.String(255))
    shipper_provider_state = db.Column(db.String(255))
    esprinter_message = db.Column(db.String(255))
    shipment_volume_micro_state_id = db.Column(db.Integer, nullable=True)
    shipment_volume_micro_state_code = db.Column(db.String(255))
    shipment_volume_micro_state_default_name = db.Column(db.String(255))
    shipment_volume_micro_state_description = db.Column(db.String(255))
    shipment_volume_micro_state_name = db.Column(db.String(255))
    file_name = db.Column(db.String(255), nullable=True)
    mime_type = db.Column(db.String(255), nullable=True)
    attachment_type = db.Column(db.String(255), nullable=True)
    processing_status = db.Column(db.String(255), nullable=True)
    additional_information = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    attachments_created = db.Column(db.String(255), nullable=True)
    attachments_created_iso = db.Column(db.String(255), nullable=True)
    attachments_modified = db.Column(db.String(255), nullable=True)
    attachments_modified_iso = db.Column(db.String(255), nullable=True)
    shipment_order_volume_state_localized = db.Column(db.String(255), nullable=True)
    shipment_order_volume_state_history = db.Column(db.String(255), nullable=True)
    event_date = db.Column(db.String(255), nullable=True)
    event_date_iso = db.Column(db.String(255), nullable=True)
    invoice_series = db.Column(db.String(255), nullable=True)
    invoice_number = db.Column(db.String(255), nullable=True)
    invoice_key = db.Column(db.String(255), nullable=True)
    order_number = db.Column(db.String(255), nullable=True)
    sales_order_number = db.Column(db.String(255), nullable=True)
    tracking_code = db.Column(db.String(255), nullable=True)
    volume_number = db.Column(db.String(255), nullable=True)
    estimated_delivery_date_client_current = db.Column(db.String(255), nullable=True)
    estimated_delivery_date_client_current_iso = db.Column(db.String(255), nullable=True)
    estimated_delivery_date_client_original = db.Column(db.String(255), nullable=True)
    estimated_delivery_date_client_original_iso = db.Column(db.String(255), nullable=True)
    estimated_delivery_date_logistic_provider_current = db.Column(db.String(255), nullable=True)
    estimated_delivery_date_logistic_provider_current_iso = db.Column(db.String(255), nullable=True)
    estimated_delivery_date_logistic_provider_original = db.Column(db.String(255), nullable=True)
    estimated_delivery_date_logistic_provider_original_iso = db.Column(db.String(255), nullable=True)
    tracking_url = db.Column(db.String(255), nullable=True)    
    
# Função para converter uma data e hora ISO em um formato formatado
def iso_to_formatted_datetime(iso_datetime):
    if iso_datetime:
        datetime_obj = parser.isoparse(iso_datetime)
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return None

# Rota para inserção de dados no banco de dados
@app.route('/api/insert_data', methods=['POST'])
def insert_data():
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            # Decodifica os dados JSON da solicitação
            json_data = request.data.decode('utf-8')
            data = json.loads(json_data)

            history = data.get("history", {})
            attachments = data.get("attachments", {})
            historico = HistoricoEnvio(
                shipment_order_volume_id=data.get("shipment_order_volume_id"),
                shipment_order_volume_state=data.get("shipment_order_volume_state"),
                tracking_state=data.get("tracking_state"),
                created_iso=iso_to_formatted_datetime(data.get("created_iso")),
                provider_message=data.get("provider_message"),
                shipper_provider_state=data.get("shipper_provider_state"),
                esprinter_message=data.get("esprinter_message"),
                shipment_volume_micro_state_id=data.get("shipment_volume_micro_state", {}).get("id"),
                shipment_volume_micro_state_code=data.get("shipment_volume_micro_state", {}).get("code"),
                shipment_volume_micro_state_default_name=data.get("shipment_volume_micro_state", {}).get("default_name"),
                shipment_volume_micro_state_description=data.get("shipment_volume_micro_state", {}).get("description"),
                shipment_volume_micro_state_name=data.get("shipment_volume_micro_state", {}).get("name"),
                file_name=attachments[0].get("file_name"), 
                mime_type=attachments[0].get("mime_type") if attachments else None,
                attachment_type=attachments[0].get("type") if attachments else None,
                processing_status=attachments[0].get("processing_status") if attachments else None,
                additional_information=json.dumps(attachments[0].get("additional_information", {})) if attachments else None,
                url=attachments[0].get("url") if attachments else None,
                attachments_created=attachments[0].get("created") if attachments else None,
                attachments_created_iso=iso_to_formatted_datetime(attachments[0].get("created_iso")) if attachments else None,
                attachments_modified=attachments[0].get("modified") if attachments else None,
                attachments_modified_iso=iso_to_formatted_datetime(attachments[0].get("modified_iso")) if attachments else None,
                shipment_order_volume_state_localized=data.get("shipment_order_volume_state_localized"),
                shipment_order_volume_state_history=data.get("shipment_order_volume_state_history"),
                event_date=data.get("event_date"),
                event_date_iso=iso_to_formatted_datetime(data.get("event_date_iso")),
                invoice_series=data.get("invoice", {}).get("invoice_series"),
                invoice_number=data.get("invoice", {}).get("invoice_number"),
                invoice_key=data.get("invoice", {}).get("invoice_key"),
                order_number=data.get("order_number"),
                sales_order_number=data.get("sales_order_number"),
                tracking_code=data.get("tracking_code"),
                volume_number=data.get("volume_number"),
                estimated_delivery_date_client_current=data.get("estimated_delivery_date", {}).get("client", {}).get("current"),
                estimated_delivery_date_client_current_iso=iso_to_formatted_datetime(data.get("estimated_delivery_date", {}).get("client", {}).get("current_iso")),
                estimated_delivery_date_client_original=data.get("estimated_delivery_date", {}).get("client", {}).get("original"),
                estimated_delivery_date_client_original_iso=iso_to_formatted_datetime(data.get("estimated_delivery_date", {}).get("client", {}).get("original_iso")),
                estimated_delivery_date_logistic_provider_current=data.get("estimated_delivery_date", {}).get("logistic_provider", {}).get("current"),
                estimated_delivery_date_logistic_provider_current_iso=iso_to_formatted_datetime(data.get("estimated_delivery_date", {}).get("logistic_provider", {}).get("current_iso")),
                estimated_delivery_date_logistic_provider_original=data.get("estimated_delivery_date", {}).get("logistic_provider", {}).get("original"),
                estimated_delivery_date_logistic_provider_original_iso=iso_to_formatted_datetime(data.get("estimated_delivery_date", {}).get("logistic_provider", {}).get("original_iso")),
                tracking_url=data.get("tracking_url")
            )

            db.session.add(historico)
            db.session.commit()

            logging.info('Dados inseridos com sucesso!')
            return jsonify({'message': 'Dados inseridos com sucesso!'})
        except OperationalError as e:
            logging.error('Erro de conexão com o banco de dados: %s', str(e))
            retry_count += 1
            time.sleep(10)
            
    if retry_count == max_retries:
        return jsonify({'error': 'Falha na inserção de dados no banco de dados'}), 500

if __name__ == '__main__':
    while True:
        try:
            # Inicializa o servidor Flask para receber solicitações
            app.run(host='0.0.0.0', port=5000)
        except OperationalError as e:
            logging.error('Erro ao executar o servidor Flask: %s', str(e))
            time.sleep(10)