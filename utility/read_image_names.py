import os
def fn():       # 1.Get file paths from directory
    file_list=os.listdir(r"/path/to/image/directory")
    f= open("test.txt", 'w')
    #print (type(file_list))
    #for i in range(len(file_list)):
    for j in file_list:
      f.write(j+'\n')
    f.close()
 #2.To rename files
fn()