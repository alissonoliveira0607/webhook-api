#!/bin/bash

host='host'
req=100
endpoint="http://$host:5000/api/insert_data"

for ((i=1; i<=req; i++))
do
    echo "Executando requisição $i"
    sleep 1

    # Função para gerar uma sequência aleatória de caracteres alfanuméricos
    generate_random_string() {
        cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $1 | head -n 1
    }

    # Gerando JSON aleatório com strings aleatórias
    json_data='{
        "shipment_order_volume_id": '$((RANDOM % 100000))',
        "shipment_order_volume_state": "'$(generate_random_string 10)'",
        "tracking_state": null,
        "created": '$((RANDOM % 10000000000))',
        "created_iso": "'$(date -Iseconds -u)'",
        "provider_message": "'$(generate_random_string 20)'",
        "provider_state": "'$(generate_random_string 6)'",
        "shipper_provider_state": "'$(generate_random_string 3)'",
        "esprinter_message": "'$(generate_random_string 15)'",
        "shipment_volume_micro_state": {
            "id": '$((RANDOM % 100))',
            "code": "'$(generate_random_string 8)'",
            "default_name": "CARGA REDESPACHADA",
            "i18n_name": null,
            "description": "'$(generate_random_string 50)'",
            "shipment_order_volume_state_id": 12,
            "shipment_volume_state_source_id": 2,
            "name": "CARGA REDESPACHADA"
        },
        "attachments": [
            {
                "file_name": "'$(generate_random_string 12).jpg'",
                "mime_type": "image/jpg",
                "type": "OTHER",
                "processing_status": "PROCESSING",
                "additional_information": {
                    "key1": "'$(generate_random_string 8)'",
                    "key2": "'$(generate_random_string 8)'"
                },
                "url": null,
                "created": '$((RANDOM % 10000000000))',
                "created_iso": "'$(date -Iseconds -u)'",
                "modified": '$((RANDOM % 10000000000))',
                "modified_iso": "'$(date -Iseconds -u)'"
            }
        ],
        "shipment_order_volume_state_localized": "Em trânsito",
        "shipment_order_volume_state_history": '$((RANDOM % 100000))',
        "event_date": '$((RANDOM % 10000000000))',
        "event_date_iso": "'$(date -Iseconds -u)'",
        "invoice": {
            "invoice_series": "'$(generate_random_string 4)'",
            "invoice_number": "'$(generate_random_string 4)'",
            "invoice_key": "'$(generate_random_string 32)'"
        },
        "order_number": "'$(generate_random_string 10)'",
        "sales_order_number": "'$(generate_random_string 15)'",
        "tracking_code": "'$(generate_random_string 12)'",
        "volume_number": "1",
        "estimated_delivery_date": {
            "client": {
                "current": '$((RANDOM % 10000000000))',
                "current_iso": "'$(date -Iseconds -u)'",
                "original": '$((RANDOM % 10000000000))',
                "original_iso": "'$(date -Iseconds -u)'"
            },
            "logistic_provider": {
                "current": '$((RANDOM % 10000000000))',
                "current_iso": "'$(date -Iseconds -u)'",
                "original": '$((RANDOM % 10000000000))',
                "original_iso": "'$(date -Iseconds -u)'"
            }
        },
        "tracking_url": "http://status.com/tracking/'$(generate_random_string 40)'"
    }'

    # Enviar a solicitação POST com o JSON aleatório
    echo "$json_data" | curl -X POST "$endpoint" -H "Content-Type: application/json" -d @- | jq
done
