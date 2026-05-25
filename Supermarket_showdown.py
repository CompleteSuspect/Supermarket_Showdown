import random
import time

DIRECTIONS = {"up" : (0,-1), #dictionary constant for translating moves into tuples to calculate the new (x,y) location
              "down" : (0,1),
              "left" : (-1,0),
              "right" : (1,0)
              }

STAFF_EXIT = (3,0)
WAREHOUSE = (1,0)
CHECKOUTS = (3,3)
NEIL_START = (0,3)
PLAYER_START = (2,0)
NEEDED_STOCKED_ROOMS = 8
MAX_CUSTOMERS = 2
MAX_COUPONS = 4
KEYCARD = "Mythical Golden Keycard"

def grid_generator():
    """The function is resposible to generating the 4x4 grid, The rooms are split into randomly placed rooms and static rooms.
        The random module is imported for the use of the shuffle function to randomise the departments for each playthrough.
        This function returns a dictionary of dictionaries with the key being coordinents for a grid position."""
    
    department_rooms = [
        {'name' : "alcohol", 'needed' : "beer", 'stocked' : False, 's_items' : [], 'status' : "open"},
        {'name' : "bakery", 'needed' : "bread", 'stocked' : False, 's_items' : [],'status' : "open"},
        {'name' : "beverages", 'needed' : "lemonade", 'stocked' : False, 's_items' : [], 'status' : "open"},
        {'name' : "confectionery", 'needed' : "chocolate", 'stocked' : False, 's_items' : [], 'status' : "open"},
        {'name' : "dairy", 'needed' : "milk", 'stocked' : False, 's_items' : [], 'status' : "open"},
        {'name' : "frozen", 'needed' : "lollies", 'stocked' : False,  's_items' : [], 'status' : "open"},
        {'name' : "fruit", 'needed' : "oranges", 'stocked' : False,  's_items' : [], 'status' : "open"},
        {'name' : "groceries", 'needed' : "baked beans", 'stocked' : False,  's_items' : [], 'status' : "open"},
        {'name' : "meat", 'needed' : "steak", 'stocked' : False,  's_items' : [], 'status' : "open"},
        {'name' : "seafood", 'needed' : "fish", 'stocked' : False,  's_items' : [], 'status' : "open"},
        {'name' : "snacks", 'needed' : "crisps", 'stocked' : False,  's_items' : [], 'status' : "open"},
        {'name' : "toiletries", 'needed' : "shampoo", 'stocked' : False,  's_items' : [], 'status' : "open"},
        {'name' : "vegetables", 'needed' : "carrots", 'stocked' : False,  's_items' : [], 'status' : "open"},
        ]
    
    special_rooms = [
        {'name' : "checkouts", 'needed' : "special", 'stocked' : True, 's_items' : [], 'status' : "closed"},
        {'name' : "staff exit", 'needed' : "special", 'stocked' : True, 's_items' : [], 'status' : "closed"}, 
        {'name' : "warehouse", 'needed' : "special", 'stocked' : True, 's_items' : [], 'status' : "open"},   
        ]
    
    random.shuffle(department_rooms) #new list with shuffled department rooms
    
    game_grid = {}
    for x in range(4):
        for y in range(4):
            if (x,y) == WAREHOUSE:
                game_grid[(x,y)] = special_rooms[2] #place the warehouse room 
                
            elif (x,y) == STAFF_EXIT:
                game_grid[(x,y)] = special_rooms[1] #place the staff exit
                
            elif (x,y) == CHECKOUTS:
                game_grid[(x,y)] = special_rooms[0] #place the checkout room
                
            else:
                game_grid[(x,y)] = department_rooms.pop(0) #place a random department room
                
    return game_grid

def check_boundaries(grid, location):
    """Helper function to check if a room is within the grid bounderies and returns a boolean.
    """   
    next_location = grid.get(location, None)
    return next_location is not None
    
