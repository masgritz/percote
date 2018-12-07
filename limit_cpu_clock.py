import subprocess


def get_default_cpu_clock():
    """Return a list with the default CPU clock"""
    command = "sudo cpupower frequency-info --hwlimits"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    output = stdout.decode("utf-8")
    output = output.replace("analyzing CPU 0:", "")
    output = output.replace("\n", "")

    default_clock = output.split(" ")

    return default_clock


def set_cpu_clock(max_clock, min_clock):
    """Set the minimum and maximum CPU clock to run a model"""
    default_clock = get_default_cpu_clock()

    if max_clock is None:
        max_clock = int(default_clock[1])
    else:
        max_clock = max_clock * 1000

    if min_clock is None:
        min_clock = int(default_clock[0])
    else:
        min_clock = min_clock * 1000

    if int(max_clock) < int(min_clock):
        print("The minimum clock (" + str(min_clock) + ") can't be higher than the maximum clock ("
              + str(max_clock) + ")!")

    else:
        command = "sudo cpupower frequency-set --max " + str(max_clock) + " --min " + str(min_clock)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = process.communicate()

        print(stdout.decode("utf-8"))
        print(stderr.decode("utf-8"))

        print("Maximum clock set as " + str(max_clock/1000) + "MHz")
        print("Minimum clock set as " + str(min_clock/1000) + "MHz\n")


def revert_cpu_clock():
    """Revert the CPU to its default clock"""
    print("Reverting CPU clock to system defaults.")
    set_cpu_clock(None, None)