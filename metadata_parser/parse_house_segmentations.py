from typing import Tuple, TypeVar
import pandas as pd
import re
import os
import pickle
import logging

# logging.basicConfig(filename='~/repos/360-visualization/logs/metadata_parser.log', level=logging.DEBUG)

LINE_PATTERN = r'^([HLRPSVICOE]) *(.*)$'
EASY_CATEGORY_MAPPING = {
    'H': 'header',
    'L': 'level',
    'R': 'region',
    'S': 'surface',
    'V': 'vertex',
    'I': 'image',
    'C': 'category',
    'O': 'object',
    'E': 'segment'
}


def map_category_to_name(category: str, values: list) -> str:
    if category in EASY_CATEGORY_MAPPING:
        return EASY_CATEGORY_MAPPING[category]

    if category == 'P':
        # Differentiate between panorama and portal category
        if len(values) == 14:  # Is a portal line
            return 'portal'
        elif len(values) == 12:  # Is a panorama line
            return 'panorama'
        return None

    return None


def get_line_category(line: str) -> Tuple[str, str]:
    """Parses one line of the xxx.house file. If it is valid,
    returns the category (fist letter of the line) and the rest of the line.
    Ohterwise, returns None"""
    result = re.search(LINE_PATTERN, line)
    if result:
        category, rest = result.groups()
        rest = re.sub(' +', ' ', rest)
        values = rest.split(' ')
        category = map_category_to_name(category, values)

        if category is None:
            return None, None

        return category, values
    return None, None


T = TypeVar('T', bound='HouseSegmentationFile')