def check_closed_room(grid, location):
    """Helper function to to check if a room is open or closed and returns a boolean.
    """
    return not grid[location]['status'] == "closed"

def open_staffroom(grid):
    grid[STAFF_EXIT]['status'] = "open"
    print(f"You have the {KEYCARD}. Get to the staff exit to exit the game!!")
    return None


def move_player(grid, player):
    """This function allows the player to move across the theoretical grid by returning the new location of the player.
        The function uses helper functions to check for grid bounderies and whether a room is closed."""
    
    location = player["location"] #access the player location from the player dictionary
    if location not in player['seen']: #track the visited rooms for the warehouse pickups
        player['seen'].append(location)

    while True:
        print(f"{player['name']} is at the {grid[location]['name']} department. {player['location']}")
        move = input(f"Please enter a command ({', '.join(DIRECTIONS)}, items, help), or press return to enter room: ").lower().strip()
        
        print("")
        if not move: #press return to enter the room
            if grid[location]['status'] != "closed": #checks to see if room is not closed
                event_dispatcher(grid, player)
                return None
            else:
                print("This room is closed!")
                
        if move == "help":
            print("Map key:")
            print("Player: P | Neil: N | Closed: X | Stocked: O | Special Item: *")
            print("Department . | Warehouse: W | Staffroom: S | Checkout: C")
        
        elif move == "items":
            display_items(player['inventory'])
            
        elif move not in DIRECTIONS: #if move input is invalid
            print("Invalid input!")
        
        else: #if valid
            coords = DIRECTIONS[move]
            next_location = (location[0] + coords[0], location[1] + coords[1]) #calculate the new (x,y) coords using current location and move coords
            if not check_boundaries(grid, next_location): #check to see if the new location is within bounds
                print("Out of bounds, try again!")
            
            elif not check_closed_room(grid, next_location): #check if room is closed
                print(f"The {grid[next_location]['name']} cannot be entered right now!")
            
            else:
                player['location'] = next_location
                return None

def event_dispatcher(grid, player):
    """The main even hander function that determines which secondary event functions are to be called,
        depending on the player location.
    """
    location = player['location'] #unpack player location
    
    if grid[location]["status"] == "customer": #if a customer is present
        print(f"\n---{player['name']} has encountered a customer!")
        customer_event(player) #launch customer event
        grid[location]['status'] = "open" #reset room status
        
    elif location == WAREHOUSE: #launch warehouse event
        print(f"\n---{player['name']} has entered the {grid[location]['name']}---")
        warehouse_event(grid, player)

    elif location == CHECKOUTS:
        print(f"\n---{player['name']} has entered the {grid[location]['name']}---")
        checkout_event(player)
        grid[location]['status'] = "closed" #reset the room status

    else: #launch andomised department room event
        print(f"\n---{player['name']} has entered the {grid[location]['name']}---")
        department_event(grid, player)
    
    return None

def warehouse_event(grid, player):
    """The main warehouse event controller that allows the player to pickup or drop items to replenish the departments.
       This function relies on several helper functions to work.
    """
    commands = ["pickup", "drop", "move", "help"]
    while True:
        if player["inventory"]: #show players inventory
            print(f"\n---{player['name']}'s inventory---")
            display_items(player["inventory"])
            
        command = input(f"\nPlease enter a command ({', '.join(commands)}): ").lower().strip()
        
        if command not in commands:
            print("Invalid command, try again!")
            
        elif command == "pickup":
            needed_items = get_needed_items(grid, player)
            if not needed_items:
                print("There are no previously visited departments in need of replenishment!")
            
            elif len(player['inventory']) == 2:
                print(f"{player['name']}'s inventory is full!")
            
            else:    
                print("---Warehouse stock for previously visited departments---")
                display_items(needed_items)
                item = pickup_item(needed_items)
                if item:
                    player['inventory'].append(item)
                    print(f"{player['name']} has added {item} to their inventory!")
                
        elif command == "drop":
            item = drop_item(player)
            if item:
                player['inventory'].remove(item)
                print(f"{player['name']} has dropped {item}.")
                
        elif command == "help":
            print("In the warehouse you can pick up stock items to replenish the stocked departments.")
            print("Commands:")
            print("- pickup: View and pick up items from previously visited departments to replenish them, you can carry up to two items.")
            print("- drop: Drop items to free up inventory space.")
            print("- move: Leave the warehouse to explore the supermarket and continue your duties.")
            
        elif command == "move":
            return None
        
