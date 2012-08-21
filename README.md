# Python pipeline parser #

This is an experimental pipeline parser for GStreamer like pipeline syntax. This parser is not aimed to be fully compatible with GStreamer, it just copies the model, not the mode. It also has an extra syntax for Qt signals and slots and supports pipeline diff.
This parser is written in Python 3.

# Syntax #

A pipeline is basically an application for the [graph theory](https://en.wikipedia.org/wiki/Graph_theory), where each element is a node of the graph and each pipe is a connection between two nodes, and the data packets are transfered throw this connections.
Bellow, the pipeline description format is explained.

## Defining elements ##

The simplest way to define new elements in the pipeline is as follow:

    element1 element2 element3 element4

This will create four independets elements (nodes) of type _elementN_ with no connections between them (no data transfer). The parser will not check if these elements can be created or not. The types of the elements can be repeated as many as you want.

## Setting properties ##

You can assign the properties for an alement as follow:

    element1 prop1=value1 prop2=value2 element2 prop3=value3 element3 element4

Each property must be in the form _key=value_ (with no spaces), and must be declared after the element containing that property. the name (_key_) for each property follow [the common rule](https://en.wikipedia.org/wiki/Naming_convention_%28programming%29) for most programming languages; only alphanumeric characters and underscore, and can't start with a number.  
The rules for values (_value_) is as follow:

    prop="value"            # String
    prop='value'            # String
    prop=value              # String
    prop=3value*#?          # String
    prop='Hello World!!!'   # String
    prop=3                  # Int
    prop=3.14               # Float
    prop=.14                # Float (0.14)
    prop=3.                 # Float (3.0)
    prop=['value', 3, 3.14]                         # List
    prop={'key1': 'value', "key2": [1, 2], 3: 3.14} # Dictionary

Lists and dictionaries uses the same syntax [as in Python](http://docs.python.org/tutorial/datastructures.html).  
There is also a special property called _objectName_ for assigning an identifying name to an element, this is equivalent to the _name_ property of GStreamer. _objectName_ values must follow the programming languages naming rules.

## Linking the elements ##

If you want to connect one or more elements, you can use pipes __!__ (exclamation sign) as follow:

    element1 prop1=value1 ! element2 prop3=value3 ! element3 element4

Here, _element1_ is connected with _element2_, and _element2_ is connected with _element1_ and _element3_, while _element4_ remains unconnected.  
This means that _element1_ can share data packets with _element2_, but not with _elemen3_ or _element4_.  
_element2_ can share data packets with _element1_ and  _elemen3_, but not with _element4_.  
_element3_ can share data packets with _element2_, but not with _elemen1_ or _element4_.  
And _element4_ can't share data packets with none of these.

If you want to connect 3 or more elements to an element, you can use references as follows:

    element1 prop1=value1 ! element2 objectName=refel2 ! element3 element4
    refel2. ! element5 prop3=value3 ! element6 element4

In the example above, _element1_,  _element3_ and  _element5_ are connected to  _element2_. To create a reference you must set the _objectName_ property of an object you want to connect, and then connect the value of that property followed by a __.__ (dot) with any other object or reference.

## Defining signals & slots ##

This parser also add a special syntax for [Qt](http://qt-project.org/) based programs that allows connecting two elements using signals & slots. Here is an example:

    element1 prop1=value1 signal1>refel2.slot2 ! element2 objectName=refel2 ! element3 element4

This will connect the _signal1_ signal from _element1_ element to _slot2_ slot of the _element2_ element. The signals & slots syntax is as follow.

    sender signal>receiver.slot
    receiver sender.signal>slot
    sender receiver.slot<signal
    receiver slot<sender.signal
    element signal>slot                 # Self connection
    element slot<signal
    element sender.signal>receiver.slot # Extern connection
    element receiver.slot<sender.signal

# Parser module #

Here is a little example:

    # Create two pipelines.
    pipeline1 = 'element1 prop1=value1 ! element2 prop3=value3 ! element3 element4'

    pipeline2 = 'element1 prop1=value1 ! element2 objectName=refel2 ! element3 element4 objectName=refel4 ' \
                'refel2. ! element5 prop3=value3 ! element6 element7 signal>refel4.slot'

    # Create a parser instance.
    pp = PipelineParser()

    # Returns a list of operations to convert from previous pipeline to the new.
    ops = pp.pipelineDiff(pipeline1)
    ops = pp.pipelineDiff(pipeline2)

    # Parse a pipeline and returns the graph.
    instances, connections, signalsAndSlots = pp.parsePipeline(pipeline2)
