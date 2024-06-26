import json 
from utils import Config
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt

benchmarks = { "0":  828, 
                "1":  828, 
                "2":  823,
                "3":  827,
                "4":  827,
                "5":  589,
                "6":  586,
                "7":  1049,
                "8":  1208,
                "9":  1262
}



# read hyperparameter_tuning.json
try: 
    with open('hyperparameter_tuning.json') as f:
        data = json.load(f)
except FileNotFoundError as e:
    print("The file hyperparameter_tuning.json does not exist. Please run the hyperparameter tuning script first and convert the output to json format.")
else: 
    # convert the config into Config objects
    configs = [Config.from_json(config["Config"]) for config in data]
    # place it into data 
    data = [{"Config": configs[i], "Statistics": data[i]["Statistics"]} for i in range(len(configs))]

    for config in data:
        for key, value in config["Statistics"].items():
            config["Statistics"][key]["travel_time_min_feasible_rel_dev"] = 100 / benchmarks[key] * (value["travel_time_min_feasible"] if value["travel_time_min_feasible"] != 0 else float("inf"))
            config["Statistics"][key]["travel_time_avg_feasible_rel_dev"] = 100 / benchmarks[key] * (value["travel_time_avg_feasible"] if value["travel_time_avg_feasible"] != 0 else float("inf"))
            config["Statistics"][key]["travel_time_max_feasible_rel_dev"] = 100 / benchmarks[key] * (value["travel_time_max_feasible"] if value["travel_time_max_feasible"] != 0 else float("inf"))
            config["Statistics"][key]["travel_time_min_all_rel_dev"] = 100 / benchmarks[key] * (value["travel_time_min_all"] if value["travel_time_min_all"] != 0 else float("inf"))
            config["Statistics"][key]["travel_time_avg_all_rel_dev"] = 100 / benchmarks[key] * (value["travel_time_avg_all"] if value["travel_time_avg_all"] != 0 else float("inf"))
            config["Statistics"][key]["travel_time_max_all_rel_dev"] = 100 / benchmarks[key] * (value["travel_time_max_all"] if value["travel_time_max_all"] != 0 else float("inf"))

        values = list(config["Statistics"].values())
        statistics_list_len = len(list(values))
        config["Statistics"]["travel_time_min_feasible_rel_dev_avg"] = sum([value["travel_time_min_feasible_rel_dev"] for value in values]) / statistics_list_len
        config["Statistics"]["travel_time_avg_feasible_rel_dev_avg"] = sum([value["travel_time_avg_feasible_rel_dev"] for value in values]) / statistics_list_len
        config["Statistics"]["travel_time_max_feasible_rel_dev_avg"] = sum([value["travel_time_max_feasible_rel_dev"] for value in values]) / statistics_list_len
        config["Statistics"]["travel_time_min_all_rel_dev_avg"] = sum([value["travel_time_min_all_rel_dev"] for value in values]) / statistics_list_len
        config["Statistics"]["travel_time_avg_all_rel_dev_avg"] = sum([value["travel_time_avg_all_rel_dev"] for value in values]) / statistics_list_len
        config["Statistics"]["travel_time_max_all_rel_dev_avg"] = sum([value["travel_time_max_all_rel_dev"] for value in values]) / statistics_list_len
    
    if input("Do you want to export the top configurations into meta_config.json? (y/n)") == "y":
        # read number to export into meta_config.json from user input
        try: 
            metric = input("Which metric do you want to use for sorting? avg, per_instance_best ")
            problem_instance = input("Which problem instance do you want to export? 0-9")
        except ValueError:
            print("Please enter a valid number.")
        else: 
            if metric == "avg":
                number_to_export = int(input("How many configurations do you want to export into meta_config.json? "))
                # sort the data by the travel_time_avg_feasible_rel_dev_avg
                data = sorted(data, key=lambda x: x["Statistics"]["travel_time_avg_feasible_rel_dev_avg"])
                # write the top number_to_export configurations into meta_config.json
                with open('./configs/meta_config.json', 'w') as f:
                    f.write('{"output_file": "outputs/meta_config.json",\n')
                    f.write('"configs": [\n')
                    for i in range(number_to_export):
                        if i == number_to_export - 1:
                            f.write(data[i]["Config"].get_config_str(problem_instance) + "\n")
                        else:
                            f.write(data[i]["Config"].get_config_str(problem_instance) + ",\n")
                    f.write("]}\n")
            elif metric == "per_instance_best":
                number_to_export = int(input("How many configurations do you want to export into meta_config.json per problem instance? "))
                with open('./configs/meta_config.json', 'w') as f:
                    f.write('{"output_file": "outputs/meta_config.json",\n')
                    f.write('"configs": [\n')
                    for i in range(10):
                        data = sorted(data, key=lambda x: x["Statistics"][str(i)]["travel_time_min_feasible_rel_dev"])
                        for j in range(number_to_export): 
                            # sort the data by the travel_time_min_feasible_rel_dev
                            if i == 9 and j == number_to_export - 1:
                                f.write(data[j]["Config"].get_config_str(problem_instance) + "\n")
                            else:
                                f.write(data[j]["Config"].get_config_str(problem_instance) + ",\n")
                    f.write("]}\n")
            

    
    # create a scatterplot where the x-axis is the problem instance and the y-axis is the travel_time_avg_feasible_rel_dev with every configuration as a point
    sns.set_theme(style="whitegrid")
    df_dict = {
        "problem_instance": [],
        "travel_time_avg_feasible_rel_dev_avg": [],
        "hue": []
    }
    for config in data:
        for problem_instance in range(10):
            df_dict["problem_instance"].append(problem_instance)
            value = config["Statistics"][str(problem_instance)]
            df_dict["travel_time_avg_feasible_rel_dev_avg"].append(value.get("travel_time_avg_feasible_rel_dev", 1000000))
            df_dict["hue"].append(config["Config"].population_size)
    df = pd.DataFrame(df_dict)
    sns.scatterplot(data=df, x="problem_instance", y="travel_time_avg_feasible_rel_dev_avg", hue="hue", palette = "bright")
    plt.show()
    
