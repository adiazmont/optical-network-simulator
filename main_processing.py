from multiprocessing import Process, Manager
from CIANTestbed import CIANTestbed
import pandas

class MainProcessing():

    def process_request(self, _list):
        _list.append(CIANTestbed().training_parameters)
        
    def main(self):
        with Manager () as manager:
            csv_list = manager.list()
            processes = []
            for iter in range(1000):
                p = Process(target=self.process_request, args=(csv_list, ))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
                
            csv_list = [x for x in csv_list]
            csv_dir = '/home/alan/Trinity-College/Research/ECOC-2019/datafiles/'
            df = pandas.DataFrame.from_records(csv_list)
            df.to_csv(csv_dir+'training_data_link_load_70.csv')
            
if __name__ == '__main__':
    MainProcessing().main()
