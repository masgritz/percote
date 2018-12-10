import subprocess, signal
import time


def collect_events(model, mode):
    """Use perf to collect pre-defined performance events"""
    if is_systemwide is True:
        all_flag = " -a"
    else:
        all_flag = ""

    # Define the command to collect the needed performance events
    events_command = "sudo perf stat -x|" + all_flag + " -e instructions,cycles,cpu-clock,cpu-migrations,branches," \
                     "branch-misses,context-switches,bus-cycles,cache-references,cache-misses,mem-loads,mem-stores," \
                     "L1-dcache-stores,L1-dcache-loads,L1-dcache-load-misses,LLC-stores,LLC-store-misses,LLC-loads," \
                     "LLC-load-misses,minor-faults,major-faults,page-faults,block:block_rq_insert," \
                     "block:block_rq_complete,block:block_rq_issue " + model

    energy_command = "perf stat -x| -a -e /power/energy-pkg/,/power/energy-cores/,/power/energy-gpu/," \
                     "/power/energy-ram/"

    # Initiate a timer
    start_time = time.perf_counter()

    # Start the execution of both processes
    events_process = subprocess.Popen(events_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    energy_process = subprocess.Popen(energy_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the events process to finish execution
    events_process.wait()

    # Terminate the timer and print its value
    elapsed_time = time.perf_counter() - start_time

    # Terminate the execution of the energy process
    energy_process.send_signal(signal.SIGINT)

    # Store the output of stdout and stderr to a variable
    stdout_output, stderr_output = events_process.communicate()
    another_stdout_output, another_stderr_output = energy_process.communicate()

    # events_collected = str(elapsed_time) + '|runtime|' + str(stderr_output) + str(another_stderr_output)
    events_collected = stderr_output.decode("utf-8") + another_stderr_output.decode("utf-8") +\
                       str(elapsed_time) + "|Runtime (s)"

    return events_collected


def is_systemwide():
    """Ask the user if the performance events will be collected only from the application or system-wide"""
    prompt = str(input("Collect the events in system-wide mode? (Y/N) "))

    print(prompt.lower())

    if prompt.lower() == "y":
        print("Events will be collected on system-wide mode.\n")
        return True
    else:
        print("Events will be collect in application-only mode.\n")
        return False
