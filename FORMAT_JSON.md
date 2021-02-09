# Implementation Details: JSON

## General Notes

JSON is a format built on attribute-value pairs (dictionaries) and arrays.
It is most commonly represented as text.

Thus, in order to differentiate between openPMD **attributes** and **data sets**, slight naming conventions need to be introduced.
An example implementation is provided in [openPMD-api](https://github.com/openPMD/openPMD-api) and in doubt, its conventions shall apply.

The following JSON keys (names) are reserved for openPMD usage with JSON:
- `attributes`
- `data`
- `datatype`

## Datatype Conventions

An openPMD **data set** is represented by a JSON object with keys `attributes`, `data` and `datatype`:
```
{"attributes": <attributes>, "data": <data>, "datatype": <datatype>}
```

**attributes** are defined further below and can also appear ath the openPMD **group** level.

The `data` dictionary stores values as a multi-dimensional array in [row-major order](https://en.wikipedia.org/wiki/Row-_and_column-major_order#Programming_languages_and_libraries).
The `datatype` key-value pair is defined for identification of the string-serialized type.

This is a reduced example, showing scalar openPMD record named `rho`, storing values in a 2D array:
```json
{
  "data": {
    "1": {
      "meshes": {
        "rho": {
          "attributes": {
            "axisLabels": {
              "datatype": "VEC_STRING",
              "value": [ "x", "y" ]
            },
            "geometry": {
              "datatype": "STRING",
              "value": "cartesian"
            },
            "unitDimension": {
              "datatype": "ARR_DBL_7",
              "value": [ 0, 0, 0, 0, 0, 0, 0 ]
            },
            "unitSI": {
              "datatype": "DOUBLE",
              "value": 1
            }
          },
          "data": [
            [ 0, 1, 2 ],
            [ 3, 4, 5 ],
            [ 6, 7, 8 ]
          ],
          "datatype": "DOUBLE"
        }
      },
      "attributes": {
        "comment": {
          "datatype": "STRING",
          "value": "1234"
        }
      }
    }
  }
}
```

The shape of an openPMD record component is derived from the array inside data in combination with its `datatype`.

### Complex Types

Complex values are serialized as simple array `[real, imaginary]`.
When reading complex data back, a reader needs to handle the case that the dimensionality of complex `data` is reduced by `1` to derive its `shape`.

### Byte Width Lookup Table

In the root of the openPMD series, an additional entry named `platform_byte_widths` shall be reserved.
It is used to map data types to byte widths for easier identification:
```json
{
  "platform_byte_widths": {
    "BOOL": 1,
    "CDOUBLE": 16,
    "CFLOAT": 8,
    "CHAR": 1,
    "CLONG_DOUBLE": 32,
    "DOUBLE": 8,
    "FLOAT": 4,
    "INT": 4,
    "LONG": 8,
    "LONGLONG": 8,
    "LONG_DOUBLE": 16,
    "SHORT": 2,
    "UCHAR": 1,
    "UINT": 4,
    "ULONG": 8,
    "ULONGLONG": 8,
    "USHORT": 2
  }
}
```
The naming conventions in [openPMD-api](https://github.com/openPMD/openPMD-api) for the types shall apply.


## Attributes

openPMD **attributes** are wrapped into an `attributes` dictionary at the location where they would usually be stored.
Inside the `attributes` dictionary, each value names an attribute.
The attribute itself is a dictionary with the value consisting of an array, containing a `datatype` and `value`.

For example, in the *root* group (path `/`) the attributes are stored as:
```json
{
  "attributes": {
    "basePath": {
      "datatype": "STRING",
      "value": "/data/%T/"
    },
    "iterationEncoding": {
      "datatype": "STRING",
      "value": "groupBased"
    }
}
```
