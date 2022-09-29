# I/O Workload Characterization


1- Draw characterization diagrams (visual results):
  
  1.1- Basic diagrams:
    Including:
      a) Read/Write percentage --> 2-D pie chart
      b) Read/Write percentage --> 3-D pie chart
      c) Distribution of I/O sizes --> Total R/W
      d) Distribution of I/O sizes --> Separated R/W
      e) Access frequency distribution
      f) Access frequency --> Cumulative Distribution Funtion (CDF)
      
    *** How to run:
        cd /path/to/source_code/tools/basic_information
        python generate_diagram.py
                  |
                  |---> input: path_to_blkparse_result.txt
                  |
                  |---> output: /path/to/source_code/results/diagram_results
                  
                  
  1.2- Resource utilization diagrams:
    Including:
      a) I/O bandwidth
      b) Disk utilization
      c) CPU utilization
      d) GPU utilization
      
    *** How to run:
        cd /path/to/source_code/tools/resource_utilization
        python resource_utilization.py
                  |
                  |---> input: path_to_iostat_result.txt
                  |
                  |---> output: /path/to/source_code/results/diagram_results  
                  
                  
2- Get textual results (.txt & .csv):
    Including:
      a) Number of Read requests
      b) Number of Write requests
      c) Read size
      d) Write size
      e) Total requests size (R + W)
      f) R/W percentage
      g) MAX/MIN requested addresses
      h) AVG Read and Write
      i) Distribution of I/O Requests (total R/W)
      j) Distribution of I/O Requests (Read)
      k) Distribution of I/O Requests (Write)
      l) Access frequency --> Cumulative Distribution Funtion (CDF)
      m) Access frequency of each address --> .csv file
      
      
    *** How to run:
        cd /path/to/source_code/tools/basic_information
        python generate_text.py
                  |
                  |---> input: path_to_blkparse_result.txt
                  |
                  |---> input: Traced application name
                  |
                  |---> output: /path/to/source_code/results/text_results           
