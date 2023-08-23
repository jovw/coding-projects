from segment import Segment

class RDTLayer(object):
    """
    The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable
     channel.
    """
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0                                # Use this for segment 'timeouts'
    currentWindow = [0, 4]
    currentSeqNum = 0
    expectedAck = 4
    iterationsWithoutAck = 0
    serverData = []

    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        self.countSegmentTimeouts = 0
        self.currAck = 0
        self.winStart = 0
        self.winEnd = 4
        self.role = "Server"
        self.timeOut = 0

    def setSendChannel(self, channel):
        """
        Called by main to set the unreliable sending lower-layer channel
        """
        self.sendChannel = channel

    def setReceiveChannel(self, channel):
        """
        Called by main to set the unreliable receiving lower-layer channel
        """
        self.receiveChannel = channel

    def setDataToSend(self,data):
        """
        Called by main to set the string data to send
        """
        self.dataToSend = data

    def getDataReceived(self):
        """
        Called by main to get the currently received and buffered string data, in order
        """

        # Identify the data that has been received
        sortedData = sorted(self.serverData)
        sortedString = ""
        for i in range(len(sortedData)):
            sortedString += sortedData[i][1]
        return sortedString

    def processData(self):
        """
        "timeslice". Called by main once per iteration
        """
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    def processSend(self):
        """
        Manages Segment sending tasks
        """

        if self.currentIteration > 1 and not self.receiveChannel.receiveQueue:
            # if we have gone 1 iteration without an ack we resend current window
            if self.timeOut == 3:
                # resend the window if we hit the timeout window
                self.currentSeqNum = self.currentWindow[0]
                self.countSegmentTimeouts += 1
            else:
                self.timeOut += 1
                return

        self.role = "Client" if self.dataToSend else "Server"

        # if a packet was received, check if all the packets are received
        if len(self.receiveChannel.receiveQueue) > 0 and self.role == "Client":
            # expected, would be the expected number of ACK to be received
            # if expected = the ack.receiveChannel.receive, it measn that all the packets are received and the
                # window can be moved on
            # if they are not equal it means that some packet loss or error occurred
            acklist = self.receiveChannel.receive()
            for i in range(0, len(acklist)):
                if acklist[i].acknum == self.expectedAck:
                    self.currentSeqNum += 4
                    self.expectedAck += 4
                    self.currentWindow[0] += 4
                    self.currentWindow[1] += 4

        # else continue to itterate through the current seqnum
        seqnum = self.currentSeqNum
        self.winStart, self.winEnd = seqnum, seqnum + 4

        if self.role == "Client":
            # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
            # These constants are given in # characters
            # splitting data input in smaller sections based on the self.Data_LENGTH
            # https://www.geeksforgeeks.org/python-split-string-in-groups-of-n-consecutive-characters/#
            data = [self.dataToSend[i:i + self.DATA_LENGTH] for i in range(0, len(self.dataToSend), self.DATA_LENGTH)]
            for i in range(self.winStart, self.winEnd):
                if self.dataToSend and seqnum < len(data):
                    # creating data segments to send.
                    segmentSend = Segment()
                    segmentSend.setData(seqnum, data[seqnum])
                    # Display sending segment
                    print("Sending segment:", segmentSend.to_string())
                    seqnum += 1
                    # Sending 4 at once, so move iteration on 4
                    segmentSend.setStartIteration(self.currentIteration)
                    segmentSend.setStartDelayIteration(4)
                    # Use the unreliable sendChannel to send the segment
                    self.sendChannel.send(segmentSend)

    def processReceiveAndSendRespond(self):
        """
        Manages Segment receive tasks
        """
        listIncomingSegments = self.receiveChannel.receive()

        if listIncomingSegments:
            segmentAck = Segment()

            currentAck = self.currentWindow[0]
            self.expectedAck = self.currentWindow[1]

            # What segments have been received?
            received = []
            # Iterate through each segment in the list of incoming segments
            for seg in listIncomingSegments:
                if seg.payload and seg.checkChecksum():
                    seq_and_payload = [seg.seqnum, seg.payload]
                    # Append the list to the received
                    received.append(seq_and_payload)

            process = []
            # Iterate through each item in received
            for item in received:
                if self.currentWindow[0] <= item[0] <= self.currentWindow[1]:
                    # If the sequence number is within the window range, add the item to process
                    process.append(item)

            recAck = len(process)
            currentAck += recAck

            if currentAck == self.expectedAck:
                self.winStart += 4
                self.currAck += 4
                segmentAck.setAck(currentAck)
                print("Sending ACK:", segmentAck.to_string())
                self.sendChannel.send(segmentAck)

            self.serverData.extend(
                item for item in process if item not in self.serverData
            )
