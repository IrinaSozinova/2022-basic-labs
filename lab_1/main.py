from pathlib import Path



def read_ecg_raw_file(file_path: Path):
    try:
        with open(file_path) as f:
            ecg_raw = f.readlines()
    except FileNotFoundError:
        print(f'This file "{file_path}" does not exist!')
    except Exception as e:
        print(f'This file "{file_path}" does not look like a file!')
        print(e)
        raise ValueError('Incorrect data file') from e

    # first line is meta-information and not an ECG item, therefore ignoring it
    only_number_lines = ecg_raw[1:]

    # creating intermediate variable for storing raw_signal
    raw_signal = []
    # each line is a number with a next line escape sequence
    for line in only_number_lines:
        # removing '\n' from line before casting to float
        numeric_value = float(line.strip())

        # adding element to a raw signal
        raw_signal.append(numeric_value)
    return raw_signal


# Lab 1 implementation goes below
def is_correct_input(input:list):
    if type(input) != list and len(input) == 0:
        return False
    for i in input:
        if type(i) != float and type(i) != int:
            return False
    return True

def calculate_threshold(signal: list):
    """Calculating threshold for RR peaks detection"""
    if not is_correct_input(signal):
        return None
    maximum = signal[0]
    for i in signal:
        if i > maximum:
            maximum=i
    return maximum*0.8

def detect_maximums(signal: list, threshold: float):
    """Labeling RR peaks"""
    if not is_correct_input(signal):
        return None
    if type(threshold) != float and type(threshold) != int:
        return None
    ecg_maximums = []
    for i in range(0,len(signal)):
        is_maximum=False
        if i == 0:
            is_maximum = signal[i] >= threshold and signal[i] > signal[i+1]
        if i > 0 and i < len(signal)-1:
            is_maximum = signal[i] >= threshold and signal[i + 1] < signal[i] and signal[i - 1] <= signal[i]
        if i == len(signal)-1:
            is_maximum = signal[i] >= threshold and signal[i] >= signal[i-1]
        if is_maximum:
            ecg_maximums.append(int(1))
        else:
            ecg_maximums.append(int(0))

    return ecg_maximums

def calculate_times(signal: list, sample_rate: int):
    """Calculating timestamp for each item in ECG"""
    if not is_correct_input(signal):
        return None
    if type(sample_rate) != int:
        return None
    ecg_times = []
    ecg_times.append(0.0)
    for i in range(1, len(signal)):
        ecg_times.append(i * 1000/sample_rate)
    return ecg_times


def calculate_rr(maximums: list, times: list):
    """Extract RR intervals"""
    if not is_correct_input(times):
        return None
    if not is_correct_input(maximums):
        return None
    for i in maximums:
        if i != 0 and i != 1:
            return None
    if len(maximums) != len(times):
        return None
    high_markers_ms = []
    rr_without_threshold = [0.0]
    ecg_rr = []
    for i in range(0,len(maximums)):
        if maximums[i] == 1:
            high_markers_ms.append(times[i])
    for i in range(0,len(high_markers_ms[1:])):
        rr_without_threshold.append(high_markers_ms[i] - high_markers_ms[i - 1])
    for rr in rr_without_threshold:
        if rr > 400:
            ecg_rr.append(rr)
    return ecg_rr

# Lab 1 demonstration goes below
if __name__ == '__main__':

    SAMPLE_RATE = 1000
    DATA_PATH = Path(__file__).parent / 'data' / 'participant_28_baseline_raw.txt'

    print(f'Opening {DATA_PATH} with ECG signal')

    ecg_raw = read_ecg_raw_file(DATA_PATH)

    print(f'Read ECG file. It has {len(ecg_raw)} values!')

    print('Detecting threshold')

    threshold = calculate_threshold(signal=ecg_raw)
    print(f'ECG maximum threshold is {threshold}')

    print('Detecting maximums')
    ecg_maximums = detect_maximums(signal=ecg_raw, threshold=threshold)


    print('Calculating times for each ECG signal entry')
    ecg_times = calculate_times (signal=ecg_raw, sample_rate=SAMPLE_RATE)


    print('Calculating RR intervals')
    ecg_rr = calculate_rr(maximums=ecg_maximums, times=ecg_times)


    if not ecg_rr:
        print('Something went wrong. Unable to extract RR intervals from ECG signal')
    else:
        print(f'Extracted {len(ecg_rr)} RR intervals from ECG raw signal')