def department_event(grid, player):
    """The main department event controller that allows the player to stock the room for game progression.
    """

    location = player['location'] #unpack current player coords
    room_name = grid[location]['name'] #unpack the room name
    needed_item = grid[location]['needed'] #unpack the needed item needed for replenishment based on player location
    special_items = grid[location]['s_items'] #unpack special items within this room
    
    if grid[location]['stocked']:
        print(f"The {room_name} department has already been replenished with {needed_item}.")
        
    else:
        print(f"The {room_name} department requires {needed_item}.")
        
    while True:
        commands = ["drop", "help", "move"] #build commands
        if special_items: #add the pickup command if a special item is in the room.
            commands.insert(0, "pickup")
            print("****There are special items in this room!****")
            
        if player['inventory'] and needed_item: #show players inventory
            print(f"\n---{player['name']}'s inventory---")
            display_items(player['inventory'])
            
        command = input(f"\nPlease enter a command ({', '.join(commands)}): ").lower().strip()
        
        if command not in commands:
            print("Invalid command, try again!")
        
        elif command == "drop":
            if grid[location]['stocked']: #check to see if room is replenished.
                print(f"{room_name} has already been stocked with {needed_item}.")
            
            else:
                item = drop_item(player)
                if not item: #if cancelled by user
                    continue
                
                elif item == needed_item: 
                    player['inventory'].remove(item)
                    grid[location]['stocked'] = True #update room replenishment status.
                    print(f"{player['name']} has replenished the {room_name} department with {needed_item}!")
                
                else:
                    print(f"You cannot stock {item} in the {room_name} department!")
                    
        elif command == "help":
            print(f"You are in the {room_name} department, replenish this room with {needed_item} to progress with your duties and pacify the manager")
            print("Commands:")
            print("- drop: Drop a matching item to replenish the stock within this department")
            print(f"- move: Leave the {room_name} to explore the supermarket and continue your duties.")
            print("- pickup: pickup special item (if availible)")
        
        elif command == "pickup": #only used if the room contains a special item (for example: golden_keycard)
            display_items(special_items)
            s_item = pickup_item(special_items)
            if s_item:
                player['s_inventory'].append(s_item) #add special item into the players special inventory
                grid[location]['s_items'].remove(s_item) #remove special item from the room's special items
                print(f"{player['name']} has added {s_item} to their special inventory!")
                
        elif command == "move":
            return None

def customer_event(player):
    """A customer event will occur a move penalty, the player can use a coupon to avoid this.
    """
    print("The customer needs to you get an item from the top shelf!")
    if "coupon" in player['s_inventory']:
        while True:
            command = input("Would you like to use a coupon to distract the customer and escape? ('yes', 'no')?: ").lower().strip()
            if command == "yes":
                player['s_inventory'].remove("coupon")
                print("You have given the coupon to the customer, and have escaped!")
                return None #use coupon and escape without penalty.
            
            elif command == "no":
                break
            
            else:
                print("Invalid command, try again!")
    
    player['move_penalty'] = True #move penalty has occured.
    print("You grab the item from the top shelf for the customer, this wastes precious time!")
    return None
            