class HouseSegmentationFile:
    base_path = '~/datasets/Matterport3DSimulator/houses/v1/scans'

    def __init__(self, house_id: str) -> None:
        self.house_id = house_id
        self.__file_path = f'{self.base_path}/{house_id}/{house_id}/house_segmentations/{house_id}.house'
        self.__cache_path = f'./metadata_parser/house_cache/{house_id}.pickle'
        self.header = None
        self.levels = pd.DataFrame(columns=[
            'index', 'num_regions', 'label',
            'px', 'py', 'pz',  'xlo', 'ylo', 'zlo', 'xhi', 'yhi', 'zhi'])
        self.regions = pd.DataFrame(columns=[
            'region_index', 'level_index', 'label',  'px', 'py', 'pz', 'xlo', 'ylo', 'zlo', 'xhi', 'yhi', 'zhi', 'height'
        ])
        self.portals = pd.DataFrame(columns=[
            'portal_index', 'region0_index', 'region1_index', 'label',  'xlo', 'ylo', 'zlo', 'xhi', 'yhi', 'zhi',
        ])
        self.surfaces = pd.DataFrame(columns=[
            'surface_index', 'region_index', 'label', 'px', 'py', 'pz',  'nx', 'ny', 'nz',  'xlo', 'ylo', 'zlo', 'xhi', 'yhi', 'zhi',
        ])
        self.vertex = pd.DataFrame(columns=[
            'vertex_index', 'surface_index', 'label',  'px', 'py', 'pz',  'nx', 'ny', 'nz',
        ])
        self.panoramas = pd.DataFrame(columns=[
            'name',  'panorama_index', 'region_index',  'px', 'py', 'pz',
        ])
        self.images = pd.DataFrame(columns=[
            'image_index', 'panorama_index',  'name', 'camera_index', 'yaw_index', 'e00', 'e01', 'e02', 'e03', 'e10', 'e11', 'e12', 'e13', 'e20', 'e21', 'e22', 'e23', 'e30', 'e31', 'e32', 'e33',  'i00', 'i01', 'i02',  'i10', 'i11', 'i12', 'i20', 'i21', 'i22',  'width', 'height',  'px', 'py', 'pz',
        ])
        self.categories = pd.DataFrame(columns=[
            'category_index', 'category_mapping_index', 'category_mapping_name', 'mpcat40_index', 'mpcat40_name',
        ])
        self.objects = pd.DataFrame(columns=[
            'object_index', 'region_index', 'category_index', 'px', 'py', 'pz',  'a0x', 'a0y', 'a0z',  'a1x', 'a1y', 'a1z',  'r0', 'r1', 'r2',
        ])
        self.segments = pd.DataFrame(columns=[
            'segment_index', 'object_index', 'id', 'area', 'px', 'py', 'pz', 'xlo', 'ylo', 'zlo', 'xhi', 'yhi', 'zhi',
        ])

    def __parse_file(self):
        with open(self.__file_path) as ar:
            lines = ar.readlines()
            n = len(lines)
            logging.info(f'{self.house_id}: {n} lines to process')
            for i, line in enumerate(lines):
                if i % n // 10 == 0:
                    logging.info(f'Processing: {i / n:.3f} %')

                category, values = get_line_category(line.strip())

                if category is None:
                    logging.info('Null line:', line)
                    continue

                if category == 'header':
                    self.header = {
                        'name': values[0],
                        'label': values[1],
                        'num_images': float(values[2]),
                        'num_panoramas': float(values[3]),
                        'num_vertices': float(values[4]),
                        'num_surfaces': float(values[5]),
                        'num_segments': float(values[6]),
                        'num_objects': float(values[7]),
                        'num_regions': float(values[8]),
                        'num_portals': float(values[9]),
                        'num_levels': float(values[10]),
                        'xlo': float(values[16]),
                        'ylo': float(values[17]),
                        'zlo': float(values[18]),
                        'xhi': float(values[19]),
                        'yhi': float(values[20]),
                        'zhi': float(values[21]),
                    }
                elif category == 'level':
                    self.levels = self.levels.append({
                        'index': values[0],
                        'num_regions': float(values[1]),
                        'label': values[2],
                        'px': float(values[3]),
                        'py': float(values[4]),
                        'pz': float(values[5]),
                        'xlo': float(values[6]),
                        'ylo': float(values[7]),
                        'zlo': float(values[8]),
                        'xhi': float(values[9]),
                        'yhi': float(values[10]),
                        'zhi': float(values[11])
                    }, ignore_index=True)
                elif category == 'region':
                    self.regions = self.regions.append({
                        'region_index': int(values[0]),
                        'level_index': int(values[1]),
                        'label': values[4],
                        'px': float(values[5]),
                        'py': float(values[6]),
                        'pz': float(values[7]),
                        'xlo': float(values[8]),
                        'ylo': float(values[9]),
                        'zlo': float(values[10]),
                        'xhi': float(values[11]),
                        'yhi': float(values[12]),
                        'zhi': float(values[13]),
                        'height': float(values[14])
                    }, ignore_index=True)
                elif category == 'portal':
                    self.portals = self.portals.append({
                        'portal_index': float(values[0]),
                        'region0_index': float(values[1]),
                        'region1_index': float(values[2]),
                        'label': values[3],
                        'xlo': float(values[4]),
                        'ylo': float(values[5]),
                        'zlo': float(values[6]),
                        'xhi': float(values[7]),
                        'yhi': float(values[8]),
                        'zhi': float(values[9]),
                    }, ignore_index=True)
                elif category == 'surface':
                    # Has a 0 in the middle
                    self.surfaces = self.surfaces.append({
                        'surface_index': float(values[0]),
                        'region_index': float(values[1]),
                        'label': values[3],
                        'px': float(values[4]),
                        'py': float(values[5]),
                        'pz': float(values[6]),
                        'nx': float(values[7]),
                        'ny': float(values[8]),
                        'nz': float(values[9]),
                        'xlo': float(values[10]),
                        'ylo': float(values[11]),
                        'zlo': float(values[12]),
                        'xhi': float(values[13]),
                        'yhi': float(values[14]),
                        'zhi': float(values[15]),
                    }, ignore_index=True)
                elif category == 'vertex':
                    self.vertex = self.vertex.append({
                        'vertex_index': float(values[0]),
                        'surface_index': float(values[1]),
                        'label': values[2],
                        'px': float(values[3]),
                        'py': float(values[4]),
                        'pz': float(values[5]),
                        'nx': float(values[6]),
                        'ny': float(values[7]),
                        'nz': float(values[8]),
                    }, ignore_index=True)
                elif category == 'panorama':
                    # Has a 0 in the middle
                    self.panoramas = self.panoramas.append({
                        'name': values[0],
                        'panorama_index': values[1],
                        'region_index': values[2],
                        'px': float(values[4]),
                        'py': float(values[5]),
                        'pz': float(values[6]),
                    }, ignore_index=True)
                elif category == 'image':
                    cols = self.images.columns
                    self.images = self.images.append({
                        x: y if len(x) > 3 or 'index' not in x else float(y)
                        for x, y in zip(cols, values)
                    }, ignore_index=True)
                elif category == 'category':
                    cols = self.categories.columns
                    self.categories = self.categories.append({
                        x: y if len(x) > 3 or 'index' not in x else float(y)
                        for x, y in zip(cols, values)
                    }, ignore_index=True)
                elif category == 'object':
                    cols = self.objects.columns
                    self.objects = self.objects.append({
                        x: y if len(x) > 3 or 'index' not in x else float(y)
                        for x, y in zip(cols, values)
                    }, ignore_index=True)
                elif category == 'segment':
                    cols = self.segments.columns
                    self.segments = self.segments.append({
                        x: y if len(x) > 3 or 'index' not in x else float(y)
                        for x, y in zip(cols, values)
                    }, ignore_index=True)
                else:
                    logging.info('Missing category:', category)

    def save_mapping(self, path: str = None):
        if path is None:
            path = self.__cache_path

        with open(path, 'wb') as ar:
            pickle.dump(self, ar)

    @classmethod
    def load_mapping(cls, house_id: str) -> T:
        cache_path = f'./metadata_parser/house_cache/{house_id}.pickle'
        if os.path.isfile(cache_path):
            logging.info('Cached file exists, loading.')
            with open(cache_path, 'rb') as ar:
                return pickle.load(ar)

        logging.info('No cache found. Generating from data')
        metadata = cls(house_id)
        metadata.__parse_file()
        logging.info('Finished generating. Caching data')
        metadata.save_mapping(cache_path)
        return metadata

    def viewpoint_objects(self, viewpoint_id: str) -> pd.DataFrame:
        region = self.panoramas.query(f'name == "{viewpoint_id}"')['region_index'].values[0]
        objects = self.objects.query(f'region_index == "{region}"')
        return objects


if __name__ == '__main__':

    base_path = '~/datasets/Matterport3DSimulator/houses/v1/scans'
    HouseSegmentationFile.base_path = base_path

    house_id = 'Z6MFQCViBuw'
    viewpoint_id = 'fe0787eb7f0348f0a0b0e84c25833fd7'
    metadata = HouseSegmentationFile.load_mapping(house_id)
    print(metadata.viewpoint_objects(viewpoint_id).head())
