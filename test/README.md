# Test

For testing, the databases of the C and Python version are compared.

    ./run_test.sh

It has been found that the mantissa rarely differs by 1 bit.  
However, this should not be a problem for calculations.  

```
+-------------+-------+-----------------------------+-----------------------------+---------------------+---------------------+
|   node_id   |  db   |    format("%!.50f",lon)     |    format("%!.50f",lat)     |    binary64_lon     |    binary64_lat     |
+-------------+-------+-----------------------------+-----------------------------+---------------------+---------------------+
| 536141      | db_c  | 7.3532162000000003132527126 | 49.310166099999996449157468 | x'401d69b181edab6a' | x'4048a7b385d3e9f7' |
| 536141      | db_py | 7.3532162000000003132527126 | 49.310166100000003552850103 | x'401d69b181edab6a' | x'4048a7b385d3e9f8' |
| 21520090    | db_c  | 7.09182739999999967039912   | 49.313916999999996447143213 | x'401c5e08007f81c0' | x'4048a82e6ea85447' |
| 21520090    | db_py | 7.09182739999999967039912   | 49.313917000000003555172656 | x'401c5e08007f81c0' | x'4048a82e6ea85448' |
| 33743557    | db_c  | 7.2362995000000003287254912 | 49.505478599999996449157468 | x'401cf1f87f023e9f' | x'4048c0b385d3e9f7' |
| 33743557    | db_py | 7.2362995000000003287254912 | 49.505478600000003552850103 | x'401cf1f87f023e9f' | x'4048c0b385d3e9f8' |
| 36160300    | db_c  | 7.2409255000000003477111931 | 49.575184900000003550800398 | x'401cf6b52c9d16fd' | x'4048c99fa8a75397' |
| 36160300    | db_py | 7.2409255000000003477111931 | 49.575184899999996447107764 | x'401cf6b52c9d16fd' | x'4048c99fa8a75396' |
+-------------+-------+-----------------------------+-----------------------------+---------------------+---------------------+
```