def checkout_event(player):
    """Checkout minigame. The player must enter a given 11-digit number in less than 10 seconds to earn 2 coupons
    """
    time_limit = 10
    target_code = str(random.randint(10**10, 10**11 - 1)) #random 11 digit code
    
    print(f"The barcode doesn't scan! Product code: {target_code}")
    
    start_time = time.time() 
    code = input("Please enter the code manually: ").strip()
    end_time = time.time()
    
    elapsed_time = end_time - start_time #calculate time taken

    if code == target_code:
        if elapsed_time <= time_limit:
            print("You've entered the code in time!")
            for _ in range(2):
                if player['s_inventory'].count("coupon") < MAX_COUPONS: #get up to 2 coupons
                    player['s_inventory'].append("coupon")
                    print("You recieve a coupon!")
            
        else:
            print("You entered the correct code, but not in time. You miss a turn!")
            player['move_penalty'] = True 
    else:
        print("You entered the incorrect code, you miss a turn!")
        player['move_penalty'] = True

    return None
     
def display_items(items):
    """Used to display a formatted list of enumerated items to the console.
    """
    if not items:
        print("There are no items to show!")
        return None
        
    for idx, item in enumerate(items, start = 1):
        print(f"{idx} - {item}")
        
    return None

def get_needed_items(grid, player):
    """Helper function for the warehouse_event()
        Get the needed items needed for stock replenishment that the player doesn't already hold.
    """

    return [room['needed'] for location, room in grid.items() #generate and return list of needed items for replenishment
              if room['stocked'] == False
              and room['needed'] not in player["inventory"]
              and location in player['seen'] #only display the items of previously visited departement
           ]
    

def drop_item(player):
    """Prompts the player for an item number to drop.
    The item at the chosen index number in the players (inventory -1) is returned.Return None if cancelled.
    """
    if not player['inventory']:
        print("You have no items to drop!")
        return None

    while True:
        item_str = input("Choose an item number to drop, or press return to cancel: ").lower().strip()
    
        if not item_str:
            return None
        
        try:
            item_idx = int(item_str) #cast string to integer
            
        except ValueError:
            print("Invalid input, try again!")
            continue
            
        if 1 <= item_idx <= len(player['inventory']):
            return player['inventory'][item_idx - 1]
        
        else:
            print("Invalid item number, try again!")
            continue

def pickup_item(items):
    """Prompts the player for an item number to pick up.
        A list of items are passed in, and the item at the chosen index (number -1) is returned. Return None if cancelled.
    """
    if not items:
        print("Error: there are no items here to pick up!") #for debug purposes
        return None
    
    while True:
        item_str = input("Choose an item number to pick up, or press return to cancel: ").lower().strip()

        if not item_str:
            return None
        
        try:
            item_idx = int(item_str) #cast string to integer
            
        except ValueError:
            print("Invalid input, try again!")
            continue
            
        if 1 <= item_idx <= len(items): #check if item index is within range of needed items
            return items[item_idx - 1] #unpack chosen item
        
        else:
            print("Invalid item number, try again!")

def get_stocked_rooms(grid):
    """Return the coordinates of stocked department rooms."""
    return [k for k, v in grid.items()
            if v["needed"] != "special" and v["stocked"]
           ]

def spawn_key(grid):
    """Spawn the Golden Keycard within a room that has been previously stocked.
    """
    stocked_rooms = get_stocked_rooms(grid)
    golden_room = random.choice(stocked_rooms)
    grid[golden_room]['s_items'].append(KEYCARD)
    print(f"\n******The {KEYCARD} been appeared inside the {grid[golden_room]['name']} department!******")
    return True

def neil_think(neil):
    """Helper function to determine Neils next move based on his anger level. Returns number of turns and anger level.
    """
    anger = neil['anger']
    if anger < 0: #minimum anger level of 0
        neil['anger'] = 0
        
    if anger <= 10: #calm
        return (1, 0.2)
    
    elif anger <= 15: #somewhat annoyed
        return (1, 0.5)
    
    elif anger <= 20: #angry
        return (2, 0.3)
    
    else: #defcon Neil
        return (2, 0.6)

