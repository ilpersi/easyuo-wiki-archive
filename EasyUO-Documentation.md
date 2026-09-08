# EasyUO Documentation

A single-file rendering of the EasyUO scripting documentation, converted from the
[EasyUO wiki](http://wiki.easyuo.com/index.php?title=Documentation). Section
order follows the wiki's `Documentation` page. The non-English *Finnish Tutorial*
is preserved in the source export but omitted here.

This document is a verbatim archive of community wiki content and is licensed,
like the wiki, under the [GNU Free Documentation License, Version 1.2](http://www.gnu.org/licenses/old-licenses/fdl-1.2.html).
Original authorship and page history are on the [source wiki](http://wiki.easyuo.com/).

## Contents

- [Getting Started](#sec-getting-started)
- [Language Reference](#sec-language-reference)
- [Command Reference](#sec-command-reference)
  - [Flow Control](#sec-flow-control)
  - [Client](#sec-client)
  - [Event](#sec-event)
  - [ExEvent](#sec-exevent)
  - [Menu](#sec-menu)
  - [Namespace](#sec-namespace)
  - [Miscellaneous](#sec-miscellaneous)
  - [Obsolete](#sec-obsolete)
- [System Variable Reference](#sec-system-variable-reference)
  - [Character Variables](#sec-character-variables)
  - [Status Variables](#sec-status-variables)
  - [Container](#sec-container)
  - [Last Action](#sec-last-action)
  - [FindItem](#sec-finditem)
  - [Shop](#sec-shop)
  - [Extended](#sec-extended)
  - [Client Variables](#sec-client-variables)
  - [Combat](#sec-combat)
  - [Namespace Variables](#sec-namespace-variables)
  - [Miscellaneous Variables](#sec-miscellaneous-variables)
  - [Result](#sec-result)
  - [Tile](#sec-tile)
  - [Constant](#sec-constant)
- [Appendices](#sec-appendices)

<a id="sec-getting-started"></a>

## Getting Started

<a id="guide-installation"></a>

### Installation

Installation of EasyUO is extremely simple.

Download the zipped file from the [EasyUO downloads](http://www.easyuo.com/downloads.php) page, and unzip it to whatever directory you prefer. There are currently two versions of EUO available; 1.42 and 1.50 beta.

After unzipping it, simply run the EasyUO.exe file ( or if you took 1.5, run "EUOX.EXE". )

> [!NOTE]
> 
>
> - Some scripts may require 1.5 in order to work as intended. Pay attention to this.
> - REMEMBER! EasyUO only works with the 2D client.
> - Many scripts call rails or other scripts from the install folder and make use of the path variable to determine the path of the client. Best to put all scripts in the Easy UO Installation folder

<a id="guide-introduction"></a>

### Introduction

#### What is EasyUO?

EasyUO is a FREE piece of software that enables you to write scripts that make your characters in Ultima Online do pretty much anything possible.

Simple answer, but what does that mean? An example:

    msg #smc Hello Sosaria$
    halt

This is a very simple example. The possibilities are endless and are really only limited by your imagination.

#### What can EasyUO do?

The possibilities in EasyUO are, pretty much, only limited by your own imagination. Here are a couple of ideas:

- Skill training
- Crafting
- Purchasing
- Survival
- and anything else you might come up with

<a id="guide-beginners-tutorial"></a>

### Beginner's Tutorial

#### What do I need?

In this tutorial we assume you are running the latest Ultima Online client, and you have installed the latest EasyUO update.

To get started, follow these simple guidelines:

1.  Make sure you have the correct EasyUO version for the current client version.
2.  Start your Ultima Online client (Remember it only works with the 2D client).
3.  Start the EasyUO program.
4.  Log in with a character.

#### Your first EasyUO script

Copy and Paste, or type in the following program:

    msg #smc Hello there!$
    halt

Now press the Run icon or press F9 inside the EasyUO script. Your character will now whisper: "Hello there!".

#### Something useful

Now we are going to try to do something more useful. We will move the character using the [move](#cmd-move) command:

    ; Calculate a new x co-ordinate based on your current position
    set %newX #charPosX + 2
    ; Calculate a new y co-ordinate based on your current position
    set %newY #charPosY + 2
    ; Move the character to the new position
    move %newX %newY 0 10s
    halt

Now we are going to open a pack using some of the event commands. First, we need to identify the ID of your backpack (inventory):

1.  Make sure you have the variable view open. Press Ctrl-R or choose View\|Variables\|Show.
2.  Open the backpack by double clicking it in your paperdoll.
3.  Find the #LOBJECTID variable in the list.
4.  Write down the value that's next to #LOBJECTID. It consists of 6-8 letters. That is your backpack's ID.

> [!NOTE]
> Most clients have the [BackpackId](#var-backpackid) system variable available, which automatically shows the item Id of the currently logged in character's backpack.

Then copy and paste this script into EasyUO, be sure to edit it where noted:

    ; The id of your pack. Change it to the value you wrote down
    set %pack XYZ
    ; Assign your pack's ID to the last object id system variable
    set #lObjectID %pack
    ; Run UO's client macro for "Use Last Object"
    event Macro 17
    halt

#### What's next?

With what you know now you should be able to understand most of the manual and also the various example scripts available in the example archives. You can also find other examples on the [EasyUO website](http://www.easyuo.com).

<a id="sec-language-reference"></a>

## Language Reference

<a id="ref-variables"></a>

### Variables

<a id="variables--basics"></a>

#### Basics

Variables in Easy UO come in four types; Standard, Namespace, Persistent and System. The type of a variable is defined by its first character. Standard variables start with a percent sign (%), Namespace variables with an exclamation mark ( ! ), Persistent variables with an asterisk sign (\*) and System variables with an hash sign (#).

Variable names follow the same rules as other labels in EasyUO. A valid variable name starts with a letter or underscore, followed by any number of letters, numbers, or underscores.

    set %var Bob
    set %Var Joe
    msg %var %Var ; outputs "Joe Joe"

    set %4bank not_yet     ; invalid; starts with a number
    set %_4bank not_yet    ; valid; starts with an underscore

<a id="variables--standard"></a>

#### Standard Variables

Standard variables in EasyUO are represented by a percent sign (%) followed by the name of the variable. The variable name is case insensitive.

<a id="variables--namespace"></a>

#### Namespace Variables and Scope

Namespace variables in EasyUO are represented by an exclamation mark ( ! ) followed by the name of the variable. Namespace variable name is case insensitive.

Namespace variables visibility is affected by the [nameSpace](#cmd-namespace-local) command.

Namespace variables within a local namespace can only be accessed by the current script.

Namespace variables within a global namespace can be accessed by all scripts running in the same instance of EasyUO (not yet available).

<a id="variables--persistent"></a>

#### Persistent Variables

Persistent variables in EasyUO are represented by an asterisk sign (\*) followed by a variable name. In earlier versions of EasyUO, the variable names were limited to numbers between 1 to 1000 inclusive. Variable names can now be any valid variable name however, just as other types of variables.

Persistent variables are stored in the registry under the key **HKEY_CURRENT_USER\Software\EasyUO** and are therefore shared between any instance of EasyUO.

<a id="variables--system"></a>

#### System Variables

System variables in EasyUO are represented by an hash sign (#) followed by a descriptive text. As is true with everything else in EasyUO, system variable names are not case sensitive, meaning that #CHARID is the same as #charid, or even #ChArId.

System variables are all described in detail in the [System Variable Reference](#sec-system-variable-reference).

<a id="variables--scope"></a>

#### Variable Scope

The term *scope* used in reference to variables describes when a variable is known and visible to other parts of a program. The following table describes, in general, the scope of variables within EasyUO.

| type | Scope |
|----|----|
| Standard | Standard variables are visible to all code within the script that crates the variable. Standard variables are cleared when EasyUO begins executing a script. |
| Namespace | Namespace variable scope can be modified by using the Local and Global qualifiers. A Local namespace is visible only to the current script running, just as standard variables are. A Global namespace is accessible to all scripts running in the same EasyUO instance (available only in EasyUO 1.5) that have the namespace defined as global. This initializes that script's usage of the global namespace. Namespace Variables are cleared when EasyUO begins executing a script. |
| Persistent | Persistent variables are visible to all scripts running on the same computer. Persistent variables are stored in the registry and are never cleared unless you clear them in a script or edit the registry manually. |
| System | System variables are visible to each instance of EasyUO that is utilizing the same instance of Ultima Online. System Variables are not saved by EasyUO. |

<a id="ref-expressions"></a>

### Expressions

Expressions are important building blocks in an EasyUO script. They can be used to create relatively advanced integer mathematics.

An expression is any of the following:

- a literal
- a variable
- an expression enclosed with parenthesis
- an unary operator followed by an expression
- an expression followed by a binary operator and an expression

    set %var 1337 ; literal numeric value
    set %name cheffe ; literal string value
    set %temp %var
    set %faux ! #true ; unary operator
    set %var %var + 1 ; binary operator
    set %calculus ( 2 + 2 ) * ( 3 - 1 ) ; parenthesis enclosed expressions

<a id="expressions--statements"></a>

#### Statements

An EasyUO script is a sequence of statements. A statement is any of the following:

- a command
- a block
- a control structure

A command typically takes the form: \<command_name\> \<parameters\>

Example:

    set %var 2 + 2

A block is a sequence of statements grouped within brackets. Opening and closing brackets *must* occurs on a distinct line (Hence one could argue that both "{" and "}" are statements by themselves). Blocks are almost exclusively used in conjunction with control structures.

    {
        set %var 2 + 2
        display ok %var
    }

Control structure are defined individually elsewhere in the documentation.

<a id="ref-operators"></a>

### Operators

<a id="operators--arithmetic"></a>

#### Arithmetic Operators

EasyUO includes the traditional arithmetic operators as specified in the table below.

| Example | Name | Result |
|----|----|----|
| %a + %b | Addition | addition combines two numbers, the augend and addend, into a single number, the sum. |
| %a - %b | Subtraction | subtraction takes one number called the minuend, away from a second number called the subtrahend, and results in the difference. |
| %a \* %b | Multiplication | multiplication is a quick way of adding identical numbers. The two numbers being multiplied are called factors, and the result is the product. |
| %a / %b | Division | division is an arithmetic operation which is the reverse operation of multiplication, and sometimes it can be interpreted as repeated subtraction. Division in EasyUO is Integer based, meaning that when the division operator is used any remainders are dropped. See below. |
| %a % %b | Modulo | the modulo operation finds the remainder of division of one number by another. |
| ABS %a | Absolute | The absolute value operation returns the numerical representation of the value provided without regard to it's sign. |

<a id="operators--comparison"></a>

#### Comparison Operators

EasyUO can perform mathimatical comparisons of any two values using the operators specified below.

| Example | Name | Result |
|----|----|----|
| %a = %b | Equality | Tests that the two operands are the same. |
| %a \<\> %b | Not equal | Tests that the two operands are not the same. |
| %a \< %b | Less than | Tests that the first operand is lesser than the second. |
| %a \> %b | Greater than | Tests that the first operand is greater than the second. |
| %a \<= %b | Less than or equal to | Tests that the first operand is exactly equal or less than the second. |
| %a \>= %b | Greater than or equal to | Tests the the first operand is exactly equal or greater than the second. |
| %a in %b | Contained In | Tests that the first string value is contained somewhere within the second. |
| %a notIn %b | Not contained in | Tests that the first string value is not contained anywhere within the second. |

EasyUO is a weakly typed language. It is therefore possible for any variable to contain either integer numeric data or string data at any time. In terms of Comparison Operations, it is therefore possible to perform invalid comparisons. If this is the case, the result will always evaluate to false. for example, the statement "if hello \> 33" will always be false. knowing this behavior it is possible to find out if a variable contains a valid number, as shown below:

    set %cnt invalid
    if ! ( %cnt > 0 || %cnt < 1 )
      set %cnt 0
    set %cnt %cnt + 1

<a id="operators--logical"></a>

#### Logical Operators

EasyUO can perform logical comparisons of any two values using the operators specified in the table below.

| Example | Name | Result |
|----|----|----|
| %a && %b | And | If both values evaluate as true, the expression is true. |
| `%a \|\| %b` | Or | If either one of the values evaluates as true, the expression is true. |
| ! %a | Not | Gives the logical inverse of the evaluation. True will exaluate to false, and false to true. |

<a id="operators--concatenation"></a>

#### Concatenation Operators

| Example | Name | Result |
|---|---|---|
| + | Line continuation | indicates that the current line is the continuation of the previous line. It must be the first character on the line, not counting white spaces. Trailing white spaces on the previous line are ignored. Unlike other operators, no space is required after the line continuation operator. If a space is present immediately after the operator, it will be parsed normally and it will be part of the final string.`display ok This+ is+ all+ on+ one+ line.$halt`Because in between every '+' sign and the next word there is a space, this will result in a line like: "This is all on one line". |
| , | String concatenation | Concatenates the value of both operands into a single string value. (left-associative)`set %var1 Aset %var2 B set %test %var1 , %var2`%test becomes "AB". |
| . | Append concatenation (array) | Appends the first operand with the value of the second operand and evaluates the result. (right-associative)`set %var1 Aset %var2 Bset %Var1B s7_is_1337 set %test %var1 . %var2`%test becomes "s7_is_1337". |

<a id="operators--precedence"></a>

#### Precedence and associativity

In an expression that contains multiple operators, EasyUO uses a number of rules to decide the order in which operators are evaluated. The first and most important rule is called operator precedence. Operators of higher precedence within an expression are executed before operators of a lower precedence. For example multiplication has a higher precedence than addition. Therefore, in the expression 2 + 3 \* 4, multiplication is evaluated before addition and the result of the whole expression is 14.

If consecutive operators in an expression have the same precedence, a rule called associativity is used to decide the order in which those operators are evaluated. An operator can be left-associative, right-associative, or non-associative.

Left-associative operators of the same precedence are evaluated in order from left to right. For example, addition and subtraction have the same precedence and they are left associative. In the expression 10 - 4 + 2, the substraction is done first because it is to the left of the addition and the expression therefore produces a value of 8.

Right-associative operators of the same precedence are evaluated in order from right to left.

A non-associative operator cannot be combined with other operators of the same precedence.

| Precedence    | Operator               | Associativity     |
|---------------|------------------------|-------------------|
| 1a | .                      | right-associative |
| 2a | ,                      | left-associative  |
| 3             | ( )                    | non-associative   |
| 4             | unary minus, and NOT   | right-associative |
| 5             | \* / %                 | left-associative  |
| 6             | \+ -                   | left-associative  |
| 7             | \< \> \<= \>= in notIn | left-associative  |
| 8             | = \<\>                 | left-associative  |
| 9             | &&                     | left-associative  |
| 10            | the OR operator        | left-associative  |
| 11            | ABS                    | left-associative  |

Note about the dot (array operator) and comma (concatenation) operators: These operators have the highest precedence. They are special for they are evaluated before everything else (including commands). This property enable their use in any context like this:

    dis . play yes , no ok
    h , a , l , t 

<a id="operators--associativity"></a>

##### Associativity for Dummies

This section was mainly added for many users that have trouble understanding the differences between the dot and comma operators and proper usage of them, but a proper understanding of associativity is all that is really needed. When an operator is RIGHT-ASSOCIATIVE such as in the case of the dot (".") operator, everything to the RIGHT of the operator is evaluated before everything to the left. Think of it as reading from right to left.

A left associative operator, such as the comma, and many other mathematical operators, everything to the left is evaluated before what is evaluated to the right. Think of this as reading normally; left to right. Let's take the following example:

    set %text1 The . #spc . quick . #spc . brown . #spc . fox . #spc . was . #spc . of . #spc . the . #spc . genus . #spc . vulpis
    set %text2 The , #spc , quick , #spc , brown , #spc , fox , #spc , was , #spc , of , #spc , the , #spc , genus , #spc , vulpis

In this case, both operators have the same effect and the two variables will be identical, as there are no evaluations done. However, it is considered proper coding to use the comma operator for string/value concatenation. But take a look at the following example:

    set %var1 3
    set %var2 spotNumber
    set %var23 Tada!

    set %Test1 %var2 , %var1
    set %Test2 %var2 . %var1

After looking at the first example and then this one, you might expect that %Test1 and %Test2 would be identical. However, they are not at all. The variable %Test1 would equal "spotNumber3" whereas the variable %Test2 would equal "Tada!" Go ahead and test it yourself. Why does this occur? Associativity! Since the comma is left-associative, you read (evaluate) the line from left to right. %var2 is evaluated to "spotNumber" and then joined with %var1 which is evaluated to "3". However, since the dot is right-associative, you "read" (evaluate) from right to left! %var1 is evaluated first to "3", and THEN joined with %var2 to become %var23.. and then %var23 is evaluated to "Tada!"

**Examples:**

    set %r 5 + 3 * 2 ; 5 + ( 3 * 2 ) = 11

    set %r 8 - 3 - 2 ; ( 8 - 3 ) - 2 = 3

    set %r 1 + 2 * 2 ; 1 + ( 2 * 2 ) = 5

    set %r 1 + 2 * 2 * 4 ; 1 + ( ( 2 * 2 ) * 4 ) = 17

    set %r ( 1 + 2 ) * 2 * 4 ; ( ( 1 + 2 ) * 2 ) * 4 = 24

    set %a 3
    set %z3 8 ; z[a]
    set %w8 1337 ; w[z[a]]
    set %euo %w . %z . %a
    display ok %euo
    halt

<a id="ref-control-structures"></a>

### Control Structures

<a id="control-structures--gotos"></a>

#### Goto's

Goto's are an archaic and powerful command to automatically move to a different point in a program. They never [return](#cmd-return) unless another goto is used. They should **never** be used to return from a subroutine.

##### label

A [label](#cmd-label) is a marker for the point a goto command will jump to. These are created by using any word that isn't a command, and suffixing it with a colon, like this...

    mylabel:

##### goto

A [goto](#cmd-goto) is used to jump directly to a label as defined above. This is accomplished by using [goto](#cmd-goto) {label}

    goto mylabel

> [!NOTE]
> You must never use goto to jump out of a sub! Use return to properly terminate a sub routine. To prevent a stack overflow, EUO only supports 1000 consecutive GoSubs without returning. Remember this when using recursion! When the GoSub stack is about to get 1001 levels, the very first level in the bottom of the stack is deleted to make room.

<a id="control-structures--subs"></a>

#### Subs

The term *sub* is short for subroutine. Subs are an important feature of the EasyUO script that will make your scripts more logically structured, easier to read, and will make you have to write less code.

A basic sub definition starts with a sub statement followed by the subs name (sub names are case insensitive), a number of script lines and ends with a return statement.

    sub testSub
      ...
      return

If parameters were added to the calling gosub command they will be present in the variables %1, %2, and so on. The variable %0 holds the number of parameters passed. As all variables are in the global scope, the %0, %1, %2.. will be overwritten if you call another sub from inside a sub.

##### gosub

The gosub command transfers the execution to a sub with the name given by the parameter.

    gosub sub_name

Parameters can be added after the sub name. They will be transfered in the variables %1, %2, and so on. The variable %0 holds the number of parameters passed.

##### return

The **return** command transfers the execution back to where the sub was called using **gosub**.

    return

<a id="sec-command-reference"></a>

## Command Reference

<a id="sec-flow-control"></a>

### Flow Control

Flow control commands allow scripts to make decisions based on the evaluation of boolean expressions.

| Command | Summary |
|---|---|
| [break](#cmd-break) | Jumps to first statement outside of loop |
| [call](#cmd-call) | Transfers execution to another script file |
| [continue](#cmd-continue) | Jumps execution of a loop to next iteration |
| [exit](#cmd-exit) | Exits a called script |
| [for](#cmd-for) | Creates a counting loop |
| [gosub](#cmd-gosub) | Transfers execution to the matching sub |
| [goto](#cmd-goto) | Jumps to another part of the script given by a label |
| [halt](#cmd-halt) | Stops the script |
| [if](#cmd-if) | Executes code based on the evaluation of an expression |
| [pause](#cmd-pause) | Temporarily stops the execution of the current script |
| [repeat..until](#cmd-repeatuntil) | Creates a loop that checks condition after execution |
| [return](#cmd-return) | Returns from a sub |
| [stop](#cmd-stop) | Ends the script |
| [while](#cmd-while) | Creates a loop that checks condition before execution |

<a id="cmd-break"></a>

#### Break

**Synopsis**

    Break

**Description**

*break* can be used to immediately exit any loop structure.

##### Example

    set %Test 1
    while %Test < 10
    {
    ;Code between these brackets, gets executed, while %Test is smaller than 10
    ;When its 10, it wont jump back to first bracket.
    if %Test = 7
       break
    set %Test %Test + 1
    }
    display ok %Test $
    halt
    ;%Test will hold the value of 7, notice how we break out from the loop when %Test is 7.

> [!NOTE]
> Only available in EasyUO 1.5+

<a id="cmd-call"></a>

#### Call

**Synopsis**

    call {file} [parameter...]

**Description**

*call* command will transfer execution to another script. It will run the script until it meets the [exit](#cmd-exit) command or the end of the file.

> [!NOTE]
> Right now EasyUO doesn't really support strings. Therefore, CALL won't work if the path to a file contains any spaces. Use the DOS short filename syntax to get around this problem.
>
> wrong: C:\My Documents\blabla.txt
>
> correct: C:\MyDocu~1\blabla.txt

##### Example

    call subs.txt recall %runebookid %runenum
    halt

Note: call arguments handling work exactly the same as goSub command. Thus, %0 will hold the number of parameters passed, %1 will hold the first argument passed value and so on. See [exit command](http://wiki.easyuo.com/index.php/Exit) page for more infos.

EDIT on 23 jan 2008: For those who know nothing about MS-DOS shortcut thing, here's a way to get around it when using paths containing spaces(Tested on Windows Vista):

Wrong: C:\My Documents\file.txt

Correct: C:\My , #spc , Documents\file.txt (tested on Windows Vista, compatibility with older systems isn't guaranteed)

##### Releated Commands

<a id="cmd-continue"></a>

#### Continue

**Synopsis**

    continue

**Description**

Continue stops execution of code inside of a loop. Control is returned at the point of the next evaluation.

##### Example

    gosub testrandom 
    sub testrandom 
    { 
      for %cnt 1 10 
      { 
        if #random % 10 <> 5 
          continue 
        display ok Five has been found! 
        return 
      } 
      display ok Nothing could be found! 
      return 
    } 
    display ok HALT! 
    halt

When random is something other than 5, the if sentence is true and therefore continue is executed. It jumps over the [display](#cmd-display) and [return](#cmd-return) commands and continues the [for](#cmd-for) loop with it's next iteration. In the case that the evaluation is false, execution proceeds to the statement following the loop structure.

**Related:** [For](#cmd-for)

> [!NOTE]
> Only available in EasyUO 1.5+

<a id="cmd-exit"></a>

#### Exit

**Synopsis**

    exit

**Description**

*exit* will stop the execution of the current script. If it's called from inside a script that was called using [call](#cmd-call) it will resume execution from the line under the [call](#cmd-call) statement. If the *exit* is used from the main script, the script will start over.

##### Example

    event macro 1 0 %pet %command
    if %pet = all
        exit
    event macro 1 0 %pet follow me

EDIT on 23 jan 2008: As you can see, when calling a file (with the call command), there is no possibility to return a value with exit as you would do when returning from a subroutine.

Here's a way to get around this "problem":

calling file

    set %a 0
    call a.txt ;You may need to ajust the path here
    display ok a = %a
    halt

called file (a.txt)

    set %a Hello,_I_am_the_variable_%a_set_in_a.txt
    exit

**Related:** [call](#cmd-call)

<a id="cmd-for"></a>

#### For

**Synopsis**

    for {variable} {start} {end} { }

**Description**

The for command controls a loop that iterates a variable over a range of numbers. Both positive and negative iterations are legal.

The variable is assigned the starting number to begin with. After each iteration it either increments or decrements the variable, until it reaches the ending number.

> [!NOTE]
> In EasyUO 1.4, you *must* use brackets, even if there is only a single line of code in a for loop. In EasyUO 1.5 however, brackets are optional when the for loop is only a single line of code.

##### Example

    for %i 1 20
    {
        msg %i $
        wait 10
    }
    halt

**Related:** [Continue](#cmd-continue)

<a id="cmd-gosub"></a>

#### Gosub

**Synopsis**

    gosub {sub name} {param1, param2, ...}

**Description**

The *gosub* command transfers the execution to a [sub](#cmd-sub) with the name given by the parameter.

Parameters can be added after the sub name. They will be transfered in the variables %1, %2, and so on. The variable %0 holds the number of parameters passed.

> [!NOTE]
> You must not jump out of a sub! Use return to properly terminate a sub routine. To prevent a stack overflow, EUO only supports 1000 consecutive GoSubs without returning. Remember this when using recursion! When the GoSub stack is about to get 1001 levels, the very first level in the bottom of the stack is deleted to make room.

##### Example 1

    gosub s7IsGreaterThan CEO RK
    ; %1 = CEO
    ; %2 = RK
    ; %0 = 2
    sub s7IsGreaterThan
       display ok %1 && %2 even %0 , gether < una
    return

##### Example 2

    ; syntax = 
    ;   gosub {subName} [parameters...]

    gosub example_goSub These are the parameters

    sub example_goSub
    ; %0 = 4
    ; %1 = These
    ; %2 = are
    ; %3 = the
    ; %4 = parameters
    set %message
    for %_cnt 1 %0
    {
       set %message %message , % . %_cnt , #spc
    }
    display ok %message
    halt

**Related:** [Sub](#cmd-sub), [Return](#cmd-return)

<a id="cmd-goto"></a>

#### Goto

**Synopsis**

    goto {label}

**Description**

The *goto* command moves the execution to another part of the script. The destination point is given by a [label](#cmd-label).

> [!NOTE]
> 
>
> - Don't goto out of a [sub](#cmd-sub). Always use [return](#cmd-return)! EasyUO will probably not crash but it is VERY bad programming style.
> - A label in the code must be followed by a colon, where as gotoing to the label does **not** require a following colon.
> - Inline comments do not work with labels in EasyUO 1.4.

##### Example

    loop:
    if %donotloop
        goto exit
    goto loop

    exit:

##### Simulating a Switch Statement

Switch structures (like seen in C/C++) can be simulated in EasyUO using the goto statement:

    set %a #random % 3 + 1
    goto case , %a

    case1:
      display ok One
      goto case_exit

    case2:
      display ok Two
      goto case_exit

    case3:
      display ok Three
      goto case_exit

    case_exit:
    halt

**Related:** [label](#cmd-label)

<a id="cmd-halt"></a>

#### Halt

**Synopsis**

    halt

**Description**

The *halt* command ends the execution of the script. The script cannot be restarted. This command does exactly the same as [stop](#cmd-stop).

##### Example

    if #findcnt < %amountNeeded
        halt

**Related:** [Stop](#cmd-stop)

<a id="cmd-if"></a>

#### If

**Synopsis**

    if ( ! ) ( expression ) ( lines | { } )
    :''or''
    if ( ! ) ( expression ) ( lines | { } ) else ( lines | { } )

**Description**

The `if` construct is one of the most important features of many languages, the EasyUO scripting language included. It allows for conditional execution of code fragments.

As described in the section about [expressions](#ref-expressions), `expression` is evaluated to its boolean value. If it evaluates to [true](#var-true), the next statement will be executed. If `else` is present and the expression evaluates to [false](#var-false), then the statement after `else` will be executed instead.

If `%a > %b` evaluates to [true](#var-true) in the following code fragment, it will display *"a is bigger than b"*; if it evaluates to [false](#var-false), *"a is equal or less than b"* will be displayed instead:

    set %a 100
    set %b #random
    if %a > %b
        display ok a is bigger than b
    else
        display ok a is equal or less than b
    halt

Often you would want to have more than one statement executed conditionally. Of course, there is no need to wrap each statement in an if clause. Instead, you have two options. You can group several statements into a statement group or you can specify how many lines after the if statement are to be evaluated. For example, if `%a > %b` evaluates to [true](#var-true) in the following fragment, it would display *"a is bigger than b"* and would then assign the value of `%a` into `%b`; if it evaluates to [false](#var-false), *"b is equal or bigger than a"* would be displayed and the value of `%b` assigned into `%a` instead:

    set %a 100
    set %b #random
    if %a > %b
    {
        display ok a is bigger than b
        set %b %a
    }
    else
    {
        display ok b is equal or bigger than a
        set %a %b
    }
    halt

OR

    set %a 100
    set %b #random
    if %a > %b 2

        display ok a is bigger than b
        set %b %a
    else 2
        display ok b is equal or bigger than a
        set %a %b
    halt

The ! right after the command is a reversal of the expression which is following.

    set %var hello 
    if %var = world 
        display ok This shouldnt be displayed. 
    if %var <> world 
        display ok This should be displayed because hello is another (<>) than world. 
    if ! %var = world 
        display ok this should be displayed because hello is not equal world. 
    stop

##### Nesting Conditional Statements

`if` statements can be nested indefinitely within other `if` or `else` statements, which provides you with complete flexibility for conditional execution of the various parts of your script.

    set %a #random % 3 + 1
    if %a = 1
    {
      display ok One
    }
    else
    {
      if %a = 2
      {
        display ok Two
      }
      else
      {
        display ok Three
      }
    }
    halt

**Related:** [Else](#cmd-else)

<a id="cmd-pause"></a>

#### Pause

**Synopsis**

    pause

**Description**

The *pause* command will stop execution of the current script, but it can be resumed by pressing the "Play" button.

##### Example 1

    onhotkey F12
    {
        display ok The script is currently paused. press the EasyUO play button to restart.
        pause
    }

##### Example 2

    sub somesub
       ; If we are debugging, pause script execution here to check current variables...
       if %debug
          pause
       set %something %1
    return %something

<a id="cmd-repeatuntil"></a>

#### Repeat..until

**Synopsis**

    repeat { } until ( expression )

**Description**

The *repeat..until* control structure executes the code block between the statements, and then evaluates the expression. This will make it so that [repeat..until](#cmd-repeatuntil) loops will always execute the code within the loop at least once. This command differs from the [while](#cmd-while) command because the expression is evaluated prior to the code inside the code block, where [while](#cmd-while) evaluates the expression after executing it's code block.

##### Example

    set %str Hello , #spc , World 
    repeat
    {
      set %str %str , ! 
      str len %str
    }
    until #strres >= 30 
    display ok %str 
    halt

The example above illustrates the difference between a repeat..until loop and a while loop. the exclamation point will always be concatinated to the end of the %str variable, and str len will be executed once before the test for #strRes \>= 30 is first evaluated.

> [!NOTE]
> Only available in EasyUO 1.5+

<a id="cmd-return"></a>

#### Return

**Synopsis**

    return { expression }

**Description**

The *return* command transfers the execution back to where the [sub](#cmd-sub) was called using [gosub](#cmd-gosub).

providing a variable or expression to *return* will put the given value into the [result](#var-result) system variable.

##### Example

    gosub makeLowerCase #charname
    event macro 1 0 my name is #result
    halt

    ;The following sub takes the first parameter
    ;makes it lowercase, and then returns the
    ;lowercase version.
    sub makeLowerCase
        str lower %1
    return #strRes    ; the lowercase version of %1 is now stored in #result and control is returned to the main script.

**Related:** [Gosub](#cmd-gosub), [Sub](#cmd-sub)

<a id="cmd-stop"></a>

#### Stop

**Synopsis**

    stop

**Description**

The *stop* command ends the execution of the script. The script cannot be restarted. This command does exactly the same as [halt](#cmd-halt).

##### Example

    gosub s7WasHere
    stop

**Related:** [Halt](#cmd-halt)

<a id="cmd-while"></a>

#### While

**Synopsis**

    while ( expression ) { }

**Description**

While loops test the expression and if true, continuously executes the code provided until the expression is no longer true. Unlike [repeat..until](#cmd-repeatuntil), while loops will not execute at all if the expression evaluates to false.

##### Example

    set %Test 1

    while %Test < 10
    {
    ;Code between these brackets, gets executed, while %Test is smaller than 10
    ;When its 10, it wont jump back to first bracket.
    set %Test %Test + 1
    }
    display ok %Test $
    halt

%Test holds the value of 10. Notice the condition "%Test \< 10". If that becomes true, the script won't jump back to the while loop start, but continues normally.

> [!NOTE]
> Only available in EasyUO 1.5+

<a id="cmd-else"></a>

#### Else

**Synopsis**

    Else

**Description**

Used in conjunction with [if](#cmd-if), processed only when the [if](#cmd-if) statement evaluates as [false](#var-false). Must be placed immediately after the [true](#var-true) command from the [if](#cmd-if) statement.

##### Example

    set %a #false
    if %a 
       display ok % , a is True
    else 
       display ok % , a is False
    halt

Will always display %a is [false](#var-false)

**Related:** [If](#cmd-if)

<a id="cmd-sub"></a>

#### Sub

**Synopsis**

    sub {sub name}

**Description**

The *sub* command starts a smaller macro within the macro. You transfer to the [sub](#cmd-sub) by using [gosub](#cmd-gosub) elsewhere in the macro. Use [return](#cmd-return) to go back to where the [gosub](#cmd-gosub) was previously.

> [!NOTE]
> You must not jump out of a sub! Use return to properly terminate a sub routine. To prevent a stack overflow, EUO only supports 1000 consecutive GoSubs without returning. Remember this when using recursion! When the GoSub stack is about to get 1001 levels, the very first level in the bottom of the stack is deleted to make room.

##### Example

    mainloop:
     gosub speakgame hi
     wait 1s
    goto mainloop

    sub speakgame
       exevent macro 1 0 %1
    return

**Related:** [Gosub](#cmd-gosub), [Return](#cmd-return)

<a id="cmd-label"></a>

#### Label

**Synopsis**

    label

**Description**

This is a marked spot for a [goto](#cmd-goto) command. The label is created by using a word (not a command) and suffixing it with a colon.

##### Example 1

    mylabel:

##### Example 2

    mainloop:
       gosub dostuff
    goto mainloop

**Related:** [goto](#cmd-goto)

<a id="sec-client"></a>

### Client

Client commands are used to send information to the Ultima Online client in order to perform an action or effect some change.

| Command | Summary |
|---|---|
| [chooseSkill](#cmd-chooseskill) | Reads the current skill value/lock status for a specific skill |
| [click](#cmd-click) | Clicks at a specific position in the UO client |
| [cmpPix](#cmd-cmppix) | Compares a current pixel to a previously saved pixel |
| [contPos](#cmd-contpos) | Moves the active topmost gump to a new position |
| [deleteJournal](#cmd-deletejournal) | Forgets the contents of the journal buffer |
| [findItem](#cmd-finditem) | Finds items, monsters, players, NPCs based on object ID or object type |
| [getShopInfo](#cmd-getshopinfo) | Retrieves information from the client about the currently shown top entry on a shopping gump |
| [getUOTitle](#cmd-getuotitle) | Gets the text on the title bar of the client |
| [hideItem](#cmd-hideitem) | Removes an items graphic from the client |
| [ignoreItem](#cmd-ignoreitem) | Removes items from the list searched by findItem |
| [key](#cmd-key) | Sends a key-stroke to the client |
| [move](#cmd-move) | Moves the character to a specified location |
| [msg](#cmd-msg) | Sends a string to the client as keystrokes |
| [nextCPos](#cmd-nextcpos) | Denotes where the next opened container/gump will open |
| [onHotKey](#cmd-onhotkey) | Performs a line of code if a specific key is pressed |
| [savePix](#cmd-savepix) | Saves the color of a pixel in a specified location |
| [setShopItem](#cmd-setshopitem) | Sets the number of items to purchase given by ID |
| [setUOTitle](#cmd-setuotitle) | Sets the text on the title bar of the client |
| [scanJournal](#cmd-scanjournal) | Scans the users journal and stores the string for examination |
| [sleep](#cmd-sleep) | Waits a specified amount of time |
| [target](#cmd-target) | Waits for a target cursor to appear |
| [terminate](#cmd-terminate) | Terminates the current client |
| [uoXL](#cmd-uoxl) | Start/manage clients |
| [wait](#cmd-wait) | Waits a specified amount of time |

<a id="cmd-chooseskill"></a>

#### ChooseSkill

> [!NOTE]
> From EUO 1.5 Test version 53 and up [Event SkillLock](#cmd-event-skilllock) has been replaced by [Exevent SkillLock](#cmd-exevent-skilllock). For compatibility, the obsolete Event is internally rerouted to the ExEvent.

**Synopsis**

    chooseSkill {skill name} ["real"]

**Description**

The chooseSkill command reads the skill value for the specified skill and places the value into the #skill system variable. The current lock status is placed in the #skillLock system variable and the current skill cap is placed in the #skillCap system variable.

The skill name is the first four characters of the actual skill name, with the exception of animal lore (ANIL) and stealth (STLT). See the list below for more info.

##### Example

    chooseSkill mage
    if #skill < 700
    {
    msg You don't have enough magery $
    halt
    }
    ...

    TSPerry72@…
    26-Feb-2005 15:52   #39
    Here is a list of 4 letter codes for each skill as of February 2005. Listed by UO catagory and alphebetized.

    Miscellaneous Skills
    Alch - Alchemy
    Blac - Blacksmithy
    Bowc - Bowcraft Fletching
    Bush - Bushido
    Carp - Carpentry
    Chiv - Chivalry
    Cook - Cooking
    Fish - Fishing
    Focu - Focus
    Heal - Healing
    Herd - Herding
    Lock - Lockpicking
    Lumb - Lumberjacking
    Mage - Magery
    Medi - Meditation
    Mini - Mining
    Musi - Musicianship
    Necr - Necromancy
    Ninj - Ninjitsu
    Remo - Remove Trap
    Resi - Resisting Spells
    Snoo - Snooping
    Stea - Stealing
    Stlt - Stealth
    Tail - Tailoring
    Tink - Tinkering
    Vete - Veterinary

    Combat Skills
    Arch - Archery
    Fenc - Fencing
    Mace - Mace Fighting
    Parr - Parrying
    Swor - Swordsmanship
    Tact - Tactics
    Wres - Wrestling

    Actions
    Anim - Animal Taming
    Begg - Begging
    Camp - Camping
    Dete - Detecting Hidden
    Disc - Discordance
    Hidi - Hiding
    Insc - Inscription
    Peac - Peacemaking
    Pois - Poisoning
    Prov - Provocation
    Spir - Spirit Speak
    Trac - Tracking

    Lore & Knowledge
    Anat - Anatomy
    Anil - Animal Lore
    Arms - Arms Lore
    Eval - Evaluating Intelligence
    Fore - Forensic Evaluation
    Item - Item Identification
    Tast - Taste Identification

<a id="cmd-click"></a>

#### Click

**Synopsis**

    click {X-coordinate} {Y-coordinate} [Modifiers]

**Description**

The click command mimics a click of the mouse in a specific position on the screen.

| Option    | Description                                  |
|-----------|----------------------------------------------|
| d         | Double Click                                 |
| dmc       | Don't Move Cursor (New from 1.42 (build 7c)) |
| f         | Fast Click                                   |
| g         | Drag                                         |
| mc        | Move Cursor (New from 1.42 (build 7c))       |
| n         | Nothing (Just moves the cursor)              |
| p         | Drop                                         |
| r         | Right Click                                  |
| x {count} | Multiple Fast Clicks                         |

> [!NOTE]
> 
>
> - Multiple specifier's are allowed.
> - Using the "Don't Move Cursor" option can make the double clicking fail randomly.
> - With the introduction of [event Drag](#cmd-event-drag), using click to drag and drop objects is obsolete.

Be sure to also read [Cheffe explains the CLICK command](http://www.easyuo.com/forum/viewtopic.php?t=10951)

##### Example

    ; close open crafting gump
    click 150 150 r

<a id="cmd-cmppix"></a>

#### CmpPix

**Synopsis**

    cmpPix {number} [true | false]

**Description**

The cmpPix command compares the pixel given by {number} previously saved with [savePix](#cmd-savepix) command. If it evaluates to either true or false (given by the option) it will execute the next statement or statement block.

| Option | Description |
|----|----|
| **true** | Executes next statement if current pixel **equals** to the previously saved pixel. |
| **false** | Executes next statement if current pixel **differs** from the previously saved pixel. |

> [!NOTE]
> the UO client **must** be top most in order for savepix and #pixcol to work

##### Example

    ;Go to the client login screen and make
    ;sure your mouse cursor is not over the
    ;Quit button (upper right corner)
    ;Start the script and move your mouse
    ;over the Quit button. The client will
    ;close even if you don't make a click.

    savePix 580 13 1
    comparePixelAgain:
    cmpPix 1 f
    {
      key F4 Alt
      halt
    }
    goto comparePixelAgain

**Related:** [savePix](#cmd-savepix)

<a id="cmd-contpos"></a>

#### ContPos

**Synopsis**

    contPos {X-Coordinate} {Y-Coordinate}

**Description**

The contPos command moves the currently active topmost gump to the coordinates specified.

##### Example

    msg bank $
    wait 20
    contpos 10 10
    halt

<a id="cmd-deletejournal"></a>

#### DeleteJournal

**Synopsis**

    deleteJournal

**Description**

deleteJournal is considered obsolete and is only kept for backwards compatibility. Please see the documentation for the system variable [JIndex](#var-jindex) for example snippets.

The deleteJournal command forgets the contents of the journal from the last read line (inclusive) and everything above so that it cannot be found using scanJournal.

Here is how the example works: Since it happens quite often that several entries get written into the journal between two checks you should scan more than just the first line of the journal. 10 lines is a very good value to make sure you don't miss any new journal text. You must use deleteJournal to mark the text you have already processed so that it does not get interpreted multiple times.

Imagine you manage to say "Hail" three times in a very short time. The example script finds the first "Hail" on line 3, says "Farewell" and forgets line 3 and everything above (because line 3 was the last line read by scanJournal). As the For loop proceeds it will find the other two "Hails" and react as intended.

The very perceptive reader might be asking himself/herself why you cannot just specify the line number as a parameter of deleteJournal. To answer that question, imagine that the journal gets two new entries right when script execution is between scanJournal and deleteJournal. So when the script recognizes the first "Hail" on line 3 and says the "Farewell", line 1 and 2 get moved up by two lines (because of those two new journal entries) and are now on line 3 and 4 which would then be ignored by "deleteJournal 3". That is why deleteJournal determines itself which line is to be ignored.

##### Example

    for %i 10 1
    {
     scanJournal %i
     if hail in #journal
     {
       msg Farewell$
       deleteJournal
     }
    }

**Related:** [scanJournal](#cmd-scanjournal)

<a id="cmd-finditem"></a>

#### FindItem

**Synopsis**

    findItem {{id} | {type} | *} [index] [[G] | [G_{dist}] | [C] | [C_{container id}]]

**Description**

The findItem command finds objects given by their ID (6-8 letters) or any object type (2-3 letters). If no index is given the first object found is returned in the #FIND\* variables. If an index is given, the {index}'th object is returned in the #FIND\*. If \* is used instead of an id or an index, all items of all types will be returned.

It is possible to specify multiply object types in the {type} parameter (i.e. NSF_FSF).

| C | Only objects in containers are returned. (Container must be open) |
|---|---|
| C\_{container id} | Only objects in the container given by {container id} are returned. (Container must be open) |
| G | Only objects on the ground are returned. |
| G\_{Dist} | Only objects on the ground, and no farther than {dist} are returned. |
| A | Hidden Objects. |
| CA\_{container id} | Only hidden objects in the container given by {container id} are returned. |

##### Example

    set %regbag XXXXX ; <- replace with your own bag

    ; find an dagger on the ground within 2 tiles (pickup distance)
    ; and picks it up and drops it at a specific position
    finditem TSF G_2
    if #FINDCNT > 0
    {
        event Drag #FINDID
        wait 20
        click 200 300 p
    }

    ; find a stack of Black Pearl in a specific bag and moves it
    ; to a specific position
    finditem KUF C_ , %regbag
    if #FINDCNT > 0
    {
        event Drag #FINDID
        wait 20
        click 200 300 p
    }

> [!NOTE]
> User Contributed Notes /docs/Command_findItem.php Add Notes About Notes Roadkill@… 25-Sep-2004 15:55 #15 I noticed the A modifier is not listed, after sending someone here. A search of the forums shows very little written, and the best I could find is Cheffe's initial explanation from the 0092 announcement:
>
> New modifiers explained:
>
> Up to now, only visible items could be found when using FINDITEM. Invisible items had to be ignored because it wouldn't always be clear if they could be found or not or whether they would mess up scripts.
>
> Example: A script drags items out of the backpack and drops them onto a closed bag in the bank box. In that situation, the item can still be found until the bank box gets closed even though the item isn't visible. If I remember correctly, older clients used to clean up those invisible items after a few seconds so it wouldn't be clear at all if they were found or not. This effect used to cause problems because scripts tried to drag items that weren't even on screen.
>
> The A modifier (for Advanced or All) tells FINDITEM to include invisible items in the search. This way you can find many new things including equipment, clothing and backpacks of other characters. You can use A alone or in connection with C_contid. (GA doesn't make sense and thus isn't valid.)
>
> Only use A if it is really required! ---end of quote from Cheffe. Note the last sentence! I expect this is a very slow and time consuming command, thus Cheffe's admonition. Roadkill
>
> From this page: <http://www.easyuo.com/docs/Command_findItem.php>

> [!NOTE]
> User Contributed Notes to distinguish mobs from items : #findStack equal to 0 is mobile\
> to distinguish corpse types quicker than event Property : #findStack seems to be some type-id\

**Related:** [ignoreItem](#cmd-ignoreitem), [findItem](#cmd-finditem), [#findCnt](#var-findcnt), [#findID](#var-findid), [#findType](#var-findtype), [#findX](#var-findx), [#findY](#var-findy), [#findZ](#var-findz), [#findDist](#var-finddist), [#findKind](#var-findkind), [#findStack](#var-findstack), [#findBagID](#var-findbagid), [#findMod](#var-findmod), [#findRep](#var-findrep), [#findCol](#var-findcol), [#findIndex](#var-findindex)

<a id="cmd-getshopinfo"></a>

#### GetShopInfo

**Synopsis**

    getShopInfo

**Description**

The getShopInfo command retrives information about the currently shown top entry on an open gump. When it is called it fills all the #shop\* system variables with their appropriate information

> [!NOTE]
> Every time you scroll to a new entry, you have to call getShopInfo to update the #shop\* system variables.

**Related:** [setShopItem](#cmd-setshopitem)

<a id="cmd-getuotitle"></a>

#### GetUOTitle

**Synopsis**

    getUOTitle

**Description**

The getUOTitle command retrieves the title of the UO client. The title is returned in the system variable [#strRes](#var-strres).

**Related:** [setUOTitle](#cmd-setuotitle)

<a id="cmd-hideitem"></a>

#### HideItem

**Synopsis**

    hideItem {id}

**Description**

The hideItem command removes a specific items graphic from the client. It can be used to unclutter the visual appreance of the EasyUO client however, it does **nothing** on the server. Only non static items that are on the ground can be hidden.

##### Example

    ; This will hide the item returned by the findItem command
    findItem * G_12
    hideItem #findId
    halt

**Related:** [findItem](#cmd-finditem)

<a id="cmd-ignoreitem"></a>

#### IgnoreItem

**Synopsis**

    ignoreItem [{Item ID} | {ID List} | {Item Type} | {Type List} | reset] {Numeric List}

**Overview**

  
ignoreItem will hide items from the [findItem](#cmd-finditem) command. If an item ID or type is ignored then any further [findItem](#cmd-finditem) commands will not find the item as long as the [findItem](#cmd-finditem) command is used with a matching parameter.

If an item *type* is ignored and [findItem](#cmd-finditem) is called using an *ID* then the item **will be found** even if the *type* of item found matches that which was previously ignored.

**item**

  
If an item ID or type is already ignored and ignoreItem is called to ignore it again the item ID or type will be removed from the ignore list even if the item is ignored in separate lists.

  
Example using a single pile of gold with a type of POF and ID of xxx

    ignoreitem POF 1
    ; all gold is ignored
    ignoreitem POF
    ; gold can be found again regardless of List number passed to previous command
    finditem xxx
    ; search was done by ID, not type, so if the pile exists it will be found.

  
ignoreItem *does* support ignoring IDs and TYPEs in the same command.

You may pass the following parameters to ignoreItem:

- *Item ID*: The unique ID of a single item

    ignoreItem BWVOKMS

- *Item ID List*: A list of 2 or more IDs joined by underscores

    ignoreItem _BWVOKMS_RFTDQWE_

- *Item Type*: The type of item, a variable common to all instances of an item. (All stacks of gold have an item type of POF, each stack has its own unique ID)

    ignoreItem POF

- *Item Type List*: A list of 2 or more item types joined by underscores

    ignoreItem _POF_LKF_

##### reset

  
The reset option will flush either all ignore item lists (global) or only a single list if the *list* option is passed

  
Example: flush list 2, but all other lists remain in tact

    ignoreitem reset 2

##### list

  
Multiple ignore lists can be managed by specifying a list in the ignoreItem command.

  
Example using item type *POF*:

    ignoreitem POF 2

  
This stores item type POF in the second ignoreItem list. It still won't show up in a [findItem](#cmd-finditem) command, and the list can be managed/reset independently of other lists.

##### Example

    ; IgnoreItem.txt
    ;
    ; This script will demonstrate how ignoreItem can be used.
    ;
    ; Press start, go to a shop and follow the instructions.

    msg #SMC Use a dagger and target an NPC$
    wait 3s
    msg #SMC (Press play to continue)
    pause

    set %npc1 #lTargetID

    msg #SMC Use a dagger and target another NPC$
    wait 3s
    msg #SMC (Press play to continue)
    pause

    set %npc2 #lTargetID

    ignoreItem %npc1 1
    ignoreItem %npc2 2

    ; Nothing will be found
    findItem %npc1
    msg #SMC 1: #findID $
    findItem %npc2
    msg #SMC 2: #findID $

    ignoreItem reset 1

    ; NPC 1 will be found
    findItem %npc1
    msg #SMC 1: #findID $
    findItem %npc2
    msg #SMC 2: #findID $

    ignoreItem %npc1 1
    ignoreItem reset 2

    ; NPC 2 will be found
    findItem %npc1
    msg #SMC 1: #findID $
    findItem %npc2
    msg #SMC 2: #findID $
    halt

**Related:** [ignoreItem](#cmd-ignoreitem), [findItem](#cmd-finditem), [#findCnt](#var-findcnt), [#findID](#var-findid), [#findType](#var-findtype), [#findX](#var-findx), [#findY](#var-findy), [#findZ](#var-findz), [#findDist](#var-finddist), [#findKind](#var-findkind), [#findStack](#var-findstack), [#findBagID](#var-findbagid), [#findMod](#var-findmod), [#findRep](#var-findrep), [#findCol](#var-findcol), [#findIndex](#var-findindex)

<a id="cmd-key"></a>

#### Key

**Synopsis**

    key {key-specifier} [[ alt ] | [ ctrl ] | [ shift ]]

**Description**

The key command sends a keystroke of your choice to the client.

The key-specifier can either be A-Z, 0-9, F1-F12 and ESC, BACK, TAB, ENTER, PAUSE, CAPSLOCK, SPACE, PGDN, PGUP, END, HOME, LEFT, RIGHT, UP, DOWN, PRNSCR, INSERT, DELETE, NUMLOCK or SCROLLLOCK.

> [!NOTE]
> If you are running more than one client, the modifier key (alt, control, shift) can sometimes not work as its supposed to.

##### Example

    ; This will hold the ALT key down and press the F4 key.
    key F4 ALT

<a id="cmd-move"></a>

#### Move

**Synopsis**

    move {X-Coordinate} {Y-Coordinate} [tolerance] [timeout]

**Description**

The move command moves the character to a specified position. No pathfinding is done, so you should probably use [event PathFind](#cmd-event-pathfind) instead.

If unspecified, tolerance defaults to 2.

if unspecified, timeout defaults to 3s.

> [!NOTE]
> Please note that if you are using UOAssist, you need to make sure these keys are not assigned to anything: Cursor Up, Cursor Down, Cursor Left, Cursor Right, Home, End, Page Up and Page Down. EasyUO uses these keys to move your character.

##### Example

    ; This will attempt to get within 2 tiles of location 1234 1234.
    ; If it does not get there within 3 seconds it will give up.
    ; The closest it will get is 2 tiles away, lower that arguement to get closer.
    move 1234 1234 2 3s

**Related:** [event PathFind](#cmd-event-pathfind)

<a id="cmd-msg"></a>

#### Msg

**Synopsis**

    msg

**Description**

The msg command sends a series of key-strokes to the client. The '$' sign denotes carriage return.

> [!NOTE]
> Instead of using [msg](#cmd-msg) to speak, whisper, yell, etc. it is more stable and easier to work with [event_Macro](#cmd-event-macro).

##### Example

    ; Locks Last Target Down
    msg I wish to lock this down$
    target 5s
    event Macro 22
    halt

<a id="cmd-nextcpos"></a>

#### NextCPos

**Synopsis**

    nextCPos {X-coordinate} {Y-coordinate}

**Description**

The nextCPos sets the position where the next container/gump will open at.

> [!NOTE]
> The "Offset interface windows rather than perfectly stacking them" option, in Interface options (Mouse Icon) must be turned on for this to work.

##### Example

    ;Closes the paperdoll and reopens it at 0,0
    event Macro 9 1
    wait 20
    nextCPos 0 0
    event Macro 8 1
    halt

<a id="cmd-onhotkey"></a>

#### OnHotKey

**Synopsis**

    onHotKey {key-specifier} {[alt] | [ctrl] | [shift]}

**Description**

The onHotKey command performs the following line of code (brackets do NOT work) when a certain key is pressed. The key-specifier can either be A-Z, 0-9, F1-F12 and ESC, BACK, TAB, ENTER, PAUSE, CAPSLOCK, SPACE, PGDN, PGUP, END, HOME, LEFT, RIGHT, UP, DOWN, PRNSCR, INSERT, DELETE, NUMLOCK or SCROLLLOCK.

> [!NOTE]
> The code is only executed when the parser passes it, if you want a key-press to perform a certain action you have to make a loop. See the example.

> [!NOTE]
> This function is **NOT** client or focus specific. Be careful what you type when running a script with onhotkey, chatting on one client, or in a different application may cause your character to do things in game you do not intend.

##### Example

    set #lpc 1000
    repeat
      onhotkey a
        gosub hotkey a
      onhotkey b
        gosub hotkey b
      onhotkey c
        gosub hotkey c
      onhotkey d
        gosub hotkey d
      onhotkey e
        gosub hotkey e
      sleep 1
    until #false

    sub hotkey
    {
      event sysmessage %1
      Loop:
      sleep 1
      onhotkey %1
        goto Loop
      return
    }

##### Example

    set #lpc 1000
    desactive:
      onhotkey t alt
        goto active
      onhotkey y alt
        halt
    goto desactive

    active:
        onhotkey r alt
          goto desactive
        goto active

<a id="cmd-savepix"></a>

#### SavePix

**Synopsis**

    savePix {X-coordinate} {Y-coordinate} [number]

**Description**

The savePix command saves the color value of the pixel given by the coordinate parameters into the memory slot given by the number parameter. saving the values into number parameter's is usefull when utilizing the [cmpPix](#cmd-cmppix) command. The last color read is also always saved to the [#pixCol](#var-pixcol) system variable.

> [!NOTE]
> the UO client **must** be top most in order for savepix and #pixcol to work

##### Example

    ; This will save the color on the screen where your cursor is into
    ; the number 1 pixel slot to be used with the cmpPix command.
    savePix #cursorX #cursorY 1

**Related:** [cmpPix](#cmd-cmppix)

<a id="cmd-setshopitem"></a>

#### SetShopItem

**Synopsis**

    setShopItem {ID} {amount}

**Description**

The setShopItem command sets the amount to purchase given by an items ID. The ID is usually gotten from the system variable #shopItemID.

> [!NOTE]
> 
>
> - Despite the fact that using setShopItem will not update the graphics in the buy gump, the ammount to sell is set in the client's memory.
> - Before calling setShopItem you have to add at least **one** item to the buy list. This means you first have to double click the item so it gets added to the buy list with amount equal to 1, then you may call setShopItem to change that amount.

##### Example

    ; This will set the amount to buy of the top item to the total number that
    ; is available to be bought.
    getShopInfo
    setShopItem #shopItemID #shopItemMax

**Related:** [getShopInfo](#cmd-getshopinfo)

<a id="cmd-setuotitle"></a>

#### SetUOTitle

**Synopsis**

    setUOTitle {title}

**Description**

The setUOTitle command changes the title bar on the client window.

> [!NOTE]
> If you are using UOAssist or razor, you should turn off the "Use titlebar for display" option on the "Display" tab.

##### Example

    ; This will set the title of your UO Client window to Easy UO rox your sox!
    setUOTitle Easy UO rox your sox!

**Related:** [getUOTitle](#cmd-getuotitle)

<a id="cmd-scanjournal"></a>

#### ScanJournal

**Synopsis**

    scanJournal {index}

**Description**

The scanJournal command scans the users journal and puts the matching string into the [#journal](#var-journal) system variable. The system variable [#jColor](#var-jcolor) is updated with the line's color.

The *index* specifies which line in the journal to use. 1 is the bottom line, 2 is the second to the last line and so on. If the index is 1000 or over it is considered a [#jIndex](#var-jindex) value.

##### Example

    ; example 1 (old way)

    waitForAttack:
    scanjournal 1
    if is_attacking_you in #journal
      msg guards $
    goto waitForAttack

    ; example 2 (new way) (won't skip lines like the old way will)

    set %jrnl #jindex
    while #true
       {
       if #jindex > %jrnl
          {
          set %jrnl %jrnl + 1
          scanjournal %jrnl
          if is_attacking_you in #journal
             event macro 1 0 Guards
          }
       }

**Related:** [deleteJournal](#cmd-deletejournal)

<a id="cmd-sleep"></a>

#### Sleep

**Synopsis**

    sleep {time}

**Description**

The sleep command suspends the processing of EasyUO for a specified amount of time, in milliseconds.

> [!NOTE]
> For values above 50 ms it is recommended that the [wait](#cmd-wait) command be used.
>
> **Quoted from Cheffe**: Wait durations have to be exactly 50ms or multiples of it because that's how long one cycle takes. Even if you could specify values shorter than 50ms it would still take 50ms because that's how long it takes for the next cycle to start. Now, sleep doesn't work with cycles. It simply stops execution right where it is (freezing the EUO window). After the specified amount of milliseconds, execution is continued and the interrupted cycle continues as well.
>
> If you only had one command per cycle then there wouldn't be any difference between sleep and wait because the interrupted cycle would end right after sleep was executed anyway (because it's only one line per cycle). If you have more lines then the cycle will continue as normal.
>
> Sleep and Wait both don't take any CPU time at all. EUO doesn't do anything while waiting for another cycle to start and Sleep simply pauses the current cycle. Sleep only makes sense for short periods of time (\<50ms). If you want to wait for exactly 125ms then you can make a "wait 2" and a "sleep 25". Sleep freezes EUO while wait does not. Thus it makes sense to limit Sleep to very low values because you can combine those two commands to build all other values.

Quote is from this thread: <http://www.easyuo.com/forum/viewtopic.php?p=34120#34120>

##### Example

    ...
    ; Wait for 5 miliseconds
    sleep 5
    ...

**Related:** [wait](#cmd-wait)

<a id="cmd-target"></a>

#### Target

**Synopsis**

    target {timeout}

**Description**

The target command waits for a target cursor to appear. If no timeout is given, the default timeout is 2 seconds.

##### Example

    ; This will pause the script until either the target cursor is displayed,
    ; or 3 seconds passes.
    ; Set the timout just over what you expect the delay to take, otherwise
    ; you may miss the target cursor and cause errors in your script.
    target 3s

**Related:** [event Macro](#cmd-event-macro)

<a id="cmd-terminate"></a>

#### Terminate

**Synopsis**

    terminate [{"uo"} | {"euo"}]

**Description**

The terminate command terminates the current client or the current EasyUO instance. If the current client is terminated the system variables #cliNr and #cliCnt are updated accordingly.

| uo (default) | Closes the current UO client |
|---|---|
| euo | Closes the current EasyUO instance |

##### Example

    ; This will cause the script containing this line to close and will NOT
    ; automatically save your work!
    terminate euo

**Related:** [UoXL](#cmd-uoxl), [Execute](#cmd-execute)

<a id="cmd-uoxl"></a>

#### UoXL

**Synopsis**

    uoXL [{"new"} | {"swap"}]

**Description**

The uoXL command starts and swaps between open clients. The system variables #cliNr and #cliCnt are updated accordingly.

| Option | Description              |
|--------|--------------------------|
| new    | Starts a new client      |
| swap   | Swaps to the next client |

**Related:** [Terminate](#cmd-terminate), [Execute](#cmd-execute)

<a id="cmd-wait"></a>

#### Wait

**Synopsis**

    wait {time} [random time]

**Description**

The wait command waits for a specified amount of time. Time is given in steps of 50 miliseconds by default, or in seconds by using the "s" specifier after the number.

Random time adds to the length of time the script waits, with a random time between 0 and the random time given.

##### Example

    ; Wait for 5 seconds
    wait 5s

    ; Wait for 1 second
    wait 20

    ; Wait for 2 seconds with a random length of 1 second
    wait 2s 1s

**Related:** [sleep](#cmd-sleep)

<a id="sec-event"></a>

### Event

Event commands cause the Ultima Online client to use one of its available internal macros.

| Command | Summary |
|---|---|
| [event Drag](#cmd-event-drag) | Drags an object |
| [event ExMsg](#cmd-event-exmsg) | Shows a message over the object given by the ID |
| [event Macro](#cmd-event-macro) | Performs a UO internal macro |
| [event PathFind](#cmd-event-pathfind) | Moves you to a specified position if it is possible |
| [event Property](#cmd-event-property) | Reads the property description of an item |
| [event SkillLock](#cmd-event-skilllock) | Changes the skill locks on the different skills |
| [event Sleep](#cmd-event-sleep) | Suspends the client for a specified time |
| [event SysMessage](#cmd-event-sysmessage) | Outputs text to the client as a system message |

<a id="cmd-event-drag"></a>

#### Event Drag

**Synopsis**

    event Drag {object id}

**Description**

The event Drag command drags an object given by its id.

##### Example

    event Drag %ore
    wait 20
    click 100 100 p
    halt

<a id="cmd-event-exmsg"></a>

#### Event ExMsg

**Synopsis**

    event ExMsg {object ID} {font} {color} {message}

**Description**

The *event ExMsg* command shows the string provided in the message parameter over the object given by the object ID. The font and color arguments change the appearance of the message that is displayed.

| Index | Description |
|----|----|
| 0 | Big font with dark edges. |
| 1 | Small font with white drop shadow |
| 2 | Big font with white drop shadow. |
| 3 | Small font with dark edges. |
| 4 | Big fancy font. |
| 5 | Medium font. |
| 6 | Tiny font. |
| 7 | Small font with recessed look. |
| 8 | Runic font replacing the following: Capital A-Z, \[, \\ \], ^, \_. Moon Phases replacing the following: € (128), � (129), ‚ (130), „ (132), … (133), † (134), ‡ (135). |
| 9 | Tiny font. |

ExMsg fonts

##### Example

    event ExMsg #charID 3 0 Welcome to my world!
    halt

<a id="cmd-event-macro"></a>

#### Event Macro

**Synopsis**

    event Macro {param 1} [param 2] [param 3]

**Description**

The event Macro command causes the client to use one of the pre-defined, internal UO client macros.

> [!NOTE]
> As noted by Cheffe in the old documentation format, EasyUO 1.5 now automatically maps any unspecified parameters to 0 if nothing is specified. For example, using *event Macro 17 0* is no longer neccesary. Using just *event Macro 17* instead, will work just as reliably. If a third parameter is required (for example, for any of the Speech macros), using the 0 as a second parameter is still required however.

##### Event Macro Table

###### Speech

| Param 1 | Param 2 | Param 3  | Description |
|---------|---------|----------|-------------|
| 1       | 0       | msg text | Say         |
| 2       | 0       | msg text | Emote       |
| 3       | 0       | msg text | Whisper     |
| 4       | 4       | msg text | Yell        |

###### Movement

| Param 1 | Param 2 | Param 3 | Description     |
|---------|---------|---------|-----------------|
| 5       | 0       |         | Walk North West |
| 5       | 1       |         | Walk North      |
| 5       | 2       |         | Walk North East |
| 5       | 3       |         | Walk East       |
| 5       | 4       |         | Walk South East |
| 5       | 5       |         | Walk South      |
| 5       | 6       |         | Walk South West |
| 5       | 7       |         | Walk West       |

###### War/Peace & Paste

| Param 1 | Param 2 | Param 3 | Description      |
|---------|---------|---------|------------------|
| 6       | 0       |         | Toggle War/Peace |
| 7       | 0       |         | Paste            |

###### Gump Control

| Param 1 | Param 2 | Param 3 | Description                 |
|---------|---------|---------|-----------------------------|
| 8       | 0       |         | Open Configuration          |
| 8       | 1       |         | Open Paperdoll              |
| 8       | 2       |         | Open Status                 |
| 8       | 3       |         | Open Journal                |
| 8       | 4       |         | Open Skills                 |
| 8       | 5       |         | Open Spellbook              |
| 8       | 6       |         | Open Chat                   |
| 8       | 7       |         | Open Backpack               |
| 8       | 8       |         | Open Overview               |
| 8       | 9       |         | Open Mail                   |
| 8       | 10      |         | Open Party Manifest         |
| 8       | 11      |         | Open Party Chat             |
| 8       | 12      |         | Open Necro Spellbook        |
| 8       | 13      |         | Open Paladin Spellbook      |
| 8       | 14      |         | Open Combat Book            |
| 8       | 15      |         | Open Bushido Spellbook      |
| 8       | 16      |         | Open Ninjutsu Spellbook     |
| 8       | 17      |         | Open Guild                  |
| 8       | 18      |         | Open Spellweaving SpellBook |
| 8       | 19      |         | Open Questlog               |
| 9       | 0       |         | Close Configuration         |
| 9       | 1       |         | Close Paperdoll             |
| 9       | 2       |         | Close Status                |
| 9       | 3       |         | Close Journal               |
| 9       | 4       |         | Close Skills                |
| 9       | 5       |         | Close Spellbook             |
| 9       | 6       |         | Close Chat                  |
| 9       | 7       |         | Close Backpack              |
| 9       | 8       |         | Close Overview              |
| 9       | 9       |         | Close Mail                  |
| 9       | 10      |         | Close Party Manifest        |
| 9       | 11      |         | Close Party Chat            |
| 9       | 12      |         | Close Necro Spellbook       |
| 9       | 13      |         | Close Paladin Spellbook     |
| 9       | 14      |         | Close Combat Book           |
| 9       | 15      |         | Close Bushido Spellbook     |
| 9       | 16      |         | Close Ninjutsu Spellbook    |
| 9       | 17      |         | Close Guild                 |
| 10      | 1       |         | Minimize Paperdoll          |
| 10      | 2       |         | Minimize Status             |
| 10      | 3       |         | Minimize Journal            |
| 10      | 4       |         | Minimize Skills             |
| 10      | 5       |         | Minimize Spellbook          |
| 10      | 6       |         | Minimize Chat               |
| 10      | 7       |         | Minimize Backpack           |
| 10      | 8       |         | Minimize Overview           |
| 10      | 9       |         | Minimize Mail               |
| 10      | 10      |         | Minimize Party Manifest     |
| 10      | 11      |         | Minimize Party Chat         |
| 10      | 12      |         | Minimize Necro Spellbook    |
| 10      | 13      |         | Minimize Paladin Spellbook  |
| 10      | 14      |         | Minimize Combat Book        |
| 10      | 15      |         | Minimize Bushido Spellbook  |
| 10      | 16      |         | Minimize Ninjutsu Spellbook |
| 10      | 17      |         | Minimize Guild              |
| 11      | 1       |         | Maximize Paperdoll          |
| 11      | 2       |         | Maximize Status             |
| 11      | 3       |         | Maximize Journal            |
| 11      | 4       |         | Maximize Skills             |
| 11      | 5       |         | Maximize Spellbook          |
| 11      | 6       |         | Maximize Chat               |
| 11      | 7       |         | Maximize Backpack           |
| 11      | 8       |         | Maximize Overview           |
| 11      | 9       |         | Maximize Mail               |
| 11      | 10      |         | Maximize Party Manifest     |
| 11      | 11      |         | Maximize Party Chat         |
| 11      | 12      |         | Maximize Necro Spellbook    |
| 11      | 13      |         | Maximize Paladin Spellbook  |
| 11      | 14      |         | Maximize Combat Book        |
| 11      | 15      |         | Maximize Bushido Spellbook  |
| 11      | 16      |         | Maximize Ninjutsu Spellbook |
| 11      | 17      |         | Maximize Guild              |

###### Open Door

| Param 1 | Param 2 | Param 3 | Description |
|---------|---------|---------|-------------|
| 12      | 0       |         | Opendoor    |

###### Use Skills

| Param 1 | Param 2 | Param 3 | Description                       |
|---------|---------|---------|-----------------------------------|
| 13      | 1       |         | Use Skill Anatomy                 |
| 13      | 2       |         | Use Skill Animal Lore             |
| 13      | 35      |         | Use Skill Animal Taming           |
| 13      | 4       |         | Use Skill Arms Lore               |
| 13      | 6       |         | Use Skill Begging                 |
| 13      | 12      |         | Use Skill Cartography             |
| 13      | 14      |         | Use Skill Detecting Hidden        |
| 13      | 15      |         | Use Skill Discordance             |
| 13      | 16      |         | Use Skill Evaluating Intelligence |
| 13      | 19      |         | Use Skill Forensic Evaluation     |
| 13      | 21      |         | Use Skill Hiding                  |
| 13      | 23      |         | Use Skill Inscription             |
| 13      | 3       |         | Use Skill Item Identification     |
| 13      | 46      |         | Use Skill Meditation              |
| 13      | 9       |         | Use Skill Peacemaking             |
| 13      | 30      |         | Use Skill Poisoning               |
| 13      | 22      |         | Use Skill Provocation             |
| 13      | 48      |         | Use Skill Remove Trap             |
| 13      | 32      |         | Use Skill Spirit Speak            |
| 13      | 33      |         | Use Skill Stealing                |
| 13      | 47      |         | Use Skill Stealth                 |
| 13      | 36      |         | Use Skill Taste Identification    |
| 13      | 38      |         | Use Skill Tracking                |
| 13      | 56      |         | Use Skill Imbuing                 |
| 14      | 0       |         | Last Skill                        |

###### Magery

| Param 1 | Param 2 | Param 3 | Description                 |
|---------|---------|---------|-----------------------------|
| 15      | 0       |         | Cast Spell Clumsy           |
| 15      | 1       |         | Cast Spell Create Food      |
| 15      | 2       |         | Cast Spell Feeblemind       |
| 15      | 3       |         | Cast Spell Heal             |
| 15      | 4       |         | Cast Spell Magic Arrow      |
| 15      | 5       |         | Cast Spell Night Sight      |
| 15      | 6       |         | Cast Spell Reactive Armor   |
| 15      | 7       |         | Cast Spell Weaken           |
| 15      | 8       |         | Cast Spell Agility          |
| 15      | 9       |         | Cast Spell Cunning          |
| 15      | 10      |         | Cast Spell Cure             |
| 15      | 11      |         | Cast Spell Harm             |
| 15      | 12      |         | Cast Spell Magic Trap       |
| 15      | 13      |         | Cast Spell Magic Untrap     |
| 15      | 14      |         | Cast Spell Protection       |
| 15      | 15      |         | Cast Spell Strength         |
| 15      | 16      |         | Cast Spell Bless            |
| 15      | 17      |         | Cast Spell Fireball         |
| 15      | 18      |         | Cast Spell Magic Lock       |
| 15      | 19      |         | Cast Spell Poison           |
| 15      | 20      |         | Cast Spell Telekinesis      |
| 15      | 21      |         | Cast Spell Teleport         |
| 15      | 22      |         | Cast Spell Unlock           |
| 15      | 23      |         | Cast Spell Wall Of Stone    |
| 15      | 24      |         | Cast Spell Arch Cure        |
| 15      | 25      |         | Cast Spell Arch Protection  |
| 15      | 26      |         | Cast Spell Curse            |
| 15      | 27      |         | Cast Spell Fire Field       |
| 15      | 28      |         | Cast Spell Greater Heal     |
| 15      | 29      |         | Cast Spell Lightning        |
| 15      | 30      |         | Cast Spell Mana Drain       |
| 15      | 31      |         | Cast Spell Recall           |
| 15      | 32      |         | Cast Spell Blade Spirits    |
| 15      | 33      |         | Cast Spell Dispel Field     |
| 15      | 34      |         | Cast Spell Incognito        |
| 15      | 35      |         | Cast Spell Magic Reflection |
| 15      | 36      |         | Cast Spell Mind Blast       |
| 15      | 37      |         | Cast Spell Paralyze         |
| 15      | 38      |         | Cast Spell Poison Field     |
| 15      | 39      |         | Cast Spell Summon Creature  |
| 15      | 40      |         | Cast Spell Dispel           |
| 15      | 41      |         | Cast Spell Energy Bolt      |
| 15      | 42      |         | Cast Spell Explosion        |
| 15      | 43      |         | Cast Spell Invisibility     |
| 15      | 44      |         | Cast Spell Mark             |
| 15      | 45      |         | Cast Spell Mass Curse       |
| 15      | 46      |         | Cast Spell Paralyze Field   |
| 15      | 47      |         | Cast Spell Reveal           |
| 15      | 48      |         | Cast Spell Chain Lightning  |
| 15      | 49      |         | Cast Spell Energy Field     |
| 15      | 50      |         | Cast Spell Flame Strike     |
| 15      | 51      |         | Cast Spell Gate Travel      |
| 15      | 52      |         | Cast Spell Mana Vampire     |
| 15      | 53      |         | Cast Spell Mass Dispel      |
| 15      | 54      |         | Cast Spell Meteor Swarm     |
| 15      | 55      |         | Cast Spell Polymorph        |
| 15      | 56      |         | Cast Spell Earthquake       |
| 15      | 57      |         | Cast Spell Energy Vortex    |
| 15      | 58      |         | Cast Spell Resurrection     |
| 15      | 59      |         | Cast Spell Air Elemental    |
| 15      | 60      |         | Cast Spell Summon Daemon    |
| 15      | 61      |         | Cast Spell Earth Elemental  |
| 15      | 62      |         | Cast Spell Fire Elemental   |
| 15      | 63      |         | Cast Spell Water Elemental  |

###### Necromancy

| Param 1 | Param 2 | Param 3 | Description                       |
|---------|---------|---------|-----------------------------------|
| 15      | 101     |         | Cast Spell \[N\] Animate Dead     |
| 15      | 102     |         | Cast Spell \[N\] Blood Oath       |
| 15      | 103     |         | Cast Spell \[N\] Corpse Skin      |
| 15      | 104     |         | Cast Spell \[N\] Curse Weapon     |
| 15      | 105     |         | Cast Spell \[N\] Evil Omen        |
| 15      | 106     |         | Cast Spell \[N\] Horrific Beast   |
| 15      | 107     |         | Cast Spell \[N\] Lich Form        |
| 15      | 108     |         | Cast Spell \[N\] Mind Rot         |
| 15      | 109     |         | Cast Spell \[N\] Pain Spike       |
| 15      | 110     |         | Cast Spell \[N\] Poison Strike    |
| 15      | 111     |         | Cast Spell \[N\] Strangle         |
| 15      | 112     |         | Cast Spell \[N\] Summon Familiar  |
| 15      | 113     |         | Cast Spell \[N\] Vampiric Embrace |
| 15      | 114     |         | Cast Spell \[N\] Vengeful Spirit  |
| 15      | 115     |         | Cast Spell \[N\] Wither           |
| 15      | 116     |         | Cast Spell \[N\] Wraith Form      |
| 15      | 117     |         | Cast Spell \[N\] Exorcism         |

###### Bushido

| Param 1 | Param 2 | Param 3 | Description                          |
|---------|---------|---------|--------------------------------------|
| 15      | 145     |         | Cast Spell \[B\] Honorable Execution |
| 15      | 146     |         | Cast Spell \[B\] Confidence          |
| 15      | 147     |         | Cast Spell \[B\] Evasion             |
| 15      | 148     |         | Cast Spell \[B\] Counter Attack      |
| 15      | 149     |         | Cast Spell \[B\] Lightning Strike    |
| 15      | 150     |         | Cast Spell \[B\] Momentum Strike     |

###### Chivalry

| Param 1 | Param 2 | Param 3 | Description                        |
|---------|---------|---------|------------------------------------|
| 15      | 201     |         | Cast Spell \[C\] Cleanse By Fire   |
| 15      | 202     |         | Cast Spell \[C\] Close Wounds      |
| 15      | 203     |         | Cast Spell \[C\] Consecrate Weapon |
| 15      | 204     |         | Cast Spell \[C\] Dispel Evil       |
| 15      | 205     |         | Cast Spell \[C\] Divine Fury       |
| 15      | 206     |         | Cast Spell \[C\] Enemy Of One      |
| 15      | 207     |         | Cast Spell \[C\] Holy Light        |
| 15      | 208     |         | Cast Spell \[C\] Noble Sacrifice   |
| 15      | 209     |         | Cast Spell \[C\] Remove Curse      |
| 15      | 210     |         | Cast Spell \[C\] Sacred Journey    |

###### Ninja Moves

| Param 1 | Param 2 | Param 3 | Description                       |
|---------|---------|---------|-----------------------------------|
| 15      | 245     |         | Cast Spell \[NI\] Focus Attack    |
| 15      | 246     |         | Cast Spell \[NI\] Death Strike    |
| 15      | 247     |         | Cast Spell \[NI\] Animal Form     |
| 15      | 248     |         | Cast Spell \[NI\] Ki Attack       |
| 15      | 249     |         | Cast Spell \[NI\] Surprise Attack |
| 15      | 250     |         | Cast Spell \[NI\] Backstab        |
| 15      | 251     |         | Cast Spell \[NI\] Shadowjump      |
| 15      | 252     |         | Cast Spell \[NI\] Mirror Image    |

###### Spellweaving

| Param 1 | Param 2 | Param 3 | Description                          |
|---------|---------|---------|--------------------------------------|
| 15      | 601     |         | Cast Spell \[SW\] Arcane Circle      |
| 15      | 602     |         | Cast Spell \[SW\] Gift of Renewal    |
| 15      | 603     |         | Cast Spell \[SW\] Immolating Weapon  |
| 15      | 604     |         | Cast Spell \[SW\] Attunement         |
| 15      | 605     |         | Cast Spell \[SW\] Thunderstorm       |
| 15      | 606     |         | Cast Spell \[SW\] Nature's Fury      |
| 15      | 607     |         | Cast Spell \[SW\] Summon Fey         |
| 15      | 608     |         | Cast Spell \[SW\] Summon Fiend       |
| 15      | 609     |         | Cast Spell \[SW\] Reaper Form        |
| 15      | 610     |         | Cast Spell \[SW\] Wildfire           |
| 15      | 611     |         | Cast Spell \[SW\] Essence of Wind    |
| 15      | 612     |         | Cast Spell \[SW\] Dryad Allure       |
| 15      | 613     |         | Cast Spell \[SW\] Ethereal Voyage    |
| 15      | 614     |         | Cast Spell \[SW\] Word of Death      |
| 15      | 615     |         | Cast Spell \[SW\] Gift of Life       |
| 15      | 616     |         | Cast Spell \[SW\] Arcane Empowerment |

###### Mysticism

| Param 1 | Param 2 | Param 3 | Description                |
|---------|---------|---------|----------------------------|
| 15      | 678     |         | Cast Spell Nether Bolt     |
| 15      | 679     |         | Cast Spell Healing Stone   |
| 15      | 680     |         | Cast Spell Purge Magic     |
| 15      | 681     |         | Cast Spell Enchant         |
| 15      | 682     |         | Cast Spell Sleep           |
| 15      | 683     |         | Cast Spell Eagle Stike     |
| 15      | 684     |         | Cast Spell Animated Weapon |
| 15      | 685     |         | Cast Spell Stone Form      |
| 15      | 686     |         | Cast Spell Spell Trigger   |
| 15      | 687     |         | Cast Spell Mass Sleep      |
| 15      | 688     |         | Cast Spell Cleaning Winds  |
| 15      | 689     |         | Cast Spell Bombard         |
| 15      | 690     |         | Cast Spell Spell Plague    |
| 15      | 691     |         | Cast Spell Hail Storm      |
| 15      | 692     |         | Cast Spell Nether Cyclone  |
| 15      | 693     |         | Cast Spell Rising Colossus |

###### Miscellanous

| Param 1 | Param 2 | Param 3 | Description       |
|---------|---------|---------|-------------------|
| 16      | 0       |         | Last Spell        |
| 17      | 0       |         | Last Object       |
| 18      | 0       |         | Bow               |
| 19      | 0       |         | Salute            |
| 20      | 0       |         | Quit Game         |
| 21      | 0       |         | All Names         |
| 22      | 0       |         | Last Target       |
| 23      | 0       |         | Target Self       |
| 24      | 1       |         | Arm/Disarm Left   |
| 24      | 2       |         | Arm/Disarm Right  |
| 25      | 0       |         | Wait For Target   |
| 26      | 0       |         | Target Next       |
| 27      | 0       |         | Attack Last       |
| 28      | 0       | ^       | Delay             |
| 29      | 0       |         | Circletrans       |
| 31      | 0       |         | Close Gumps       |
| 32      | 0       |         | Always Run        |
| 33      | 0       |         | Save Desktop      |
| 34      | 0       |         | Kill Gump Open    |
| 35      | 0       |         | Primary Ability   |
| 36      | 0       |         | Secondary Ability |
| 37      | 0       |         | Equip Last Weapon |

###### Client's Range Control

| Param 1 | Param 2 | Param 3 | Description                |
|---------|---------|---------|----------------------------|
| 38      | 0       | ^       | Set Update Range           |
| 39      | 0       | ^       | Modify Update Range        |
| 40      | 0       |         | Increase Update Range      |
| 41      | 0       |         | Decrease Update Range      |
| 42      | 0       |         | Maximum Update Range       |
| 43      | 0       |         | Minimum Update Range       |
| 44      | 0       |         | Default Update Range       |
| 45      | 0       |         | Update Update Range        |
| 46      | 0       |         | Enable Update Range Color  |
| 47      | 0       |         | Disable Update Range Color |
| 48      | 0       |         | Toggle Update Range Color  |

###### Invoke Virtues

| Param 1 | Param 2 | Param 3 | Description                             |
|---------|---------|---------|-----------------------------------------|
| 49      | 1       |         | Invoke Honor Virtue                     |
| 49      | 2       |         | Invoke Sacrifice Virtue                 |
| 49      | 3       |         | Invoke Valor Virtue                     |
| 49      | 4       |         | Invoke Compassion Virtue (Does Nothing) |
| 49      | 5       |         | Invoke \*1 Virtue                       |
| 49      | 6       |         | Invoke \*1 Virtue                       |
| 49      | 7       |         | Invoke Justice Protection               |
| 49      | 8       |         | Invoke \*1 Virtue                       |

- 1 - These are Humility Honesty and Spirituality. At present time they do nothing. Which is which is as yet unknown.

###### Targeting System

| Param 1 | Param 2 | Param 3 | Description                     |
|---------|---------|---------|---------------------------------|
| 50      | 1-5\*   |         | select next                     |
| 51      | 1-5\*   |         | select previous                 |
| 52      | 1-5\*   |         | select nearest                  |
| 53      |         |         | attack selected                 |
| 54      |         |         | use selected                    |
| 55      |         |         | current target                  |
| 56      |         |         | targeting system on/off         |
| 57      |         |         | toggle buff window (open/close) |
| 58      |         |         | bandage self                    |
| 59      |         |         | bandage target                  |

- Sets #ltargetid , Opens and Sets Target_status_gump to current targets healthbar

`1 = hostile   2 = Party Members `\
`3 = Followers 4 = Objects  `\
`5 = Mobiles`

###### Gargoyle

| Param 1 | Param 2 | Param 3 | Description         |
|---------|---------|---------|---------------------|
| 60      |         |         | toggle gargoyle fly |

##### Example

    set #lTargetX 1000
    set #lTargetY 1000
    set #lTargetKind 3

    ; uses a shovel and targets ground at 1000, 1000
    set #lObjectID %shovel
    event Macro 17 ; use shovel
    target 5s
    event macro 22 ; target ground
    halt

##### Available Tutorials

[Event Macro 22/26/27 Tutorial](http://www.easyuo.com/forum/viewtopic.php?t=15047)

<a id="cmd-event-pathfind"></a>

#### Event PathFind

**Synopsis**

    event PathFind {X-Coordinate} {Y-Coordinate} [Z-Coordinate]

**Description**

The event PathFind moves you to the position given by the coordinates. If the Z coordinate os omitted, it is assumed to be -1.

> [!NOTE]
> 
>
> - Please note that your script will keep on executing while the character is moving. Take a look at the example below which mimics the way that the move command works.
> - The event PathFind command only works within one screen. If you need to move longer you need to break up the path in to several calls.

##### Example

    ;===========================================================
    ; Name: pathFind
    ; Author: ScriptFellow (the.WZA)
    ; Parameters: %1 = X
    ;             %2 = Y
    ;             %3 = Z
    ;             %4 = tolerance
    ;             %5 = timeout (in seconds)
    ; Purpose: Pathfind to the given coordinates
    ; Return: %return (#true or #false )
    ;-----------------------------------------------------------
    sub pathFind
    set %_x %1
    set %_y %2
    if %0 <= 2 || %2 = N/A
       set %_z -1
    else
       set %_z %3
    if %0 <= 3 || %3 = N/A
       set %_tolerance 0
    else
       set %_tolerance %4
    if %0 <= 4
       set %_endTime #sCnt + 15
    else
       set %_endTime #sCnt + %5
    set %return #false
    deleteJournal
    scanJournal 2
    event PathFind %_x %_y %_z
    _pathFindScanAgain:
    scanJournal 1
    if pathfinding in #journal
       goto _pathFindOkay
    if can't_get_there in #journal || #sCnt > %_endTime
       return
    goto _pathFindScanAgain
    _pathFindOkay:
    gosub _pathFindDist %_x %_y %_z #charPosX #charPosY #charPosZ
    set %return %return <= %_tolerance
    if %return
    {
       if %_tolerance > 0
       {
          set %1 #cliLeft + #cliXRes / 2
          set %2 #cliTop + #cliYRes / 2
          if #charDir < 3
              set %1 %1 + 1
          else
          {
             if #charDir > 3 && #charDir < 7
                set %1 %1 - 1
          }
          if #charDir = 0 || #charDir = 6
             set %2 %2 - 1
          else
          {
             if #charDir > 1 && #charDir < 5
                set %2 %2 + 1 
          }
          click %1 %2 R
       }
       return
    }
    if #sCnt > %_endTime
       return
    goto _pathFindOkay

    sub _pathFindDist
    set %1 %1 - %4 abs
    set %2 %2 - %5 abs
    set %3 %3 - %6 abs
    gosub max %1 %2 %3
    return

    ; to be defined
    sub max
    set %return %1
    for %_idx 2 %0
    {
       if % . %_idx > %return
       set %return % . %_idx
    }
    return

<a id="cmd-event-property"></a>

#### Event Property

**Synopsis**

    event Property {ID}

**Description**

The event Property command reads the description and properies of an item and places the information in the system variable #property. Each line in the #property variable is seperated by '$'.

Note: event Property doesn't work for pre-AoS (Age of Shadow) freeshards.

##### Example

    ; This will use the item returned by the findItem command and save
    ; the information displayed in game by the property pop-up widow
    ; into the #property variable.
    findItem ABC
    event Property #findID

<a id="cmd-event-skilllock"></a>

#### Event SkillLock

**Synopsis**

    event SkillLock {[skill name] | [all]} {[up] | [down] | [locked]}

**Description**

The event SkillLock command changes the skill lock on the specified skill to either: up, down or locked. If you want to change the lock of all the skills as name use the keyword "all".

> [!NOTE]
> From EUO 1.5 Test version 53 [Event SkillLock](#cmd-event-skilllock) has been replaced by [Exevent SkillLock](#cmd-exevent-skilllock). For compatibility, the obsolete Event is internally rerouted to the ExEvent.

##### Example

    ; changes magery to down
    Exevent SkillLock mage down
    ; locks armlore
    Exevent SkillLock arms locked

    TSPerry72@…
    26-Feb-2005 15:52   #39
    Here is a list of 4 letter codes for each skill as of February 2005. Listed by UO catagory and alphebetized.

    Miscellaneous Skills
    Alch - Alchemy
    Blac - Blacksmithy
    Bowc - Bowcraft Fletching
    Bush - Bushido
    Carp - Carpentry
    Chiv - Chivalry
    Cook - Cooking
    Fish - Fishing
    Focu - Focus
    Heal - Healing
    Herd - Herding
    Lock - Lockpicking
    Lumb - Lumberjacking
    Mage - Magery
    Medi - Meditation
    Mini - Mining
    Musi - Musicianship
    Necr - Necromancy
    Ninj - Ninjitsu
    Remo - Remove Trap
    Resi - Resisting Spells
    Snoo - Snooping
    Stea - Stealing
    Stlt - Stealth
    Tail - Tailoring
    Tink - Tinkering
    Vete - Veterinary

    Combat Skills
    Arch - Archery
    Fenc - Fencing
    Mace - Mace Fighting
    Parr - Parrying
    Swor - Swordsmanship
    Tact - Tactics
    Wres - Wrestling

    Actions
    Anim - Animal Taming
    Begg - Begging
    Camp - Camping
    Dete - Detecting Hidden
    Disc - Discordance
    Hidi - Hiding
    Insc - Inscription
    Peac - Peacemaking
    Pois - Poisoning
    Prov - Provocation
    Spir - Spirit Speak
    Trac - Tracking

    Lore & Knowledge
    Anat - Anatomy
    Anil - Animal Lore
    Arms - Arms Lore
    Eval - Evaluating Intelligence
    Fore - Forensic Evaluation
    Item - Item Identification
    Tast - Taste Identification

<a id="cmd-event-sleep"></a>

#### Event Sleep

**Synopsis**

    event Sleep {ms}

**Description**

The event Sleep command suspends the client for a specified number of miliseconds. The client will be completely unresponsive, but will use 0% CPU time.

##### Example

    if %waitForVendorRespawn = #true
    {
    ; sleep for one minute
    event Sleep 60000
    }
    ...

<a id="cmd-event-sysmessage"></a>

#### Event SysMessage

**Synopsis**

    event SysMessage {message}

**Description**

The event SysMessage command outputs a message as a system message inside the client.

> [!NOTE]
> This command does NOT work unless you have enabled the "Enable Event Sysmessage" configuration option.

##### Example

    ;prints "Your character name is <your character's name>" to the bottom of the screen
    event sysMessage Your character name is #charname

<a id="sec-exevent"></a>

### ExEvent

ExEvent commands send packet information directly to the Ultima Online server in order to perform actions.

| Command | Summary |
|---|---|
| [exevent Drag](#cmd-exevent-drag) | Drags an object using packets |
| [exevent Dropc](#cmd-exevent-dropc) | Drops an object in a given container using packets |
| [exevent Droppd](#cmd-exevent-droppd) | Drops wearable items into the paperdoll |
| [exevent Dropg](#cmd-exevent-dropg) | Drops an object on the ground using packets |
| [exevent Popup](#cmd-exevent-popup) | Opens the context menu of an item/npc |
| [exevent RenamePet](#cmd-exevent-renamepet) | Renames a pet |
| [exevent SkillLock](#cmd-exevent-skilllock) | Changes the skill locks on the different skills |
| [exevent StatLock](#cmd-exevent-statlock) | Changes the stat locks on the different stats |

<a id="cmd-exevent"></a>

#### Exevent

##### Exevents

The exevents are version 1.5+ only, and the available exevents are as follows..

| [exevent Drag](#cmd-exevent-drag) | Drags an object using packets |
|----|----|
| [exevent Dropc](#cmd-exevent-dropc) | Drops an object in a given container using packets |
| [exevent Droppd](#cmd-exevent-droppd) | Drops wearable items into the paperdoll |
| [exevent Dropg](#cmd-exevent-dropg) | Drops an object on the ground using packets |
| [exevent Popup](#cmd-exevent-popup) | Opens the context menu of an item/npc |
| [exevent RenamePet](#cmd-exevent-renamepet) | Renames a pet |
| [exevent SkillLock](#cmd-exevent-skilllock) | Changes the skill locks on the different skills |
| [exevent StatLock](#cmd-exevent-statlock) | Changes the stat locks on the different stats |

<a id="cmd-exevent-drag"></a>

#### Exevent Drag

**Synopsis**

    Exevent Drag {object id} [amount]

**Description**

The *exEvent Drag* command drags an object given by its id. *exEvent Drag* is also able to drag a given amount from a stack of items by using the amount argument. if no amount is specified, the default amount is 1.

> [!NOTE]
> This command is only available from EUO 1.5

##### Example

    finditem %gold G_2
    if #FINDCNT > 0
    {
        Exevent Drag #findid #findstack
        wait 10
        Exevent Dropc #backpackid
        wait 10
    }
    halt

**Related:** [exevent](#cmd-exevent)

<a id="cmd-exevent-dropc"></a>

#### Exevent Dropc

**Synopsis**

    Exevent Dropc {container id} [x y]

**Description**

The *Exevent Dropc* command drops obects you drag using the [Exevent Drag](#cmd-exevent-drag) command to any container you want.

If you specify x/y then the item will be dropped in the container at the x/y coordinates relative to the container's location, otherwise it will be dropped on the container.

If you want to combine the stack being dragged with another stack of the same item type, just pass the ID of the destination stack as `{container id}`.

> [!NOTE]
> 
>
> - This command is only available from EUO 1.5
> - The x/y parameter is only available from EUO 1.5 TV 56
> - You shouldn't use [Event Drag](#cmd-event-drag) in connection with [Exevent Dropc](#cmd-exevent-dropc) command or you'll end up with a ghost item on your cursor. That's why there is an [Exevent Drag](#cmd-exevent-drag) command

##### Example

    finditem %gold G_2
    if #FINDCNT > 0
    {
        Exevent Drag #findid #findstack
        wait 10
        Exevent Dropc #backpackid  ;drops in a random location in backpack or stacks with existing
        wait 10
    }

    event macro 8 7   ;opens backpack
    contpos 100 100   ;positions it at 100,100
    finditem %mushroom G_2
    if #FINDCNT > 0
    {
            Exevent Drag #findid 1
            wait 10
            Exevent Dropc #backpackid 80 80  ;drops the mushroom at 80,80
            wait 10
    }
    halt

##### User Contributed Notes

**Orngrimm 11.Apr.07:**\
Use [Exevent DropC](#cmd-exevent-dropc) to add one stack to another (stacking): Think of the other stack as a container!

       exevent drag %itemID %StackAmmount  ;%itemID being the ID of the stack you want to add to another stack
        exevent dropc %StackID  ;%StackID being the ID of the target-stack

Recent findings about [exevent dropc](#cmd-exevent-dropc): Some users noticed some problems with the method above: Sone (all?) Pol96-Servers dont handle stacks as containers like EA or RunUO does. So the first stack reappears at the original location after the dropC-try.

**snicker7 10/21/05:**\
Here are a few things to note about [exevent dropc](#cmd-exevent-dropc):

[exevent dropc](#cmd-exevent-dropc) can drop to ANY container or object (see below) that is within reach, REGARDLESS of whether or not the container or object is actually visible on the screen. This means that even if you have a bag 2 levels deep in a chest locked down on the floor of your house, if you know the ID of the container, you can drop things into it. Attempting to drop to a container that does not exist or that is out of reach will cause the item to "bounce back" to its original position.

Additionally, [exevent dropc](#cmd-exevent-dropc) will take ANYTHING as a parameter that you could normally drag and drop an item onto; it is not solely limited to containers. This includes things like NPCs, Spellbooks, BOD Books, Animals (beetles, packhorses, etc), even other players to initiate trade sessions. For a simple example, say you wanted to drop an item into the backpack of your beetle:

    finditem %beetleID G_2
    if #FINDCNT > 0
    {
        exevent drag %itemID    ;%itemID being the ID of the object
        exevent dropc #findid   ;#findID being the ID of the beetle
    }

You don't actually have to even know the ID of the beetle's backpack (which is different from the beetle's actual ID), because it functions just as if you had actually dropped the item onto the beetle normally. This also means that if you were to drop meat onto it, it would not go into the pack, but would instead be considered food to the beetle.

**Related:** [exevent](#cmd-exevent)

<a id="cmd-exevent-droppd"></a>

#### Exevent Droppd

**Synopsis**

    Exevent Droppd

**Description**

The *Exevent Droppd* command drops previously dragged (using [Exevent Drag](#cmd-exevent-drag)) wearable item into the paperdoll.

> [!NOTE]
> 
>
> - This command is only available from EUO 1.5 TV 57
> - You shouldn't use [Event Drag](#cmd-event-drag) in connection with [Exevent Droppd](#cmd-exevent-droppd) command or you'll end up with a ghost item on your cursor. That's why there is an [Exevent Drag](#cmd-exevent-drag) command

##### Example

    finditem %weapon C_ , #backpackid
    if #FINDCNT > 0
    {
        Exevent Drag #findid #findstack
        wait 10
        Exevent Droppd
        wait 10
    }
    halt

**Related:** [exevent](#cmd-exevent)

<a id="cmd-exevent-dropg"></a>

#### Exevent Dropg

**Synopsis**

    Exevent Dropg {x} {y} [z]

**Description**

The *Exevent Dropg* command drops obects you drag using the [Exevent Drag](#cmd-exevent-drag) command to the given ground coordinate. If no Z coordinate is specified, the default will be [#charPosZ](#var-charposz).

> [!NOTE]
> 
>
> - This command is only available from EUO 1.5
> - You shouldn't use [Event Drag](#cmd-event-drag) in connection with [Exevent Dropg](#cmd-exevent-dropg) command or you'll end up with a ghost item on your cursor. That's why there is an [Exevent Drag](#cmd-exevent-drag) command

##### Example

    finditem %trash C_ , #backpackid
    if #FINDCNT > 0
    {
        Exevent Drag #findid #findstack
        wait 10
        Exevent Dropg #charposx #charposy #charposz
        wait 10
    }
    halt

**Related:** [exevent](#cmd-exevent)

<a id="cmd-exevent-popup"></a>

#### Exevent Popup

**Synopsis**

    Exevent Popup {id} [x] [y]

**Description**

The *Exevent Popup* command opens the context menu of an item/npc given by its id. Default values for x and y are 0/0.

> [!NOTE]
> This command is only available from EUO 1.5 TV 56. The syntax for this command has been changed in EasyUO 1.5.1 build 252. It used to be Exevent: Popup {id} \[entry\] **SCRIPT USING OLD SYNTAX MUST BE UPDATED**.

##### Example

    finditem %vendor G_10
    if #FINDCNT > 0
        exevent Popup #findid 10 10
    halt

**Related:** [exevent](#cmd-exevent)

<a id="cmd-exevent-renamepet"></a>

#### Exevent RenamePet

**Synopsis**

    Exevent RenamePet {id} {name}

**Description**

The *Exevent RenamePet* command changes the name of the pet given by its id to name.

> [!NOTE]
> This command is only available from EUO 1.5 TV 56

##### Example

    finditem %horse G_2
    if #FINDCNT > 0
    {
        exevent RenamePet #FINDID Name
    }
    halt

**Related:** [exevent](#cmd-exevent)

<a id="cmd-exevent-skilllock"></a>

#### Exevent SkillLock

**Synopsis**

    Exevent SkillLock {[skill name] | [all]} {[up] | [down] | [locked]}

**Description**

The Exevent SkillLock command changes the skill lock on the specified skill to either: up, down or locked. If you want to change the lock of all the skills as name use the keyword "all".

> [!NOTE]
> This command is only available from EUO 1.5 Test version 53.

##### Example

    ; changes magery to down
    Exevent SkillLock mage down
    ; locks armlore
    Exevent SkillLock arms locked

    TSPerry72@…
    26-Feb-2005 15:52   #39
    Here is a list of 4 letter codes for each skill as of February 2005. Listed by UO catagory and alphebetized.

    Miscellaneous Skills
    Alch - Alchemy
    Blac - Blacksmithy
    Bowc - Bowcraft Fletching
    Bush - Bushido
    Carp - Carpentry
    Chiv - Chivalry
    Cook - Cooking
    Fish - Fishing
    Focu - Focus
    Heal - Healing
    Herd - Herding
    Lock - Lockpicking
    Lumb - Lumberjacking
    Mage - Magery
    Medi - Meditation
    Mini - Mining
    Musi - Musicianship
    Necr - Necromancy
    Ninj - Ninjitsu
    Remo - Remove Trap
    Resi - Resisting Spells
    Snoo - Snooping
    Stea - Stealing
    Stlt - Stealth
    Tail - Tailoring
    Tink - Tinkering
    Vete - Veterinary

    Combat Skills
    Arch - Archery
    Fenc - Fencing
    Mace - Mace Fighting
    Parr - Parrying
    Swor - Swordsmanship
    Tact - Tactics
    Wres - Wrestling

    Actions
    Anim - Animal Taming
    Begg - Begging
    Camp - Camping
    Dete - Detecting Hidden
    Disc - Discordance
    Hidi - Hiding
    Insc - Inscription
    Peac - Peacemaking
    Pois - Poisoning
    Prov - Provocation
    Spir - Spirit Speak
    Trac - Tracking

    Lore & Knowledge
    Anat - Anatomy
    Anil - Animal Lore
    Arms - Arms Lore
    Eval - Evaluating Intelligence
    Fore - Forensic Evaluation
    Item - Item Identification
    Tast - Taste Identification

**Related:** [exevent](#cmd-exevent)

<a id="cmd-exevent-statlock"></a>

#### Exevent StatLock

**Synopsis**

    Exevent StatLock {str|dex|int} {[up] | [down] | [locked]}

**Description**

The Exevent StatLock command changes the stat lock on the specified stat to either: up, down or locked.

> [!NOTE]
> This command is only available from EUO 1.5 Test version 53.

##### Example

    ; changes dex to down
    Exevent StatLock dex down
    ; locks str
    Exevent StatLock str locked

**Related:** [exevent](#cmd-exevent)

<a id="sec-menu"></a>

### Menu

Commands to interact with menu elements.

| Command | Summary |
|---|---|
| [menu Activate](#cmd-menu-activate) | Activates a window element in the EasyUO menu window |
| [menu Button](#cmd-menu-button) | Creates a button at position x/y with specified size on the EasyUO menu window |
| [menu Check](#cmd-menu-check) | Creates a checkbox at position x/y with specified size on the EasyUO menu window |
| [menu Clear](#cmd-menu-clear) | Clears all window elements from the EasyUO menu window |
| [menu Combo](#cmd-menu-combo) | Creates a combobox at position x/y with specified size on the EasyUO menu window or adds entries to the combobox |
| [menu Delete](#cmd-menu-delete) | Deletes a window element from the EasyUO menu window |
| [menu Edit](#cmd-menu-edit) | Creates a edit field at position x/y with specified width in the EasyUO menu window |
| [menu Font Align](#cmd-menu-font-align) | Changes the font alignment in the EasyUO menu window |
| [menu Font BGColor](#cmd-menu-font-bgcolor) | Changes the font background color in the EasyUO menu window |
| [menu Font Color](#cmd-menu-font-color) | Changes the font color in the EasyUO menu window |
| [menu Font Name](#cmd-menu-font-name) | Changes the font in the EasyUO menu window |
| [menu Font Size](#cmd-menu-font-size) | Changes the font size in the EasyUO menu window |
| [menu Font Style](#cmd-menu-font-style) | Changes the font style in the EasyUO menu window |
| [menu Font Transparent](#cmd-menu-font-transparent) | Sets the transparency of the background color of the font |
| [menu Get](#cmd-menu-get) | Returns the value associated with a control in the EasyUO menu window |
| [menu GetNum](#cmd-menu-getnum) | Returns the number in an edit field in the EasyUO menu window |
| [menu Hide](#cmd-menu-hide) | Hides the EasyUO menu window |
| [menu HideEUO](#cmd-menu-hideeuo) | Hides the main EasyUO window |
| [menu Image Create](#cmd-menu-image-create) | Creates a new image control in the menu |
| [menu Image Ellipse](#cmd-menu-image-ellipse) | Draws an ellipse/circle within a specified image |
| [menu Image File](#cmd-menu-image-file) | Loads an external image file |
| [menu Image FloodFill](#cmd-menu-image-floodfill) | Applies the FloodFill effect in the area around a specified pixel within a specified image |
| [menu Image Line](#cmd-menu-image-line) | Draws a line within a specified image |
| [menu Image Pix](#cmd-menu-image-pix) | Paints a single pixel within a specified image |
| [menu Image PixLine](#cmd-menu-image-pixline) | Prints a horizontal line of pixels within a specified image |
| [menu Image Pos](#cmd-menu-image-pos) | Moves an already existing image control to a different position |
| [menu Image Rectangle](#cmd-menu-image-rectangle) | Draws a rectangle within a specified image |
| [menu List](#cmd-menu-list) | Creates a listbox at position x/y with specified size on the EasyUO menu window or adds entires to the listbox |
| [menu Set](#cmd-menu-set) | Sets the text of a control |
| [menu Shape](#cmd-menu-shape) | Creates a shape in the EasyUO menu window |
| [menu Show](#cmd-menu-show) | Shows the EasyUO menu window |
| [menu Text](#cmd-menu-text) | Creates a label at the specified position in the EasyUO menu window |
| [menu Window Color](#cmd-menu-window-color) | Changes the color of the EasyUO menu window |
| [menu Window Size](#cmd-menu-window-size) | Changes the size of the EasyUO menu window |
| [menu Window Title](#cmd-menu-window-title) | Changes the title of the EasyUO menu window |
| [menu Window Transparent](#cmd-menu-window-transparent) | Sets the transparency of the window |

<a id="cmd-menu-activate"></a>

#### Menu Activate

**Synopsis**

    menu Activate {name}

**Description**

The [menu Activate](#cmd-menu-activate) command activates the window element given by its name, in the EasyUO menu window

##### Example

    ; This will choose the menu element called EditBox. This is
    ; useful if you want your script to type something into an edit
    ; box as the script runs.
    menu Activate EditBox

<a id="cmd-menu-button"></a>

#### Menu Button

**Synopsis**

    menu Button {name} {x} {y} {width} {height} {text}

**Description**

The [menu Button](#cmd-menu-button) command creates a button on the EasyUO menu window at the specified postion with the specified size.

The #[MenuButton](#var-menubutton) system variable gives the name of the last button that was pressed.

##### Example

    ; This will create a button named button_1 in position 10 20
    ; with a width of 50 and hight of 25. The text on the button
    ; will say Click me!
    ; Note that when refering to this button later in the script
    ; you will reference the NAME and not the displayed TEXT.
    menu Button button_1 10 20 50 25 Click me!

<a id="cmd-menu-check"></a>

#### Menu Check

**Synopsis**

    menu Check {name} {x} {y} {width} {height} {checked} {text}

**Description**

The **menu Check** command creates a checkbox on the EasyUO menu.

Name can be any valid EasyUO Name.

X, Y, width, and height are given in pixels.

Checked is either #true or #false.

Text is any descriptive text that will be placed in a label to the right of the actual text box.

##### Example

    ; Creates a check box at 75 75, with a size of 60 10.
    ; The #false sets it to unchecked and Loot? is the label.

    menu check Lootchk 75 75 60 10 #false Loot?

    ; To find if its checked or not

    menu get Lootchk
    set %loot #menures

    ; This sets %loot to #false if unchecked
    ; or #true if checked.

<a id="cmd-menu-clear"></a>

#### Menu Clear

**Synopsis**

    menu Clear

**Description**

The *menu Clear* command clears all window elements (i.e. text, button, edit) from the EasyUO menu window

> [!NOTE]
> stopping your EasyUO script will not clear the current menu, so you may want to put *menu Clear* at the top of your script to preserve memory.

<a id="cmd-menu-combo"></a>

#### Menu Combo

**Synopsis**

    menu Combo ( {"Create"} {name} {x} {y} {width} )  |  ( {"Add"} {name} {text} )  |  ( {"SELECT"} {name} {index} )

**Description**

The [menu Combo](#cmd-menu-combo) command creates a combobox at position x/y with specified size on the EasyUO menu window or adds entires to the combobox. Select defines what entry is currently showing, similar to [menu Set](#cmd-menu-set).

<a id="cmd-menu-delete"></a>

#### Menu Delete

**Synopsis**

    menu Delete {name}

**Description**

The *menu Delete* command deletes a window element (i.e. text, button, edit) from the EasyUO window menu.

##### Example

    ; This will remove the menu item named button_1 from the current menu
    ; and from memory. Please use this command and do not just create
    ; new items over old ones. This is expecially important when using
    ; menu Text items, as they sometimes need to be updated regularly.
    menu Delete button_1

<a id="cmd-menu-edit"></a>

#### Menu Edit

**Synopsis**

    menu Edit {name} {x} {y} {width} {text}

**Description**

The [menu Edit](#cmd-menu-edit) command creates an edit field at the specified postion and with the specified dimensions in the EasyUO window menu.

##### Example

    ; This will create an editable field named edit_1 in position 10 20
    ; with a width of 50 and hight of 25. The text in the field
    ; will say Change me!
    ; Note that when refering to this field later in the script
    ; you will reference the NAME and not the displayed TEXT.
    menu Edit edit_1 10 20 150 Change , #spc , me!

<a id="cmd-menu-font-align"></a>

#### Menu Font Align

**Synopsis**

    menu Font Align {{left}}}

**Description**

The [menu Font Align](#cmd-menu-font-align) command sets the alignment of the font used in the EasyUO menu window.

<a id="cmd-menu-font-bgcolor"></a>

#### Menu Font BGColor

**Synopsis**

    menu Font BGColor {color-descriptor}

**Description**

The [menu Font BGColor](#cmd-menu-font-bgcolor) command changes the background color of the font used in the EasyUO menu window.

Color-descriptor can be a few different things: black, red, btnface or a hexadecial (i.e. $aabbcc).

<a id="cmd-menu-font-color"></a>

#### Menu Font Color

**Synopsis**

    menu Font Color {color-descriptor}

**Description**

The [menu Font Color](#cmd-menu-font-color) command changes the color of the font used in the EasyUO menu window.

Color-descriptor can be a few different things: black, red, btnface or a hexadecimal (i.e. $aabbcc).

> [!NOTE]
> When using hexadecimal you may get confused if attempting to use #RRBBGG standard as used in web pages. If you've got a hex value and want to use it with this function then swap the GG and RR, so an RGB value of #0099FF would be $FF9900 (GGBBRR)

<a id="cmd-menu-font-name"></a>

#### Menu Font Name

**Synopsis**

    menu Font Name {font-descriptor}

**Description**

The [menu Font Name](#cmd-menu-font-name) command changes the font used in the EasyUO menu window.

<a id="cmd-menu-font-size"></a>

#### Menu Font Size

**Synopsis**

    menu Font Size {point-size}

**Description**

The [menu Font Size](#cmd-menu-font-size) command changes the font size used in the EasyUO menu window.

<a id="cmd-menu-font-style"></a>

#### Menu Font Style

**Synopsis**

    menu Font Style { "b" }  |  { "i" }  |  { "u" }  |  { "s" }

**Description**

The [menu Font Style](#cmd-menu-font-style) command changes the font style used in the EasyUO menu window.

| Value | Description |
|-------|-------------|
| b     | Bold        |
| i     | Italics     |
| u     | Underline   |
| s     | Strikeout   |

<a id="cmd-menu-font-transparent"></a>

#### Menu Font Transparent

**Synopsis**

    menu Font Transparent {#true | #false}

**Description**

The [menu Font Transparent](#cmd-menu-font-transparent) command sets the transparency of the background color of the font.

<a id="cmd-menu-get"></a>

#### Menu Get

**Synopsis**

    menu Get {name}

**Description**

The [menu Get](#cmd-menu-get) command returns value associated with a control in the EasyUO menu window in the [#menuRes](#var-menures) system variable.

Usage with a combo box returns the index of the item selected within the combo box, starting with 0, for nothing selected.

Usage with a check box returns #true if the checkbox is checked, #false if it is not.

> [!NOTE]
> Clicking menu button's (including the window's close button) set's [#menuButton](#var-menubutton) without the need to use menu Get.

##### Example

    ; This will save the text in the edit field named edit_1 into the
    ; variable #menuRes. This will only work for edit field items.
    ; #menuRes will return as a string.
    menu Get edit_1

##### Example w/ ComboBox

    menu show
    menu combo create test 0 0 100
    menu combo add test One
    menu combo add test Two
    menu combo add test Three
    pause
    menu get test
    display ok #menures

<a id="cmd-menu-getnum"></a>

#### Menu GetNum

**Synopsis**

    menu GetNum {name} {default}

**Description**

The [menu GetNum](#cmd-menu-getnum) command returns the number in an edit field in the EasyUO menu window in the [#menuRes](#var-menures) system variable. If the edit field does not hold a number, the default value is returned.

##### Example

    ; This will save the text in the edit field named edit_1 into the
    ; variable #menuRes. If the field is blank it will save 144 into
    ; the variable #menuRes. This will only work for edit field items.
    ; #menuRes will return as a number.
    menu GetNum edit_1 144

<a id="cmd-menu-hide"></a>

#### Menu Hide

**Synopsis**

    menu Hide

**Description**

The *menu Hide* command hides the EasyUO menu window

> [!NOTE]
> Calling [menu Show](#cmd-menu-show) is the only way to make the menu visible again

<a id="cmd-menu-hideeuo"></a>

#### Menu HideEUO

**Synopsis**

    menu HideEUO

**Description**

The [menu HideEUO](#cmd-menu-hideeuo) command hides the main EasyUO window.

> [!NOTE]
> The only way to make the EasyUO window visible again is to close the current menu and restore the EasyUO window.

<a id="cmd-menu-image-create"></a>

#### Menu Image Create

**Synopsis**

    menu Image Create {name} {x} {y} {width} {height}

**Description**

The **menu Image Create** command creates a new image control with the specified name at the given positions and dimensions.

name is any valid EUO name. It is used to reference the created container.

The X and Y parameters place the control at the specified position on the menu. These parameter's are in pixels, with 0,0 being the top left of the menu.

width and height are the size of the image container, in pixels.

> [!NOTE]
> 
>
> - This command is only available from EUO 1.5.''
> - The image is completely transparent at the beginning. For a different background, simply use [Menu Image Rectangle](#cmd-menu-image-rectangle)

<a id="cmd-menu-image-ellipse"></a>

#### Menu Image Ellipse

**Synopsis**

    menu Image Ellipse {name} {x1} {y1} {x2} {y2} {color} {fill} [width]

**Description**

The [menu Image Ellipse](#cmd-menu-image-ellipse) command draws an ellipse/circle within the specified image. x1/y1 and x2/y2 define the rectangle/square that encloses the ellipse. If fill is #false then only the outer line is drawn, otherwise the ellipse is filled.

For the color parameter, you can use names like "red", "yellow" or "windowtext" or use a hexadecimal number like $AABBCC (BBGGRR encoded). $FEEEED is used for transparency. If you do not fill the ellipse, you may also specify a line width (default is 1).

> [!NOTE]
> This command is only available from EUO 1.5.

<a id="cmd-menu-image-file"></a>

#### Menu Image File

**Synopsis**

    menu Image File {name} {x} {y} {filename}

**Description**

The **menu Image File** command loads an external image file at position x/y within the specified image.

name is a valid EUO name. it should match the name used with the [menu Image Create](#cmd-menu-image-create) command.

The X and Y values provided to this command are relative to within the Image created with the [menu Image Create](#cmd-menu-image-create) command, not the window itself. Therefore, menu Image File Test 0 0 test.bmp will place the image at the top right of the image container, not the top right of the window.

filename must be a valid path to an existing file.

> [!NOTE]
> 
>
> - This command is only available from EUO 1.5.
> - The number of supported formats may depend on your OS, but BMP, GIF and JPG should always be suppored. File types that support transparency should also appear transparent in the image.

<a id="cmd-menu-image-floodfill"></a>

#### Menu Image FloodFill

**Synopsis**

    menu Image FloodFill {name} {x} {y} {color}

**Description**

The [menu Image FloodFill](#cmd-menu-image-floodfill) command applies the FloodFill effect in the area around the pixel x/y within the specified image. The effect will only spread as far as the pixel colors do not change.

For the color parameter, you can use names like "red", "yellow" or "windowtext" or use a hexadecimal number like $AABBCC (BBGGRR encoded). $FEEEED is used for transparency.

> [!NOTE]
> This command is only available from EUO 1.5.

<a id="cmd-menu-image-line"></a>

#### Menu Image Line

**Synopsis**

    menu Image Line {name} {x1} {y1} {x2} {y2} {color} [width]

**Description**

The [menu Image Line](#cmd-menu-image-line) command draws a line from x1/y1 to x2/y2 within the specified image.

For the color parameter, you can use names like "red", "yellow" or "windowtext" or use a hexadecimal number like $AABBCC (BBGGRR encoded). You may also specify a line width (default is 1).

> [!NOTE]
> This command is only available from EUO 1.5.

<a id="cmd-menu-image-pix"></a>

#### Menu Image Pix

**Synopsis**

    menu Image Pix {name} {x} {y} {color}

**Description**

The [menu Image Pix](#cmd-menu-image-pix) command paints a single pixel at x/y within the specified image.

For the color parameter, you can use names like "red", "yellow" or "windowtext" or use a hexadecimal number like $AABBCC (BBGGRR encoded). $FEEEED is used for transparency.

> [!NOTE]
> 
>
> - This command is only available from EUO 1.5.
> - For faster pixel output, use [Menu Image PixLine](#cmd-menu-image-pixline) instead.

<a id="cmd-menu-image-pixline"></a>

#### Menu Image PixLine

**Synopsis**

    menu Image PixLine {name} {x} {y} {data}

**Description**

The [menu Image PixLine](#cmd-menu-image-pixline) command prints a horizontal line of pixels starting at position x/y within the specified image. "data" is encoded as follows:

Each pixel has an RGB value that is defined by three consecutive characters in the data string. Valid characters are A-Z, 1-6 and 9. These characters specify the intensity of each color (RGB) whereas A=0, B=8, C=16 ... Z=200, 1=208 ... 6=248 and 9=transparent.

Examples: AAA = black, 666 = white (equals $F8F8F8), 6AA = red (equals $0000F8) AAAPPP666999AAP = black,gray,white,transparent,navy (=5 pixels).

You can create interesting effects by using partial transparency like in 9A9 which only removes the green intensity from the overpainted pixel. Transparency only works for the specified image, i.e. other images below or above do not have any influence.

> [!NOTE]
> 
>
> - This command is only available from EUO 1.5.
> - Do not overuse this feature. Small images (also called Sprites) are okay, but we don't want 200KB scripts just because you like to have a nice background. Use external JPG or GIF images instead. Very advanced scripters may also consider creating their own image compression format and converting it into a data string at the initial script run. Resulting strings can be stored in persistent variables for future access.

<a id="cmd-menu-image-pos"></a>

#### Menu Image Pos

**Synopsis**

    menu Image Pos {name} {x} {y} [width] [height]

**Description**

The [menu Image Pos](#cmd-menu-image-pos) command moves an already existing image control to a different position. You can use the width and height parameters to enlarge or shrink the image.

> [!NOTE]
> This command is only available from EUO 1.5.

<a id="cmd-menu-image-rectangle"></a>

#### Menu Image Rectangle

**Synopsis**

    menu Image Rectangle {name} {x1} {y1} {x2} {y2} {color} {fill} [width]

**Description**

The *menu Image Rectangle* command draws a rectangle between x1/y1 and x2/y2 within the specified image. If fill is #false then only the outer line is drawn, otherwise the rectangle is filled.

For the color parameter, you can use names like "red", "yellow" or "windowtext" or use a hexadecimal number like $AABBCC (BBGGRR encoded). $FEEEED is used for transparency. If you do not fill the rectangle, you may also specify a line width (default is 1).

> [!NOTE]
> This command is only available from EUO 1.5.

<a id="cmd-menu-list"></a>

#### Menu List

**Synopsis**

    menu List Create {name} {x} {y} {width} {height}
    menu List Add {name} {string}
    menu List Select {list name} {item number}

**Description**

The [menu List](#cmd-menu-list) creates a listbox at position x/y with specified size on the EasyUO menu window, adds entires to the listbox or selects an entry in the list.

##### Example

    menu Clear
    menu Font BGColor white                           ; sets list's background color to white
    menu List Create lstTest 10 10 180 120            ; create listbox
    menu List Add lstTest This is a simple example    ; add a string
    menu List Add lstTest showing how to use          ; another one
    menu List Add lstTest a listbox!                  ; and another...

    menu List Add lstTest                             ; adds a blank line
    menu List Add lstTest This line will be selected. ; yet another line
    menu List Select lstTest 5                        ; select line with index 5

    menu Window Title Listbox Example
    menu Window Size 200 140
    menu Show
    halt

<a id="cmd-menu-set"></a>

#### Menu Set

**Synopsis**

    menu Set {name} {text}

**Description**

The [menu Set](#cmd-menu-set) command sets the text of a control.

<a id="cmd-menu-shape"></a>

#### Menu Shape

**Synopsis**

    menu Shape {name} {left} {top} {width} {height} {shapetype} {linetype} {linewidth} {linecolor} {filltype} {fillcolor}

**Description**

The [menu Shape](#cmd-menu-shape) command creates a shape in the EasyUO menu window.

**Table 17. menu Shape shapetype**

| Value | Description     |
|-------|-----------------|
| 1     | Circle          |
| 2     | Ellipse         |
| 3     | Rectangle       |
| 4     | Round Rectangle |
| 5     | Round Square    |
| 6     | Square          |

| Value | Description  |
|-------|--------------|
| 1     | Clear        |
| 2     | Dash         |
| 3     | Dash Dot     |
| 4     | Dash Dot Dot |
| 5     | Dot          |
| 6     | Inside Frame |
| 7     | Solid        |

| Value | Description    |
|-------|----------------|
| 1     | BDiagonal      |
| 2     | Clear          |
| 3     | Cross          |
| 4     | Diagonal Cross |
| 5     | FDiagonal      |
| 6     | Horizontal     |
| 7     | Solid          |
| 8     | Vertical       |

<a id="cmd-menu-show"></a>

#### Menu Show

**Synopsis**

    menu Show {x} {y}

**Description**

The [menu Show](#cmd-menu-show) command shows the main EasyUO window at the specified position.

> [!NOTE]
> Calling menu Show is the only way to make a menu, hidden by calling [menu Hide](#cmd-menu-hide) visible again.

<a id="cmd-menu-text"></a>

#### Menu Text

**Synopsis**

    menu Text {name} {x} {y} {text}

**Description**

The [menu Text](#cmd-menu-text) command creates a label at the specified position in the EasyUO menu window.

##### Example

    ; This will create a text line named text_1 at position 10 20
    ; with the words Read me!
    ; Note that when refering to this field later in the script
    ; you will reference the NAME and not the displayed TEXT.
    menu Text text_1 10 20 Read me!

<a id="cmd-menu-window-color"></a>

#### Menu Window Color

**Synopsis**

    menu Window Color {color-descriptor}

**Description**

The [menu Window Color](#cmd-menu-window-color) command changes the color of the EasyUO menu window.

Color-descriptor can be a few different things: black, red, btnface or a hexadecial (i.e. $aabbcc).

<a id="cmd-menu-window-size"></a>

#### Menu Window Size

**Synopsis**

    menu Window Size {width} {height}

**Description**

The [menu Window Size](#cmd-menu-window-size) command changes the size of the EasyUO menu window.

<a id="cmd-menu-window-title"></a>

#### Menu Window Title

**Synopsis**

    menu Window Title {title}

**Description**

The [menu Window Title](#cmd-menu-window-title) command changes the window title of the EasyUO menu window.

<a id="cmd-menu-window-transparent"></a>

#### Menu Window Transparent

**Synopsis**

`menu window transparent [ opacity percentile ]`

**Description**

`The menu window transparent sets the transparency of the window ( 0 is almost invisible and 100 is fully opaque ).`\
`Note: This command doesn't work under Linux + Wine (1.1.2).`

##### Example

    menu window $000000 ;Window will be dark black
    menu show 200 200 ;Shows window

    for %i 0 100 ;Loops from 0 to 100
    {
        menu window transparent %i ;Sets the transparency of the window
        wait 5 ;Waits 1/4 second
    }

    halt ;Terminates the script

<a id="sec-namespace"></a>

### Namespace

Commands to interact with namespaces and their related variables.

| Command | Summary |
|---|---|
| [nameSpace local](#cmd-namespace-local) | Defines the current namespace and its scope |
| [nameSpace global](#cmd-namespace-global) | Defines the current namespace and its scope |
| [nameSpace clear](#cmd-namespace-clear) | Clears every variables within the current namespace |
| [nameSpace push](#cmd-namespace-push) | Stores the current namespace name and scope |
| [nameSpace pop](#cmd-namespace-pop) | Restores the current namespace name and scope |
| [nameSpace copy](#cmd-namespace-copy) | Copy variables from one namespace to another |

<a id="cmd-namespace-local"></a>

#### NameSpace local

**Synopsis**

    nameSpace local {namespace name}

**Description**

The namespace local command defines the current namespace name and scope. The {namespace name} cannot start with a number, but can start with an underscore and can include any aphanumeric character. A local namespace can only be accessed by the script that defined it.

The default namespace is named STD and has local scope. This namespace is restored when the script is stopped, or there are no previous namespaces defined at the point that a [nameSpace pop](#cmd-namespace-pop) occurs.

##### Example

    namespace local ns1
    set !test test1

    namespace local ns2
    set !test test2

    namespace local ns3
    set !test test3

    namespace local ns1
    display ok !test

    namespace local ns2
    display ok !test

    namespace clear ns2
    namespace local ns2
    display ok !test

    namespace local ns3
    display ok !test

    halt

<a id="cmd-namespace-global"></a>

#### NameSpace global

**Synopsis**

    nameSpace global {namespace name}

**Description**

*(Added in 1.39)* The **[Namespace](#sec-namespace)** global command defines the current [Namespace](#sec-namespace) name and scope. The {namespace name} must be a valid EasyUO name. The scope is global. A Global [Namespace](#sec-namespace) can be accessed by any script running within the same EasyUO instance.

The default [Namespace](#sec-namespace) is [local](#cmd-namespace-local) and named STD. This setting is restored when the script is stopped.

> [!NOTE]
> Global namespaces are only available in EasyUO 1.5.

##### Example

EDIT on 2 feb. 2008: global nameSpaces are particularly useful when running multiple scripts at the same time. To test these snippets copy/paste each one in a different page (run the first script, then the second, then the third to test). They MUST be wittin the same EUO instance though!!

first script:

    nameSpace global test
    set !testMsg Vhann_was_here_to_show_ppl_how_to_use_global_namespaces
    pause

second script:

    ;Important: you MUST enter the nameSpace before you can access
    ;the variables created in other scripts
    nameSpace global test
    display Ok !testMsg
    set !testMsg !testMsg , $you_can_use_globals_in_more_than_2_scripts_at_a_time.
    pause

Third script:

    nameSpace global test
    display Ok !testMsg
    halt

<a id="cmd-namespace-clear"></a>

#### NameSpace clear

**Synopsis**

    nameSpace clear

**Description**

*(Added in 1.39)* The **[Namespace](#sec-namespace)** clear command clears every variables within the current [Namespace](#sec-namespace).

The default [Namespace](#sec-namespace) is [local](#cmd-namespace-local) and named STD. This setting is restored when the script is stopped.

> [!NOTE]
> Global namespaces are only available in EasyUO 1.5.

##### Example

    set !return ; make sure !return is empty
    gosub test
    display ok !return
    halt

    sub test
        nameSpace Push ; saves current namespace
        nameSpace Local Test ; create a new temporary namespace to work with
        set !return this_is_a_test
        nameSpace Pop ; restore previous namespace
        nameSpace Copy ret* From Local Test ; copy variables to the original namespace
        nameSpace Push ; saves current namespace
        nameSpace Local Test
        nameSpace Clear ; free memory used by temporary namespace
        nameSpace Pop ; restore previous namespace
    return

<a id="cmd-namespace-push"></a>

#### NameSpace push

**Synopsis**

    nameSpace push

**Description**

*(Added in 1.40)* The **[Namespace](#sec-namespace)** push command stores the current [Namespace](#sec-namespace) name and scope in an internal stack.

The default [Namespace](#sec-namespace) is [local](#cmd-namespace-local) and named STD. This setting is restored when the script is stopped.

> [!NOTE]
> Currently only Local scope is available. Global scope is to be introduced in a future version of EasyUO.

##### Example

    set !return ; make sure !return is empty
    gosub test
    display ok !return
    halt

    sub test
        nameSpace Push ; saves current namespace
        nameSpace Local Test ; create a new temporary namespace to work with
        set !return this_is_a_test
        nameSpace Pop ; restore previous namespace
        nameSpace Copy ret* From Local Test ; copy variables to the original namespace
        nameSpace Push ; saves current namespace
        nameSpace Local Test
        nameSpace Clear ; free memory used by temporary namespace
        nameSpace Pop ; restore previous namespace
    return

<a id="cmd-namespace-pop"></a>

#### NameSpace pop

**Synopsis**

    nameSpace pop

**Description**

The namespace pop command restores the current namespace name and scope from an internal stack.

The default namespace is named STD and has local scope. This namespace is restored when the script is stopped, or there are no previous namespaces defined at the point that a nameSpace pop occurs.

##### Example

    set !return ; make sure !return is empty
    gosub test
    display ok !return
    halt

    sub test
        nameSpace Push ; saves current namespace
        nameSpace Local Test ; create a new temporary namespace to work with
        set !return this_is_a_test
        nameSpace Pop ; restore previous namespace
        nameSpace Copy ret* From Local Test ; copy variables to the original namespace
        nameSpace Push ; saves current namespace
        nameSpace Local Test
        nameSpace Clear ; free memory used by temporary namespace
        nameSpace Pop ; restore previous namespace
    return

<a id="cmd-namespace-copy"></a>

#### NameSpace copy

**Synopsis**

    nameSpace copy {filter} {from  |  to} {local  |  global} {namespace name}

**Description**

*(Added in 1.40)* The **[Namespace](#sec-namespace)** copy command allows to copy all or part of variables within a [Namespace](#sec-namespace) into another. The {filter} parameter is use to specify which variables should be copied and accepts two special characters "?" and "\*".

The "?" character matches any single character and can be use multiple times within one {filter} expression. I.e. "return?" will match any variable whose name start with "return" and has one additional character.

The "\*" character matches zero or more unspecified character. It can only appear but once within a {filter} expression. I.e. "return\*" will match any variable whose name start with "return".

The {from \| to} parameter defines the direction for the copy, while the {local \| global} {namespace name} parameters define the [name](#var-nsname) and scope of the [Namespace](#sec-namespace) to be used.

From: copies variables from the specified [Namespace](#sec-namespace) into the current [Namespace](#sec-namespace).

To: copies variables from the current [Namespace](#sec-namespace) into the specified [Namespace](#sec-namespace). If the specified [Namespace](#sec-namespace) doesn't exist at this time, it will be created.

The default [Namespace](#sec-namespace) is [local](#cmd-namespace-local) and named STD. This setting is restored when the script is stopped.

> [!NOTE]
> Global namespaces are only available in EasyUO 1.5.

##### Example

    set !return ; make sure !return is empty
    gosub test
    display ok !return
    halt

    sub test
        nameSpace Push ; saves current namespace
        nameSpace Local Test ; create a new temporary namespace to work with
        set !return this_is_a_test
        nameSpace Pop ; restore previous namespace
        nameSpace Copy ret* From Local Test ; copy variables to the original namespace
        nameSpace Push ; saves current namespace
        nameSpace Local Test
        nameSpace Clear ; free memory used by temporary namespace
        nameSpace Pop ; restore previous namespace
    return

<a id="sec-miscellaneous"></a>

### Miscellaneous

Miscellaneous commands

| Command | Summary |
|---|---|
| [display](#cmd-display) | Shows a message |
| [execute](#cmd-execute) | Executes an external program |
| [linesPerCycle](#cmd-linespercycle) | Sets the execution speed |
| [set](#cmd-set) | sets a variable to a value (variable assignment) |
| [send](#cmd-send) | Sends a HTTP request to a server and runs the code that is returned |
| [shutDown](#cmd-shutdown) | Shuts your computer down |
| [sound](#cmd-sound) | Plays a wave file or the SystemDefault beep |
| [str](#cmd-str-command) | performs a operation on a string |
| [tile](#cmd-tile) | retrieves information about tiles |

<a id="cmd-display"></a>

#### Display

**Synopsis**

    display {[ok]  |  [okcancel]  |  [yesno]  |  [yesnocancel]} {message}

**Description**

The [display](#cmd-display) command displays a standard Windows messagebox with a set of buttons of your choice.

##### Example

    display yesno You have run out of ingots. Do you want to end the script?
    if #dispRes = yes
        halt
    ...

> [!NOTE]
> Use $ to create a newline:
>
>     display ok Test $1$2$3
>
> creates:
>
>     Test
>     1
>     2
>     3
>     [ ok ]

<a id="cmd-execute"></a>

#### Execute

**Synopsis**

    execute {filename} [argument...]

**Description**

The *execute* command executes an external command with the argunments given.

> [!NOTE]
> This command does NOT work unless you have enabled the "Allow Execute" configuration option.

###### Examples

##### Example 1 : Script in Script

Running a script, from a script.

    execute EasyUO.exe healthWatch.euo

##### Example 2 : File Writing

For example purposes, assume the following:

    %task is move
    %guardzone is #false
    #charPosX is 4321 
    #charPosY is 1234
    #charPosZ is 3
    %tileid is 7

###### Write line at a time to a file

    execute cmd.exe /c echo gosub railtask move %task %guardzone #charPosX #charPosY #charPosZ %tileid >>rail.txt

Makes a file named rail.txt that consists of:

    gosub railtask move 0 4321 1234 3 7

###### Write a many lines to a file at once

The magic of cmd.exe! This only opens console window once, improves long write times dramatically. Windows 2000+ only: Maximum command in Win2000 is 4096, WinXP and Vista 8192

**Do not press Enter anywhere on the execute line until the final ", it must be one solid line without line breaks.** (The Wiki is limited in its ability to wrap code text.)

       for %counter 1 %endspot
       {
          execute cmd.exe /c "echo set % , RailStep %counter >> rail.txt && echo set % , Task , %counter %Task >> rail.txt && echo set % , Guardzone 
    , %counter %GuardZone >> rail.txt && echo set % , SpotX , %counter #charPosX >> rail.txt && echo set % , SpotY , %counter #charPosY >> rail.txt && echo 
    set % , SpotZ , %counter #charPosZ >> rail.txt && echo set % , TileID , %counter %TileID >> rail.txt"   
       }

EDIT on 23 jan 2008: You can break lines, though you must use the concatenation operator '+' as the first character on the "breaked lines":

       for %counter 1 %endspot
       {
          execute cmd.exe /c "echo set % , RailStep %counter >> rail.txt && echo set % , Task , %counter %Task
           + >> rail.txt && echo set % , Guardzone , %counter %GuardZone >> rail.txt && echo set % , SpotX , %counter
           + #charPosX >> rail.txt && echo set % , SpotY , %counter #charPosY >> rail.txt && echo
           + set % , SpotZ , %counter #charPosZ >> rail.txt && echo set % , TileID , %counter %TileID >> rail.txt"   
       }

Makes a file named rail.txt that consists of:

    set %RailStep 1
    set %Task1 move
    set %Guardzone1 0
    set %SpotX1 4321  
    set %SpotY1 1234  
    set %SpotZ1 3  
    set %TileID1 7 

**Related:** [Terminate](#cmd-terminate), [UoXL](#cmd-uoxl)

<a id="cmd-linespercycle"></a>

#### LinesPerCycle

**Synopsis**

    linesPerCycle {linespercycle}

**Description**

The [LinesPerCycle](#cmd-linespercycle) command sets the number of lines that the EasyUO parser runs through for every cycle. The default value is 10 and is reset when you stop the script.

Cheffe's description of lines per cycle, and cycles per second:

"EUO has 20 cycles per second and in each cycle it executes 10 lines (default). Some commands have built in waits so that the script speed slows down considerably.

You can't say that one command is faster than the other. EUO gives away most of the available processing time so that the UO client can have it.

EUO doesn't know the difference between a processing intensive task such as "finditem \*" at WBB or a simple "set %x 3". While 10 lines per cycle is already too fast if you have 10 finditems in a row you could execute hundreds of set instructions in the same time without stressing the CPU."

Read here: http://www.easyuo.com/forum/viewtopic.php?p=21269

##### Example

    linespercycle 10

<a id="cmd-set"></a>

#### Set

**Synopsis**

    set {{!namespaceVariable}}} [expression] [abs]

**Description**

The [set](#cmd-set) command, sets a varible to what an expression evaluates to. If the abs option is specified, the absolute (mathimatically) value will be assigned. Ommitting the expression will set the variable to a blank string.

##### Example

    set %a 2
    set %b $a ;we can use hexadecimal too
    set %c ( %a * %b ) + 1 ;%c is 21
    set %d %a * ( %b + 1 ) ;%d is 22
    set %e %a * %b + 1 ;%e is 21
    set %f ;set %f to a blank string
    set %varname 0 ;initializing a variable to 0
    halt

> [!NOTE]
> Set is used to increment a variable by 1 by doing: set %varname %varname + 1

<a id="cmd-send"></a>

#### Send

**Synopsis**

    send {{"HTTPPost[port]"}}}  {site} {path} {post data}

**Description**

The [send](#cmd-send) command sends a HTTP request to a web server and executes the code that is returned.

> [!NOTE]
> Allow Send must be enabled for this command to work.

##### Example

    ;******************************
    ; EUO Chat V1.0 by Cheffe
    ;******************************
    ;
    ; Allow send must be enabled!!!

    menu Clear
    menu Window Size 245 120
    menu Window Title EUO Chat V1.0
    menu Show 200 200
    menu HideEUO

    menu Text 1 20 20 Please enter your nickname:
    menu Font BGColor White
    menu Edit 2 20 40 200
    menu Font BGColor BtnFace
    menu Button 3 130 70 90 25 OK

    set #menuButton 0
    N1:
        if #menuButton = closed
            halt
        if #menuButton <> 3
    goto N1

    menu Get 2
    set %nickname #menuRes

    ;******************************

    menu Clear
    menu Window Size 500 230
    menu Font BGColor White
    menu Edit e1 20 180 360
    menu Font BGColor BtnFace
    menu Button b1 400 180 80 25 Send!

    set #menuButton 0
    N2:
        N3:
            if #scnt2 > 30
            {
                send HTTPPost www.easyuo.com /webscripts/euochat.pl R
                set #scnt2 0
            }

            if #menuButton = CLOSED
                halt

            if #menuButton <> b1
        goto N3
        set #menuButton 0

        menu Get e1
        send HTTPPost www.easyuo.com /webscripts/euochat.pl S %nickname , : #menuRes
        menu Activate e1

    goto N2

<a id="cmd-shutdown"></a>

#### ShutDown

**Synopsis**

    shutDown ["force"]

**Description**

The [shutDown](#cmd-shutdown) command shuts your computer down. The option force forces non-responsive application to shut down, as well.

##### Example

    if #charGhost = YES
    {
    shutDown
    }

<a id="cmd-sound"></a>

#### Sound

**Synopsis**

    sound [filename]

**Description**

The [sound](#cmd-sound) command plays a wave file or the SystemDefault beep.

##### Example

    if #charghost = YES
    {
    sound
    halt
    }

> [!NOTE]
> For File Use:
>
> If the sound file is in a directory which exists in your dos PATH environment variable, you do not need to include a full path. Try this:
>
> sound chimes.wav
>
> You should hear the windows chimes sound. Sound will also accept absolute paths.
>
> sound c:\windows\media\chimes.wav

<a id="cmd-str-command"></a>

#### Str (command)

**Synopsis**

    str {"Len"} {string}
    str {"Pos"} {string} {sub string} [index]
    str {"Left"} {string} {length}
    str {"Right"} {string} {length}
    str {"Mid"} {string} {start} {length}
    str {"Lower"} {string}
    str {"Ins"} {string} {sub string} {start}
    str {"Del"} {string} {start} {length}
    str {"Count"} {string} {substring}

**Description**

The [str](#cmd-str-command) command performs a string operation on the string given and stores the result in #strRes.

| Value | Description |
|----|----|
| Len | Stores the length of the string in the #strRes system variable. |
| Pos | Stores the position of the sub string in the #strRes system variable. *index* tells which occurrence to return (if there's more than one). |
| Left | Stores a part of the string taken from the left, in the #strRes system variable. |
| Right | Stores a part of the string taken from the right, in the #strRes system variable. |
| Mid | Stores a part of the string taken from the middle, in the #strRes system variable. |
| Lower | Stores a lower case version of the string in the #strRes system variable. |
| Ins | Inserts a string into the string and stores it in the #strRes system variable. |
| Del | Deletes a part of the string and stores it in the #strRes system variable. |
| Count | Returns the number of occurrences of substring in string. |

> [!NOTE]
> 
>
> - Index parameter in Str Pos is only avalable from EUO 1.5 Test version 27.
> - Str Count command is only avalable from EUO 1.5 Test version 27.

##### Example

    set %string HELLO
    str Len %string     ; #strRes = 5
    str Pos %string LL  ; #strRes = 3
    str Left %string 4  ; #strRes = HELL
    str Right %string 2 ; #strRes = LO
    str Mid %string 2 3 ; #strRes = ELL
    str Lower %string   ; #strRes = hello
    str Ins %string I 3 ; #strRes = HELILO
    str Del %string 3 2 ; #strRes = HEO
    str Count %string L ; #strRes = 2

    ; This is a sample on how to use Str Count
    ; command and index parameter of Str Pos
    ; Made by Cheffe.

    set %test _this_is_a_test_and_tests_are_cool_
     
    str count %test _
    for %cnt #strres 2 
    { 
      set %tmp %cnt - 1 
      str pos %test _ %tmp 
      set %tmp #strres + 1 
      str pos %test _ %cnt 
      set %len #strres - %tmp 
      str mid %test %tmp %len 
      display ok #strres 
    }

<a id="cmd-tile"></a>

#### Tile

**Synopsis**

    tile {Init} [noOverrides]
    tile {Cnt} {x} {y} [facet]
    tile {Get} {x} {y} {index} [facet]

**Description**

The tile command retrieves information about map tiles.

| Option | Description |
|----|----|
| Init | Initializes the tile information for retrieval in EasyUO. Using the "noOverrides" option forces EasyUO to not read the statics override file (VerData.mul), which could be useful for freeshards that do not use the overrides. If you don't know what VerData.mul is, you probably don't need to use the noOverrides option. |
| Cnt | Retrieves the number of tiles for a specific position. The value in [#tileCnt](#var-tilecnt) is updated. The default value for facet is the current facet. Otherwise follows the values for [#cursKind](#var-curskind). |
| Get | Retrives the tile type and z value. The values in [#tileType](#var-tiletype) and [#tileZ](#var-tilez) are updated. The index goes from 1 to [#tileCnt](#var-tilecnt). The default value for facet is the current facet. Otherwise follows the values for [#cursKind](#var-curskind) |

> [!NOTE]
> See the [#tileFlags](#var-tileflags) page for a list of all of the possible #tileFlag values.

**Related**

<a id="sec-obsolete"></a>

### Obsolete

Obsolete commands that are only used for backward compatibility.

| Command | Summary |
|---|---|
| [deleteVar](#cmd-deletevar) | Sets a variable to an empty string |
| [initEvents](#cmd-initevents) | Initializes all event commands |

<a id="cmd-deletevar"></a>

#### DeleteVar

**Synopsis**

    deleteVar {variable name}

**Description**

The [deleteVar](#cmd-deletevar) command deletes the content of a variable.

> [!NOTE]
> 
>
> - The content can only be deleted if the variable has already been assigned to.
>
> <!-- -->
>
> - The deleteVar command is deprecated since the set command can now assign an empty string value to a variable.

##### Example

    ...
    ; set %test to something
    set %test TEST

    ; note there is no % char in front.
    deleteVar test

    ; %test now holds nothing
    ...

<a id="cmd-initevents"></a>

#### InitEvents

**Synopsis**

    initEvents

**Description**

The *initEvents* command initializes all event commands. If it is not run once per script, none of the event commands will function. You should only call *initEvents* once per script.

> [!NOTE]
> It should be noted that *InitEvents* is no longer required on current releases of EasyUO. The first time you use an [event Macro](#cmd-event-macro) it will automatically initialize. If it is used now it hurts nothing. But serves no purpose either

<a id="sec-system-variable-reference"></a>

## System Variable Reference

<a id="sec-character-variables"></a>

### Character Variables

The character category of system variables contains information specific to the character in the current instance of Ultima Online that EasyUO is attached to.

| Variable | Summary |
|---|---|
| [#charPosX](#var-charposx) _(ro)_ | Returns the characters world X-coordinate |
| [#charPosY](#var-charposy) _(ro)_ | Returns the characters world Y-coordinate |
| [#charPosZ](#var-charposz) _(ro)_ | Returns the characters world Z-coordinate |
| [#charDir](#var-chardir) _(ro)_ | Returns the direction the character is facing |
| [#charStatus](#var-charstatus) _(ro)_ | Returns different states that the character can be in |
| [#charID](#var-charid) _(ro)_ | Returns the id of the character |
| [#charGhost](#var-charghost) _(ro)_ | Returns if your character is dead |
| [#backpackID](#var-backpackid) _(ro)_ | Displays the ID of your player's backPack (Inventory) |

<a id="var-charposx"></a>

#### CharPosX

*Read-only.* Determines the characters world X-coordinate. The #charPosX system variable determines the characters world X-coordinate. It is the same coordinate system as used in UO Auto Map.

##### Example

    if #charPosX = 4515
    {
      event SysMessage X marks the spot!
      pause
    }

<a id="var-charposy"></a>

#### CharPosY

*Read-only.* Determines the characters world Y-coordinate.The #charPosY system variable determines the characters world Y-coordinate. It is the same coordinate system as used in UO Auto Map.

##### Example

    if #charPosY = 328
    {
      event SysMessage Y marks the spot!
      pause
    }

<a id="var-charposz"></a>

#### CharPosZ

*Read-only.* Determines the characters world Z-coordinate (Height). The #charPosZ system variable determines the characters world Z-coordinate. It is the same coordinate system as used in UO Auto Map.

##### Example

    if #charPosZ = 35
    {
      event SysMessage Climb that mountain!
      pause
    }

<a id="var-chardir"></a>

#### CharDir

*Read-only.* The #charDir system variable determines the direction the character is facing.

  

| Value | Facing     |
|-------|------------|
| 0     | North      |
| 1     | North East |
| 2     | East       |
| 3     | South East |
| 4     | South      |
| 5     | South West |
| 6     | West       |
| 7     | North West |

Table of #charDir values

##### Example

    top:
    if #CHARDIR = 0
        msg : Looking North $
    wait 2s
    goto top

<a id="var-charstatus"></a>

#### CharStatus

*Read-only.* Determines different states that the character can be in.

| Value | Description |
|----|----|
| C | Character is poisoned. |
| H | Character is hidden. |
| B | Character is female. |
| G | Character is in war mode. |
| D | Character is affected with lethal strike. |
| A | Character is frozen (actively casting a spell / Waiting for transport after using help-menu) . |

Table of #charStatus values

##### Example

    ...
    if C in #charStatus
    {
        gosub cureMe
    }

    ...

    sub cureMe
        ...
        return

<a id="var-charid"></a>

#### CharID

*Read-only.* The #charID system variable determines the id of your character. This is a unique identifier, so it can be used to identify different characters and make specific actions depending on what character it is. This variable can also be used as a container for [findItem](#cmd-finditem).

##### Example

    findItem *
    for #findIndex 1 #findCnt
    {
      if #findId <> #charId
        event ExMsg #findId 3 0 This is someone or something else.
      if #findId = #charId
        event ExMsg #charID 3 0 This is me!
    }
    halt

<a id="var-charghost"></a>

#### CharGhost

*Read-only.* The #charGhost system variable determines if your character is dead. If the character is dead it holds "YES", if it is alive it holds "NO".

| Value | Description         |
|-------|---------------------|
| YES   | Character is dead.  |
| NO    | Character is alive. |

Table of #charGhost values

##### Example

    ...
    if #charGhost = YES
    {
        gosub logOut
        halt
    }
    ...

<a id="var-backpackid"></a>

#### BackpackId

*Read-only.* The #backpackId variable contains the id of the current characters main backpack.

##### Example

    findItem * C_ , #backpackId
    display ok there are #findCnt items in your backpack.
    halt

<a id="sec-status-variables"></a>

### Status Variables

Status variables come from the UO Status Bar in game. They provide information about the current character.

**The character's status bar MUST be opened for these values to work!**

| Variable | Summary |
|---|---|
| [#charName](#var-charname) _(ro)_ | Returns the name of the character |
| [#sex](#var-sex) _(ro)_ | Returns the sex of the character |
| [#str](#var-str-system-variable) _(ro)_ | Returns the strength of the character |
| [#hits](#var-hits) _(ro)_ | Returns the current number of hitpoints of the character |
| [#maxHits](#var-maxhits) _(ro)_ | Returns the maximum number of hitpoints of the character |
| [#dex](#var-dex) _(ro)_ | Returns the dexterity of the character |
| [#stamina](#var-stamina) _(ro)_ | Returns the current stamina level or the character |
| [#maxStam](#var-maxstam) _(ro)_ | Returns the maximum stamina level or the character |
| [#int](#var-int) _(ro)_ | Returns the intelligence of the character |
| [#mana](#var-mana) _(ro)_ | Returns the current mana pool for the character |
| [#maxMana](#var-maxmana) _(ro)_ | Returns the maximum mana pool for the character |
| [#maxStats](#var-maxstats) _(ro)_ | Returns the current maximum stats of the character |
| [#luck](#var-luck) _(ro)_ | Returns the current luck of the character |
| [#weight](#var-weight) _(ro)_ | Returns the current weight of the character |
| [#maxWeight](#var-maxweight) _(ro)_ | Returns the maximum weight of the character |
| [#minDmg](#var-mindmg) _(ro)_ | Returns the minimum damage done with the currently yielded weapon |
| [#maxDmg](#var-maxdmg) _(ro)_ | Returns the maximum damage done with the currently yielded weapon |
| [#gold](#var-gold) _(ro)_ | Returns the amount of gold on the character |
| [#followers](#var-followers) _(ro)_ | Returns the current number of followers of the character |
| [#maxFol](#var-maxfol) _(ro)_ | Returns the maximum number of followers of the character |
| [#AR](#var-ar) _(ro)_ | Returns the Armor Rating of the character |
| [#FR](#var-fr) _(ro)_ | Returns the Fire Resist of the character |
| [#CR](#var-cr) _(ro)_ | Returns the Cold Resist of the character |
| [#PR](#var-pr) _(ro)_ | Returns the Poison Resist of the character |
| [#ER](#var-er) _(ro)_ | Returns the Energy Resist of the character |
| [#TP](#var-tp) _(ro)_ | Returns the Tithing Points of the character |

<a id="var-charname"></a>

#### CharName

*Read-only.* The #charName system variable contains the name of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg My name is #CHARNAME $
    halt

<a id="var-sex"></a>

#### Sex

*Read-only.* The #sex system variable determines the sex of the character.

| Value | Description         |
|:-----:|---------------------|
|   0   | Character is Male   |
|   1   | Character is Female |

#sex System Variable Values

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

<a id="var-str-system-variable"></a>

#### Str (system variable)

*Read-only.* The #str system variable determines the strength of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg My strength is #STR $
    halt

<a id="var-hits"></a>

#### Hits

*Read-only.* The #hits system variable determines the current number of hitpoints of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg I have #HITS hitpoints $
    halt

<a id="var-maxhits"></a>

#### MaxHits

*Read-only.* The #maxHits system variable determines the maximum number of hitpoints of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg I can have total of #MAXHITS hitpoints $
    halt

<a id="var-dex"></a>

#### Dex

*Read-only.* The #dex system variable determines the dexterity of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg My dexterity is #DEX $
    halt

<a id="var-stamina"></a>

#### Stamina

*Read-only.* The #stamina system variable determines the current stamina level of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg My stamina is #stamina
    halt

<a id="var-maxstam"></a>

#### MaxStam

*Read-only.* The #maxStam system variable determines the maximum stamina level of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    ...
    if #stamina < #maxStam
      gosub drinkRefresh
    ...

<a id="var-int"></a>

#### Int

*Read-only.* The #int system variable determines the intelligence of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg My intelligence is #INT $
    halt

<a id="var-mana"></a>

#### Mana

*Read-only.* The #mana system variable determines the current mana pool for the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg I have #MANA mana in my pool $
    halt

<a id="var-maxmana"></a>

#### MaxMana

*Read-only.* The #maxMana system variable determines the maximum mana pool for the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    ...
    if #mana < #maxMana
      gosub meditate
    ...

<a id="var-maxstats"></a>

#### MaxStats

*Read-only.* The #maxStats system variable determines the current maximum stats of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

<a id="var-luck"></a>

#### Luck

*Read-only.* The #luck system variable determines the current luck of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

<a id="var-weight"></a>

#### Weight

*Read-only.* The #weight system variable determines the current weight of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    ...
    if #weight > 350
      gosub gotoBank
    ...

<a id="var-maxweight"></a>

#### MaxWeight

*Read-only.* The #maxWeight system variable determines the maximum weight of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    ...
    if #weight > #maxWeight
       display ok You are over weight!
    ...

<a id="var-mindmg"></a>

#### MinDmg

*Read-only.* The #minDmg system variable determines the minimum damage done with the currently yielded weapon.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

<a id="var-maxdmg"></a>

#### MaxDmg

*Read-only.* The #maxDmg system variable determines the maximum damage done with the currently yielded weapon.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

<a id="var-gold"></a>

#### Gold

*Read-only.* The #gold system variable determines the amount of gold on the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    ...
    if #gold < 1000
    gosub gotoBank
    ...

<a id="var-followers"></a>

#### Followers

*Read-only.* The #followers system variable determines the current number of followers of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

<a id="var-maxfol"></a>

#### MaxFol

*Read-only.* The #maxFol system variable determines the maximum number of followers of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

<a id="var-ar"></a>

#### AR

*Read-only.* The #AR system variable determines the Armor Rating (Physical Resistance with AoS system) of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg My Physical Resist is #AR $
    halt

<a id="var-fr"></a>

#### FR

*Read-only.* The #FR system variable determines the Fire Resist of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg My Fire Resist is #FR $
    halt

<a id="var-cr"></a>

#### CR

*Read-only.* The #CR system variable determines the Cold Resist of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg My Cold Resist is #CR $
    halt

<a id="var-pr"></a>

#### PR

*Read-only.* The #PR system variable determines the Poison Resist of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg My Poison Resist is #PR $
    halt

<a id="var-er"></a>

#### ER

*Read-only.* The #ER system variable determines the Energy Resist of the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg My Energy Resist is #ER $
    halt

<a id="var-tp"></a>

#### TP

*Read-only.* The #TP system variable determines the Tithing Points Available to the character.

> [!NOTE]
> This variable will not work unless the character status bar is open. You can use [Event Macro 8 2](#cmd-event-macro) to open it from your script.

##### Example

    msg My Tithing Points are currently #TP$
    halt

<a id="sec-container"></a>

### Container

Container system variables represent information available about the top most (or most reacent) gump that was opened, moved, or clicked in the Ultima Online Client.

| Variable | Summary |
|---|---|
| [#nextCPosX](#var-nextcposx) _(rw)_ | Returns the x-coordinate of where the next container/gump will open |
| [#nextCPosY](#var-nextcposy) _(rw)_ | Returns the y-coordinate of where the next container/gump will open |
| [#contSize](#var-contsize) _(ro)_ | Returns the size of the currently selected container/gump |
| [#contPosX](#var-contposx) _(rw)_ | Returns the x-coordinate of the currently selected container/gump |
| [#contPosY](#var-contposy) _(rw)_ | Returns the y-coordinate of the currently selected container/gump |
| [#contKind](#var-contkind) _(ro)_ | Returns the kind of the currently selected container/gump |
| [#contID](#var-contid) _(ro)_ | Returns the id of the currently selected container/gump |
| [#contType](#var-conttype) _(ro)_ | Returns the object type of the currently selected container/gump |
| [#contName](#var-contname) _(ro)_ | Returns the name of currently selected container/gump |

<a id="var-nextcposx"></a>

#### NextCPosX

*Read / write.* The #nextCPosX system variable determines the x-coordinate of where the next container/gump will open.

> [!NOTE]
> The "Offset interface windows rather than perfectly stacking them" option, in Interface options (Mouse Icon) must be turned on for the #nextCPosX and #nextCPosY variables to work.

##### Example

    ; Open bank box at 10,10
    set #nextCPosX 10
    set #nextCPosY 10
    msg bank$
    halt

<a id="var-nextcposy"></a>

#### NextCPosY

*Read / write.* The #nextCPosY system variable determines the y-coordinate of where the next container/gump will open.

> [!NOTE]
> The "Offset interface windows rather than perfectly stacking them" option, in Interface options (Mouse Icon) must be turned on for the #nextCPosX and #nextCPosY variables to work.

##### Example

    ; Open bank box at 10,10
    set #nextCPosX 10
    set #nextCPosY 10
    msg bank$
    halt

<a id="var-contsize"></a>

#### ContSize

*Read-only.* The [#contSize](#var-contsize) system variable determines the size of the currently selected container/gump. The format is as follows: "{Width}\_{Height}".

> [!NOTE]
> EasyUO currently only holds information in the #cont\* on the "top most" gump. This means that the last gump that was opened or moved in any way is what EUO is reporting.

##### Example

    if #contSize = 101_101 ;if the front container/gump's size is 101 101
    {
    .....
    }

<a id="var-contposx"></a>

#### ContPosX

*Read / write.* The #contPosX system variable determines the x-coordinate of the currently selected container/gump.

> [!NOTE]
> EasyUO currently only holds information in the #cont\* on the "top most" gump. This means that the last gump that was opened or moved in any way is what EUO is reporting.

##### Example

    set #contPosX 10
    set #contPosY 10
    contpos
    ;Will move the current container/Gump to position 10 10

<a id="var-contposy"></a>

#### ContPosY

*Read / write.* The #contPosY system variable determines the Y-coordinate of the currently selected container/gump.

> [!NOTE]
> EasyUO currently only holds information in the #cont\* on the "top most" gump. This means that the last gump that was opened or moved in any way is what EUO is reporting.

##### Example

    set #contPosX 10
    set #contPosY 10
    contpos
    ;Will move the current container/Gump to position 10 10

<a id="var-contkind"></a>

#### ContKind

*Read-only.* The #contKind system variable determines the kind of the currently selected container/gump. Most menus have a kind attached to them. The can be utilized to find out if a crafting menu is open, if something is being dragged, if a runebook is open and many other things.

> [!NOTE]
> This variable can change every time a new patch is released for the client, and EasyUO is updated. Good scripting standards dictate that you use variables in top of your script for #contKind's. In this way #contKind values can easily be updated when the client is patched.

> [!NOTE]
> EasyUO currently only holds information in the #cont\* on the "top most" gump. This means that the last gump that was opened or moved in any way is what EUO is reporting.

##### Example

    ...
    if #contKind <> %craftMenuKind
         gosub useNewTool
    ...

<a id="var-contid"></a>

#### ContID

*Read-only.* The #contID system variable determines the id of the currently selected container/gump.

> [!NOTE]
> EasyUO currently only holds information in the #cont\* on the "top most" gump. This means that the last gump that was opened or moved in any way is what EUO is reporting.

##### Example

    ........
    if #contId <> %gumpid
            gosub usenewtool
    ........

<a id="var-conttype"></a>

#### ContType

*Read-only.* The #contType system variable determines the object type of the currently selected container/gump.

> [!NOTE]
> EasyUO currently only holds information in the #cont\* on the "top most" gump. This means that the last gump that was opened or moved in any way is what EUO is reporting.

##### Example

    ....
    if #contType <> %trashbarreltype
           gosub opentrash
    ....

<a id="var-contname"></a>

#### ContName

*Read-only.* The #contName system variable determines the name of the currently selected container/gump. The values that have been found so far are included in the table below. It may not be comprehensive, and Freeshards can and often do include custom gumps that will show up in this variable.

| Value | Description |
|----|----|
| stack_gump | comes up for amount input when dragging a stack |
| drag_gump | when something is dragged on the cursor |
| paperdoll_gump | Gump that shows your character's paperdoll. |
| status_gump | Gump that displays all your character's information. |
| skill_gump | The list gump that shows all your character's skills. |
| text_gump | from a journal open. |
| YesNo_gump | from a logout. |
| OptionsGump | Gump that is displayed when the Options button is pressed on the paperdoll. |
| generic_gump | The gump that is displayed by clicking the help button on the paperdoll, runebooks, and crafting menus to name a few. |
| missile_gump | seems to be an intermediate/transitional status, shows up when something is flying through the air. |
| normal_gump | seen with: chat screen and the shard selection screen. |
| container_gump | clicking on any item that acts as a container that holds other items will bring up this gump. |
| MainMenu_gump | ? |
| waiting_gump | this one comes up for stuff like bad password. Informational Gump. |
| login_gump | The login screen gump, where you type in your username and password. |
| dumb_gump | Gump for individual drops of snow or rain. It can interfear with scripts that are looking for other gumps, so if you want to prevent it from showing up you can use the UOA or Razer weather filter. |
| GameAreaEdgeGump | very quick, hard to catch, name might be wrong. |
| radar_gump | The map. |
| DamageNumbers_gump | comes up when doing damage to a target. Only available on AoS enabled clients/shards. |
| skillicon_gump | The rectangular gump with a skill's name in it that you can drag from the skill list gump. |
| spellicon_gump | Any one of the square spell icon's that you can drag from a spell book. |
| party_gump | The party system control menu gump. |
| profile_gump | The scroll that you can type information about yourself into, or display information that others have typed about themself if it's from another person. |
| combat_ability_book_gump | Any one of the square combat move icon's that you can drag from the combat book on your character's paperdoll. |
| spellbook_gump | The gump that opens when you open a spell book. |
| Course_gump | Treasure Map gump. |
| Bill_gump | Buy/Sell gump. |
| hue_gump | gump that allows you to set a color. most commonly seen when you set the color of a dye tub. |
| CharCreation_gump | character creation screen gump. |
| ListBoxControl_gump | it can be found on option gump, and the character creation gump, to name a couple. you need to actually select the control in order to see this gump. |
| resize_gump | Seen when resizing other gumps such as the journal, skill gump, etc... |
| map_gump | Character creation screen, when you choose the city to you wish to start in. |
| CONTEXT_HELP | Codex of Wisdom Gump. |

Known contName Values

> [!NOTE]
> EasyUO currently only holds information in the #cont\* on the "top most" gump. This means that the last gump that was opened or moved in any way is what EUO is reporting.

##### Example

    ...
    if #contName = login_gump
         gosub login
    ......

<a id="sec-last-action"></a>

### Last Action

The last action system variables are adjusted when certain activities are performed in the Ultima Online Client.

| Variable | Summary |
|---|---|
| [#lObjectID](#var-lobjectid) _(rw)_ | Returns the id of the last used object |
| [#lObjectType](#var-lobjecttype) _(ro)_ | Returns the type of the last used object |
| [#lTargetID](#var-ltargetid) _(rw)_ | Returns the id of the last target used |
| [#lTargetX](#var-ltargetx) _(rw)_ | Returns the world x-coordinate of the last target used |
| [#lTargetY](#var-ltargety) _(rw)_ | Returns the world y-coordinate of the last target used |
| [#lTargetZ](#var-ltargetz) _(rw)_ | Returns the world z-coordinate of the last target used |
| [#lTargetKind](#var-ltargetkind) _(rw)_ | Returns the kind of what was last targeted |
| [#lTargetTile](#var-ltargettile) _(rw)_ | Returns the tile last targeted |
| [#lLiftedID](#var-lliftedid) _(ro)_ | Returns the id of the object last dragged/lifted |
| [#lLiftedType](#var-lliftedtype) _(ro)_ | Returns the type of the object last dragged/lifted |
| [#lLiftedKind](#var-lliftedkind) _(ro)_ | Returns if an object is being dragged/lifted |
| [#lSkill](#var-lskill) _(rw)_ | Returns the skill last used |
| [#lSpell](#var-lspell) _(rw)_ | Returns the last spell cast |

<a id="var-lobjectid"></a>

#### LObjectID

*Read / write.* The #lObjectID system variable contains the ID of the last used object. You can also write to this variable and use it in conjuction with [event Macro](#cmd-event-macro) 17 (LastObject), which will use the object as if it was double-clicked with the mouse.

> [!NOTE]
> This variable is UO client dependent. Setting #LOBJECTID in one instance of EasyUO will affect the variable as it is seen by all other instances of EasyUO bound to that client. It is recommended to sanitize the variable by saving the existing value before overwriting it, then restoring the original value when the function is complete.

##### Example

    set #lObjectID %carpentryTool
    event macro 17
    ; crafting menu is now open
    ...

    set !_orig.lobjectid #LOBJECTID
    set #LOBJECTID %BandageID
    event macro 17
    set #LOBJECTID !_orig.lobjectid
    target 2s
    ...

<a id="var-lobjecttype"></a>

#### LObjectType

*Read-only.* The #lObjectType system variable determines the type of the last used object.

<a id="var-ltargetid"></a>

#### LTargetID

*Read / write.* The #lTargetID system variable determines the id of the last target used. You can also write to this variable and use it in conjuction with "event Macro 22" (LastTarget), which will target the object as if it was clicked with the mouse.

> [!NOTE]
> [#lTargetKind](#var-ltargetkind) must be set to 2 or 3 for event Macro 22 to use the target position.

##### Example

    ; use the dagger
    set #lObjectID %dagger
    event Macro 17

    ; wait for target cursor
    target 5s

    ; carve the hides from the corpse
    set #lTargetID %cowCorpse
    set #lTargetKind 1 ; make sure it targets an object
    event Macro 22
    ...

<a id="var-ltargetx"></a>

#### LTargetX

*Read / write.* The #lTargetX system variable determines the world x-coordinate of the last target used.

> [!NOTE]
> [#lTargetKind](#var-ltargetkind) must be set to 2 or 3 for event Macro 22 to use the target position.

##### Example

    ; use the shovel
    set #lObjectID %shovel
    event Macro 17

    ; wait for target cursor
    target 5s

    ; mine a spot
    set #lTargetX 1000
    set #lTargetY 1000
    set #lTargetZ -1
    set #lTargetKind 3
    event Macro 22
    ...

<a id="var-ltargety"></a>

#### LTargetY

*Read / write.* The #lTargetY system variable determines the world y-coordinate of the last target used.

> [!NOTE]
> [#lTargetKind](#var-ltargetkind) must be set to 2 or 3 for event Macro 22 to use the target position.

##### Example

    ; use the shovel
    set #lObjectID %shovel
    event Macro 17

    ; wait for target cursor
    target 5s

    ; mine a spot
    set #lTargetX 1000
    set #lTargetY 1000
    set #lTargetZ -1
    set #lTargetKind 3
    event Macro 22
    ...

<a id="var-ltargetz"></a>

#### LTargetZ

*Read / write.* The #lTargetZ system variable determines the world z-coordinate of the last target used.

> [!NOTE]
> [#lTargetKind](#var-ltargetkind) must be set to 2 or 3 for event Macro 22 to use the target position.

##### Example

    ; use the shovel
    set #lObjectID %shovel
    event Macro 17

    ; wait for target cursor
    target 5s

    ; mine a spot
    set #lTargetX 1000
    set #lTargetY 1000
    set #lTargetZ -1
    set #lTargetKind 3
    event Macro 22
    ...

<a id="var-ltargetkind"></a>

#### LTargetKind

*Read / write.* The #LTargetKind system variable determines the class of object that was last targeted. The possible values of this variable are listed in the table below.

| Setting | Object Class           |
|---------|------------------------|
| 1       | Object                 |
| 2       | Ground,Mountains,Caves |
| 3       | Resource: Tree,Water   |

LTargetKind Values

> [!NOTE]
> Not setting #LTargetKind (usually to 1) is by far one of the most common mistakes made when scripting. Simply put, every time that you use Event Macro 22 you must *always* make sure #LTargetKind is set properly or you will most likely have sporadic targeting problems.

##### Object Example

    ; use the dagger
    set #LObjectID %dagger
    event Macro 17

    ; wait for target cursor
    target 5s

    ; carve the hides from the corpse
    set #LTargetID %cowCorpse
    set #LTargetKind 1 ; make sure it targets an object
    event Macro 22
    ...

##### World Position Example

    ; use the shovel
    set #LObjectID %shovel
    event Macro 17

    ; wait for target cursor
    target 5s

    ; mine a spot
    set #LTargetX 1000
    set #LTargetY 1000
    set #LTargetZ -1
    set #LTargetKind 3
    event Macro 22
    ...

<a id="var-ltargettile"></a>

#### LTargetTile

*Read / write.* The #lTargetTile system variable determines the tile last targeted. The number in this variable is determined by the graphic of the tile.

<a id="var-lliftedid"></a>

#### LLiftedID

*Read-only.* The #lLiftedID system variable determines the id of the object last dragged/lifted.

##### Example

    finditem JTL
    event Drag #findID
    wait 20
    msg The ID of the item you lifted is #lLiftedID $
    halt

<a id="var-lliftedtype"></a>

#### LLiftedType

*Read-only.* The #lLiftedType system variable determines the type of the object last dragged/lifted.

##### Example

    finditem JTL
    event Drag #findID
    wait 20
    msg The type of the item you lifted is #lLiftedType $
    halt

<a id="var-lliftedkind"></a>

#### LLiftedKind

*Read-only.* The #lLiftedKind system variable determines if an object is being dragged/lifted. The possible values of this variable are included in the table below.

| Value | Description                    |
|-------|--------------------------------|
| 0     | An object is not on the cursor |
| 1     | An object is on the cursor     |

#lLiftedKind values

<a id="var-lskill"></a>

#### LSkill

*Read / write.* The #lSkill system variable determines the skill last used. You can also write to this variable and use it in conjuction with "event Macro 14" (LastSkill), which will perform the skill as if you clicked the blue diamond in the skill list.

| Skill Number | Skill name              | \+**Use Skills** |
|--------------|-------------------------|------------------|
| 1            | Anatomy                 |                  |
| 2            | Animal Lore             |                  |
| 35           | Animal Taming           |                  |
| 4            | Arms Lore               |                  |
| 6            | Begging                 |                  |
| 12           | Cartography             |                  |
| 14           | Detecting Hidden        |                  |
| 15           | Discordance             |                  |
| 16           | Evaluating Intelligence |                  |
| 19           | Forensic Evaluation     |                  |
| 21           | Hiding                  |                  |
| 23           | Inscription             |                  |
| 3            | Item Identification     |                  |
| 46           | Meditation              |                  |
| 9            | Peacemaking             |                  |
| 30           | Poisoning               |                  |
| 22           | Provocation             |                  |
| 48           | Remove Trap             |                  |
| 32           | Stealing                |                  |
| 47           | Stealth                 |                  |
| 36           | Taste Identification    |                  |
| 38           | Tracking                |                  |

<a id="var-lspell"></a>

#### LSpell

*Read / write.* The #lSpell system variable determines the last spell cast. You can also write to this variable and use it in conjuction with "event Macro 16" (LastSpell), which will cast the spell.

##### Magery

| Spell number | Spell Name              |
|--------------|-------------------------|
| 0            | Clumsy                  |
| 1            | Create Food             |
| 2            | Feeblemind              |
| 3            | Heal                    |
| 4            | Magic Arrow             |
| 5            | Night Sight             |
| 6            | Reactive Armor          |
| 7            | Weaken                  |
| 8            | Agility                 |
| 9            | Cunning                 |
| 10           | Cure                    |
| 11           | Harm                    |
| 12           | Magic Trap              |
| 13           | Magic Untrap            |
| 14           | Protection              |
| 15           | Strength                |
| 16           | Bless                   |
| 17           | Fireball                |
| 18           | Magic Lock              |
| 19           | Poison                  |
| 20           | Telekinesis             |
| 21           | Teleport                |
| 22           | Unlock                  |
| 23           | Wall Of Stone           |
| 24           | Arch Cure               |
| 25           | Arch Protection         |
| 26           | Curse                   |
| 27           | Fire Field              |
| 28           | Greater Heal            |
| 29           | Lightning               |
| 30           | Mana Drain              |
| 31           | Recall                  |
| 32           | Blade Spirits           |
| 33           | Dispel Field            |
| 34           | Incognito               |
| 35           | Magic Reflection        |
| 36           | Mind Blast              |
| 37           | Paralyze                |
| 38           | Poison Field            |
| 39           | Summon Creature         |
| 40           | Dispel                  |
| 41           | Energy Bolt             |
| 42           | Explosion               |
| 43           | Invisibility            |
| 44           | Mark                    |
| 45           | Mass Curse              |
| 46           | Paralyse Field          |
| 47           | Reveal                  |
| 48           | Chaing Lightning        |
| 49           | Energy Field            |
| 50           | Flame Strike            |
| 51           | Gate Travel             |
| 52           | Mana Vampire            |
| 53           | Mass Dispel             |
| 54           | Meteor Swarm            |
| 55           | Polymorph               |
| 56           | Earthquake              |
| 57           | Energy Vortex           |
| 58           | Resurrection            |
| 59           | Air Elemental           |
| 60           | Summon Daemon           |
| 61           | Earth Elemental         |
| 62           | Fire Elemental          |
| 63           | Water Elemental         |
| 63           | Water Elemental         |
| 101          | \[N\] Animate Dead      |
| 102          | \[N\] Blood Oath        |
| 103          | \[N\] Corpse Skin       |
| 104          | \[N\] Curse Weapon      |
| 105          | \[N\] Evil Omen         |
| 106          | \[N\] Horrific Beast    |
| 107          | \[N\] Lich Form         |
| 108          | \[N\] Mind Rot          |
| 109          | \[N\] Pain Spike        |
| 110          | \[N\] Poison Strike     |
| 111          | \[N\] Strangle          |
| 112          | \[N\] Summon Familiar   |
| 113          | \[N\] Vampiric Embrace  |
| 114          | \[N\] Vengeful Spirit   |
| 115          | \[N\] Wither            |
| 116          | \[N\] Wraith Form       |
| 201          | \[C\] Cleanse By Fire   |
| 202          | \[C\] Close Wounds      |
| 203          | \[C\] Consecrate Weapon |
| 204          | \[C\] Dispel Evil       |
| 205          | \[C\] Divine Fury       |
| 206          | \[C\] Enemy Of One      |
| 207          | \[C\] Holy Light        |
| 208          | \[C\] Noble Sacrifice   |
| 209          | \[C\] Remove Curse      |
| 210          | \[C\] Sacred Journey    |

<a id="sec-finditem"></a>

### FindItem

These system variables are set when the FindItem command is used.

| Variable | Summary |
|---|---|
| [#findID](#var-findid) _(ro)_ | Returns the id of the object returned by findItem |
| [#findType](#var-findtype) _(ro)_ | Returns the type of the object returned by findItem |
| [#findX](#var-findx) _(ro)_ | Returns the x-coordinate of the object returned by findItem |
| [#findY](#var-findy) _(ro)_ | Returns the y-coordinate of the object returned by findItem |
| [#findZ](#var-findz) _(ro)_ | Returns the z-coordinate of the object returned by findItem |
| [#findDist](#var-finddist) _(ro)_ | Returns the distance from the character to the object returned by findItem |
| [#findKind](#var-findkind) _(ro)_ | Returns the kind of the object returned by findItem |
| [#findStack](#var-findstack) _(ro)_ | Returns the number of stacked items in the object returned by findItem |
| [#findBagID](#var-findbagid) _(ro)_ | Returns the bag the object returned by findItem is contained in |
| [#findMod](#var-findmod) _(rw)_ | Returns displacement for #findX and #findY |
| [#findRep](#var-findrep) _(ro)_ | Returns the reputation of the object returned by findItem |
| [#findCol](#var-findcol) _(ro)_ | Returns the color of the object returned by findItem |
| [#findIndex](#var-findindex) _(rw)_ | Gets the values of all other findItem results without restarting the time-consuming FindItem command. |
| [#findCnt](#var-findcnt) _(ro)_ | Returns the number of objects that matches what was searched for with the findItem command |

<a id="var-findid"></a>

#### FindID

*Read-only.* The #findID system variable contains the id of the object at the current #[findIndex](#var-findindex) position. All of the find\* variables are populated by using the [findItem](#cmd-finditem) command.

##### Example

    finditem POF C_ , #BACKPACKID
    if #FINDCNT > 0
    {
     msg #FINDID is the ID of the gold in my bag. There is #FINDSTACK gold in that stack.$
    }
    halt

<a id="var-findtype"></a>

#### FindType

*Read-only.* The #findType system variable contains the type of the object returned by [findItem](#cmd-finditem).

##### Example

    finditem * C_ , #BACKPACKID
    for #FINDINDEX 1 #FINDCNT
    {
     event sysmessage Found item, the type of that item is #FINDTYPE
     wait 20
    }
    halt

<a id="var-findx"></a>

#### FindX

*Read-only.* The #findX system variable contains the x-coordinate of the object returned by [findItem](#cmd-finditem). If [#findKind](#var-findkind) equals 0, the coordinate is a screen coordinate, if [#findKind](#var-findkind) equals 1, the coordinate is a world coordinate.

##### Example

    .....
    loop:
    finditem %target
    if #CHARPOSX <> #findx || #CHARPOSY <> #findy
    {
    move #findx #findy 0 0
    goto loop
    }
    .....

<a id="var-findy"></a>

#### FindY

*Read-only.* The #findY system variable contains the y-coordinate of the object returned by [findItem](#cmd-finditem). If [#findKind](#var-findkind) equals 0, the coordinate is a screen coordinate, if [#findKind](#var-findkind) equals 1, the coordinate is a world coordinate.

##### Example

    ....
    loop:
    finditem %target
    if #CHARPOSX <> #findx || #CHARPOSY <> #findy
    {
    move #findx #findy 0 0
    goto loop
    }
    ....

<a id="var-findz"></a>

#### FindZ

*Read-only.* The #findZ system variable contains the z-coordinate of the object returned by [findItem](#cmd-finditem). If [#findKind](#var-findkind) equals 0, the coordinate is a screen coordinate, if [#findKind](#var-findkind) equals 1, the coordinate is a world coordinate.

##### Example

<a id="var-finddist"></a>

#### FindDist

*Read-only.* The #findDist system variable contains the distance from the character to the object returned by [findItem](#cmd-finditem).

##### Example

    finditem POF G_15
    if #FINDCNT > 0
    {
        display ok I found a stack of gold #FINDDIST tiles away from me
    }
    if #FINDCNT < 1
    {
        display ok No gold was found on the ground.
    }
    halt

<a id="var-findkind"></a>

#### FindKind

*Read-only.* The #findKind system variable contains the kind of the object returned by [findItem](#cmd-finditem).

| Value | Description               |
|-------|---------------------------|
| -1    | No objects found.         |
| 0     | Object is in a container. |
| 1     | Object is on the ground.  |

> [!NOTE]
> 
>
> 1.  Findkind is not the preferred method to check whether an item was found or not because it is harder for humans to debug. Please use [#FINDCNT](#var-findcnt) instead, whenever possible.

##### Example

    if #findkind = -1
    { 
    event sysmessage item not found.
    }

<a id="var-findstack"></a>

#### FindStack

*Read-only.* The #findStack system variable contains the number of stacked items in the object returned by [findItem](#cmd-finditem).

##### Example

    finditem POF C_ , #BACKPACKID
    if #FINDCNT > 0
    {
        display ok I found a stack of gold and there are #FINDSTACK gold pieces in it.
    }
    if #FINDCNT < 1
    {
        display ok No gold was found in backpack.
    }
    halt

<a id="var-findbagid"></a>

#### FindBagID

*Read-only.* The #findBagID system variable contains the bagID the object returned by [findItem](#cmd-finditem) is contained in.

##### Example

    finditem POF C
    if #FINDCNT > 0
    {
        display ok I found a stack of gold in a bag, the ID of the bag I found it in is #FINDBAGID
    }
    if #FINDCNT < 1
    {
        display ok I could not find any gold in open containers.
    }
    halt

<a id="var-findmod"></a>

#### FindMod

*Read / write.* The #findMod system variable Determines displacement for #[findX](#var-findx) and #[findY](#var-findy). The displacement is in the format {X}\_{Y} and is added to #[findX](#var-findx) and #[findY](#var-findy) respectively.

##### Example

    set #findmod 140_220 ;displacement of backpack location on paperdoll
    finditem #backpackid C_ , #charid
    event drag %something
    msg $
    wait 2s
    click #findx #findy p ; drop on paperdoll's backpack icon

<a id="var-findrep"></a>

#### FindRep

*Read-only.* The #findRep system variable contains the reputation of the object returned by [findItem](#cmd-finditem).

| Value | Description           |
|-------|-----------------------|
| 1     | Innocent (Blue)       |
| 2     | Friend (Green)        |
| 3     | Grey (Grey - Animal)  |
| 4     | Criminal (Grey)       |
| 5     | Enemy (Orange)        |
| 6     | Murderer (Red)        |
| 7     | Invulnerable (Yellow) |

##### Example

    finditem HS_IS G_10

    if #findrep = 1
       display ok The item found is (blue) Innocent

    halt

<a id="var-findcol"></a>

#### FindCol

*Read-only.* The #findCol system variable contains the color of the object returned by [findItem](#cmd-finditem).

##### Example

    finditem POF C_ , #BACKPACKID
    if #FINDCNT > 0
    {
        display ok I found a stack of gold, the color value of it is #FINDCOL
    }
    if #FINDCNT < 1
    {
        display ok No gold was found.
    }
    halt

<a id="var-findindex"></a>

#### FindIndex

*Read / write.* The #findIndex system variable get the values of all other [findItem](#cmd-finditem) results without restarting the time-consuming [findItem](#cmd-finditem) command. Its range vary from 1 to [#findcnt](#var-findcnt).

> [!NOTE]
> This command is only available from EUO 1.5.

##### Example

    finditem %TypeToIgnore C_ , #backpackid
    ignoreAgain:
    if #findIndex <= #findCnt
    {
        ignoreItem #findid
        set #findIndex #findIndex + 1
        goto ignoreAgain
    }
    halt

    ; Use a single finditem to display the properties of each item on my paperdoll. 
    ; Output is set to the journal via event sysmessage
    ; -Seg
    finditem * C_ , #CHARID
    for #FINDINDEX 1 #FINDCNT
    {
        event property #FINDID
        event sysmessage #PROPERTY
        wait 20
    }
    halt

<a id="var-findcnt"></a>

#### FindCnt

*Read-only.* The #findCnt system variable contains the number of objects that matches what was searched for with the [findItem](#cmd-finditem) command.

##### Example

    ....
    loop:
    finditem %housesign G_5
    if #findcnt < 1
    {
    gosub placement
    }
    goto loop
    ....

    finditem * C_ , #BACKPACKID
    if #FINDCNT > 0
    {
     display ok There are #FINDCNT items in your backpack!
    }
    if #FINDCNT < 1
    {
     display ok No items were found in your backpack!
    }
    halt

<a id="sec-shop"></a>

### Shop

The shop system variables allow you to work with NPC vendor gumps through the use of the getShopInfo command.

| Variable | Summary |
|---|---|
| [#shopCurPos](#var-shopcurpos) _(ro)_ | Returns the current position on the shop menu |
| [#shopCnt](#var-shopcnt) _(ro)_ | Returns the total number of lines on the shop menu |
| [#shopItemType](#var-shopitemtype) _(ro)_ | Returns the item type of the current line on the shop menu |
| [#shopItemID](#var-shopitemid) _(ro)_ | Returns the item ID of the current line on the shop menu |
| [#shopItemName](#var-shopitemname) _(ro)_ | Returns the name of the item the current line on the shop menu |
| [#shopItemPrice](#var-shopitemprice) _(ro)_ | Returns the price of the current line in the shop menu |
| [#shopItemMax](#var-shopitemmax) _(ro)_ | Returns the number of items in the stack of the current line in the shop menu |

<a id="var-shopcurpos"></a>

#### ShopCurPos

*Read-only.* The #shopCurPos system variable determines the current position on the shop menu.

<a id="var-shopcnt"></a>

#### ShopCnt

*Read-only.* The #shopCnt system variable determines the total number of lines on the shop menu.

<a id="var-shopitemtype"></a>

#### ShopItemType

*Read-only.* The #shopItemType determines the item type of the current line on the shop menu.

> [!NOTE]
> To initialize this variable, you need to call [getShopInfo](#cmd-getshopinfo).

<a id="var-shopitemid"></a>

#### ShopItemID

*Read-only.* The #shopItemID system variable determines the item ID of the current line on the shop menu.

> [!NOTE]
> To initialize this variable, you need to call [getShopInfo](#cmd-getshopinfo).

<a id="var-shopitemname"></a>

#### ShopItemName

*Read-only.* The #shopItemName system variable determines the name of the item the current line on the shop menu.

> [!NOTE]
> To initialize this variable, you need to call [getShopInfo](#cmd-getshopinfo).

<a id="var-shopitemprice"></a>

#### ShopItemPrice

*Read-only.* The #shopItemPrice system variable determines the price of the current line in the shop menu.

> [!NOTE]
> To initialize this variable, you need to call [getShopInfo](#cmd-getshopinfo).

<a id="var-shopitemmax"></a>

#### ShopItemMax

*Read-only.* The #shopItemMax system variable determines the number of items in the stack of the current line in the shop menu.

> [!NOTE]
> To initialize this variable, you need to call [getShopInfo](#cmd-getshopinfo).

<a id="sec-extended"></a>

### Extended

Extended system variables show information about various systems in the Ultima Online client that can be gained by using certain commands.

| Variable | Summary |
|---|---|
| [#skill](#var-skill) _(ro)_ | Returns the current skill level for a skill chosen with chooseSkill command |
| [#skillCap](#var-skillcap) _(ro)_ | Returns the current skill cap for a skill chosen with chooseSkill command |
| [#skillLock](#var-skilllock) _(ro)_ | Returns the current lock status of the skill chosen with chooseSkill command |
| [#journal](#var-journal) _(ro)_ | Returns the journal line selected using the scanJournal command |
| [#jIndex](#var-jindex) _(ro)_ | Returns the index of the current journal entry |
| [#jColor](#var-jcolor) _(rw)_ | Returns the color of the text in the journal |
| [#sysMsg](#var-sysmsg) _(ro)_ | Returns the current system message |
| [#sysMsgCol](#var-sysmsgcol) _(rw)_ | Returns the current system message color |
| [#targCurs](#var-targcurs) _(rw)_ | Returns if cursor is a target cursor |
| [#cursKind](#var-curskind) _(ro)_ | Returns the facet where the character is |

<a id="var-skill"></a>

#### Skill

*Read-only.* The #Skill system variable determines the current skill level for a skill chosen with [chooseSkill](#cmd-chooseskill) command.

##### Example

    chooseSkill anim
    if #skill < 1000
        event SysMessage You need to tame bulls.
    if #skill >= 1000
        event SysMessage You need to tame ridgebacks.

<a id="var-skillcap"></a>

#### SkillCap

*Read-only.* The #SkillCap system variable determines the current skill cap for a skill chosen with [chooseSkill](#cmd-chooseskill) command.

##### Example

    ....
    chooseSkill mage
    if #skill = #skillCap
        halt
    ....

<a id="var-skilllock"></a>

#### SkillLock

*Read-only.* The #skillLock system variable determines the current lock status of the skill chosen with [chooseSkill](#cmd-chooseskill) command.

| Value  | Description                  |
|--------|------------------------------|
| up     | Skill lock is pointing up.   |
| down   | Skill lock is pointing down. |
| locked | Skill lock is locked.        |

#skillLock Values

##### Example

    chooseSkill taming
    if #skillLock = locked
    {
        event SysMessage Your taming is locked. Cannot continue.
        halt
    }

<a id="var-journal"></a>

#### Journal

*Read-only.* The #journal system variable determines the journal line selected using the [scanJournal](#cmd-scanjournal) command.

##### Example

    ; example 1 (old way)

    waitForAttack:
    scanjournal 1
    if is_attacking_you in #journal
      msg guards $
    goto waitForAttack

    ; example 2 (new way) (won't skip lines like the old way will)

    set %jrnl #jindex
    while true
       {
       if #jindex > %jrnl
          {
          set %jrnl %jrnl + 1
          scanjournal %jrnl
          if is_attacking_you in #journal
             event macro 1 0 Guards
          }
       }

<a id="var-jindex"></a>

#### JIndex

*Read-only.* The #jIndex system variable determines the index of the current journal entry. By calling [scanJournal](#cmd-scanjournal) with #jIndex as the parameter you will get the last line in the journal. By saving the value of #jIndex at appropriate times you can scan a section of the journal without ever losing a string.

##### Example

    set %success #false
    ; remember the journal position before something happened
    set %jstart #jIndex + 1
    ; do something what we want to watch
    msg #smc TestA$
    msg #smc TestB$
    msg #smc TestC$
    wait 1s
    ; remember the journal position after something has happened
    set %jend #jIndex
    ; loop through the journal checking each line between %jstart and %jend
    for %ji %jstart %jend
    {
        scanJournal %ji
        if TestB in #journal
            set %success #true ; found it
        msg #smc Interference$ ; new messages don't disturb the scan
    }
    ; examine the result and act as required
    if %success = #true
        display Ok Success
    else
        display Ok Failure
    halt

    ; Here is a little snippet to explaine the usage of this variable, its scans for the
    ; phrase "your char has been inactive" and makes a party message.

    set %_jindex #jindex
    scanloop:
       if #jindex >= %_jindex
       {
          scanjournal %_jindex
          if your_char_has_been_inactive in #journal
             msg /party stay active $
          set %_jindex %_jindex + 1
       }
    wait 0
    goto scanloop

<a id="var-jcolor"></a>

#### JColor

*Read / write.* The #jColor system variable determines the color of the text in the journal.

> [!NOTE]
> This variable is readonly, it cannot be written to. But even if it could there really is no reason to since you can't change the color of text already in the journal.

<a id="var-sysmsg"></a>

#### SysMsg

*Read-only.* The #sysMsg system variable determines the current system message.

##### Example

    ...
    if something in #sysMsg
         gosub dosomething
    .....

<a id="var-sysmsgcol"></a>

#### SysMsgCol

*Read / write.* The #sysMsgCol system variable determines the current system message color.

##### Example

    set #sysmsgcol 1264
    halt

<a id="var-targcurs"></a>

#### TargCurs

*Read / write.* The #targCurs system variable determines if cursor is a target cursor. It can also be written to, to get a target cursor.

| Value | Description                |
|-------|----------------------------|
| 0     | Cursor is a normal cursor. |
| 1     | Cursor is a target cursor. |

#targCurs Values

##### Example

    event SysMessage Target something!

    set #targCurs 1
    targLoop:
    if #targCurs = 1
      goto targLoop

    event SysMessage The ID of the target is #lTargetID
    halt

<a id="var-curskind"></a>

#### CursKind

*Read-only.* The #cursKind system variable determines the facet where the character is.

| Value | Description |
|-------|-------------|
| 0     | Felucca     |
| 1     | Trammel     |
| 2     | Ilshenar    |
| 3     | Malas       |
| 4     | Tokuno      |

#cursKind Values

##### Example

    msg Hmmm I wonder where I am$
    if #cursKind = 0
         set %iamin Felucca
    if #cursKind = 1
         set %iamin Trammel
    if #cursKind = 2
         set %iamin Ilshenar
    if #cursKind = 3
         set %iamin Malas
    if #cursKind = 4
         set %iamin Tokuno
    msg Oh Ok I am in %iamin $
    halt

<a id="sec-client-variables"></a>

### Client Variables

The client variables hold information about the Ultima Online client that EasyUO is attached to.

| Variable | Summary |
|---|---|
| [#cliVer](#var-cliver) _(ro)_ | Returns the version of the client |
| [#cliCnt](#var-clicnt) _(ro)_ | Returns the number of clients currently running |
| [#cliNr](#var-clinr) _(ro)_ | Returns which client is currently active for EasyUO |
| [#cliXRes](#var-clixres) _(rw)_ | Returns the width of the gameplay window |
| [#cliYRes](#var-cliyres) _(rw)_ | Returns the height of the gameplay window |
| [#cliLeft](#var-clileft) _(rw)_ | Returns the X coordinate of the left edge of the gameplay window |
| [#cliTop](#var-clitop) _(rw)_ | Returns the Y coordinate of the top edge of the gameplay window |
| [#cliLogged](#var-clilogged) _(ro)_ | Returns if a character is logged into the game |

<a id="var-cliver"></a>

#### CliVer

*Read-only.* Contains the version of the Ultima Online client that EasyUO is attached to.

##### Example

    if #cliVer <> 4.0.0e
    {
      event SysMessage This script was developed for client 4.0.0e. Be aware of any changes.
      pause
    }

<a id="var-clicnt"></a>

#### CliCnt

*Read-only.* Contains the number of clients currently running.

##### Example

<a id="var-clinr"></a>

#### CliNr

*Read-only.* Contains which client is currently active for EasyUO.

##### Example

<a id="var-clixres"></a>

#### CliXRes

*Read / write.* The #cliXRes system variable determines the width of the gameplay window.

##### Example

    ; Make the game play window small
    set #cliXRes 100
    set #cliYRes 100
    halt

<a id="var-cliyres"></a>

#### CliYRes

*Read / write.* The #cliYRes system variable determines the height of the gameplay window.

##### Example

    ; Make the game play window small
    set #cliXRes 100
    set #cliYRes 100
    halt

<a id="var-clileft"></a>

#### CliLeft

*Read / write.* Returns the X coordinate of the left edge of the gameplay window

##### Example

    ; Move the gameplay window to the top/left corner
    set #cliLeft 0
    set #cliTop 0
    halt

<a id="var-clitop"></a>

#### CliTop

*Read / write.* Returns the Y coordinate of the top edge of the gameplay window

##### Example

    ; Move the gameplay window to the top/left corner
    set #cliLeft 0
    set #cliTop 0
    halt

<a id="var-clilogged"></a>

#### CliLogged

*Read-only.* Returns if a character is logged into the game.

| Value | Description   |
|-------|---------------|
| 0     | Not logged in |
| 1     | Logged in     |

#cliLogged Values

##### Example

    if #cliLogged = 1
       gosub login

<a id="sec-combat"></a>

### Combat

The combat system variables allow you to see and control information that deals with combat.

| Variable | Summary |
|---|---|
| [#lHandID](#var-lhandid) _(rw)_ | Returns the ID of the item to be armed in the left hand |
| [#rHandID](#var-rhandid) _(rw)_ | Returns the ID of the item to be armed in the right hand |
| [#enemyHits](#var-enemyhits) _(ro)_ | Returns the percentage of hit points left on the current enemy |
| [#enemyID](#var-enemyid) _(ro)_ | Returns the ID of the current enemy |

<a id="var-lhandid"></a>

#### LHandID

*Read / write.* The #lHandID system variable holds the ID of the item to be armed in the left hand.

> [!NOTE]
> This variable is used with [event Macro](#cmd-event-macro) in order to place an item in your characters left hand. It must be set to a valid items ID, and the item must be able to be held in the characters left hand in order to work.

##### Example

    set #lHandID %shieldID
    event macro 24 1

<a id="var-rhandid"></a>

#### RHandID

*Read / write.* The #rHandID system variable holds the ID of the item to be armed in the right hand.

> [!NOTE]
> This variable is used with [event Macro](#cmd-event-macro) in order to place an item in your characters right hand. It must be set to a valid items ID, and the item must be able to be held in the characters right hand in order to work.

##### Example

    set #rHandID %weaponID
    event macro 24 2

<a id="var-enemyhits"></a>

#### EnemyHits

*Read-only.* The #enemyHits system variable represents the percentage of hit points left on the current enemy.

> [!NOTE]
> It is only possible to see one enemy at a time using this variable. If you have more than one enemy, the variable will switch values randomly.

##### Example

    if #enemyID <> N/A
      display ok You're being attacked! The attacker has , #enemyHits , % Hits.

<a id="var-enemyid"></a>

#### EnemyID

*Read-only.* The #enemyID system variable holds the ID of the current enemy.

> [!NOTE]
> It is only possible to see one enemy at a time using this variable. If you have more than one enemy, the variable will switch ID's randomly.

##### Example

    if #enemyID <> N/A
      display ok You're being attacked! The attacker has , #enemyHits , % Hits.

<a id="sec-namespace-variables"></a>

### Namespace Variables

| Variable | Summary |
|---|---|
| [#nsName](#var-nsname) _(ro)_ | Returns the name of the currently active namespace |
| [#nsType](#var-nstype) _(ro)_ | Returns the type of the currently active namespace |

<a id="var-nsname"></a>

#### NsName

*Read-only.* Holds the name of the currently active [local](#cmd-namespace-local) or [global](#cmd-namespace-global) namespace.

> [!NOTE]
> Global namespaces are only available in EasyUO 1.5.

##### Example

    if #nsName <> test && #nsType = local
    {
      namespace push
      namespace local test
    }

<a id="var-nstype"></a>

#### NsType

*Read-only.* Holds the type of the currently active [local](#cmd-namespace-local) or [global](#cmd-namespace-global) namespace.

> [!NOTE]
> Global namespaces are only available in EasyUO 1.5.

##### Example

    if #nsName <> test && #nsType = local
    {
      namespace push
      namespace local test
    }

<a id="sec-miscellaneous-variables"></a>

### Miscellaneous Variables

These system variables are not easily categorized in any other category, and therefore are placed here.

| Variable | Summary |
|---|---|
| [#shard](#var-shard) _(ro)_ | Returns which shard you are logged into |
| [#date](#var-date) _(ro)_ | Returns the local date on your computer |
| [#time](#var-time) _(ro)_ | Returns the local time on your computer |
| [#sysTime](#var-systime) _(ro)_ | Counts the number of milliseconds since 01/Jan/1980 UTC |
| [#sCnt](#var-scnt) _(rw)_ | Timer in seconds since Windows boot |
| [#sCnt2](#var-scnt2) _(rw)_ | Timer in tenths of seconds since Windows boot |
| [#pixCol](#var-pixcol) _(ro)_ | Returns the color of the pixel last saved with savePix |
| [#cursorX](#var-cursorx) _(ro)_ | Returns the x-coordinate of the cursor |
| [#cursorY](#var-cursory) _(ro)_ | Returns the y-coordinate of the cursor |
| [#random](#var-random) _(ro)_ | Holds a random number |
| [#dispRes](#var-dispres) _(ro)_ | Returns button clicked in last call to display |
| [#lShard](#var-lshard) _(rw)_ | Set the last shard of your choice |
| [#osVer](#var-osver) _(ro)_ | Returns the OS version |
| [#euoVer](#var-euover) _(ro)_ | Returns the current EasyUO version |

<a id="var-shard"></a>

#### Shard

*Read-only.* Holds the name of the shard that the client is logged in to.

##### Example

    if Alexandria in #shard
    {
      msg this shard is great!$
    }

<a id="var-date"></a>

#### Date

*Read-only.* Represents the local date of the computer that EasyUO is running on. The format is YYMMDD, where YY is the year, MM is the month and DD is the day.

##### Example

    if #date = 031225
    {
      event SysMessage Merry christmas!
      pause
    }

<a id="var-time"></a>

#### Time

*Read-only.* Represents the local time of the computer that EasyUO is running on. The format is HHMMSS, where HH is the hour in 24 hour format, MM is the minutes and SS is the seconds.

##### Example

    if #time = 120000
    {
      event SysMessage Time for lunch!
      pause
    }

<a id="var-systime"></a>

#### SysTime

*Read-only.* Represents the time passed since 01/Jan/1980 UTC (it is timezone independant) in millisecond increments. It can be useful for timing and time calculations. it is also not affected by overflow issues or speedhack tools.

##### Example

    set %startTime #sysTime
    for %testLoop 1 1000
    {
      set %testCnt %testCnt + 1
    }
    set %endTime #sysTime - %startTime
    Display ok time elapsed in milliseconds: , #spc , %endTime
    halt

<a id="var-scnt"></a>

#### SCnt

*Read / write.* Represents the time passed in seconds since the last time that windows started.

##### Example

    set %startTime #sCnt
    for %testLoop 1 1000
    {
      set %testCnt %testCnt + 1
    }
    set %endTime %startTime - #sCnt
    Display ok time elapsed in seconds: , #spc , %endTime
    halt

<a id="var-scnt2"></a>

#### SCnt2

*Read / write.* Represents the time passed in tenths of seconds since the last time that windows started.

##### Example

    set %startTime #scnt2
    for %testLoop 1 1000
    {
      set %testCnt %testCnt + 1
    }
    set %endTime %startTime - #scnt2
    Display ok time elapsed in tenths of a second: , #spc , %endTime
    halt

<a id="var-pixcol"></a>

#### PixCol

*Read-only.* Holds the color of the last pixel saved using [savePix](#cmd-savepix). The colors returned by #pixCol are in the format $BBGGRR (where BB = hex value of blue color channel, GG = hex value of green color channel, RR = hex value of red channel). All colors rendered on the screen are created from these 3 primary colors. Each color ranges from 0 (darkest) to 255 (brightest) -- or $00 to $FF.

> [!NOTE]
> 
>
> - The client window **must** be unobscured by other windows in order for savePix and #pixColor to work.
> - #pixCol values differ slightly from computer to computer.
> - Most of the content of this page is shamelessly ripped off from a post that Cedryk made in the CC forum. Thanks for the knowledge Cedryk! --Kedrick Valorite

##### Example

    sub TestColor
    ; pass   %1   Color to Test
    ;   %2   Color to Match
    ;   %3   Channel Similarity
      set %_ct %1 
      set %_cm %2 
      set %_cs %3 
      gosub ColorChannels %_cm 
      set %_rm %r 
      set %_bm %b 
      set %_gm %g 
      gosub ColorChannels %_ct 
      set %_rd %r - %_rm abs
      set %_bd %b - %_bm abs
      set %_gd %g - %_gm abs
      set %_result ( %_rd <= %_cs ) && ( %_bd <= %_cs ) && ( %_gd <= %_cs ) 
    return %_result

<a id="var-cursorx"></a>

#### CursorX

*Read-only.* Holds the current x-coordinate screen position of the mouse cursor.

> [!NOTE]
> the cursor coordinates (#cursorX and #cursorY) are given relative to the upper left corner of the clients game play window. above and to the left of the game play window, these coordinates will be negative.

##### Example

<a id="var-cursory"></a>

#### CursorY

*Read-only.* Holds the current y-coordinate screen position of the mouse cursor.

> [!NOTE]
> The cursor coordinates (#cursorX and #cursorY) are given relative to the upper left corner of the clients game play window. above and to the left of the game play window, these coordinates will be negative.

##### Example

<a id="var-random"></a>

#### Random

*Read-only.* Holds a changing random value that ranges between 0 and 999.

##### Example

    ;make a random number between 0 and 99.
    set %a #random % 100

    ;make a random number between a range of two numbers
    ;set %random1 #random % %increments + #bottom
    ;%increments is (top# - bottom#) + 1
    ;#top is the highest number of the range
    ;#bottom is the lowest number of the range
    ;example of two random numbers between 3 and 10
    set %random1 #random % 8 + 3

<a id="var-dispres"></a>

#### DispRes

*Read-only.* Holds the value of the last message box button that was clicked.

| Value  | Button               |
|--------|----------------------|
| OK     | "Ok" was clicked     |
| CANCEL | "Cancel" was clicked |
| YES    | "Yes" was clicked    |
| NO     | "No" was clicked     |

Table of #dispRes values

##### Example

<a id="var-lshard"></a>

#### LShard

*Read / write.* Sets the last shard of your choice.

The system variable #LShard is where the unique shard number for the last shard picked is stored. This is the shard that is shown next to the globe on the shard selection page. Setting #LShard before logging in an account will make the client show the desired shard as the last shard logged in. Only exception will be when that specific shard isn't availible. [More info here](http://www.easyuo.com/forum/viewtopic.php?t=17758&highlight=lshard)

##### A compiled list of #LShard numbers and associated shard, (as of 11/30/2006)

| Shard          | #lshard |
|----------------|----------|
| Atlantic       | 0        |
| Lake Superior  | 1        |
| Pacific        | 2        |
| Great Lakes    | 3        |
| Baja           | 5        |
| Chesapeake     | 6        |
| Napa Valley    | 7        |
| Catskills      | 8        |
| Sonoma         | 9        |
| Lake Austin    | 10       |
| Siege Perilous | 12       |
| Legends        | 14       |
| Sakura         | 16       |
| Mugen          | 18       |
| Oceania        | 19       |
| Yamato         | 20       |
| Asuka          | 21       |
| Wakoku         | 22       |
| Hokuto         | 23       |
| Europa         | 24       |
| Drachenfels    | 25       |
| Formosa        | 26       |
| Izumo          | 27       |
| Arirang        | 28       |
| Balhae         | 29       |
| Minuho         | 31       |
| Test Center    | 41       |
| Origin         | 45       |

<a id="var-osver"></a>

#### OsVer

*Read-only.* Contains the version of the Operating System.

<a id="var-euover"></a>

#### EuoVer

*Read-only.* The #euoVer system variable displays the version information of the currently executing EasyUO program. The format is as follows: (MAJOR)\_(MINOR)\_(BUILD).

##### Example

    ;Checks to make sure the correct version of EUO is used for your script requirements. 
    ;#euo = 1_40_88 ,which is version 1.40 (build 0058)  58 hex = 88 dec 
    set %euoBuildRequired  $ , 58 
    set %euoVersionRequired 1_40 
    str Left #euoVer 4 
    set %euover #strRes 
    str Right #euover 2 
    set %euoBuild #strRes 
    if  %euoVer <> %euoVersionRequired || %euoBuild < %euoBuildRequired 
    { 
       display ok This program requires EUO version 1.4 (build 0058) or higher in order$ 
    + to work. Download the latest version from www.easyuo.com.$ 
       halt 
    }

<a id="sec-result"></a>

### Result

Result variables hold values that are the direct by-product of actions taken by commands in a script. The exact details of what they contain is determined by the command and variable.

| Variable | Summary |
|---|---|
| [#menuButton](#var-menubutton) _(rw)_ | Returns the name of the last clicked menu Button |
| [#menuRes](#var-menures) _(ro)_ | Returns the result of the last menu Get or menu GetNum command |
| [#sendHeader](#var-sendheader) _(rw)_ | Holds HTTP header information for the send command |
| [#strRes](#var-strres) _(rw)_ | Returns the result of the last str command |
| [#property](#var-property) _(ro)_ | Returns the result of the last event Property command |
| [#result](#var-result) _(rw)_ | Returns the result of the last return command |
| [#opts](#var-opts) _(ro)_ | Determines which EasyUO configuration options are active |
| [#lpc](#var-lpc) _(rw)_ | Determines the number of lines that are executed per cycle |

<a id="var-menubutton"></a>

#### MenuButton

*Read / write.* Holds the name of the last menu button pressed.

If you close the menu window, the #menuButton value is set to "Close". The minimize and maximize buttons do not set the #menuButton variable, however.

> [!NOTE]
> You should set #menuButton to a meaningless value when you have read which button was clicked in order to distinguish between two seperate clicks

##### Example

    menu Window Size 200 200
    menu Window Title Test
    menu Button button_1 10 20 50 25 Click me!
    menu Button button_2 10 50 50 25 Click me!
    menu Button button_3 10 80 50 25 Click me!
    menu Show

    set #menuButton Nothing
    lookButton:
    if #menuButton <> Nothing
    {
      display ok #menuButton , #spc , was pressed
      set #menuButton Nothing
    }
    goto lookButton

<a id="var-menures"></a>

#### MenuRes

*Read-only.* Holds the value from the last [menu Get](#cmd-menu-get) or [Menu GetNum](#cmd-menu-getnum) statement executed.

##### Example

    menu Clear
    menu Window Title Example
    menu Window Color BtnFace
    menu Window Size 117 95
    menu Font Transparent #true
    menu Font Align Right
    menu Font Name Default
    menu Font Size 8
    menu Font Style 
    menu Font Color Black
    menu Font Align Left
    menu Check CheckBox1 8 8 97 17 #false Check Box 1 ;<-- CheckBox not ticked = #False
    menu Check CheckBox2 8 32 97 17 #true Check Box 2 ;<-- CheckBox ticked = #True
    menu Font Name MS Sans Serif
    menu Font Color WindowText
    menu Button OKButton 40 64 35 25 OK
    menu Show 421 270

    MenuLoop:
    Wait 1

    If #MenuButton <> OKButton ;<-- Check to see if OK button has been pressed.
        Goto MenuLoop

    Menu Get CheckBox1 ;<-- Gets the value from CheckBox1 menu item
    If #MenuRes = #True ;<-- If #MenuRes is true the checkbox has been ticked
        Set %CheckBox1 #True
    Else
        Set %CheckBox1 #False

    Menu Get CheckBox2
    If #MenuRes = #True
        Set %CheckBox2 #True
    Else
        Set %CheckBox2 #False

    Halt

<a id="var-sendheader"></a>

#### SendHeader

*Read / write.* The system variable #sendHeader is a variable that lets you add additional header lines to the post request sent by the send command. Each line must be finished with a $ to mark the end.

    set #sendheader content-type: , #spc , blabla$line2: , #spc , blabla2$

- If #sendheader doesn't contain any $ signs at all then no additional lines will be added to the header. Setting #sendheader to $$$ will obviously mess up the outgoing packet so that is not recommended.

- First let's look at EUO default format for http requests:

    ; test1
    send debugHTTPPost localhost /euo/action.php?getVar=getValue postVar=postValue
    halt

- Outgoing HTTP request:

    POST /euo/action.php?getvar=getvalue HTTP/1.0 Host: localhost Content-Length: 17 postVar=postValue

- Supposing you want your HTTP request to be identifiied as issued by EasyUO by adding the directive "User-Agent: EasyUO #cliVer" to the HTTP header:

    ; test2
    set #sendHeader User-Agent: , #spc , EasyUO , #spc , #cliVer , $
    send debugHTTPPost localhost /euo/action.php?getVar=getValue postVar=postValue
    halt

- Outgoing HTTP request:

    POST /euo/action.php?getvar=getvalue HTTP/1.0 Host: localhost Content-Length: 17 user-agent: easyuo 4.0.0e postVar=postValue

- If you need to specify more than one http directive, you may use the following syntax:

    set #sendHeader User-Agent: , #spc , EasyUO , #spc , #cliVer , $ ,
    + Content-type: , #spc , application/x-www-form-urlencoded$

  
or

    set #sendHeader User-Agent: , #spc , EasyUO , #spc , #cliVer , $
    set #sendHeader #sendHeader , Content-type: , #spc , application/x-www-form-urlencoded$

- In order to reset #sendHeader, try any of these:

    set #sendHeader N/A
    set #sendHeader invalid content

> [!NOTE]
> 
>
> - Two consecutive '$' will break the header structure and are likely to cause inpredictable results!
> - You cannot SET a value containing spaces to #sendHeader without 'escaping' them using the #spc constant.
> - The value of #sendHeader is converted to lowercase when added to the HTTP header.
> - It must be terminated by a single end-of-line symbol '$'. Without this symbol, #sendHeader value will be ignored and not added to the HTTP header.

###### Example

    set #sendHeader Content-type: , #spc , application/x-www-form-urlencoded$

##### Send cookie

    set #sendheader Cookie:Var1=Val1 , #smc , Var2=Val2 $

    Example ( send cookie for php session ):
    set #sendheader Cookie: , #spc , PHPSESSID= , %sessionid , #smc , #spc , path=/ $

##### HTTP POST

    set %USERID_POST userid= , %username
    set %PASSWD_POST passwd= , %password

    set #sendheader Content-Type: , #spc , application/x-www-form-urlencoded , $  ;without headers, no post data
    send DebugHTTPPost localhost /login.php !USERID_POST , & , !PASSWD_POST

<a id="var-strres"></a>

#### StrRes

*Read / write.* Holds the value from the last [Str (command)](#cmd-str-command) statement executed.

##### Example

    finditem *
    if #FINDCNT > 0
    {
      event Property #findID
      str len #property
      display ok the length if the string in the property variable is , #spc , #strRes
    }
    halt

<a id="var-property"></a>

#### Property

*Read-only.* Holds the value from the last [event Property](#cmd-event-property) statement executed. Each line from a context menu in the client is delimited with a $ character, with denotes "new line". For example, a runebook will show up in game as:`

Runebook

Blessed

`in the #property variable, this would look like: RUNEBOOK$BLESSED

##### Example

    finditem *
    if #FINDCNT > 0
    {
      event Property #findID
      display ok #property
    }
    halt

<a id="var-result"></a>

#### Result

*Read / write.* holds the value from the last [return](#cmd-return) statement executed.

##### Example

    gosub xor 1875 618 
    display #result 
    halt 
     
    sub xor
    { 
      return %1 && ! %2 || ! %1 && %2 
    }

**Related:** [Return](#cmd-return)

<a id="var-opts"></a>

#### Opts

*Read-only.* The #opts system variable displays which EasyUO configuration options are active.

| Value | Option            |
|-------|-------------------|
| SOT   | Stay On Top       |
| SYS   | event SysMessage  |
| DMC   | Don't Move Cursor |
| EXEC  | Allow Execute     |
| SEND  | Allow Send        |

Table of #opt values

##### Example

    if DMC notin #opts 
    { 
        display ok This script requires "Don't move cursor" enabled!$ 
    +Enable this option in the EasyUO Tools menu and restart the script.$ 
        halt 
    }

<a id="var-lpc"></a>

#### Lpc

*Read / write.* References the current setting for [linesPerCycle](#cmd-linespercycle), which determines how many lines are processed during each cycle that EasyUO is operating. One cycle is 1/20th of a second.

##### Example

    set #lpc 10
    set %beginTimeNormal #sysTime
    for %test 1 1000
    {
      set %speedTest %speedTest + 1
    }
    set %endTimeNormal #sysTime - %beginTimeNormal

    set #lpc 250
    set %beginTimeFast #sysTime
    for %test 1 1000
    {
      set %speedTest %speedTest + 1
    }
    set %endTimeFast #sysTime - %beginTimeFast
    display ok at normal LPC the time was , #spc , %endTimeNormal , $At a fast LPC the time was , #spc , %endTimeFast

<a id="sec-tile"></a>

### Tile

These system variables contain data gathered using the tile command.

| Variable | Summary |
|---|---|
| [#tileType](#var-tiletype) _(ro)_ | Returns the type of the last read tile |
| [#tileZ](#var-tilez) _(ro)_ | Returns the z-coordinate of the last read tile |
| [#tileCnt](#var-tilecnt) _(ro)_ | Returns the number of tile layers of the last read position |
| [#tileName](#var-tilename) _(ro)_ | Returns the name of the last read tile |
| [#tileFlags](#var-tileflags) _(ro)_ | Returns the flags of the last read tile |

<a id="var-tiletype"></a>

#### TileType

*Read-only.* The #tileType system variable shows the numeric value of the last tile read using the [tile](#cmd-tile) command.

Each tile graphic in the map files has a unique identifier, which is represented in EasyUO with the #tileType value.

##### Example

    Tile init

    Tile cnt #charPosX #charPosY #cursKind
    tile Get #charPosX #charPosY #tileCnt #cursKind
    display ok The tileType value of the tile at X: , #charPosX , #spc , / Y: , #charPosY , #spc , is: , #spc , #tileType $
    +Remember: There are #tileCnt layers and the informations given are for the topmost layer
    halt

<a id="var-tilez"></a>

#### TileZ

*Read-only.* The #tileZ system variable determines the z-coordinate for the last tile read using the [tile](#cmd-tile) command.

##### Example

    tile init

    Tile cnt #charPosX #charPosY #cursKind
    display ok The Z value of the tile at X: , #charPosX , #spc , / Y: , #charPosY , #spc , is: , #tileZ
    halt

<a id="var-tilecnt"></a>

#### TileCnt

*Read-only.* The #tileCnt system variable determines the number of layers for the last tile read using the [tile](#cmd-tile) command.

To understand the tile system think of each tile as a stack of layers, each layer shows something visible in UO whether it be a tree, mountain, grass, or water. So to search these layers you must first count the number of layers in a tile.

##### Example

    Tile init

    Tile cnt #charPosX #charPosY #cursKind
    set %layer_ammount 0
    set %text
    for %cnt #tileCnt 1
        {
        tile Get #charPosX #charPosY %cnt #cursKind
        set %layer_ammount %layer_ammount + 1
        set %text %text , $Layer , #spc , %cnt , : , #spc , #tiletype
        }
    set %text [You , #spc , are , #spc , standing , #spc , here] , %text , $[The , #spc , very , #spc , bootom , #spc , of , #spc , the , #spc , world]
    display ok The layers at your positions look like the following:$ %text
    halt

<a id="var-tilename"></a>

#### TileName

*Read-only.* The #tileName system variable determines the name for the last tile read using the [tile](#cmd-tile) command.

There are over 3000 values for tile names. Some of the more usefull names include Water, Rock, Cave_Floor, Cave_Wall, and variations that include the word Tree (for example "Ohii_Tree").

##### Example

    tile init

    Tile get #charPosX #charPosY 1
    display ok The tile at X: , #charPosX , #spc , / Y: , #charPosY , #spc , has the following Name:$ , #tileName
    halt

<a id="var-tileflags"></a>

#### TileFlags

*Read-only.* The #tileFlags system variable determines the flags for the last tile read using the [tile](#cmd-tile) command.

Possible values include those listed in the table below.

| Background | Weapon     | Transparent | Translucent      |
|------------|------------|-------------|------------------|
| Wall       | Damaging   | Impassable  | Wet              |
| Unknown    | Surface    | Bridge      | GenericStackable |
| Window     | NoShoot    | PrefixA     | PrefixAn         |
| Internal   | Foliage    | PartialHue  | Unknown1         |
| Map        | Container  | Wearable    | LightSource      |
| Animated   | NoDiagonal | Unknown2    | Armor            |
| Roof       | Door       | StairBack   | StairRight       |

Tile Flag Values

##### Example

    tile init

    Tile get #charPosX #charPosY 1
    display ok The tile at X: , #charPosX , #spc , / Y: , #charPosY , #spc , has the following Flags:$ , #tileFlags
    halt

<a id="sec-constant"></a>

### Constant

Constant system variables represent characters that are used as tokens within the EasyUO language itself, or characters that would not normally be parsed properly by EasyUO.

| Variable | Summary |
|---|---|
| [#dot](#var-dot) _(ro)_ | A constant that represents the dot character |
| [#false](#var-false) _(ro)_ | A constant that represents boolean false |
| [#smc](#var-smc) _(ro)_ | A constant that represents the semicolon character |
| [#spc](#var-spc) _(ro)_ | A constant that represents the space character |
| [#true](#var-true) _(ro)_ | A constant that represents boolean true |

<a id="var-dot"></a>

#### Dot

*Read-only.* A constant that represents a dot character.

The constant `#dot` is used to assign or compare a variable or an expression with the dot character.

This is required because the dot character is used as an operator.

##### Example

    display ok This is the proper way to use dot:$ 125 , #dot , 25

<a id="var-false"></a>

#### False

*Read-only.* A constant that represents boolean false.

The constant `#false` is used to assign or compare a variable or an expression with the boolean *false* value.

Internally, `#false` is represented by the integer value 0.

##### Example

    if #false
      display ok This will never be displayed
    if #true
      display ok This will always be displayed

**Related:** [True](#var-true)

<a id="var-smc"></a>

#### Smc

*Read-only.* A constant that represents *semi-colon* character.

The constant `#smc` is used to assign or compare a variable or an expression with the *semi-colon* character.

This is required because the semi-colon character ';' is used for inline comments.

##### Example

    set %charInfo #charName , #smc , #charGhost
    menu window size 100 100
    menu window title %charInfo
    menu show

<a id="var-spc"></a>

#### Spc

*Read-only.* A constant that represents *space* character.

The constant `#spc` is used to assign or compare a variable or an expression with the *space* character.

This is required to be used in variables that contain strings which have embedded spaces. EasyUO uses whitespace (spaces, tabs, newlines) as delimiters, therefore you cannot include spaces in strings with the [set](#cmd-set) command.

##### Example

    set %testMessage hello , #spc , world
    msg %testMessage , $

<a id="var-true"></a>

#### True

*Read-only.* A constant that represents boolean true.

The constant `#true` is used to assign or compare a variable or an expression with the boolean *true* value.

Internally, `#true` is represented by the integer value -1.

##### Example

    if #false
      display ok This will never be displayed
    if #true
      display ok This will always be displayed

**Related:** [False](#var-false)

<a id="sec-appendices"></a>

## Appendices

<a id="apx-item-database"></a>

### Item Database

<table>
<tr><th>Container/Gump Name</th><th>#ContName</th><th>#ContType</th><th>#ContSize</th></tr>
<tr><td>Login Screen</td><td>MainMenu_gump</td><td>KZTB</td><td>640_480</td></tr>
<tr><td rowspan="10">Possibly place pictures here</td><td colspan="3">Logon Screen Buttons</td></tr>
<tr><td>Quit</td><td>57</td><td>23</td></tr>
<tr><td>My UO</td><td>43</td><td>175</td></tr>
<tr><td>Account</td><td>43</td><td>229</td></tr>
<tr><td>Movie</td><td>43</td><td>317</td></tr>
<tr><td>Credits</td><td>43</td><td>340</td></tr>
<tr><td>Help</td><td>43</td><td>368</td></tr>
<tr><td>Account Name</td><td>529</td><td>359</td></tr>
<tr><td>Password</td><td>529</td><td>398</td></tr>
<tr><td>Green Arrow</td><td>617</td><td>456</td></tr>
<tr><td colspan="4"></td></tr>
<tr><td>Shard Selection Screen</td><td>Normal_gump</td><td>QQL</td><td>640_480</td></tr>
<tr><td rowspan="12">Possibly place pictures here</td><td colspan="3">Shard Selection Buttons</td></tr>
<tr><td>Quit</td><td>57</td><td>23</td></tr>
<tr><td>My UO</td><td>43</td><td>175</td></tr>
<tr><td>Account</td><td>43</td><td>229</td></tr>
<tr><td>Credits</td><td>43</td><td>340</td></tr>
<tr><td>Help</td><td>43</td><td>368</td></tr>
<tr><td>Timezone</td><td>271</td><td>377</td></tr>
<tr><td>%Full</td><td>376</td><td>377</td></tr>
<tr><td>Connection</td><td>484</td><td>377</td></tr>
<tr><td>World</td><td>187</td><td>431</td></tr>
<tr><td>Red Arrow</td><td>596</td><td>455</td></tr>
<tr><td>Green Arrow</td><td>619</td><td>455</td></tr>
<tr><td colspan="4"></td></tr>
<tr><td>Character Selection Screen</td><td>Login_gump</td><td>STFD</td><td>640_480</td></tr>
<tr><td rowspan="16">Possibly place pictures here</td><td colspan="3">Character Selection Buttons</td></tr>
<tr><td>Quit</td><td>57</td><td>23</td></tr>
<tr><td>My UO</td><td>43</td><td>175</td></tr>
<tr><td>Account</td><td>43</td><td>229</td></tr>
<tr><td>Credits</td><td>43</td><td>340</td></tr>
<tr><td>Help</td><td>43</td><td>368</td></tr>
<tr><td>Red Arrow</td><td>596</td><td>455</td></tr>
<tr><td>Green Arrow</td><td>619</td><td>455</td></tr>
<tr><td>New</td><td>254</td><td>408</td></tr>
<tr><td>Delete</td><td>471</td><td>408</td></tr>
<tr><td>Character 1</td><td>355</td><td>160</td></tr>
<tr><td>Character 2</td><td>355</td><td>200</td></tr>
<tr><td>Character 3</td><td>355</td><td>240</td></tr>
<tr><td>Character 4</td><td>355</td><td>280</td></tr>
<tr><td>Character 5</td><td>355</td><td>220</td></tr>
<tr><td>Character 6</td><td>355</td><td>360</td></tr>
<tr><td colspan="4"></td></tr>
<tr><td>Paper Doll Gump</td><td>Paperdoll_gump</td><td>KX</td><td>262_324</td></tr>
<tr><td rowspan="15">Possibly place pictures here</td><td colspan="3">Paperdoll Buttons</td></tr>
<tr><td>Virtue</td><td>95</td><td>19</td></tr>
<tr><td>Help</td><td>216</td><td>55</td></tr>
<tr><td>Options</td><td>216</td><td>83</td></tr>
<tr><td>Log Out</td><td>216</td><td>109</td></tr>
<tr><td>Journal</td><td>216</td><td>134</td></tr>
<tr><td>Skills</td><td>216</td><td>160</td></tr>
<tr><td>Guild</td><td>216</td><td>190</td></tr>
<tr><td>Peace/War</td><td>216</td><td>216</td></tr>
<tr><td>Status</td><td>216</td><td>239</td></tr>
<tr><td>Minimize</td><td>233</td><td>269</td></tr>
<tr><td>Chivalry Book</td><td>163</td><td>221</td></tr>
<tr><td>Backpack</td><td>139</td><td>218</td></tr>
<tr><td>Party Manifest</td><td>45</td><td>223</td></tr>
<tr><td>Character Profile</td><td>32</td><td>223</td></tr>
<tr><td colspan="4"></td></tr>
<tr><td>Party Manifest Gump</td><td>PartyGump</td><td>CBRD</td><td>543_480</td></tr>
<tr><td rowspan="26">Possibly place pictures here</td><td colspan="3">Party Manifest Buttons</td></tr>
<tr><td>Tell Button 1</td><td>47</td><td>60</td></tr>
<tr><td>Kick Button 1</td><td>92</td><td>60</td></tr>
<tr><td>Tell Button 2</td><td>47</td><td>86</td></tr>
<tr><td>Kick Button 2</td><td>92</td><td>86</td></tr>
<tr><td>Tell Button 3</td><td>47</td><td>111</td></tr>
<tr><td>Kick Button 3</td><td>92</td><td>111</td></tr>
<tr><td>Tell Button 4</td><td>47</td><td>132</td></tr>
<tr><td>Kick Button 4</td><td>92</td><td>132</td></tr>
<tr><td>Tell Button 5</td><td>47</td><td>161</td></tr>
<tr><td>Kick Button 5</td><td>92</td><td>161</td></tr>
<tr><td>Tell Button 6</td><td>47</td><td>186</td></tr>
<tr><td>Kick Button 6</td><td>92</td><td>186</td></tr>
<tr><td>Tell Button 7</td><td>47</td><td>210</td></tr>
<tr><td>Kick Button 7</td><td>92</td><td>210</td></tr>
<tr><td>Tell Button 8</td><td>47</td><td>232</td></tr>
<tr><td>Kick Button 8</td><td>92</td><td>232</td></tr>
<tr><td>Tell Button 9</td><td>47</td><td>260</td></tr>
<tr><td>Kick Button 9</td><td>92</td><td>260</td></tr>
<tr><td>Tell Button 10</td><td>47</td><td>286</td></tr>
<tr><td>Kick Button 10</td><td>92</td><td>286</td></tr>
<tr><td>Send Party Message</td><td>82</td><td>321</td></tr>
<tr><td>Party Can Loot</td><td>82</td><td>345</td></tr>
<tr><td>Disband Party</td><td>82</td><td>370</td></tr>
<tr><td>Add New Member</td><td>82</td><td>395</td></tr>
<tr><td>Okay</td><td>217</td><td>432</td></tr>
</table>

<a id="apx-qg-true-false"></a>

### QG True False

#### Quick Guide: #True & #False

**Author: Una**

**Purpose**

To teach you the idea of #true and #false and how to use em in scripts

#### #True and #False

##### How to use em and why

Boolean #true and #false are like ON / OFF variables. If something is ON, Positive, running or it has happened, its #True. If something is OFF, negative or has not yet happened its #False.

    set %UseMagery yes

    if %UseMagery = yes
       Use Spell Mini heal

    if %UseMagery = no
       Heal with bandages

Most of beginners do it this way. Theres nothing really wrong, its just harder way. If you do it this way, you dont have to type so much and it looks better.

    set %UseMagery #true

    if %UseMagery
       Use Spell Mini Heal

    if ! %UseMagery
       Heal with bandages

This may look confusing at start, but further look, will make it all clear. Lets take a closer look at those lines:

    if %UseMagery

This will check, if %UseMagery is #true. If it is, then "if" sentence gets executed.

    if ! %UseMagery

This is same, but it will turn things upside down. It will check if its UNtrue. So if this is #false, it gets executed Using #true and #false makes your script look better and easyer to understand. If you can, use these.

This was all for Booleans today. Hope you got something from this Quickye!

<hr>

Back to Tutorials

<a id="apx-tutorialscheffe1"></a>

### Tutorials:Cheffe1

The question about execution speeds of different EasyUO commands like...

"Is GOTO faster than GOSUB?"

...has come up a couple of times so I thought I'd write an extended answer in form of a tutorial for this.

I've found an old post of mine that I will quote here:

> EUOhas 20 cycles per second and in each cycle it executes 10 lines of the script (default). Some commands have built in waits so that the script speed slows down considerably.

> You can't say that one command is faster than the other. EUO gives away most of the available processing time so that the UO client and other Windows applications can have it.

> EUO doesn't know the difference between a processing intensive task such as "FINDITEM \*" at WBB or a simple "SET %X 3". While 10 lines per cycle is already too fast if you have 10 FINDITEMs in a row, you could execute hundreds of SET instructions in the same time without causing the CPU any stress.

> I'm working on a concept that'll automatically estimate the needed processing time for each command and speed up execution for commands that need virtually no time at all (so that you can execute more of those per cycle).

> You can already do that now using LINESPERCYCLE or #LPC. If you use this command wisely you can speed up execution speed in parts of the script where a lot of time is wasted and slow down execution in parts that are more difficult for the CPU.

So, to sum that up:

1\. EUO executes a fixed amount of lines per cycle (10 per default).

2\. It doesn't matter if these lines are comments, GOTOs or GOSUBs because the script will always sleep for 50ms between the cycles (resulting in ~20 cycles per second in which each cycle processes 10 lines causing a total of 200 lines to be executed per second).

Therefore, if you want to speed up your scripts, you have two options:

1\. Removing lines (e.g. comments) from the script so that it runs faster even with a low #lpc value. This is the dumb solution because it only treats the symptoms.

2\. Setting #lpc to a higher value for parts of the script that can be executed really fast and lowering it for commands that execute processing intensive tasks. This is the preferred solution.

Because EUO is currently unable to guess which commands really consume a lot of CPU time and which not, it automatically yields the CPU after a fixed amount of lines. If you want to help EUO then you should set #lpc to an appropriate value in all parts of the script.

Let's take a look at how EUO works internally:

    Start:
        read (#lpc) number of lines
        execute these lines
        sleep for 50ms
    goto Start

While the script sleeps for 50ms, other applications and even the EasyUO main window can use the CPU. If that sleep period were somehow removed then the following would happen:

1\. EUO consumes 100% CPU time 2. The EUO application window freezes up 3. Other processes with equal or lower priority are affected by lag.

Why would you want to remove that 50ms sleeping period then? Only if you REALLY want to know how fast the different commands are.

How come? Because the usual execution looks like this:

    SET command:
    0.1ms execution for 10 lines of SET
    50ms sleeping period

    FINDITEM command:
    5ms execution for 10 lines of FINDITEM
    50ms sleeping period

As you can see, in the first case we get a total of 50.1ms and in the second case 55ms. In order to find out how much slower FINDITEM is you could simply subtract 50ms from both results and then compare again. But there's the problem that those 50ms for the sleeping period are not too accurate (depends on the OS).

And because very small time spans are difficult to measure, you usually want to use not only a single instruction in your tests but thousands of it to get accurate values. To get 1 second of SET execution time, you'd end up with ~500 seconds of sleeping time ballast. That can't be the solution, can it?

By the way, the model presented above also explains why you may not always get 200 lines executed per second even if #LPC is 10. You only have 20 cycles per second if the execution of the commands takes virtually no time at all. In our example, FINDITEM uses up 5ms resulting in a total cycle time of 55ms which is 18.1 cycles per second. But that small asymmetric behavior isn't really important, just interesting to know.

So, if you really want to know how fast the different commands are in relation to each other, then you must somehow overcome that 50ms sleep period because it's messing with the results.

To do this, set #LPC to an extremely high value like 100000000. This will cause EasyUO to use 100% processing time and the sleeping period will never be reached (unless you want to wait a year or so).

As mentioned before, this will also freeze up the main window but the script will be running at the maximum speed your CPU can provide.

Now that sounds like a better way to get good results, right? Just be sure to HALT your script after executing those 100'000 SET instructions or you'll have an endless loop and must kill the EasyUO process.

Here's a script that measures how fast comments can be executed:

    set #lpc 1000000000
    for %cnt 1 10000
    {
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    ;this is a test, this is a test, this is a test, this is a test
    }
    halt

This script executes 1 million comment lines and 10,000 jumps (because of the FOR instruction). On my 2GHz Intel Centrino, that takes 18 seconds with EUO1.42 and 5 seconds with EUO1.5. Not exactly slow, is it?

Now I could do the same with 100,000 SET instructions or 10,000 FINDITEM instructions and do some basic math to get the execution speeds of all commands in relation to each other. Don't forget that some commands like KEY, CLICK, TARGET and WAIT have built-in waits that makes any execution speed tests pointless.

By the way, when I implement the dynamic LinesPerCycle system for EUO1.5, I will use the exact same method as described above to get average execution speed values for all commands. According to the results, I will give points to each command. When the parser executes your script, it will not pay any attention to the number of lines but the sum of the points of all executed commands to estimate when it is right to yield the CPU again and go into slumber for another 50ms.

The optimal maximum sum of points depends on your CPU and the amount of CPU time (in percent) you want to give to EUO. For that value, I might make a constant that can be set by the user and whose default value is determined at the first startup.

I hope I could give you some insight into EasyUO's inner workings and prove that it really depends on the script authors how fast their scripts run (at least until that dynamic LPC system works) and that you shouldn't remove all comments and GOSUBs in your scripts simply because of execution speed considerations.

Tutorials

<a id="apx-how-stat-and-skill-gains-work-on-runuo-freeshards"></a>

### How stat and skill gains work on RunUO freeshards

Originally written by Roadkill here: <http://www.easyuo.com/forum/viewtopic.php?t=15601>. This is pretty much a straight copy of his post, I simply cleaned up a little bit of the first half is all. Most of the "clean up" was actually just formatting, so all the content is still Roadkill's. Hopefully he'll come and check this out and edit it some more to his personal taste.

The internal mechanics of skill and stat gains on RunUO freeshards are available to anyone that knows how to read C# code. Roadkill has made the point that for most players, by the time you move to play on a freeshard, the primary enjoyment from playing Ultima Online does not come from trying to gain skills. If that is true, knowing the internal mechanics of how skill and stat gains are made on RunUO is of primary concern.

The points in the list below are central facts of the skill gain system on RunUO:

**Stat Gains:**

- There is no 8x8 on RunUO shards.

Whatever the code/algorithm on EA/OSI that exhibits the symptoms of a line of "gain spots" in 8 x 8 tile area, it doesn't exist on RunUO. This means that players can gain much faster by just going slow forward on a boat, or walking around on land. Any movement to "find the gainline" or "recapture the line", one forwarding, one back, etc., is all wasted time.

- There is anti-macro code in RunUO.

The same skills that are affected by the anti-macro code on OSI are affected on RunUO. However, the details of how the RunUO anti-macro code works are different that OSI's anti-macro code in the following ways:

- as on OSI, the anti-macro code operates as either target-based, or movement based. for target based skills, each unique object is considered to be one target.
- For movement based skills, RunUO divides the map into 5x5 areas which means that you do not have to move as much as on OSI. These area's are not based on your character's position in the world, but instead are layed out from the 0,0 tile on each map.
- For target and movement based anti-macro, you can gain on one target or one 5x5 area up to three times.
- All of each character's gains are tracked for five minute periods of time. This means that three gains on one area, where the gains occur within 5 minutes of the first gain, are all that is allowed. after 5 minutes passes for the first gain, the second gain is used to track the five minute period.
- if the character has less than 10 skill points in the skill being gained, the anti-macro code is not checked.
- the anti-macro code does not apply to pets at all.

**Skill gains:**

- The "skillgain" calculation to determine whether you gain while attempting the skill is pretty complex. With less than 10 points in the skill being checked, if you do gain you get a random increase from .1 to .4. With greater than 10 skill points in the skill being checked, it's always a .1 increase.

There are THREE weighted elements that are checked to determine if you gain, and your ability to optimize all three will GREATLY increase your gain rate. Here they are: a. 50%, "success factor": Each skill attempt on an object or action will have three skill levels associated with it. YOUR skill, the minimum skill for the object to gain from it, and the maximum skill that object can gain at. For example, a tinkered locked box may have a minskill of 50 lockpicking and a maxskill of 75. If YOUR lockpicking is \< 50 it's too hard--no gain; if your skill is \> 75, no gain--you must be between the two. Now, the closer you are to the MINSKILL, the more weight this is--it approaches zero as you approach the max skill. However, if you SUCCEED you get .5 of this, but if you fail, you get .2. Thus, you want to be working on objects where you are WELL AWAY from the MAXSKILL of that object! This factor is weighted 50% of the total, and if it's almost zero because you are doing things almost too easy for you, ...suxx.

b\. 25%, "Total Skills" factor: (Totalskillcap - TotalSkills ) / totalskillcap This means that if you have 700 skill cap and you're at 697 trying to gain, you'll get almos ZERO! But if you are at 400 skills you get .5 chance to gain from this alone! Therefore, DONT GET TO SKILLCAP! The LOWER your total skills are the more chance you have to gain! Therefore, gain your HARDEST and most EXPENSIVE skills first! Magery should be done FIRST, not last "when you have $$",or it costs 4 times as much. Use some non-resource using skill like anat or spirit speak etc. for the final "top off".

c\. 25% "base skill" factor: (Specific Skill Cap - base skill ) / skillcap This obvioiusly approaches zero as your baseskill reaches it's cap, so this factor is SQUAT if you are at 99.8 and your cap is 100! You LOSE 25% of your gain chance BAM. Instead, ALWAYS increase your skill cap if able with a POWER SCROLL, EVEN IF YOU DON"T INTEND ON BOOSTING THE SKILL!! A 120ps in magery when you are at 99.7 magery or so, say, will let this be 20/120 = 17% gain chance boost!! HUGE increase.

In summary: 1. LOCK YOUR SKILLS except for your gainers, DONT hit skillcap, train most expensive/hardest skills FIRST 2. EAT a Power Scroll if at ALL possible, even if you're going to 100! 3. Always train WELL BELOW the maxskill for an item, but enough you succeed about 20-40%. As soon as you can jump up to the next "thing" or level for skill training, do so if you're near the max with the old. Example, Don't train taming on horses at 60, move up to bears, kinda thing. 4. Just slow forward instead of 8x8. At higher levels, you're probably NOT gaining .3/5min, so you could just sit dead still conceivably...

Good luck, enjoy
