import json
import MatterSim
import numpy as np
import networkx as nx

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Panoramic image dimensions
IMG_HEIGHT = 1440
IMG_WIDTH = 2880

# Forbidden and noisy objects
FORBIDDEN_WORDS = [
  'doorframe', 'light', 'floor', 'ceiling', 'remove', 'otherroom',
  'roof', 'unknown', 'wall', 'door', 'rug', 'frame', 'column', 'window',
  'column', 'celing', 'door', 'picture', 'delete'
]

# Loads navigation graph to calculate the relative heading of the next location
def load_nav_graph(graph_path):
    with open(graph_path) as f:
        G = nx.Graph()
        positions = {}
        data = json.load(f)
        for i,item in enumerate(data):
            if item['included']:
                for j,conn in enumerate(item['unobstructed']):
                    if conn and data[j]['included']:
                        positions[item['image_id']] = np.array([item['pose'][3],
                                item['pose'][7], item['pose'][11]]);
                        assert data[j]['unobstructed'][i], 'Graph should be undirected'
                        G.add_edge(item['image_id'],data[j]['image_id'])
        nx.set_node_attributes(G, values=positions, name='position')
    return G

# Computes relative heading of the next viewpoint based on the current viewpoint and heading
def compute_rel_heading(graph, current_viewpoint, current_heading, next_viewpoint):
    if current_viewpoint == next_viewpoint:
        return 0.
    target_rel = graph.nodes[next_viewpoint]['position'] - graph.nodes[current_viewpoint]['position']
    target_heading = np.pi/2.0 - np.arctan2(target_rel[1], target_rel[0]) # convert to rel to y axis

    rel_heading = target_heading - current_heading
    # normalize angle into turn into [-pi, pi]
    rel_heading = rel_heading - (2*np.pi) * np.floor((rel_heading + np.pi) / (2*np.pi))
    return rel_heading

# For a specific house scan, viewpoint, heading and elevation, shows panoramic image
def visualize_panorama_img(scan, viewpoint, heading, elevation):
    WIDTH = 80
    HEIGHT = 480
    pano_img = np.zeros((HEIGHT, WIDTH*36, 3), np.uint8)
    VFOV = np.radians(55)
    sim = MatterSim.Simulator()
    sim.setCameraResolution(WIDTH, HEIGHT)
    sim.setCameraVFOV(VFOV)
    sim.initialize()
    for n_angle, angle in enumerate(range(-175, 180, 10)):
        sim.newEpisode([scan], [viewpoint], [heading + np.radians(angle)], [elevation])
        state = sim.getState()
        im = state[0].rgb
        im = np.array(im)
        pano_img[:, WIDTH*n_angle:WIDTH*(n_angle+1), :] = im[..., ::-1]
    return pano_img

# For a specific house scan, viewpoint, heading and elevation, shows tunnel image
def visualize_tunnel_img(scan, viewpoint, heading, elevation):
    WIDTH = 640
    HEIGHT = 480
    VFOV = np.radians(60)
    sim = MatterSim.Simulator()
    sim.setCameraResolution(WIDTH, HEIGHT)
    sim.setCameraVFOV(VFOV)
    sim.init()
    sim.newEpisode(scan, viewpoint, heading, elevation)
    state = sim.getState()
    im = state.rgb
    return im[..., ::-1].copy()

# Objects labels mapping

LABEL_MAPPING = {
    'a': 'bathroom',
    'b': 'bedroom',
    'c': 'closet',
    'd': 'dining room',
    'e': 'entryway',
    'f': 'family room',
    'g': 'garage',
    'h': 'hallway',
    'i': 'library',
    'j': 'laundry',
    'k': 'kitchen',
    'l': 'living room',
    'm': 'conference room',
    'n': 'lounge',
    'o': 'office',
    'p': 'terrace',
    'r': 'game room',
    's': 'stairs',
    't': 'toilet',
    'u': 'utility room',
    'v': 'tv',
    'w': 'gym',
    'x': 'outdoor area',
    'y': 'balcony',
    'z': 'other room',
    'B': 'bar',
    'C': 'classroom',
    'D': 'dining booth',
    'S': 'spa',
    'Z': 'junk',
    '-': 'other room'
}

# Gets viewpoint region name
def get_viewpoint_region_name(metadata, viewpoint):
    values = metadata.get_region(viewpoint).label.values
    if not values.size > 0:
        return 'other room'
    label_keyword = values[0]
    return LABEL_MAPPING[label_keyword]