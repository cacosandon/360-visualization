# Simulator object visualization with 360° views

At first, fill the constants and the import paths for correctly importing the Matterport 3D Simulator (`MatterSim`) and the metadata parser provided in this repository.

You are able to select any scan and viewpoint, all scans are provided below. To get the viewpoints/panoramas, you would like to use the following script provided also on this repository:

```python

# Located on metadata_parser/
from parse_house_segmentations import HouseSegmentationFile

base_cache_path = '/360-visualization/metadata_parser/house_cache' # Or the directory where cached files are stored
base_path = 'Matterport3DSimulator/houses/v1/scans' # Or the folder containing the scans with xxx.house files
HouseSegmentationFile.base_cache_path = base_cache_path
HouseSegmentationFile.base_path = base_path

scan = '17DRP5sb8fy'

metadata = HouseSegmentationFile.load_mapping(scan)
metadata.panoramas
```

---

## Scan IDs (i.e. House IDs)

```python
17DRP5sb8fy # this is the one used on examples
1LXtFkjw3qL
1pXnuDYAj8r
29hnd4uzFmX
2azQ1b91cZZ
2n8kARJN3HM
2t7WUuJeko7
5LpN3gDmAk7
5q7pvUzZiYa
5ZKStnWn8Zo
759xd9YjKW5
7y3sRwLe3Va
8194nk5LbLH
82sE5b5pLXE
8WUmhLawc2A
aayBHfsNo7d
ac26ZMwG7aT
ARNzJeq3xxb
B6ByNegPMKs
b8cTxDM8gDG
cV4RVeZvu5T
D7G3Y4RVNrH
D7N2EKCX4Sj
dhjEzFoUFzH
E9uDoFAP3SH
e9zR4mvMWw7
EDJbREhghzL
EU6Fwq7SyZv
fzynW3qQPVF
GdvgFV5R1Z5
gTV8FGcVJC9
gxdoqLR6rwA
gYvKGZ5eRqb
gZ6f7yhEvPG
HxpKQynjfin
i5noydFURQK
JeFG25nYj2p
JF19kD82Mey
jh4fc5c5qoQ
JmbYfDe2QKZ
jtcxE69GiFV
kEZ7cmS4wCh
mJXqzFtmKg4
oLBMNvg9in8
p5wJjkQkbXX
pa4otMbVnkk
pLe4wQe7qrG
Pm6F8kyY3z2
pRbA3pwrgk9
PuKPg4mmafe
PX4nDJXEHrG
q9vSo1VnCiC
qoiz87JEwZ2
QUCTc6BB5sX
r1Q1Z4BcV1o
r47D5H71a5s
rPc6DW4iMge
RPmz2sHmrrY
rqfALeAoiTq
s8pcmisQ38h
S9hNv5qa7GM
sKLMLpTHeUy
SN83YJsR3w2
sT4fr6TAbpF
TbHJrupSAjP
ULsKaCPVFJR
uNb9QFRL6hY
ur6pFq6Qu1A
UwV83HsGsw3
Uxmj2M2itWa
V2XKFyX4ASd
VFuaQ6m2Qom
VLzqgDo317F
Vt2qJdWjCF2
VVfe2KiqLaN
Vvot9Ly1tCj
vyrNrziPKCB
VzqfbhrpDEA
wc2JMjhGNzB
WYY7iVyf5p8
X7HyMhZNoso
x8F5xyUWy9e
XcA2TqTSSAj
YFuZgdQ5vWj
YmJkqBEsHnH
yqstnuAEVhm
YVUC4YcDtcY
Z6MFQCViBuw
ZMojNkEp431
zsNo4HB9uLZ

```
