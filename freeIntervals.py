from datetime import datetime
import pytz

# Sample response from FreeBusy API
# freebusy_response = {
#     "kind": "calendar#freeBusy",
#     "timeMin": "2024-02-01T17:30:00.000Z",
#     "timeMax": "2024-02-29T19:00:00.000Z",
#     "calendars": {
#         "4c9d380b330580be36ca243cbf5b90b14664fbe0208dcd707c967fa7d7ef0aa7@group.calendar.google.com": {
#             "busy": [
#                 {"start": "2024-02-16T04:30:00Z", "end": "2024-02-16T12:30:00Z"}
#             ]
#         },
#         "7d3e6bfcdf8a27acf7fbc7301b8b32615f183e57f250740e4699fbae6d614e3d@group.calendar.google.com": {
#             "busy": [
#                 {"start": "2024-02-16T13:30:00Z", "end": "2024-02-16T14:30:00Z"},
#                 {"start": "2024-02-17T05:00:00Z", "end": "2024-02-17T05:30:00Z"}
#             ]
#         }
#     }
# }

# def convert_utc_to_ist(utc_time):
#     utc = pytz.utc.localize(utc_time)
#     ist = utc.astimezone(pytz.timezone('Asia/Kolkata'))
#     return ist.strftime('%Y-%m-%d %H:%M:%S')

def find_free_slots(response, date):
    # Convert date to datetime object
    date = datetime.strptime(date, '%Y-%m-%d')

    # Initialize list to store free time slots
    free_slots = []

    # Get busy intervals for each calendar
    for calendar, busy_info in response['calendars'].items():
        busy_slots = busy_info['busy']
        for slot in busy_slots:
            start = datetime.fromisoformat(slot['start'][:-1])
            end = datetime.fromisoformat(slot['end'][:-1])

            # Check if the slot falls on the specified date
            if start.date() == date.date():
                free_slots.append((start, end))

    # Sort the free slots by start time
    free_slots.sort(key=lambda x: x[0])

    # Merge overlapping slots
    merged_slots = []
    for slot in free_slots:
        if not merged_slots or slot[0] > merged_slots[-1][1]:
            merged_slots.append(slot)
        else:
            merged_slots[-1] = (merged_slots[-1][0], max(slot[1], merged_slots[-1][1]))

    # Find the free time intervals
    free_intervals = [(date.replace(hour=0, minute=0), merged_slots[0][0])]
    for i in range(len(merged_slots) - 1):
        free_intervals.append((merged_slots[i][1], merged_slots[i + 1][0]))
    free_intervals.append((merged_slots[-1][1], date.replace(hour=23, minute=59)))

    return free_intervals

# # Example usage
# date_to_check = '2024-02-16'
# free_intervals = find_free_slots(freebusy_response, date_to_check)

# # Print free intervals in IST
# for interval in free_intervals:
#     start_ist = convert_utc_to_ist(interval[0])
#     end_ist = convert_utc_to_ist(interval[1])
#     print(f"Free from {start_ist} IST to {end_ist} IST")