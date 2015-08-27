# pather

Manage file system structure using patterns. 
Parse, format and list your paths.

### Search you file structure

Need to look up a specific dataset in your file structure? Easy and fast.

```python
import pather
pather.ls('project/assets/{item}/{task}/published/{family}')
# ['project/assets/john/modeling/published/model',
#  'project/assets/john/modeling/published/review',
#  'project/assets/mike/rigging/published/rig',
#  'project/assets/mike/modeling/published/model']
```

Have your pattern defined and want to perform a subquery. Let's do it!

```python
import pather
pather.ls('project/assets/{item}/{task}/published/{family}', data={'item': 'mike'})
# ['project/assets/mike/rigging/published/rig',
#  'project/assets/mike/modeling/published/model']
```

### Format your paths

Have some information about your file, but don't know where it should go?

Well, it's good you planned ahead when you started the project with a pipeline.

Let's pick up the pattern you laid out for the team.

```python
import pather
pattern = '{project}/art/{episode}/{character}/{application}
data = {'project': "foobar",
        'episode': "s01e01",
        'character': "john_doe",
        'application': "photoshop"}

pather.format(pattern, data)
# "foobar/art/s01e01/john_doe/photoshop"
```

### Parse the data from a path

So you've found yourself in a location in the project and want to grab the information about where you are. 

Parse it.

```python
import pather
path = 'stuntman_production/art/s08e15/crazy_horse/maya'
pattern = '{project}/art/{episode}/{character}/{application}

data = pather.parse(pattern, parse)
# {'project': "stuntman_production",
#  'episode': "s08e15",
#  'character': "crazy_horse",
#  'application': "maya"}
```

### Get your freak on

Want to spice it up? 

So you want to find all other versions of the model that you're currently using.

```python
current_file = 'thedeal/assets/ben/modeling/published/model/ben_default/v01/'
pattern = '{project}/assets/{item}/{task}/published/{family}/{instance}/{version}/'

data = pather.parse(pattern, current_file)
data.pop('version')

all_versions = pather.ls(pattern, data=data)
# ['thedeal/assets/ben/modeling/published/model/ben_default/v01/',
#  'thedeal/assets/ben/modeling/published/model/ben_default/v02/',
#  'thedeal/assets/ben/modeling/published/model/ben_default/v03/']
```

Or find all published content among all tasks with the same version number?
```python
current_file = 'thedeal/assets/ben/modeling/published/model/ben_default/v01/'
pattern = '{project}/assets/{item}/{task}/published/{family}/{instance}/{version}/'

data = pather.parse(pattern, current_file)
# Remove the keys that we don't want to filter on.
data.pop('task')
data.pop('family')

files = pather.ls(pattern, data=data)
# ['thedeal/assets/ben/modeling/published/model/ben_default/v01/',
#  'thedeal/assets/ben/rigging/published/rig/ben_default/v01/',
#  'thedeal/assets/ben/lookdev/published/shaders/ben_default/v01/']
```

---

Managing files is ~~that~~ *dead easy*.
