from limit_cpu_clock import set_cpu_clock, revert_cpu_clock
from collect_events import collect_events
from parse_output import parse_output

def main():
    revert_cpu_clock()

    model = input("Type the command to run: ")
    mode = is_systemwide()

    try:
        min_clock = int(input("Type the minimum clock (in MHz) to run the command: "))
    except:
        min_clock = None
        pass

    events_collected = collect_events(model, mode)

    revert_cpu_clock()
    parse_output(events_collected)


if __name__ == '__main__':
    main()
