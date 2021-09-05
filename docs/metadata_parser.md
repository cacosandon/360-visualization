# Metadata Parser

This documentation will detail the inner workings and usage of [parse_house_segmentations.py](../metadata_parser/parse_house_segmentations.py).

An instance of `HouseSegmentationFile` contains the information of an xxx.house file (as shown in [matterport3D github](https://github.com/niessner/Matterport/blob/master/data_organization.md)), parsed into pandas DataFrames.

A different DataFrame is created for each type of line within the file (levels, regions, portals, surfaces, vertices, panoramas, images, categories, objects and edges). Also, a dictionaru is created with the information in the header line.

## Parsing, Caching and Loading House Data

### Data Parsing and Caching

If you don't have the cache'd files, this script will parse the data from the xxx.house file. To do this, you have to set the path to the Matterport3DSimulator house scans path. Then, when the object is instanced with a specific house id, it will read the file and parse it into dataframes. It will also save a file with this data in pickle form in [house_cache](../metadata_parser/house_cache), so that the next time it will load faster (this also requires you to set the path for the house_cache folder).

```py
HouseSegmentationFile.base_path = "Matterport3DSimulator/houses/v1/scans"
HouseSegmentationFile.base_cache_path = "metadata_parser/house_cache"

metadata = HouseSegmentationFile(house_id)
```

### Data Loading

If a cache file is present, calling `HouseSegmentationFile.load_mapping(house_id)` will prioritize loading the data from the cache, which is a lot faster. This function will also generate the cache if it doesn't exist.

```py
HouseSegmentationFile.base_path = "Matterport3DSimulator/houses/v1/scans"
HouseSegmentationFile.base_cache_path = "metadata_parser/house_cache"

metadata = HouseSegmentationFile.load_mapping(house_id)
```

## Usage

Assuming you have already instanciated the metadata for a house, you can now access the data on the pandas dataframes as instance attributes, for example:

```py
metadata.objects
```

Is the dataframe containing all objects in the house.

### Available Methods

All methods are documented within the code. Here's a list of implemented methods:

- `get_panorama(viewpoint_id)`
- `get_region(viewpoint_id)`
- `get_reigon_index(viewpoint_id)`
- `viewpoint_objects(viewpoint_id)`
- `relative_viewpoint_objects(viewpoint_id)`
- `angle_relative_viewpoint_objects(viewpoint_id)`
- `angle_relative_viewpoints(viewpoint_id)`
- `get_images_with_heading(viewpoint_id)`