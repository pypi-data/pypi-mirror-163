# Py4DMath

Py4DMath is a math engine that contains functions which allows a 3D object to translate and rotate.

It consists of the following classes:
1) Vectors
2) Matrix
3) Quaternions

## Table of Contents
- [Documentation](#documentation)
- [Developer's Guide](#developers-guide)
- [Contact](#contact)

## Documentation

This section is meant to outline the classes, please see the documented section of code for more details.

### Vector3D

```
A class to represent a vector in 3D space.

...
Attributes
----------
  x: float
    the x position of the vector
  y: float
    the y position of the vector
  z: float
    the z position of the vector

Methods
----------
  copy():
    Returns a copy of the vector.
  show():
    Prints visual representation of the vector.
  add():
    Returns the result of vector addition.
  subtract():
    Returns the result of vector subtraction.
  multiply():
    Returns a vector multiplied by a scalar value.
  divide():
    Returns a vector divided by a scalar value.
  dot():
    Returns the dot product between two vectors.
  cross():
    Returns the cross product between two vectors.
  magnitude():
    Returns the magnitude of the vector.
  normalize():
    Returns the normalized unit vector.
  rotate():
    Rotates a vector using an angle and an axis.
```

### Matrix3D

```
A class to represent a 3x3 matrix.

...
Attributes
----------
  matrix: float[9]
    the array representing the matrix (column-major format)

Static/Class Methods
----------
  getIdentityMatrix():
    Returns an identity matrix.

Methods
----------
  copy():
    Returns a copy of the matrix.
  show():
    Prints visual representation of matrix.
  add():
    Returns the result of matrix addition.
  subtract():
    Returns the result of matrix subtraction.
  scalar_multiply():
    Returns a vector multiplied by a scalar value.
  matrix_multiply():
    Returns a vector multiplied by another matrix.
  inverse():
    Returns the inverse of the matrix.
  transpose():
    Returns the transpose of the matrix.
  transform():
    Returns vector transformed by matrix.
```

### Quaternion

```
A class representing a Quaternion.

q = s + v

where s is a scalar number, v is a vector representing an axis

...
Attributes
----------
  s: float
    the scalar number
  v: Vector3D
    the vector representing an axis

Static/Class Methods
----------
  getRotationQuaternion():
    Returns the rotation quaternion.

Methods
----------
  copy():
    Returns a copy of the quaternion.
  add():
    Returns the result of quaternion addition.
  subtract():
    Returns the result of quaternion subtraction.
  scalar_multiply():
    Returns the result of a quaternion multiplied by a scalar value.
  quaternion_multiply():
    Returns the result of quaternion multiplication.
  norm():
    Returns the norm of the quaternion.
  normalize():
    Returns the normalized quaternion (unit norm).
  conjugate():
    Returns the conjugate of the quaternion.
  inverse():
    Returns the inverse of the quaternion.
```

## Developer's Guide

### Prerequistes
- Python 3.10+
- virtualenv

### Installation

1) Create a new virtual environment, if not already created

```
python -m virtualenv venv
```

2) Activate the virtual environment

```
source venv/bin/activate
```

3) Install dependencies

```
make install-deps
```

### Version Changes

***NOTE***: When making updates to the source code, make sure to bump versions.

1) Update the version number in Py4DMath/version.py, using [semantic versioning](https://semver.org).

2) Update the CHANGES.txt with the new version number and detail what changed.

### Deployment

This package is available on PyPi.

To deploy to PyPi,

1) Build the `dist` package using `make build`

2) Upload to PyPi using `make upload`

## Contact 
Nicholas Chumney - [nicholas.chumney@outlook.com](nicholas.chumney@outlook.com) 

## Acknowledgements
- [3D Math Engine Project](https://www.haroldserrano.com/math-engine-project/)
