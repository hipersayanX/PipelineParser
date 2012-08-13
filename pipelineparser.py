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
        NoOp = 0
        ChangeId = 1
        AddElement = 2
        RemoveElement = 3
        ConnectElement = 4
        DisconnectElement = 5
        ConnectSignalsAndSlots = 6
        DisconnectSignalsAndSlots = 7

    def parsePipeline(self, pipeline=''):
        # sender receiver.slot<.signal
        # receiver slot<sender.signal
        # sender .signal>receiver.slot
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

        r = re.findall('[0-9a-zA-Z.<>=]+=["\'][^\r^\n]+["\']|!{1}|[0-9a-zA-Z.<>=]+', pipeline)

        for k, p in enumerate(r):
            if '=' in p:
                key, value = p.split('=', 1)

                if value.startswith('\'') or value.startswith('"'):
                    value = value[1: -1]

                properties[key] = value
            elif '<' in p:
                s1, s2 = p.split('<')

                if '.' in s1:
                    sender = '{0},{1}'.format(i, j)
                    signal = s2[1:]
                    receiver, slot = s1.split('.')
                    receiver += '.'
                else:
                    sender, signal = s2.split('.')
                    sender += '.'
                    receiver = '{0},{1}'.format(i, j)
                    slot = s1

                ss.append([sender, signal, receiver, slot])
            elif '>' in p:
                s1, s2 = p.split('>')

                if '.' in s2:
                    sender = '{0},{1}'.format(i, j)
                    signal = s1[1:]
                    receiver, slot = s2.split('.')
                    receiver += '.'
                else:
                    sender, signal = s1.split('.')
                    sender += '.'
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

    def indexOfSubList(self, l=[], sub=[]):
        if len(sub) > len(l):
            return -1

        for i in range(len(l) - len(sub) + 1):
            j = 0
            eq = True

            for s in sub:
                if l[i + j] != s:
                    eq = False

                    break

                j += 1

            if eq:
                return i

        return -1

    def sequences(self, instances=[], connections=[]):
        while True:
            nextConnections = []
            wasChanged = False

            for connection in connections:
                change = False

                for nextConnection in connections:
                    if nextConnection[0] == connection[len(connection) - 1]:
                        nextConnections.append(connection + nextConnection[1:])
                        wasChanged = True
                        change = True

                if not change:
                    nextConnections.append(connection)

            if wasChanged:
                connections = nextConnections
            else:
                break

        sequencesId = []

        for sequenceId in nextConnections:
            repeated = False

            for oldSequence in range(len(sequencesId)):
                if self.indexOfSubList(sequencesId[oldSequence], sequenceId) >= 0:
                    repeated = True

                    break
                elif self.indexOfSubList(sequenceId, sequencesId[oldSequence]) >= 0:
                    sequencesId[oldSequence] = sequenceId

                    break

            if not repeated:
                sequencesId.append(sequenceId)

        for instance in instances:
            has = False

            for sequenceId in sequencesId:
                if instance in sequenceId:
                    has = True

                    break

            if not has:
                sequencesId.append([instance])

        sequences = []

        for sequenceId in sequencesId:
            sequence = []

            for element in sequenceId:
                sequence.append([instances[element][0], element])

            if not sequence in sequences:
                sequences.append(sequence)

        return sequences

    def lcs(self, a=[], b=[]):
        ja = -1
        jb = -1
        n = 0

        if a == [] or b == []:
            return ja, jb, n

        l = len(a) + len(b) - 1
        ia = len(a) - 1
        ib = 0
        s = 1

        for k in range(l):
            nCur = 0

            for r in range(s):
                if a[ia + r][0] == b[ib + r][0]:
                    nCur += 1

                    if nCur > n:
                        ja = ia + r - nCur + 1
                        jb = ib + r - nCur + 1
                        n = nCur
                else:
                    nCur = 0

            if k < min(len(a), len(b)) - 1:
                ia -= 1
                s += 1
            elif k > l - min(len(a), len(b)) - 1:
                ib += 1
                s -= 1
            elif ia > 0:
                ia -= 1
            else:
                ib += 1

        return ja, jb, n

    def alignSequences(self, sequence1=[], sequence2=[]):
        index1, index2, l = self.lcs(sequence1, sequence2)

        if l == 0:
            return sequence1 + [[]] * len(sequence2) , [[]] * len(sequence1) + sequence2
        else:
            left1 = sequence1[: index1]
            left2 = sequence2[: index2]
            right1 = sequence1[index1 + l:]
            right2 = sequence2[index2 + l:]

            leftAlign = self.alignSequences(left1, left2)
            rightAlign = self.alignSequences(right1, right2)

            return leftAlign[0] + sequence1[index1: index1 + l] + rightAlign[0], leftAlign[1] + sequence2[index2: index2 + l] + rightAlign[1]

    def unalignSequence(self, sequence=[]):
        return [element for element in sequence if element != []]

    def sequenceCount(self, sequences=[], sequence=[]):
        count = 0

        for s in sequences:
            if self.unalignSequence(s) == self.unalignSequence(sequence):
                count += 1

        return count

    def alignScore(self, aSequence1=[], aSequence2=[]):
        score = 0

        for i in range(len(aSequence1)):
            if aSequence1[i] != [] and aSequence2[i] != [] and aSequence1[i][0] == aSequence2[i][0]:
                # match
                score += 1
            else:
                # gap
                score -= 1

        return score

    def msa(self, sequences1=[], sequences2=[]):
        sSequences1 = []
        sSequences2 = []
        scores = []

        for sequence2 in sequences2:
            for sequence1 in sequences1:
                aSequence1, aSequence2 = self.alignSequences(sequence1, sequence2)
                score = self.alignScore(aSequence1, aSequence2)

                if scores == []:
                    sSequences1.append(aSequence1)
                    sSequences2.append(aSequence2)
                    scores.append(score)
                else:
                    # Insert sort
                    imin = 0
                    imax = len(scores) - 1
                    imid = (imax + imin) >> 1

                    while True:
                        if score == scores[imid]:
                            sSequences1 = sSequences1[: imid + 1] + [aSequence1] + sSequences1[imid + 1:]
                            sSequences2 = sSequences2[: imid + 1] + [aSequence2] + sSequences2[imid + 1:]
                            scores = scores[: imid + 1] + [score] + scores[imid + 1:]

                            break
                        elif score < scores[imid]:
                            imax = imid
                        elif score > scores[imid]:
                            imin = imid

                        imid = (imax + imin) >> 1

                        if imid == imin or imid == imax:
                            if score < scores[imin]:
                                sSequences1 = sSequences1[: imin] + [aSequence1] + sSequences1[imin:]
                                sSequences2 = sSequences2[: imin] + [aSequence2] + sSequences2[imin:]
                                scores = scores[: imin] + [score] + scores[imin:]
                            elif score > scores[imax]:
                                sSequences1 = sSequences1[: imax + 1] + [aSequence1] + sSequences1[imax + 1:]
                                sSequences2 = sSequences2[: imax + 1] + [aSequence2] + sSequences2[imax + 1:]
                                scores = scores[: imax + 1] + [score] + scores[imax + 1:]
                            else:
                                sSequences1 = sSequences1[: imin + 1] + [aSequence1] + sSequences1[imin + 1:]
                                sSequences2 = sSequences2[: imin + 1] + [aSequence2] + sSequences2[imin + 1:]
                                scores = scores[: imin + 1] + [score] + scores[imin + 1:]

                            break

        i = 0

        while i < len(scores):
            count1 = self.sequenceCount(sSequences1, sSequences1[i])
            count2 = self.sequenceCount(sSequences2, sSequences2[i])

            if count1 > 1 and count2 > 1:
                del sSequences1[i]
                del sSequences2[i]
                del scores[i]

                i -= 1
            elif count1 > 1 and count2 < 2:
                sSequences2[i] = self.unalignSequence(sSequences2[i])
                sSequences1[i] = len(sSequences2[i]) * [[]]
            elif count1 < 2 and count2 > 1:
                sSequences1[i] = self.unalignSequence(sSequences1[i])
                sSequences2[i] = len(sSequences1[i]) * [[]]

            i += 1

        return sSequences1, sSequences2

    def isIdInUse(self, id='', instances={}):
        for instance in instances:
            if instance == id:
                return True

        return False

    def changeId(self, oldId='', newId='', instances={}, connections=[], ss=[], aSequences=[]):
        instances[newId] = instances[oldId]
        del instances[oldId]

        for i in range(len(connections)):
            if connections[i][0] == oldId:
                connections[i][0] = newId

            if connections[i][1] == oldId:
                connections[i][1] = newId

        for i in range(len(ss)):
            if ss[i][0] == oldId:
                ss[i][0] = newId

            if ss[i][2] == oldId:
                ss[i][2] = newId

        for j in range(len(aSequences)):
            for i in range(len(aSequences[j])):
                if aSequences[j][i] != []:
                    if aSequences[j][i][1] == oldId:
                        aSequences[j][i][1] = newId

    def pipelineDiff(self, pipeline1='', pipeline2=''):
        instances1, connections1, ss1 = self.parsePipeline(pipeline1)
        instances2, connections2, ss2 = self.parsePipeline(pipeline2)

        sequences1 = self.sequences(instances1, connections1)
        sequences2 = self.sequences(instances2, connections2)

        s1, s2 = self.msa(sequences1, sequences2)

        for i in range(len(s1)):
            for j in range(len(s1[i])):
                if s1[i][j] == []:
                    if self.isIdInUse(s2[i][j][1], instances1):
                        self.changeId(s2[i][j][1], '.{0}'.format(s2[i][j][1]), instances1, connections1, ss1, s1)
                        print('Change Id {0} -> {1}'.format(s2[i][j][1], '.{0}'.format(s2[i][j][1])))

                    print('Add Element {0}'.format(s2[i][j]))
                elif s2[i][j] == []:
                    print('Remove Element {0}'.format(s1[i][j][1]))
                elif s1[i][j][1] != s2[i][j][1]:
                    if self.isIdInUse(s2[i][j][1], instances1):
                        self.changeId(s2[i][j][1], '.{0}'.format(s2[i][j][1]), instances1, connections1, ss1, s1)
                        print('Change Id {0} -> {1}'.format(s2[i][j][1], '.{0}'.format(s2[i][j][1])))

                    print('Change Id {0} -> {1}'.format(s1[i][j][1], s2[i][j][1]))


pipeline1 = 'element1 objectName=el1 prop1=10 prop2=val2 ' \
            'el1. ! element2 .signal1>el5.slot1 ' \
            'el1. ! element3 prop3=\"Hola, mundo cruel !!!\" ! element1 ! element5 ! el5. ' \
            'element4 prop1=3.14 slot5<el5.signal5 ! el5. ' \
            'element5 objectName=el5 el1.signal2>slot2 ! element6 prop1=val1 el1.slot1<.signal1'

pipeline2 = 'element1 objectName=el1 prop1=10 prop2=val2 ' \
            'element5 objectName=el5 el1.signal2>slot2 ! element6 prop1=val1 el1.slot1<.signal1 ' \
            'el1. ! element3 prop3=\"Hola, mundo cruel !!!\" ! element5 ! el5. ' \
            'element4 prop1=3.14 slot5<el5.signal5 ! el5. ' \
            'el1. ! element2 .signal1>el5.slot1 ' \
            'element10 ! element12 ' \
            'element11'

pp = PipelineParser()
pp.pipelineDiff(pipeline1, pipeline2)
