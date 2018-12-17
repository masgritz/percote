from limit_cpu_clock import select_cpu_clock, revert_cpu_clock
from collect_events import collect_events, is_systemwide
from parse_output import parse_output


def main():
    revert_cpu_clock()

    model = input("Type the command to run: ")
    mode = is_systemwide()

    select_cpu_clock()

    try:
        times = int(input("How many times will the model be executed? "))

    except:
        times = 1

    for x in range(0, times):
        print("Collecting performance events for " + model + "... (" + str(x+1) + "/" + str(times) + ")")
        events_collected = collect_events(model, mode)

        output = parse_output(events_collected)

        print(output)


if __name__ == '__main__':
    main()
