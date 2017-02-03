def _serialize_rooms(room_set):
    rooms = []
    for room in room_set:
        rooms.append({
            "name": room.name,
            "room_id": room.roomid,
            "site_id": room.siteid,
            "capacity": room.capacity,
            "classification": room.classification,
            "zone": room.zone
        })
    return rooms
