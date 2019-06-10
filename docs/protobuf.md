# Protobuf

> Protobuf study notes.


## Content

  * [Introduction](#intro)
  * [Reference](#ref)



<br /><a name="intro"></a>
## Introduction

### Define a Message

  ```protobuf
  // addr_book.proto
  syntax = "proto2";

  package addr_book;  // no use for python

  enum PhoneType {
    MOBILE = 0;
    WORK = 1;
    HOME = 3;
  }

  message PhoneNumber {
    required string number = 1;
    optional PhoneType type = 2 [default = MOBILE];
  }

  message Person {
    required int id = 1;
    required string name = 2;
    optional string email = 3;
    repeated PhoneNumber phone = 4;
    map<string, Person> relations = 9;
  }

  message AddressBook {
    repeated Person contacts = 1;
  }
  ```

### Field number

  Field numbers (up to `2^29 - 1`, or `536,870,911`) in the range 1 through 15 take
  one byte to encode (see [Protocol Buffer Encoding](https://developers.google.com/protocol-buffers/docs/encoding.html#structure)); range 16 through 2047 take two bytes.

  Cannot use:
  - Numbers 19,000 through 19,999 (`FieldDescriptor::kFirstReservedNumber` through `FieldDescriptor::kLastReservedNumber`) are reserved.
  - Previously reserved field numbers.

### Filed type

  |protobuf| Java | Go     | Python  | Notes|
  |:-------|:-----|:-------|:--------|:-----|
  | float  | float| float32| float   ||
  | double | double|float64| float   ||
  | int32/sint32|int| int32| int     |vari-length encoding. use `sint32` for negative values.|
  | sfixed32    |int| int32| int     |always 4 bytes|
  | uint32 | int  | uint32 | int/long|vari-length encoding.|
  | int64/sint64|long|int64| int/long|vari-length encoding. use `sint64` for negative values.|
  | sfixed64    |int| int64| int/long|always 8 bytes|
  | uint64 | int  | uint64 | int/long|vari-length encoding.|
  | bool  |boolean| bool   | bool    ||
  | string |String| string | str/unicode|contain UTF-8 encoded or 7-bit ASCII text.|
  | bytes  |ByteString|[]byte| str   |any arbitrary sequence of bytes.|

  * change a field from one of these types to another won't break forwards-
    or backwards-compatibility:
    - `int32`, `uint32`, `int64`, `uint64`, and `bool`
  * these types are compatible with each other but are not compatible with the other integer types:
    - `fixed32` and `sfixed32`
    - `fixed64` and `sfixed64`
    - `sint32` and `sint64`
  * these types are compatible as long as the bytes are valid UTF-8:
    - `string` and `bytes`
  * in terms of wire format, `enum` is compatible with `int32`, `uint32`, `int64`, and `uint64`.
    however, deserialization is language-dependent.


### Enumerations

  * every enum definition must contain a constant that maps to zero as its first element, also as a numeric default value for such enum type.
  * enumerator constants must be in the range of a 32-bit integer; however, negative values are inefficient and thus not recommended.
  * any removing enum entry (name and value) should be specified as "`reserved`".

    ```protobuf
    enum Foo {
      DEF = 0;
      // OLD = 2 [deprecated=true];
      NEW = 3;
      // BAR = 15;
      reserved 2, 15, 9 to 11, 40 to max;
      reserved "OLD", "BAR";
    }
    ```

### Import

  Assume an `def.proto` file is moved to `new/location`.

  ```protobuf
  // new/location/def.proto
  // All original `def.proto` definitions are moved here.
  ```
  And there is a dummy "`def.proto`" in original location to forward all imports
  to "`new/location`".

  ```protobuf
  // def.proto
  // This is some proto that all clients are importing.
  import public "new/location/def.proto"; // only public import are transitive.
  import "misc.proto";
  ```
  Dependencies can be transitively relied upon by anyone importing the proto
  containing the "`import public`" statement.

  ```protobuf
  // client.proto
  import "def.proto";
  // Now can use definitions from def.proto and old.proto, but not misc.proto
  ```

  It's possible to import proto2 message types and use them in your proto3 messages, and vice versa. However, proto2 enums cannot be used directly in proto3 syntax (it's okay if an imported proto2 message uses them).



<br /><a name="ref"></a>
## Reference

  * https://developers.google.com/protocol-buffers/docs/overview
