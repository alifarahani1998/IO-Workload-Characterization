# I/O Workload Characterization


1- Draw characterization diagrams (visual results):
  
  1.1- Basic diagrams:<br />
    Including:<br />
      a) Read/Write percentage --> 2-D pie chart<br />
      b) Read/Write percentage --> 3-D pie chart<br />
      c) Distribution of I/O sizes --> Total R/W<br />
      d) Distribution of I/O sizes --> Separated R/W<br />
      e) Access frequency distribution<br />
      f) Access frequency --> Cumulative Distribution Funtion (CDF)
      
    *** How to run:
        cd /path/to/source_code/tools/basic_information
        python generate_diagram.py
                  |
                  |---> input: path_to_blkparse_result.txt
                  |
                  |---> output: /path/to/source_code/results/diagram_results
                  
                  
  1.2- Resource utilization diagrams:<br />
    Including:<br />
      a) I/O bandwidth<br />
      b) Disk utilization<br />
      c) CPU utilization<br />
      d) GPU utilization<br />
      
    *** How to run:
        cd /path/to/source_code/tools/resource_utilization
        python resource_utilization.py
                  |
                  |---> input: path_to_iostat_result.txt
                  |
                  |---> output: /path/to/source_code/results/diagram_results  
                  
                  
2- Get textual results (.txt & .csv):<br />
    Including:<br />
      a) Number of Read requests<br />
      b) Number of Write requests<br />
      c) Read size<br />
      d) Write size<br />
      e) Total requests size (R + W)<br />
      f) R/W percentage<br />
      g) MAX/MIN requested addresses<br />
      h) AVG Read and Write<br />
      i) Distribution of I/O Requests (total R/W)<br />
      j) Distribution of I/O Requests (Read)<br />
      k) Distribution of I/O Requests (Write)<br />
      l) Access frequency --> Cumulative Distribution Funtion (CDF)<br />
      m) Access frequency of each address --> .csv file<br />
      
      
    *** How to run:
        cd /path/to/source_code/tools/basic_information
        python generate_text.py
                  |
                  |---> input: path_to_blkparse_result.txt
                  |
                  |---> input: Traced application name
                  |
                  |---> output: /path/to/source_code/results/text_results           
