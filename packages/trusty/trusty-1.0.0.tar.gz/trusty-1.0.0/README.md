# Trusty
Persistent dictionary

## Example Usage
```python
import os
import trusty

# Create a trusty dictionary.
pack = trusty.get('pack')

# Set a key value pair.
pack['food'] = 'lembas'

# Persist the dictionary to disk.
pack.save()

# Confirm that the dictionary was saved.
print(pack.location())
print(os.path.exists(pack.location()))
```

We can later retrieve the dictionary like so:
```python
import trusty

new_session = trusty.get('pack')
print(new_session)

# We can then further edit the data, and store it to the same location.
new_session['supplies'] = 'taters'
new_session.save()
```

By default, trusty saves dictionaries to `$HOME/.trusty/<dictionary_name>`. To change this, simply set the `TRUSTY_PATH` environmental variable:
```bash
# This will make .save() persist to /tmp/.trusty/<dictionary_name>
export TRUSTY_PATH='/tmp'
```
