#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pipeline parser.
# Copyright (C) 2012  Gonzalo Exequiel Pedone
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with This program. If not, see <http://www.gnu.org/licenses/>.
#
# Email   : hipersayan DOT x AT gmail DOT com
# Web-Site: http://hipersayanx.blogspot.com/

import re

class PipelineParser:
    class DiffOp:
        DisconnectSignalsAndSlots = 0
        DisconnectElement = 1
        RemoveElement = 2
        ChangeId = 3
        AddElement = 4
        SetProperties = 5
        ResetProperties = 6
        ConnectElement = 7
        ConnectSignalsAndSlots = 8

    def __init__(self):
        self.instances1 = {}
        self.connections1 = []
        self.ss1 = []

    def parseValue(self, value):
        if value.startswith('\'') or value.startswith('"'):
            return value[1: -1]
        elif value.startswith('{'):
            r = re.findall('[0-9]+\.[0-9]+ *: *[0-9]+\.[0-9]+|'
                            '[0-9]+\.[0-9]+ *: *\.[0-9]+|'
                            '[0-9]+\.[0-9]+ *: *[0-9]+\.|'
                            '[0-9]+\.[0-9]+ *: *[0-9]+|'
                            '[0-9]+\.[0-9]+ *: *"[^"]+"|'
                            '[0-9]+\.[0-9]+ *: *\'[^\']+\'|'
                            '[0-9]+\.[0-9]+ *: *\{[^\r^\n]+\}|'
                            '[0-9]+\.[0-9]+ *: *\[[^\r^\n]+\]|'
                            '\.[0-9]+ *: *[0-9]+\.[0-9]+|'
                            '\.[0-9]+ *: *\.[0-9]+|'
                            '\.[0-9]+ *: *[0-9]+\.|'
                            '\.[0-9]+ *: *[0-9]+|'
                            '\.[0-9]+ *: *"[^"]+"|'
                            '\.[0-9]+ *: *\'[^\']+\'|'
                            '\.[0-9]+ *: *\{[^\r^\n]+\}|'
                            '\.[0-9]+ *: *\[[^\r^\n]+\]|'
                            '[0-9]+\. *: *[0-9]+\.[0-9]+|'
                            '[0-9]+\. *: *\.[0-9]+|'
                            '[0-9]+\. *: *[0-9]+\.|'
                            '[0-9]+\. *: *[0-9]+|'
                            '[0-9]+\. *: *"[^"]+"|'
                            '[0-9]+\. *: *\'[^\']+\'|'
                            '[0-9]+\. *: *\{[^\r^\n]+\}|'
                            '[0-9]+\. *: *\[[^\r^\n]+\]|'
                            '[0-9]+ *: *[0-9]+\.[0-9]+|'
                            '[0-9]+ *: *\.[0-9]+|'
                            '[0-9]+ *: *[0-9]+\.|'
                            '[0-9]+ *: *[0-9]+|'
                            '[0-9]+ *: *"[^"]+"|'
                            '[0-9]+ *: *\'[^\']+\'|'
                            '[0-9]+ *: *\{[^\r^\n]+\}|'
                            '[0-9]+ *: *\[[^\r^\n]+\]|'
                            '"[^"]*" *: *[0-9]+\.[0-9]+|'
                            '"[^"]*" *: *\.[0-9]+|'
                            '"[^"]*" *: *[0-9]+\.|'
                            '"[^"]*" *: *[0-9]+|'
                            '"[^"]*" *: *"[^"]+"|'
                            '"[^"]*" *: *\'[^\']+\'|'
                            '"[^"]*" *: *\{[^\r^\n]+\}|'
                            '"[^"]*" *: *\[[^\r^\n]+\]|'
                            '\'[^\']*\' *: *[0-9]+\.[0-9]+|'
                            '\'[^\']*\' *: *\.[0-9]+|'
                            '\'[^\']*\' *[0-9]+\.|'
                            '\'[^\']*\' *[0-9]+|'
                            '\'[^\']*\' *: *"[^"]+"|'
                            '\'[^\']*\' *: *\'[^\']+\'|'
                            '\'[^\']*\' *: *\{[^\r^\n]+\}|'
                            '\'[^\']*\' *: *\[[^\r^\n]+\]|'
                            '\{[^\r^\n]+\} *: *[0-9]+\.[0-9]+|'
                            '\{[^\r^\n]+\} *: *\.[0-9]+|'
                            '\{[^\r^\n]+\} *[0-9]+\.|'
                            '\{[^\r^\n]+\} *[0-9]+|'
                            '\{[^\r^\n]+\} *: *"[^"]+"|'
                            '\{[^\r^\n]+\} *: *\'[^\']+\'|'
                            '\{[^\r^\n]+\} *: *\{[^\r^\n]+\}|'
                            '\{[^\r^\n]+\} *: *\[[^\r^\n]+\]|'
                            '\[[^\r^\n]+\] *: *[0-9]+\.[0-9]+|'
                            '\[[^\r^\n]+\] *: *\.[0-9]+|'
                            '\[[^\r^\n]+\] *[0-9]+\.|'
                            '\[[^\r^\n]+\] *[0-9]+|'
                            '\[[^\r^\n]+\] *: *"[^"]+"|'
                            '\[[^\r^\n]+\] *: *\'[^\']+\'|'
                            '\[[^\r^\n]+\] *: *\{[^\r^\n]+\}|'
                            '\[[^\r^\n]+\] *: *\[[^\r^\n]+\]|'
                            ',', value[1: -1])

            d = {}

            for item in r:
                if item != ',':
                    k, v = item.split(':', 1)
                    d[self.parseValue(k.strip())] = self.parseValue(v.strip())

            return d
        elif value.startswith('['):
            r = re.findall('[0-9]+\.[0-9]+|'
                            '\.[0-9]+|'
                            '[0-9]+\.|'
                            '[0-9]+|'
                            '"[^"]*"|'
                            '\'[^\']*\'|'
                            '\{[^\r^\n]+\}|'
                            '\[[^\r^\n]+\]|'
                            ',', value[1: -1])

            l = []

            for item in r:
                if item != ',':
                    l.append(self.parseValue(item))

            return l
        else:
            try:
                return int(value)
            except:
                try:
                    return float(value)
                except:
                    return value

    def parsePipeline(self, pipeline=''):
        # sender receiver.slot<signal
        # receiver slot<sender.signal
        # sender signal>receiver.slot
        # receiver sender.signal>slot
        #
        # [sender, signal, receiver, slot]

        instances = {}
        pipes = []
        pipe = []
        elementName = ''
        properties = {}
        ss = []
        i = 0
        j = 0

        r = re.findall('[a-zA-Z_][0-9a-zA-Z_]*=\'[^\']+\'|'                # Property strings.
                       '[a-zA-Z_][0-9a-zA-Z_]*="[^"]+"|'
                       '[a-zA-Z_][0-9a-zA-Z_]*=\[[^\r^\n]+\]|'             # Property lists.
                       '[a-zA-Z_][0-9a-zA-Z_]*=\{[^\r^\n]+\}|'             # Property dictionaries.
                       '[a-zA-Z_][0-9a-zA-Z_]*=[^\r^\n^ ]+|'               # Property any.
                       '!{1}|'                                             # Pipe.
                       '[a-zA-Z_]+[0-9a-zA-Z_]*\.[a-zA-Z_]+[0-9a-zA-Z_]*<' # Signal & Slot
                       '[a-zA-Z_]+[0-9a-zA-Z_]*\.[a-zA-Z_]+[0-9a-zA-Z_]*|'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*<'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*\.[a-zA-Z_]+[0-9a-zA-Z_]*|'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*\.[a-zA-Z_]+[0-9a-zA-Z_]*<'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*|'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*<'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*|'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*\.[a-zA-Z_]+[0-9a-zA-Z_]*>'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*\.[a-zA-Z_]+[0-9a-zA-Z_]*|'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*>'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*\.[a-zA-Z_]+[0-9a-zA-Z_]*|'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*\.[a-zA-Z_]+[0-9a-zA-Z_]*>'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*|'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*>'
                       '[a-zA-Z_]+[0-9a-zA-Z_]*|'
                       '[a-zA-Z_][0-9a-zA-Z_]*\.|'                         # Reference
                       '[a-zA-Z_][0-9a-zA-Z_]*', pipeline)                 # Element.

        for k, p in enumerate(r):
            if '=' in p:
                key, value = p.split('=', 1)
                properties[key] = self.parseValue(value)
            elif '<' in p:
                s1, s2 = p.split('<')

                if '.' in s1:
                    receiver, slot = s1.split('.')
                    receiver += '.'
                else:
                    receiver = '{0},{1}'.format(i, j)
                    slot = s1

                if '.' in s2:
                    sender, signal = s2.split('.')
                    sender += '.'
                else:
                    sender = '{0},{1}'.format(i, j)
                    signal = s2

                ss.append([sender, signal, receiver, slot])
            elif '>' in p:
                s1, s2 = p.split('>')

                if '.' in s1:
                    sender, signal = s1.split('.')
                    sender += '.'
                else:
                    sender = '{0},{1}'.format(i, j)
                    signal = s1

                if '.' in s2:
                    receiver, slot = s2.split('.')
                    receiver += '.'
                else:
                    receiver = '{0},{1}'.format(i, j)
                    slot = s2

                ss.append([sender, signal, receiver, slot])
            else:
                if elementName != '' and elementName != '!':
                    if not elementName.endswith('.'):
                        instances['{0},{1}'.format(i, j)] = [elementName, properties]

                    pipe.append([elementName, properties])

                    i += 1

                    if p != '!':
                        pipes.append(pipe)
                        pipe = []
                        i = 0
                        j += 1

                elementName = p
                properties = {}

            if k == len(r) - 1:
                if elementName != '' and elementName != '!':
                    if not elementName.endswith('.'):
                        instances['{0},{1}'.format(i, j)] = [elementName, properties]

                    pipe.append([elementName, properties])

                    i += 1

                    if p != '!':
                        pipes.append(pipe)
                        pipe = []
                        i = 0
                        j += 1

        references = {}

        for pipe in pipes:
            for element in pipe:
                if element[0].endswith('.'):
                    for instance in instances:
                        if 'objectName' in instances[instance][1] and instances[instance][1]['objectName'] == element[0][:-1]:
                            references[element[0]] = instance

        # sender -> receiver

        connections = []

        for j, pipe in enumerate(pipes):
            for i, element in enumerate(pipe):
                if element[0].endswith('.'):
                    cur = references[element[0]]
                else:
                    cur = '{0},{1}'.format(i, j)

                if i + 1 < len(pipe):
                    nextElement = pipe[i + 1]

                    if nextElement[0].endswith('.'):
                        nxt = references[nextElement[0]]
                    else:
                        nxt = '{0},{1}'.format(i + 1, j)

                    connections.append([cur, nxt])

        for s in ss:
            if s[0].endswith('.'):
                s[0] = references[s[0]]

            if s[2].endswith('.'):
                s[2] = references[s[2]]

        return instances, connections, ss

    def pipelineDiff(self, pipeline2=''):
        instances2, connections2, ss2 = self.parsePipeline(pipeline2)

        cInstances1 = self.instances1.copy()
        cInstances2 = instances2.copy()

        cConnections1 = self.connections1[:]
        cConnections2 = connections2[:]

        cSs1 = self.ss1[:]
        cSs2 = ss2[:]

        disconnectSignalsAndSlots = []
        disconnectElement = []
        removeElement = []
        changeId = []
        setProperties = {}
        resetProperties = {}
        connectElement = []
        connectSignalsAndSlots = []

        while cInstances1 != {}:
            instance1 = cInstances1.popitem()
            bestMatchId = ''

            for instance2 in cInstances2:
                if instance1[1][0] == cInstances2[instance2][0]:
                    if bestMatchId == '':
                        bestMatchId = instance2
                    elif 'objectName' in instance1[1][1] and \
                         'objectName' in cInstances2[instance2][1] and \
                         instance1[1][1]['objectName'] == cInstances2[instance2][1]['objectName']:
                        bestMatchId = instance2

                        break

            if bestMatchId == '':
                removeElement.append(instance1[0])
                i = 0

                while i < len(cConnections1):
                    if cConnections1[i][0] == instance1[0] or cConnections1[i][1] == instance1[0]:
                        disconnectElement.append(cConnections1[i])
                        del cConnections1[i]
                    else:
                        i += 1

                i = 0

                while i < len(cSs1):
                    if cSs1[i][0] == instance1[0] or cSs1[i][2] == instance1[0]:
                        disconnectSignalsAndSlots.append(cSs1[i])
                        del cSs1[i]
                    else:
                        i += 1
            else:
                if instance1[0] != bestMatchId:
                    if bestMatchId in cInstances1:
                        changeId.append([instance1[0], '.{0}'.format(bestMatchId)])
                    else:
                        changeId.append([instance1[0], bestMatchId])

                setProps = {}

                for prop in cInstances2[bestMatchId][1]:
                    if not prop in instance1[1][1] or (prop in instance1[1][1] and cInstances2[bestMatchId][1][prop] != instance1[1][1][prop]):
                        setProps[prop] = cInstances2[bestMatchId][1][prop]

                if setProps != {}:
                    setProperties[bestMatchId] = setProps

                resetProps = []

                for prop in instance1[1][1]:
                    if not prop in cInstances2[bestMatchId][1]:
                        resetProps.append(prop)

                if resetProps != []:
                    resetProperties[bestMatchId] = resetProps

                del cInstances2[bestMatchId]

        i = 0

        while i < len(changeId):
            if changeId[i][1].startswith('.'):
                if changeId[i][1][1:] in removeElement:
                    changeId[i][1] = changeId[i][1][1:]
                else:
                    changeId.append([changeId[i][1], changeId[i][1][1:]])

            i += 1

        i = 0

        while i < len(cConnections1):
            dstConnection = cConnections1[i][:]
            fst = False
            snd = False

            for change in changeId:
                dst = change[1][1:] if change[1].startswith('.') else change[1]

                if not fst and dstConnection[0] == change[0]:
                    dstConnection[0] = dst
                    fst = True

                if not snd and dstConnection[1] == change[0]:
                    dstConnection[1] = dst
                    snd = True

                if fst and snd:
                    break

            if not dstConnection in cConnections2 and not list(reversed(dstConnection)) in cConnections2:
                disconnectElement.append(cConnections1[i])
                del cConnections1[i]
            else:
                i += 1

        i = 0

        while i < len(cConnections2):
            dstConnection = cConnections2[i][:]
            fst = False
            snd = False

            for change in changeId:
                src = change[1][1:] if change[1].startswith('.') else change[1]

                if not fst and dstConnection[0] == src:
                    dstConnection[0] = change[0]
                    fst = True

                if not snd and dstConnection[1] == src:
                    dstConnection[1] = change[0]
                    snd = True

                if fst and snd:
                    break

            if not dstConnection in cConnections1 and not list(reversed(dstConnection)) in cConnections1:
                connectElement.append(cConnections2[i])
                del cConnections2[i]
            else:
                i += 1

        i = 0

        while i < len(cSs1):
            dstSs = cSs1[i][:]
            fst = False
            snd = False

            for change in changeId:
                dst = change[1][1:] if change[1].startswith('.') else change[1]

                if not fst and dstSs[0] == change[0]:
                    dstSs[0] = dst
                    fst = True

                if not snd and dstSs[2] == change[0]:
                    dstSs[2] = dst
                    snd = True

                if fst and snd:
                    break

            if not dstSs in cSs2:
                disconnectSignalsAndSlots.append(cSs1[i])
                del cSs1[i]
            else:
                i += 1

        i = 0

        while i < len(cSs2):
            dstSs = cSs2[i][:]
            fst = False
            snd = False

            for change in changeId:
                src = change[1][1:] if change[1].startswith('.') else change[1]

                if not fst and dstSs[0] == src:
                    dstSs[0] = change[0]
                    fst = True

                if not snd and dstSs[2] == src:
                    dstSs[2] = change[0]
                    snd = True

                if fst and snd:
                    break

            if not dstSs in cSs1:
                connectSignalsAndSlots.append(cSs2[i])
                del cSs2[i]
            else:
                i += 1

        addElement = {}

        for instance in cInstances2:
            addElement[instance] = cInstances2[instance][0]

            if cInstances2[instance][1] != {}:
                setProperties[instance] = cInstances2[instance][1]

            i = 0

            while i < len(cConnections2):
                if cConnections2[i][0] == instance or cConnections2[i][1] == instance:
                    connectElement.append(cConnections2[i])
                    del cConnections2[i]
                else:
                    i += 1

            i = 0

            while i < len(cSs2):
                if cSs2[i][0] == instance or cSs2[i][2] == instance:
                    connectSignalsAndSlots.append(cSs2[i])
                    del cSs2[i]
                else:
                    i += 1

        ops = []

        for ss in disconnectSignalsAndSlots:
            ops.append([self.DiffOp.DisconnectSignalsAndSlots, ss])

        for connection in disconnectElement:
            ops.append([self.DiffOp.DisconnectElement, connection])

        for elementId in removeElement:
            ops.append([self.DiffOp.RemoveElement, [elementId]])

        for change in changeId:
            ops.append([self.DiffOp.ChangeId, change])

        for elementId in addElement:
            ops.append([self.DiffOp.AddElement, [elementId, addElement[elementId]]])

        for elementId in setProperties:
            for prop in setProperties[elementId]:
                ops.append([self.DiffOp.SetProperties, [elementId, prop, setProperties[elementId][prop]]])

        for elementId in resetProperties:
            for prop in resetProperties[elementId]:
                ops.append([self.DiffOp.ResetProperties, [elementId, prop]])

        for connection in connectElement:
            ops.append([self.DiffOp.ConnectElement, connection])

        for ss in connectSignalsAndSlots:
            ops.append([self.DiffOp.ConnectSignalsAndSlots, ss])

        self.instances1 = instances2
        self.connections1 = connections2
        self.ss1 = ss2

        return ops


