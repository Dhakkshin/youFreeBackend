# from datetime import datetime, timezone, timedelta

# def ist_to_utc(ist_time_str):
#     # Convert IST time string to datetime object
#     ist_time = datetime.strptime(ist_time_str, "%Y-%m-%dT%H:%M:%S")

#     # Get the IST timezone
#     ist_timezone = timezone(timedelta(hours=5, minutes=30))

#     # Attach the timezone information to the datetime object
#     ist_time = ist_time.replace(tzinfo=ist_timezone)

#     # Convert to UTC time
#     utc_time = ist_time.astimezone(timezone.utc)

#     return utc_time

# def is_everyone_free(response, start_time_str, end_time_str):
#     # Convert user-provided start and end times from IST to UTC
#     start_time_utc = ist_to_utc(start_time_str)
#     end_time_utc = ist_to_utc(end_time_str)

#     calendars = response.get('calendars', {})
#     busy_intervals = []

#     # Extract busy intervals from each calendar
#     for calendar_info in calendars.values():
#         busy_intervals.extend([(datetime.fromisoformat(event['start']).replace(tzinfo=timezone.utc),
#                                 datetime.fromisoformat(event['end']).replace(tzinfo=timezone.utc))
#                                 for event in calendar_info['busy']])

#     # print(busy_intervals)
#     # Check if each person is free during the specified time slot
#     for interval in busy_intervals:
#         if interval[0] <= start_time_utc < interval[1] or interval[0] < end_time_utc <= interval[1]:
#             return False  # Someone is busy during the specified time slot

#     return True  # Everyone is free during the specified time slot

# # Example usage:
# response = {
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



from datetime import datetime, timezone, timedelta

def ist_to_utc(ist_time_str):
    # Convert IST time string to datetime object
    ist_time = datetime.strptime(ist_time_str, "%Y-%m-%dT%H:%M:%S")

    # Get the IST timezone
    ist_timezone = timezone(timedelta(hours=5, minutes=30))

    # Attach the timezone information to the datetime object
    ist_time = ist_time.replace(tzinfo=ist_timezone)

    # Convert to UTC time
    utc_time = ist_time.astimezone(timezone.utc)

    return utc_time

def is_everyone_free(response, start_time_str, end_time_str):
    # Convert user-provided start and end times from IST to UTC
    start_time_utc = ist_to_utc(start_time_str)
    end_time_utc = ist_to_utc(end_time_str)

    calendars = response.get('calendars', {})
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
        if (busy_start <= start_time_utc < busy_end) or (busy_start < end_time_utc <= busy_end):
            unavailable_people.append(person)

    if not unavailable_people:
        return True, []
    else:
        return False, unavailable_people

# Example usage:
response = {
    "kind": "calendar#freeBusy",
    "timeMin": "2024-02-01T17:30:00.000Z",
    "timeMax": "2024-02-29T19:00:00.000Z",
    "calendars": {
        "4c9d380b330580be36ca243cbf5b90b14664fbe0208dcd707c967fa7d7ef0aa7@group.calendar.google.com": {
            "busy": [
                {"start": "2024-02-16T04:30:00Z", "end": "2024-02-16T12:30:00Z"}
            ]
        },
        "7d3e6bfcdf8a27acf7fbc7301b8b32615f183e57f250740e4699fbae6d614e3d@group.calendar.google.com": {
            "busy": [
                {"start": "2024-02-16T13:30:00Z", "end": "2024-02-16T14:30:00Z"},
                {"start": "2024-02-17T05:00:00Z", "end": "2024-02-17T05:30:00Z"}
            ]
        }
    }
}

