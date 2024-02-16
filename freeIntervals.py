from datetime import datetime

def find_free_slots(response, date):
    # Convert date to datetime object
    if isinstance(date, datetime):
        date_obj = date
    else:
        date_obj = datetime.strptime(date, '%Y-%m-%d')

    # Initialize list to store free time slots
    free_slots = []
    response_dict = response.json()
    
    # Get busy intervals for each calendar
    for calendar, busy_info in response_dict['calendars'].items():
        busy_slots = busy_info['busy']
        for slot in busy_slots:
            start = datetime.fromisoformat(slot['start'][:-1])
            end = datetime.fromisoformat(slot['end'][:-1])

            # Check if the slot falls on the specified date
            if start.date() == date_obj.date():
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

    # Check if merged_slots is empty
    if not merged_slots:
        # If there are no busy slots for the specified date, return the entire day as free
        return [(date_obj.replace(hour=0, minute=0), date_obj.replace(hour=23, minute=59))]

    # Find the free time intervals
    free_intervals = [(date_obj.replace(hour=0, minute=0), merged_slots[0][0])]
    for i in range(len(merged_slots) - 1):
        free_intervals.append((merged_slots[i][1], merged_slots[i + 1][0]))
    free_intervals.append((merged_slots[-1][1], date_obj.replace(hour=23, minute=59)))

    return free_intervals
