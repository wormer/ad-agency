from datetime import datetime


def dayparting_from_json(json_list):
    dayparting = []
    for pair in json_list:
        if isinstance(pair, list) and len(pair) == 2:
            from_time_str, to_time_str = pair
            try:
                from_time = datetime.strptime(from_time_str, '%H:%M').time()
            except ValueError:
                continue
            try:
                to_time = datetime.strptime(to_time_str, '%H:%M').time()
            except ValueError:
                continue
            dayparting.append([from_time, to_time])
    return dayparting


def dayparting_to_json(dayparting):
    json_list = []
    for pair in dayparting:
        from_time, to_time = pair
        from_time_str = from_time.strftime('%H:%M')
        to_time_str = to_time.strftime('%H:%M')
        json_list.append([from_time_str, to_time_str])
    return json_list


def is_time_in_dayparting(time, dayparting):
    if dayparting == []:
        return True
    return any([from_time < time < to_time for from_time, to_time in dayparting])
