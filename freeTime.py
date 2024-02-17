from datetime import datetime, timezone, timedelta

def is_everyone_free(response, start_time_str, end_time_str):

    resJSON = response.json()
    # print(resJSON)
    calendars = resJSON.get('calendars', {})
    busy_intervals = []

    # Extract busy intervals from each calendar
    for calendar_id, calendar_info in calendars.items():
        for event in calendar_info['busy']:
            busy_start = datetime.fromisoformat(event['start']).replace(tzinfo=timezone.utc)
            busy_end = datetime.fromisoformat(event['end']).replace(tzinfo=timezone.utc)
            busy_intervals.append((busy_start, busy_end, calendar_id))

    # Check if each person is free during the specified time slot
    unavailable_people = []
    for busy_start, busy_end, person in busy_intervals:
        if (busy_start <= start_time_str < busy_end) or (busy_start < start_time_str <= busy_end):
            unavailable_people.append(person)

    if not unavailable_people:
        return True, []
    else:
        return False, unavailable_people
