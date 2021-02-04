# Implementation Details: HDF5

## General Notes

Generally, implementations of openPMD shall be as compatible as possible to the low-level datatype conventions supported by the popular [h5py](https://www.h5py.org) library.
The motivation behind this is that many post-processing tools rely on or can effectively be implemented against `h5py`.

## Datatype Conventions

Also see the [h5py datatypes FAQ](https://docs.h5py.org/en/latest/faq.html).

### Boolean Types

HDF5 is a C library and as such as no notion for boolean types.
Although the openPMD-standard avoids using boolean types itself, developers might choose to implement them as attributes or dataset types.

For compatibility, boolean types shall be stored as HDF5 enum.
The enum type is a one-byte `H5T_NATIVE_INT8`.
The enum labels are `TRUE` (values of `1`) and `FALSE` (values of `0`).

#### h5dump output

Example output from `h5dump` for a boolean attribute with name `mybool`:
```
ATTRIBUTE "mybool" {
  DATATYPE  H5T_ENUM {
      H5T_STD_I8LE;
      "TRUE"             1;
      "FALSE"            0;
   }
   DATASPACE  SCALAR
   DATA {
   (0): FALSE
   }
}
```

#### C++ Snippet

Example code to create a custom HDF5 type `m_H5T_BOOL_ENUM` that is compatible to `h5py` boolean representation:

```c++
#include <hdf5.h>
#include <cassert>
#include <cstdint>
// ...

/* ... */ {
    // declare a type for boolean
    hid_t m_H5T_BOOL_ENUM{H5Tenum_create(H5T_NATIVE_INT8)};
    assert(m_H5T_BOOL_ENUM >= 0);

    // add case-sensitive labels
    std::string t{"TRUE"};
    std::string f{"FALSE"};
    int64_t tVal = 1;
    int64_t fVal = 0;
    herr_t status;
    status = H5Tenum_insert(m_H5T_BOOL_ENUM, t.c_str(), &tVal);
    assert(status == 0);
    status = H5Tenum_insert(m_H5T_BOOL_ENUM, f.c_str(), &fVal);
    assert(status == 0);
}
```


### Complex Types

HDF5 has no unified convention to represent complex types.
Although the openPMD-standard avoids complex types itself, developers might choose to implement them as attributes or dataset types.

For compatibility, complex types shall be stored as HDF5 compound (struct).
The compound type consists of a simple, unpadded sequence of two floating point numbers of the same type.
The order is real and then imaginary part of the complex number.
The compound labels are `r` (the real part)  and `i` (the imaginary part).

#### h5dump output

Example output from `h5dump` for a complex double attribute with name `mycplxdouble`:
```
ATTRIBUTE "mycplxdouble" {
   DATATYPE  H5T_COMPOUND {
      H5T_IEEE_F64LE "r";
      H5T_IEEE_F64LE "i";
   }
   DATASPACE  SCALAR
   DATA {
   (0): {
         3,
         4
      }
   }
}
```

#### C++ Snippet

Example code to creates three custom HDF5 types `m_H5T_CFLOAT`, `m_H5T_CDOUBLE` and `m_H5T_CLONG_DOUBLE` that are compatible to `h5py` complex representation:

```c++
#include <hdf5.h>
#include <cassert>
// ...

/* ... */ {
    // declare types for for complex numbers of float, double and long double
    hid_t m_H5T_CFLOAT{H5Tcreate(H5T_COMPOUND, sizeof(float) * 2)},
    hid_t m_H5T_CDOUBLE{H5Tcreate(H5T_COMPOUND, sizeof(double) * 2)},
    hid_t m_H5T_CLONG_DOUBLE{H5Tcreate(H5T_COMPOUND, sizeof(long double) * 2)}
    assert(m_H5T_CFLOAT >= 0);
    assert(m_H5T_CDOUBLE >= 0);
    assert(m_H5T_CLONG_DOUBLE >= 0);

    // add case-sensitive labels
    H5Tinsert(m_H5T_CFLOAT, "r", 0, H5T_NATIVE_FLOAT);
    H5Tinsert(m_H5T_CFLOAT, "i", sizeof(float), H5T_NATIVE_FLOAT);
    H5Tinsert(m_H5T_CDOUBLE, "r", 0, H5T_NATIVE_DOUBLE);
    H5Tinsert(m_H5T_CDOUBLE, "i", sizeof(double), H5T_NATIVE_DOUBLE);
    H5Tinsert(m_H5T_CLONG_DOUBLE, "r", 0, H5T_NATIVE_LDOUBLE);
    H5Tinsert(m_H5T_CLONG_DOUBLE, "i", sizeof(long double), H5T_NATIVE_LDOUBLE);
}
```

#### Fortran Snippet

Example code to create a HDF5 type `m_H5T_CREAL8` that is compatible to `h5py` complex representation:

```fortran
USE hdf5
USE ISO_C_BINDING
IMPLICIT NONE

INTEGER, PARAMETER :: r_k8 = KIND(0.0d0)
INTEGER(HID_T)   :: m_H5T_CREAL8
INTEGER :: error
INTEGER :: i
INTEGER(8) :: real_size, real_complex_size

! ...

real_size = storage_size(1_r_k8, r_k8) / 8
real_complex_size = real_size * 2_8  ! a complex is (real,real)

! declare a type for complex numbers of r_k8
CALL H5Tcreate_f(H5T_COMPOUND_F, real_complex_size, m_H5T_CREAL8, error)
! add case-sensitive labels
CALL H5Tinsert_f( m_H5T_CREAL8, "r", &
   0_8, h5kind_to_type(r_k8,H5_REAL_KIND), error)
CALL H5Tinsert_f( m_H5T_CREAL8, "i", &
   real_size, h5kind_to_type(r_k8,H5_REAL_KIND), error)
```

Types for other real-kinds are defined equivalently.
A fully self-contained example writing a 1D field of complex floating point values [can be found here](https://gist.github.com/ax3l/807f5bd7e10f4277ac3a498552a9726d).


### Strings

Strings can be stored in multiple formats in HDF5, some easier and some harder to read.
openPMD tries to rely on simple semicolon-separted lists of strings where possible to store simple attributes.
Nonetheless, some use cases might need to store arrays of strings.

For compatibility, arrays of strings shall be implemented as fixed-length strings and `\0` padded to the longest value.

#### h5dump output

Example output from `h5dump` for a 1D array of strings with name `axisLabels`:
```
ATTRIBUTE "axisLabels" {
   DATATYPE  H5T_STRING {
      STRSIZE 5;
      STRPAD H5T_STR_NULLTERM;
      CSET H5T_CSET_ASCII;
      CTYPE H5T_C_S1;
   }
   DATASPACE  SIMPLE { ( 3 ) / ( 3 ) }
   DATA {
   (0): "r", "theta", "phi"
   }
}
```

Example output from `h5dump` for a scalar string attribute with name `comment`:
```
ATTRIBUTE "comment" {
   DATATYPE  H5T_STRING {
      STRSIZE 33;
      STRPAD H5T_STR_NULLPAD;
      CSET H5T_CSET_ASCII;
      CTYPE H5T_C_S1;
   }
   DATASPACE  SCALAR
   DATA {
   (0): "this is a scalar string attribute"
   }
}
```

#### Python Snippet

Example code to create a type named `atype` for writing the `axisLabels` attribute with varying length of strings per axis:
```py
import h5py as h5
# ...

# ... create a file and open the h5.Group meshes at the openPMD meshesPath location
E = meshes["E"]
E.attrs["axisLabels"] = np.array([b"r", b"theta", b"phi"])
E.attrs["comment"] = np.string_("this is a scalar string attribute")
```

#### C++ Snippet

Example code to create a type named `atype` for writing the `axisLabels` attribute with varying length of strings per axis:
```c++
#include <hdf5.h>

#include <algorithm>
#include <cassert>
#include <cstddef>
#include <cstring>
#include <memory>
#include <string>
#include <vector>
// ...

/* ... */ {
   // a vector-of-strings for axisLabels
   std::vector< std::string > vs = {"r", "theta", "phi"};

   // find longest string
   std::size_t max_len = 0u;
   for( std::string const& s : vs )
       max_len = std::max(max_len, s.size());

   // concatiante into a zero-padded array
   std::unique_ptr< char[] > c_str(new char[max_len * vs.size()]);
   for( size_t i = 0; i < vs.size(); ++i )
       strncpy(c_str.get() + i*max_len, vs[i].c_str(), max_len);

   /* Create the 1D dataspace for the array */
   //   number of elements
   hsize_t dimsa[1] = {vs.size()};
   hid_t aid = H5Screate_simple(1, dimsa, NULL);
   hid_t atype = H5Tcopy(H5T_C_S1);

   //   size of each element (all padded to same size)
   herr_t status = H5Tset_size(atype, max_len);
   assert(status >= 0);

   /* Write the attribute */
   // ... H5Gopen, H5Acreate, ...
   H5Awrite(attr, atype, c_str.get());
   // ...
}
```
