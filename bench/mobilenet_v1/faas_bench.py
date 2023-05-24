#preprocessing library
from mobilenet_v1 import preprocessing
import numpy as np

#REST 요청 관련 library
from module import module_faas
import json

#병렬처리 library
import concurrent.futures

def run_bench(num_tasks, server_address):
    image_file_path = "../../dataset/imagenet/imagenet_1000_raw/n01843383_1.JPEG"
    
    data = json.dumps({"inputs": { "input_1": preprocessing.run_preprocessing(image_file_path).tolist()}})

    # REST 요청 병렬 처리
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_tasks) as executor:
        futures = [executor.submit(lambda: module_faas.predict(server_address, data)) for _ in range(num_tasks)]
    
    inference_times = []
    network_latency_times = []
    for future in concurrent.futures.as_completed(futures):
        result, thread_elapsed_time = future.result()
        inference_times.append(result['inference_time'])
        network_latency_times.append(thread_elapsed_time)

    return inference_times, network_latency_times
