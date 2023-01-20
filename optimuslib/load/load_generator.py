"""
Classes and functions for generating load for an application.
"""

from ast import List, Tuple
from typing import Any, List, Tuple
import requests
import time
import subprocess
import re

class LoadGenerator:
    """
    LoadGenerator generates loads for a service and returns
    the metrics obtained from the load.
    """
    
    def __init__(self, service_url: str, load_inputs: List[int]):
        self.service_url = service_url
        self.load_inputs = load_inputs
        
    def __send_request_with_load(self, load: int) -> Tuple[int, bool]:
        """
        Performs a single request to the service with the
        given load and returns the time taken to complete the request
        and if the reponse was a successful once 
        """
        try:
            start_time = time.time()
            load_url = f"{self.service_url}/{load}"
            print(f"performing request : {load_url}")
            response = requests.get(url=load_url)
            if response.status_code == 200:
                end_time = time.time()
                return end_time-start_time, True
            print(response.status_code)    
        except Exception as e:
            return 0, False    


    def get_average_latency(self) -> float:
        """
        Generates the load and returns the latency metrics for the service
        """
        average_latency = 0.0
        success_count = 0
        for load in self.load_inputs:
            time_taken_for_request, success = self.__send_request_with_load(load=load)
            if success:
                success_count += 1
                average_latency += time_taken_for_request
        
        return average_latency/success_count    

    
class ApacheLoadGenerator:
    """
    Load generator for apache httpd server 
    """
    def __init__(self, url: str, time: int) -> None:
        self.url = url 
        self.time = time 

    def get_average_request_per_sec(self) -> int:
        """
        run the Apache Benchmark and return mean
        reqeusts per seconds
        """
        result = subprocess.run(args=[f'ab -t {self.time} -c 50 {self.url}'], shell=True, text=True, capture_output=True)
        output = result.stdout

        requests_per_second_line = re.findall('Requests per second: .* \d+',output)
        requests_per_second = int(requests_per_second_line[0].replace(" ","").split(':')[1])

        return requests_per_second

    def get_average_latency(self) -> int:
        """
        run the Apache Benchmark and return mean.
        average latency.
        """
        result = subprocess.run(args=[f'ab -t {self.time} -c 1000 -n 50000 {self.url}'], shell=True, text=True, capture_output=True)
        output = result.stdout

        requests_per_second_line = re.findall('Time per request: .* \d+',output)
        requests_per_second = int(requests_per_second_line[0].replace(" ","").split(':')[1])

        return requests_per_second    




