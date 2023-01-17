"""
Classes and functions for generating load for an application.
"""

from ast import List, Tuple
from typing import Any, List, Tuple
import requests
import time


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

    