def neil_skip(neil, game_state):
    """Incapicitate Neil for a turn if roll_event is true.
    """
    if roll_event(game_state): #incapacitate Neil if True
        print("Neil slipped on a spill and cannot move!")
        neil['move_penalty'] = True
    return None
    

def neil_homing(player, neil):
    """Helper function to guarentee a move closer to the player. Returns a list of 2 possible moves.
    """
    n_x, n_y = neil['location']
    p_x, p_y = player['location']
    possible_moves = []
    
    if n_x < p_x:
        possible_moves.append((1, 0))
    elif n_x > p_x:
        possible_moves.append((-1, 0))
    
    if n_y < p_y:
        possible_moves.append((0, 1))
    elif n_y > p_y:
        possible_moves.append((0, -1))
        
    return possible_moves
    
def try_neil_move(grid, neil, move):
    """Validate Neil's next possible move. Return True if valid
    """
    new_location = (neil['location'][0] + move[0], neil['location'][1] + move[1])
    if check_boundaries(grid, new_location) and check_closed_room(grid, new_location): #check if next move within bounds and next room is open
        return new_location
    
    return None
    
def neil_turn(grid, player, neil):
    """Check if next move is homing or random using random.random() and update Neils location.
    """
    _, homing_chance = neil_think(neil) #get homing chance based off anger level
    
    if random.random() < homing_chance: #decide if homing or random
        possible_moves = neil_homing(player, neil)
        random.shuffle(possible_moves)
        for move in possible_moves:
            new_location = try_neil_move(grid, neil, move)
            if new_location:
                neil['location'] = new_location
                print("Neil did a homing move to: ", neil['location'])
                return None
    
    possible_moves = [move for move in DIRECTIONS.values()] #random moves are defaulted to
    random.shuffle(possible_moves)
    for move in possible_moves:
        new_location = try_neil_move(grid, neil, move)
        if new_location:
            neil['location'] = new_location
            print("Neil did a random move to: ", neil['location'])
            return None

def neil_collision(player, neil):
    """Determine if Neil is in the same room as the player, this is the losing condition for the game!
    """
    if neil['location'] == player['location']:
        if "coupon" in player['s_inventory']: #A coupon is automatically used as an extra life
            print("You have dropped a coupon on the floor, distracting Neil. Close call!")
            neil['anger'] -= 3
            player['s_inventory'].remove("coupon")
            neil['move_penalty'] = True #stun Neil for a turn!
            return False
        
        print("Neil has caught you, and you have lost!")
        return True #player has lost

def roll_event(game_state, base_rate = 0.1):
    """Helper function to randomly decide whether an event takes place. The chance of an event increases until an event occurs.
    """
    if random.random() < base_rate * game_state['chance_multiplier']:
        game_state['chance_multiplier'] = 0
        return True
    
    return False
    
def spawn_customer(grid, game_state):
    """Use roll_event() and spawn a customer in a random department room.
    """
    turn = game_state['turns']
    current_customers = [room for room in grid.values() if room['status'] == "customer"]
    if len(current_customers) < MAX_CUSTOMERS and roll_event(game_state): #if less than max customers and roll event is true
        open_rooms = [coords for coords, room in grid.items()
                      if room['needed'] != "special" and room['status'] == "open"]
        if open_rooms:
            room = random.choice(open_rooms)
            grid[room]['status'] = "customer"
            game_state['events'].append({'decay_turn': turn + 5, 'location' : room, 'type' : "customer", 'new_status' : "open"}) #add to event_decay dict
            print(f"\n------A customer has appeared in the {grid[room]['name']} department------")
        
    return None

