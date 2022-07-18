import random
import math
import re
import numpy as np
import random

IALAB_USER = 'jiossandon'
train_vocabulary_path = f"/home/{IALAB_USER}/storage/speaker_follower_with_objects/tasks/R2R/data/train_vocab.txt"

TURN_EXPRESSIONS = [
    lambda orientation: f"turn {orientation}",
    lambda orientation: f"take a {orientation}",
    lambda orientation: f"make a {orientation}",
]
MOVE_FROM_REGION_TO_OTHER =  [
    lambda current_region, next_region: f"exit the {current_region} to the {next_region}",
]
MOVE_TO_OBJECT_REFERENCE = [
    lambda orientation, object_name: f"go straight with the {object_name} on your {orientation}",
    lambda orientation, object_name: f"walk straight down the {opposite_orientation(orientation)} side of the {object_name}",
]

MOVE_TO_OTHER_ROOM_WITH_OBJECT = [
    lambda current_region, next_region, object_orientation, object_name: f"exit the {current_region} to the {next_region} walking by the {opposite_orientation(object_orientation)} side of the {object_name}",
    lambda current_region, next_region, object_orientation, object_name: f"go out of the {current_region} into the {next_region} walking with the {object_name} on your {object_orientation}"
]

MOVE_ON_THE_SAME_ROOM = [
    lambda orientation: f"turn a little to the {orientation} and walk forward",
    lambda orientation: f"walk straight a little to the {orientation}",
    lambda orientation: f"walk straight slightly to the {orientation}",
    lambda orientation: f"turn slightly to the {orientation} and walk forward"
]

MOVE_ON_THE_SAME_ROOM_BACK = [
    lambda orientation: f"turn around and walk forward a little to the {orientation}",
    lambda orientation: f"turn around and go straight slightly to the {orientation}",
    lambda orientation: f"turn around and walk forward slightly to the {orientation}",
    lambda orientation: f"turn around and go straight a little to the {orientation}"
]

WAIT = [
    'wait there',
    'stop',
    ''
]

# Load vocabulary
with open(train_vocabulary_path) as file:
    train_vocab = [line.rstrip() for line in file]

# Gets distnace between object and viewpoint
def get_distance_between(obj, viewpoint_heading, viewpoint_distance):
    angle_between = abs(viewpoint_heading - obj['heading'])

    distance_between = math.sqrt(
      obj['distance']**2 + viewpoint_distance**2 -
      2* obj['distance']* viewpoint_distance * math.cos(angle_between)
    )

    return distance_between

# Get better object for orientating the agent navigate to the next node
def get_closer_object(objects, viewpoint_heading, viewpoint_distance, used_objects):
    pi = np.pi
    sort_func = lambda obj: get_distance_between(obj, viewpoint_heading, viewpoint_distance)

    sorted_objs = sorted(objects, key=sort_func)

    for obj in sorted_objs:

        # Filter if object not on the vision cone
        angle_between = viewpoint_heading - obj['heading']
        if not -pi/2 <= angle_between <= pi/2:
            continue

        # Filter if object is over elevation limit (filtering lamps, roofs)
        if abs(obj['elevation']) > 0.6:
            continue

        # Transform objects like bath#sink
        obj_components = re.split('#|/', obj['name'])
        obj_components = [x for x in obj_components if x]
        obj['name'] = ' '.join(obj_components)

        # Filter if object not in vocabulary
        object_in_vocab = all([x in train_vocab for x in obj_components])

        # If is closer than the next node and is not already used in generated crafted instruction
        if obj['distance'] < viewpoint_distance and object_in_vocab and obj['name'] not in used_objects:
            return obj

# Gets closer object for the final atomic crafted instruction (last action)
def get_final_closer_object(objects):
    sort_func = lambda obj: obj['distance']

    sorted_objs = sorted(objects, key=sort_func)
    for obj in sorted_objs:
        obj_components = re.split('#|/', obj['name'])
        obj_components = [x for x in obj_components if x]
        obj['name'] = ' '.join(obj_components)

        object_in_vocab = all([x in train_vocab for x in obj_components])

        heading = obj['heading']
        while heading > np.pi:
            heading -= 2 * np.pi
        while heading < -np.pi:
            heading += 2 * np.pi

        if object_in_vocab and get_reference(heading) != 'behind' and obj['distance'] < 2:
            obj['orientation'] = get_reference(heading)
            return obj

# Get reference of some relative heading
def get_reference(heading):
    pi = np.pi
    if pi/2 <= heading < (pi - 1/2):
        return 'left'
    elif (pi - 1/2) <= heading <= (pi + 1/2):
        return 'front'
    elif (pi + 1/2) < heading < 3 * pi/2:
        return 'right'
    else:
        return 'behind'

# Get hard turn reference if necessary
def get_hard_turn(heading):
    pi = np.pi
    RANGE_GAP = 0.4
    if pi/2 - RANGE_GAP <= heading <= pi/2 + RANGE_GAP:
        return 'left'
    elif 3 * pi/2 - RANGE_GAP <= heading <= 3 * pi/2 + RANGE_GAP:
        return 'right'
    elif heading <= RANGE_GAP  or heading >=  2 * pi - RANGE_GAP:
        return 'around'

    return None

# Gets object reference on route
def get_object_from_viewpoint_orientation(obj, next_viewpoint):
    if obj['heading'] > next_viewpoint['heading']:
        return 'right'
    return 'left'

# Gets same room move instruction
def get_same_room_instruction(next_viewpoint, hard_turn):
    RANGE_GAP = 0.4
    pi = np.pi

    if hard_turn:
        return 'walk forward'
    heading = next_viewpoint['heading']

    if pi/2 + RANGE_GAP < heading < pi - RANGE_GAP * 3:
        return 'turn around and walk forward'
    elif pi + 3 * RANGE_GAP < heading < 3 * pi/2 - RANGE_GAP:
        return 'turn around and walk forward'
    elif RANGE_GAP < heading < pi/2 - RANGE_GAP:
        return 'turn around and walk forward'
    elif 3 * pi/2 + RANGE_GAP < heading < 2 * pi - RANGE_GAP :
        return 'turn around and walk forward'
    else:
        return 'walk forward'

def opposite_orientation(orientation):
    if (orientation == 'left'):
        return 'right'
    return 'left'

# Get final object instruction
def final_object(object_name, orientation):
    if orientation == "front":
        return random.choice([
            f"stop in front of the {object_name}",
            f"wait just in front of the {object_name}"
        ])
    elif orientation == "behind":
        return random.choice([
            f"wait with the {object_name} on your back",
            f"stop passing by the {object_name} behind you"
        ])
    else:
        if orientation == 'left':
            opposite_orientation = 'right'
        else:
            opposite_orientation = 'left'
        return random.choice([
            f"wait at the {opposite_orientation} of the {object_name}",
            f"stop on the {opposite_orientation} of the {object_name}"
        ])