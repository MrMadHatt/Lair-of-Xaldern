def get_new_room(user_input, current_room_id, rooms_list): 
    direction = user_input.replace('go', '').strip().lower()
    current_room_data = rooms_list.get(current_room_id)

    if not current_room_data:
        print("Error: Location data missing.")
        return current_room_id
            
    destination_id = current_room_data.get(direction)   

    if destination_id is not None and destination_id in rooms_list:
        dest_room_data = rooms_list[destination_id]
        
        if dest_room_data.get('status') != 'finished':
            print(f"The path {direction} leads to a place still under construction...")
            return current_room_id

        print(f"You head {direction}...")
        return destination_id
        
    else:
        print("YOU SHALL NOT PASS! There is no path that way.")
        return current_room_id