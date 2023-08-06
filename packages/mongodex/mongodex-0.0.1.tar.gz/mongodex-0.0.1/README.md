# mongodex

Mongodex is a Python library to migrate your MongoDB database indexes.

## Installation

```
pip install mongodex
```

## How to use

To migrate your indexes to a MongoDB database, you need to create a dictionary that contains each collection index. The indexes must be a `mongodex.Index` instance. For example:

```python
from pymongo import ASCENDING, DESCENDING
import mongodex

collections = {
    "<COLLECTION_NAME>": [
        mongodex.Index({"<FIELD_NAME>": ASCENDING}, unique=True),
        mongodex.Index({"<FIELD_NAME>": ASCENDING, "<FIELD_NAME>": ASCENDING}),
    ],
    "<COLLECTION_NAME>": [
        mongodex.Index({"<FIELD_NAME>": DESCENDING}, name="custom_index_name"),
    ]
}
```

Then you can migrate your indexes by calling the `mongodex.migrate` function with your database URI.

```python
mongodex.migrate("<DATABASE_URI>", collections)
```

## Markdown docs generator

You can also create a markdown file with all your indexes using the same collection index dictionary mentioned in the previous topic. For example:

```python
mongodex.md_generator(collections)
```
