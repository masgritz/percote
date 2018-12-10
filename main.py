from limit_cpu_clock import select_cpu_clock, revert_cpu_clock
from collect_events import collect_events, is_systemwide
from parse_output import parse_output


def main():
    revert_cpu_clock()

    model = input("Type the command to run: ")
    mode = is_systemwide()

    select_cpu_clock()

    pre_events = collect_events("sleep 30", True)
    events_collected = collect_events(model, mode)
    post_events = collect_events("sleep 30", True)

    revert_cpu_clock()

    parse_output(events_collected, "pre")
    parse_output(events_collected, "main")
    parse_output(events_collected, "post")


if __name__ == '__main__':
    main()
