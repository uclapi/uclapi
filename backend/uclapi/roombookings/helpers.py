def _serialize_rooms(room_set):
    rooms = []
    for room in room_set:
        rooms.append({
            "name": room.name,
            "roomid": room.roomid,
            "siteid": room.siteid,
            "capacity": room.capacity,
            "classification": room.classification,
            "zone": room.zone
        })
    return rooms
