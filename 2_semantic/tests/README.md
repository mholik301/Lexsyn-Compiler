# Testing your semantic analyzer

0. If on Linux, the first-time-only prep is setting the execute flag
    `sudo chmod +x analyze.sh`
    `sudo chmod +x compare.sh`
1. Place the analyzer source code in the `./tests` folder
2. Position a shell in `./tests`, compile the source code and start the tests by running `./analyze.sh` (it will take around a minute)
3. Next, run `./compare.sh` to generate a report comparing expected vs your outputs, found in `differences.txt`

# Explanations of the files

- `c` - source code used to generate the syntax tree

- `lex` - output created by lexical analysis

- `in` - generative tree, aka. input to your semantic analyzer

- `out` - your semantic analyzer output (might be empty) -> found in /expectedOutput

- `explain` - input explanation (what happened, on which line)
  
     - note: `.out` and `.explain` files will be empty if `.c` is semantically correct

# Explanation of `differences.txt`

Entries will be in the following format

```
input/file.in
===========================================
<differences between expected and your output>
```

For example

```
input/file1.in
===========================================
input/file2.in
===========================================
<error message>
input/file3.in
===========================================
```

- Files 1 and 3 tested okay, while there was an error parsing file2



`<error message>` is the output of `diff`, meaning

```
# means your analyzer didnt output anything, and it was supposed to output <expected output>
0a1:
  <expected output>

# means your analyzer outputted <your output>, and it was not supposed to output anything
1d0:
  <your output>

# mismatch between <your output> and <expected output>:
1c1:
  <your output>
  ----
  <expected output>
```
