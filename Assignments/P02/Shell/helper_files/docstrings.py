cd_doc= """
    USAGE: cd [dir]

    DESCRIPTION:
    Change the current directory to DIR.  The variable $ is the
    default DIR.  The variable CD PATH defines the search path for
    the directory containing DIR.A null directory name is the same as
    the current directory, i.e. `.'.  If DIR begins with a slash (/),
    then CD PATH is not used.  

    EXAMPLES:
     The command:

        cd dir1 : change directory to dir1
        cd dir1/dir2 : change directory to dir2
        cd .. : change to parent directory
        cd ~ : change to home directory
        cd dir1/dir2/../inDir2: change to directory inDir1 in Dir1  
"""

chmod_doc = """
    USAGE: chmod [MODE] [FILE...]

    DESCRIPTION:
    Change the file mode bits.
"""

clear_doc = """
USAGE: clear 

DESCRIPTION:
       clear clears your screen if this is possible, 
       including its scrollback buffer. clear ignores 
       any command-line parameters that may be present.
"""

echo_doc = """
USAGE: echo [-n] [string ...]

DESCRIPTION: 
    Applications aiming for the echo utility writes any specified operands, 
    separated by single blank(‘ ’) characters and followed by a newline 
    (‘\n’) character, to the standard output.

OPTIONS:
    echo – write arguments to the standard output
    -n    Do not print the trailing newline character. 

EXAMPLES:
    The command:

        echo [string]

    will print the contents  to the standard output.
"""

exit_doc = """
USAGE: exit 

DESCRIPTION:
    Exit from the terminal.
"""

cat_doc = """    

USAGE: cat [OPTION]... [FILE]...

DESCRIPTION:
    The cat utility reads files sequentially, writing them to the standard
    output.  The file operands are processed in command-line order. 

EXAMPLES:
    The command:

        cat file1

    will print the contents of file1 to the standard output.

    The command:

        cat file1 file2 > file3

    will sequentially print the contents of file1 and file2 to the file
    file3, truncating file3 if it already exists.  
"""

head_doc= """
USAGE: head [-n count] [file ...]

DESCRIPTION:
     head – display first 10 lines of a file if no options are mentioned.

OPTIONS:
    [-n  count]: count specifies number of lines printed.

EXAMPLES:
    To display the first 500 lines of the file foo:

        $ head -n 500 foo

    head can be used in conjunction with tail(1) in the following way to, for
    example, display only line 500 from the file foo:

        $ head -n 500 foo | tail -n 1
"""

tail_doc= """
USAGE: tail [-n count] [file ...]

DESCRIPTION:
    tail – display the last part of a file

OPTIONS:
    [-n  count]: count specifies number of lines to be printed.

EXAMPLES:
    To display the last 500 lines of the file foo:

        $ tail -n 500 foo
"""

touch_doc= """
USAGE: touch [OPTION...] [file ...]

DESCRIPTION:
    touch – change file access and modification times
    The touch utility sets the modification and access times of files. If
    any file does not exist, it is created with default permissions.
"""

less_doc= """
USAGE: less [file ...]

DESCRIPTION:
    Less is a program similar to more(1), but which allows backward
    movement in the file as well as forward movement.  Also, less does not
    have to read the entire input file before starting.  

COMMANDS:
    q: quit from less command execution.
    n: next page of total page.
"""

mv_doc= """
USAGE: mv [source] [Dir..]
   
DESCRIPTION:
    Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.
"""

cp_doc= """
USAGE: cp [files] [Dir..]

DESCRIPTION:
    copy files to DEST, or move SOURCE(s) to DIRECTORY.
"""

rm_doc= """
USAGE: rm [files]

DESCRIPTION:
    remove files from directory.
"""

grep_doc = """
USAGE: grep [OPTION]... PATTERNS [FILE]...

DESCRIPTION:
    The grep utility searches any given input files, selecting lines that
    match one or more patterns.  By default, a pattern matches an input line
    if the regular expression (RE) in the pattern matches the input line
    without its trailing newline.  An empty expression matches every line.
    Each input line that matches at least one of the patterns is written to
    the standard output.

    grep is used for simple patterns and basic regular expressions (BREs);
    egrep can handle extended regular expressions (EREs).  See re_format(7)
    for more information on regular expressions.  fgrep is quicker than both
    grep and egrep, but can only handle fixed patterns (i.e., it does not
    interpret regular expressions).  Patterns may consist of one or more
    lines, allowing any of the pattern lines to match a portion of the input.

OPTIONS:
    -i, --ignore-case         ignore case distinctions in patterns and data
    -l, --files-with-matches  print only names of FILEs with selected lines
    -c, --count only a count of selected lines is written to standard output.
"""

history_doc = """
USAGE: history 

DESCRIPTION:
    Shows the history of commands executed in the current session
"""

ls_doc = """ 
USAGE: ls [OPTION]... [FILE]...

DESCRIPTION:
    For each operand that names a file of a type other than directory, ls
    displays its name as well as any requested, associated information.  For
    each operand that names a file of type directory, ls displays the names
    of files contained within that directory, as well as any requested,
    associated information.

OPTIONS:
    -a, --all                  do not ignore entries starting with .
    -h, --human-readable       with -l and -s, print sizes like 1K 234M 2G etc.
    -l                         use a long listing format
 """

mkdir_doc = """
USAGE: mkdir [OPTION]... DIRECTORY...

DESCRIPTION:
    If directory already exist, update modified date.
    Create the DIRECTORY, if they do not already exist.

EXAMPLES:
     Create a directory named foobar:

        $ mkdir foobar
        $ mkdir dir/new_directory
"""

pwd_doc = """
USAGE: pwd [OPTION..]

DESCRIPTION:
    pwd – return working directory name.
    The pwd utility writes the absolute pathname of the current working
    directory to the standard output.

EXAMPLES:
     Create a directory named foobar:

        $ pwd 
        /usr/home/fernape
"""

sort_doc = """
USAGE: sort [OPTION..] [file...]

DESCRIPTION:
     The sort utility sorts text and binary files by lines.  A line is a
     record separated from the subsequent record by a newline (default) or NUL
     ´\0´ character (-z option).  A record can contain any printable or
     unprintable characters.  Comparisons are based on one or more sort keys
     extracted from each line of input, and are performed lexicographically,
     according to the current locale's collating rules and the specified
     command-line options that can tune the actual sorting behavior.  By
     default, if keys are not given, sort uses entire lines for comparison.

OPTIONS:
    -n, --numeric-sort, --sort=numeric
        Sort fields numerically by arithmetic value.  Fields are supposed
        to have optional blanks in the beginning, an optional minus sign,
        zero or more digits (including decimal point and possible
        thousand separators).

    -r, --reverse
        Sort in reverse order.
"""

wc_doc = """

    USAGE: wc [OPTION]... [FILE]...

    DESCRIPTION:
    Print newline, word, and byte counts for each FILE, and a total line if
    more than one FILE is specified. A word is a non-zero-length sequence of
    characters delimited by white space.

    OPTIONS:
        -l, --lines            print the newline counts  
        -w, --words            print the word counts
 """
 
whoami_doc = """
    USAGE: whoami 

    DESCRIPTION:
    This function gets the current user and current directory structure which are used to 
    print prompt in command line.
"""

