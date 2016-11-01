import fileinput
import sys
import itertools
import re
#./run < testcases/or.arff.in

if __name__ == '__main__':
    input   = []
    nodes   = []
    queries = []
    realtion= []

    # Read each input line
    for line in sys.stdin:
        # sys.stdout.write(line)
        if line[0] != "%":
            line = line.strip("\n")
            if line != "":
                input.append(line)

    for idx, line in enumerate(input):
        #Read relation
        if line.startswith("@relation"):
            relation = line.split(" ");
            print(relation[1])

        #Read attributes
        if line.startswith("@attribute"):
            attribute = line.split(" ");
            name = attribute[1]
            print(name) # attribute name
            values = re.search("{(.+?)}", line).group(1)
            f_values = values.split(", ") # attribute values
            print(f_values[0] + ' ' + f_values[1])
        
        
        if line.startswith("@data"):
            data_list= list(input)
            for data in itertools.islice(data_list, idx+1, None):
                data_set= data.split(",")
                print(data_set[0] + ' ' + data_set[1] + ' ' + data_set[2]) #data_sets