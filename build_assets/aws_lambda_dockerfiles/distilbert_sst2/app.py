import json
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
from tensorflow.keras.models import load_model
model = load_model('./distilbert_sst2')
model_load_end_time = time.time()

def lambda_handler(event, context):
    start_time = time.time()
    json_body = json.loads(event['body'])
    bert_input_ids = np.array(json_body['inputs']['bert_input_ids'])
    bert_input_masks = np.array(json_body['inputs']['bert_input_masks'])
    result = model([bert_input_masks, bert_input_ids])
    end_time = time.time()
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'loading_time': model_load_end_time - model_load_start_time,
            'inference_time': end_time - start_time,
            'body': result.tolist()
        })
    }
    return response