from limit_cpu_clock import select_cpu_clock, revert_cpu_clock
from collect_events import collect_events, is_systemwide
from parse_output import parse_output, check_dir
import re


def main():
    revert_cpu_clock()

    model = input("Type the command to run: ")
    mode = is_systemwide()

    model_name = re.sub('[\W\_]', '', model)

    select_cpu_clock()

    try:
        times = int(input("How many times will the model be executed? "))

    except:
        times = 1

    for x in range(0, times):
        print("Collecting performance events for " + model + "... (" + str(x + 1) + "/" + str(times) + ")")

        pre_events = collect_events("sleep 30", True)
        events_collected = collect_events(model, mode)
        post_events = collect_events("sleep 30", True)

        output_pre = parse_output(pre_events)
        output_main = parse_output(events_collected)
        output_post = parse_output(post_events)

        check_dir("events")

        output_pre.to_json("events/output_" + model_name + "_" + str(x) + "_pre.json", orient="records")
        output_main.to_json("events/output_" + model_name + "_" + str(x) + "_main.json", orient="records")
        output_post.to_json("events/output_" + model_name + "_" + str(x) + "_post.json", orient="records")


if __name__ == '__main__':
    main()