def spawn_coupon(grid, game_state):
    """Use roll_event() and spawn a coupon in a random department room.
    """
    turn = game_state['turns']
    current_coupons = [room for room in grid.values() if "coupons" in room['s_items']] #see if there are less than 4 coupons
    if len(current_coupons) < MAX_COUPONS and roll_event(game_state, base_rate = 0.2):
        open_rooms = [coords for coords, room in grid.items()
                      if room['needed'] != "special" and room['status'] == "open" and not room['s_items']] #check if a department room is open and has no special items
        if open_rooms:
            room = random.choice(open_rooms)
            grid[room]['s_items'].append("coupon")
            game_state['events'].append({'decay_turn': turn + 5, 'location' : room, 'type' : "coupon", 'new_status' : []})#add event to event_decay
            print(f"\n*****A coupon has appeared in the {grid[room]['name']} department!*****")
        
    return None              

def clean_room(grid, game_state):
    """An event that uses the roll_event() function to close a random department room for cleaning
    """
    turn = game_state['turns']
    if roll_event(game_state):
        open_rooms = [
            coords for coords, room in grid.items()
            if not room['stocked'] and room['status'] == "open"
        ]

        if open_rooms:
            room = random.choice(open_rooms)
            grid[room]['status'] = "closed"
            game_state['events'].append({'decay_turn': turn + 5, 'location' : room, 'type' : "cleaning", 'new_status' : "open"})
            print(f"-----The {grid[room]['name']} department is closed for cleaning!-----")

    return None

def open_checkout(grid, game_state):
    """An event that uses the roll_event() function to open the checkouts room to allow the player to access the
        checkout minigame.
    """
    turn = game_state['turns']
    if grid[CHECKOUTS]['status'] == "closed" and roll_event(game_state):
        grid[CHECKOUTS]['status'] = "open"
        game_state['events'].append({'decay_turn': turn + 5, 'location' : CHECKOUTS, 'type' : "checkouts", 'new_status' : "closed"})
        print("You are needed on checkouts!")
        return None
        
def event_decay(grid, game_state):
    """End the events after a certain amount of turns have elapsed. Uses the event_decay dictionaries in game_state.
    """
    for event in game_state['events'][:]:
        if game_state['turns'] == event['decay_turn']:
            location = event['location']
            new_status = event['new_status']
            game_state['events'].remove(event)
            if event['type'] == "cleaning": #open department room
                grid[location]['status'] = new_status
                print(f"The {grid[location]['name']} department has been cleaned and is now open!")
            elif event['type'] == "customer": #remove customer
                grid[location]['status'] = new_status
                print(f"The {grid[location]['name']} department is now free of customers!")
            elif event['type'] == "checkouts": #close checkouts
                grid[location]['status'] = new_status
                print(f"You are no longer needed on checkouts!")
            elif event['type'] == "coupon": #silently remove coupon
                grid[location]['s_items'] = new_status
         
    return None

def display_grid(grid, player, neil):
    """Display a simple map the supermarket grid to the console
    """
    max_x = 4
    max_y = 4
    print("")
    print("-----------------")
    for y in range(max_y):
        row = []
        for x in range(max_x):
            location = (x, y)
            room = grid[location]
            
            if location == player['location'] and location == neil['location']: #Neil catches player
                tag = "!"
            elif player['location'] == location: #elif chain determines tag priority
                tag = "P"
            elif neil['location'] == location:
                tag = "N"
            elif room['status'] == "closed":
                tag = "X"
            elif room['s_items']:
                tag = "*"
            elif location == WAREHOUSE:
                tag = "W"
            elif location == STAFF_EXIT:
                tag = "S"
            elif location == CHECKOUTS:
                tag = "C"
            elif room['stocked']:
                tag = "O"
            else:
                tag = "."

            row.append(tag)
         
        row_display = " | ".join(row)
        print(f"| {row_display} |")
        
        if y < max_y:
            print("-----------------")
    print("")
        
    return None

