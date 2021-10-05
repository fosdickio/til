# Java Tools

## JDK Environment

After you install Java, the core `java` runtime command may appear in your path (available to run) automatically. However, many of the other commands provided with the JDK may not be available unless you add the Java `bin` directory to your execution path. The following commands show how to do this on Linux, macOS, and Windows. You will, of course, have to change the path to match the version of Java you have installed.

```shell
# Linux
export JAVA_HOME=/usr/lib/jvm/java-12-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

# Mac OS X
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-12.jdk/Contents/Home
export PATH=$PATH:$JAVA_HOME/bin

# Windows
set JAVA_HOME=c:\Program Files\Java\jdk12
set PATH=%PATH%;%JAVA_HOME%\bin
```

## System Properties

Although it is possible to read host environment variables from Java, it is discouraged for application configuration. Instead, Java allows any number of _system property_ values to be passed to the application when the VM is started. System properties are simply name-value string pairs that are available to the application through the static `System.getProperty()` method. You can use these properties as a more structured and portable alternative to command-line arguments and environment variables for providing general configuration information to your application at startup. Each system property is passed to the interpreter on the command line using the `-D` option followed by `name=value`.

```shell
java -Dstreet=sesame -Dscene=alley animals.birds.BigBird
```

The value of the `street` property is then accessible this way:

```java
String street = System.getProperty("street");
```

## The Classpath

The concept of a _path_ should be familiar to anyone who has worked on a DOS or Unix platform. It’s an environment variable that provides an application with a list of places to look for some resource. The most common example is a path for executable programs. In a Unix shell, the `PATH` environment variable is a colon-separated list of directories that are searched, in order, when the user types the name of a command. The Java `CLASSPATH` environment variable, similarly, is a list of locations that are searched for Java class files. Both the Java interpreter and the Java compiler use the `CLASSPATH` when searching for packages and Java classes.

An element of the classpath can be a directory or a JAR file. Java also supports archives in the conventional ZIP format, but JAR and ZIP are really the same format. JARs are simple archives that include extra files (metadata) that describe each archive’s contents. JAR files are created with the JDK’s _jar_ utility; many tools for creating ZIP archives are publicly available and can be used to inspect or create JAR files as well. The archive format enables large groups of classes and their resources to be distributed in a single file; the Java runtime automatically extracts individual class files from the archive as needed.

On a Unix system (including macOS), you set the `CLASSPATH` environment variable with a colon-separated list of directories and class archive files:

```shell
export CLASSPATH=/home/fosdick/Java/classes:/home/fosdick/lib/foo.jar:.
```

If you don’t specify the `CLASSPATH` environment variable or command-line option, the classpath defaults to the current directory (`.`); this means that the files in your current directory are normally available.

## javap

A useful tool to know about is the `javap` command. With `javap`, you can print a description of a compiled class.

```shell
javap java.util.Stack

Compiled from "Stack.java"
public class java.util.Stack<E> extends java.util.Vector<E> {
  public java.util.Stack();
  public E push(E);
  public synchronized E pop();
  public synchronized E peek();
  public boolean empty();
  public synchronized int search(java.lang.Object);
}
```

Using `javap`, you can determine whether a class is in the classpath and possibly even which version you are looking at (many classpath issues involve duplicate classes in the classpath).

## jshell

Java 9 introduced a utility call `jshell`, which allows you to try out bits of Java code and see the results immediately. jshell is a REPL — a Read Evaluate Print Loop.

Just type `jshell` at your command prompt and you’ll see a bit of version information along with a quick reminder about how to view help from within the REPL.

## JAR Files

Java archive (JAR) files are Java’s suitcases. They are the standard and portable way to pack up all the parts of your Java application into a compact bundle for distribution or installation.

### File Compression

Items stored in JAR files are compressed with the standard ZIP file compression.

### The jar Utility

The `jar` utility provided with the JDK is a simple tool for creating and reading JAR files.

```shell
# Create jarFile containing path(s).
jar -cvf jarFile path [ path ] [ … ]

# List the contents of jarFile, optionally showing just path(s).
jar -tvf jarFile [ path ] [ … ]

# Extract the contents of jarFile, optionally extracting just path(s).
jar -xvf jarFile [ path ] [ … ]
```

### JAR Manifests

Note that the `jar` command automatically adds a directory called `META-INF` to our archive. The `META-INF` directory holds files describing the contents of the JAR file. It always contains at least one file: `MANIFEST.MF`. The `MANIFEST.MF` file can contain a “packing list” naming the files in the archive along with a user-definable set of attributes for each entry.

The manifest is a text file containing a set of lines in the form `keyword: value`. The manifest is, by default, empty and contains only JAR file version information:

```
Manifest-Version: 1.0
Created-By: 1.7.0_07 (Oracle Corporation)
```

It is also possible to sign JAR files with a digital signature. When you do this, digest (checksum) information is added to the manifest for each archived item (as shown next) and the `META-INF` directory holds digital signature files for items in the archive:

```
Name: com/oreilly/Test.class
SHA1-Digest: dF2GZt8G11dXY2p4olzzIc5RjP3=
```

### Making a JAR File Runnable

Aside from attributes, you can put a few special values in the manifest file. One of these, Main-Class, allows you to specify the class containing the primary main() method for an application contained in the JAR:

```
Main-Class: io.fosdick.Game
```