if __name__ == '__main__':
    pipeline1 = 'element1 objectName=el1 prop1=10 prop2=val2 ' \
                'el1. ! element2 ' \
                'el1. ! element3 prop3=\"Hola, mundo cruel !!!\" ! element1 signal>el1.slot ! element5 ! el5. ' \
                'element4 prop1=3.14 prop10=50 slot5<el5.signal5 ! el5. ' \
                'element5 objectName=el5 el1.signal2>slot2 ! element6 prop1=val10 el1.slot1<signal1'

    pipeline2 = 'element1 objectName=el1 prop1={\'hola\': [9.87, \'chau\', \'perro\']} prop2=val2 ' \
                'element5 objectName=el5 el1.signal2>slot2 ! element6 prop1=val1 ' \
                'el1. ! element3 prop3=\"Hola, mundo cruel !!!\" ! element5 ' \
                'element4 prop1=3.14 slot5<el5.signal5 ! el5. ' \
                'el1. ! element2 signal1>el5.slot1 ' \
                'element10 prop1=78 ! element12 ' \
                'element11 signal1>el5.slot1'

    pp = PipelineParser()

    pp.pipelineDiff(pipeline1)

    for op in pp.pipelineDiff(pipeline2):
        if op[0] == PipelineParser.DiffOp.DisconnectSignalsAndSlots:
            opName = 'DisconnectSignalsAndSlots'
        elif op[0] == PipelineParser.DiffOp.DisconnectElement:
            opName = 'DisconnectElement'
        elif op[0] == PipelineParser.DiffOp.RemoveElement:
            opName = 'RemoveElement'
        elif op[0] == PipelineParser.DiffOp.ChangeId:
            opName = 'ChangeId'
        elif op[0] == PipelineParser.DiffOp.AddElement:
            opName = 'AddElement'
        elif op[0] == PipelineParser.DiffOp.SetProperties:
            opName = 'SetProperties'
        elif op[0] == PipelineParser.DiffOp.ResetProperties:
            opName = 'ResetProperties'
        elif op[0] == PipelineParser.DiffOp.ConnectElement:
            opName = 'ConnectElement'
        else:
            opName = 'ConnectSignalsAndSlots'

        print('{0} {1}'.format(opName, op[1]))
