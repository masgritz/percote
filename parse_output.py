import pandas as pd
from collections import Counter

pd.options.display.float_format = '{:20,.4f}'.format
pd.options.display.max_columns = None


def parse_output(output):
    """Parse the events collected by perf into a Pandas DataFrame"""

    # Replace gibberish and split into a list
    output = output.replace("|Joules", "|")
    output = output.replace("0||\n", "|NaN|Delete\n")
    output = output.replace("\n", "|")
    output = output.replace(",", ".")
    output = output.replace("||", ",")
    output = output.replace("|", ",")

    output_list = output.split(",")
    output_list = list(filter(None, output_list))

    # Define a new list to include the column names
    column_names = []
    garbage = []
    item = 0

    # Include the column names popped from the previous list in an interval
    while item < len(output_list):
        try:
            column_names.append(output_list.pop(item + 1))
            column_names.append(output_list.pop(item + 4))

            item += 4
        except:
            break

    item = 0

    while item < len(output_list):
        try:
            garbage.append(output_list.pop(item + 1))
            garbage.append(output_list.pop(item + 1))

            item += 2
        except:
            break

    output_list = [e for e in output_list if e not in {'NaN', '100.0'}]
    column_names = [e for e in column_names if e not in {'Delete'}]

    output_list = [float(i) for i in output_list]

    column_names.extend(["/power/energy-pkg/ (W)", "/power/energy-cores/ (W)", "/power/energy-gpu (W)",
                         "/power/energy-ram/ (W)"])
    output_list.extend([output_list[50]/output_list[54], output_list[51]/output_list[54],
                        output_list[52]/output_list[54],output_list[53]/output_list[54]])

    column_names = rename_duplicates(column_names)

    output_dict = dict(zip(column_names, output_list))

    performance_data = pd.DataFrame(output_dict, index=[0])
    performance_data.to_json("output.json", orient='records')

def rename_duplicates(my_list):
    """Rename repeated items in a list"""
    counts = Counter(my_list)

    for s, num in counts.items():
        if num > 1:
            for suffix in range(1, num + 1):
                my_list[my_list.index(s)] = s + "_" + str(suffix)
    return my_list