def game_logic(name):
    grid = grid_generator()
    player = {'name' : name, 'location' : PLAYER_START, 'seen' : [], 'inventory' : [], 's_inventory' : [], 'move_penalty' : False}
    neil = {'location' : NEIL_START, 'anger' : 0, 'move_penalty' : False}
    game_state = {'turns': 0, 'stocked' : 0, 'chance_multiplier' : 0, 'events' : [], 'keycard' : False}
    while True:
        event_decay(grid, game_state) #check event expiry
        display_grid(grid, player, neil) #display grid
        
        print(f"You have stocked {game_state['stocked']}/{NEEDED_STOCKED_ROOMS} rooms.")
        if "coupon" in player["s_inventory"]:
            print(f"You have {player['s_inventory'].count("coupon")} coupon(s).")
            
            
        if grid[STAFF_EXIT]['status'] == "closed" and KEYCARD in player['s_inventory']:#if the player has keycard
            print("farts")
            open_staffroom(grid)
            
        if neil_collision(player, neil): #if Neil catches player
            print(f"Turns taken: {game_state['turns']}")
            return None #player has lost!
        
        if not player['move_penalty']: 
            move_player(grid, player) #main player turn function
            game_state['turns'] += 1 #add a turn to game_state
            neil_skip(neil, game_state) #attempt to incapacitate Neil
            spawn_coupon(grid, game_state) #attempt to spawn coupon
            clean_room(grid, game_state) #attempt to clean room 
            spawn_customer(grid, game_state) #attempt to spawn customer
            open_checkout(grid, game_state) #attempt to open checkouts
        else:
            player['move_penalty'] = False #reset move penalty flag
            
        if grid[STAFF_EXIT]['status'] == "closed" and KEYCARD in player['s_inventory']:#if the player has keycard
            print("farts")
            open_staffroom(grid)
            
        if not game_state['keycard'] and len(get_stocked_rooms(grid)) == NEEDED_STOCKED_ROOMS: #golden keycard spawn conditions
            game_state['keycard'] = True
            spawn_key(grid)
            
        stocked_rooms = len(get_stocked_rooms(grid)) #Neil anger manipulation depending on current stocked rooms
        if stocked_rooms > game_state['stocked']: #if there is a change of stocked rooms
            neil['anger'] -= 5
            
        else:
            neil['anger'] += 1
        
        game_state['stocked'] = stocked_rooms #update stocked rooms game state for the next turn 
        game_state['chance_multiplier'] += 1
        if player['location'] == STAFF_EXIT:
            print("Congratulations, you have entered the staff exit and finished your shift!")
            print(f"Turns taken: {game_state['turns']}")
            return None #player has won!
            
        #Neils turn
        if not neil['move_penalty']:
            n_turns, _ = neil_think(neil) #get Neil thoughts based on anger level
            print(f"Neil anger level: {neil['anger']}")
            for _ in range(n_turns):
                neil_turn(grid, player, neil)
                
        else:
            neil['move_penalty'] = False #reset move penalty flag
    return None

def main():
    print("--------------Supermarket Showdown!---------------")
    name = None
    while True:
        name = input("Please enter your name: ").strip()
        if name:
            break
        
    while True:
        commands = ["start", "help"]
        command = input(f"Please enter a command ({', '.join(commands)}): ").lower().strip()
        if command == "help":
            print("Traverse the supermarket and replenish the department rooms with items from the warehouse.")
            print("Stock 8 department rooms to spawn the Mythical Golden Keycard and escape your shift.")
            print("Rooms will be shut for cleaning, customers will surprise you, and the angry manager, Neil will be hunting you down!")
            print("Collect coupons along the way to distract Neil and escape customers!")
            print("Hint: Enter a room without moving to let Neil move if you don't want to move.\n")
        
        if command == "start":
            game_logic(name)
            while True:
                command = input("Try again? (yes/no): ").lower().strip()
                if command == "yes":
                    game_logic(name) #launch game
                    
                elif command == "no":
                    return None
                
                else:
                    print("Invalid command")

main()       
