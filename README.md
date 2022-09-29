# I/O Workload Characterization


1- Draw characterization diagrams (visual results):
  
  1.1- Basic diagrams:__
    Including:__
      a) Read/Write percentage --> 2-D pie chart__
      b) Read/Write percentage --> 3-D pie chart__
      c) Distribution of I/O sizes --> Total R/W__
      d) Distribution of I/O sizes --> Separated R/W__
      e) Access frequency distribution__
      f) Access frequency --> Cumulative Distribution Funtion (CDF)
      
    *** How to run:
        cd /path/to/source_code/tools/basic_information
        python generate_diagram.py
                  |
                  |---> input: path_to_blkparse_result.txt
                  |
                  |---> output: /path/to/source_code/results/diagram_results
                  
                  
  1.2- Resource utilization diagrams:__
    Including:__
      a) I/O bandwidth__
      b) Disk utilization__
      c) CPU utilization__
      d) GPU utilization__
      
    *** How to run:
        cd /path/to/source_code/tools/resource_utilization
        python resource_utilization.py
                  |
                  |---> input: path_to_iostat_result.txt
                  |
                  |---> output: /path/to/source_code/results/diagram_results  
                  
                  
2- Get textual results (.txt & .csv):__
    Including:__
      a) Number of Read requests__
      b) Number of Write requests__
      c) Read size__
      d) Write size__
      e) Total requests size (R + W)__
      f) R/W percentage__
      g) MAX/MIN requested addresses__
      h) AVG Read and Write__
      i) Distribution of I/O Requests (total R/W)__
      j) Distribution of I/O Requests (Read)__
      k) Distribution of I/O Requests (Write)__
      l) Access frequency --> Cumulative Distribution Funtion (CDF)__
      m) Access frequency of each address --> .csv file__
      
      
    *** How to run:
        cd /path/to/source_code/tools/basic_information
        python generate_text.py
                  |
                  |---> input: path_to_blkparse_result.txt
                  |
                  |---> input: Traced application name
                  |
                  |---> output: /path/to/source_code/results/text_results           
