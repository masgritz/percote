from limit_cpu_clock import set_cpu_clock, revert_cpu_clock
from collect_events import collect_events
from parse_output import parse_output

def main():
    revert_cpu_clock()

    model = input("Type the command to run: ")
    try:
        max_clock = int(input("Type the maximum clock (in MHz) to run the command: "))
    except:
        max_clock = None
        pass

    try:
        min_clock = int(input("Type the minimum clock (in MHz) to run the command: "))
    except:
        min_clock = None
        pass

    set_cpu_clock(max_clock, min_clock)

    events_collected = collect_events(model)

    revert_cpu_clock()
    parse_output(events_collected)


if __name__ == '__main__':
    main()
