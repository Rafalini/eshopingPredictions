class Session:
    def __init__(self, sessionId, timeStamp, userId, productId, eventType, offeredDiscount, purchaseId):
        self.sessionId = sessionId
        self.timeStamp = timeStamp
        self.userId = userId
        self.productId = productId
        self.eventType = eventType
        self.offeredDiscount = offeredDiscount
        self.purchaseId = purchaseId

    def print(self):
        print('sessionId:        '+str(self.sessionId) +'\n'+
              'timeStamp:        '+self.timeStamp +'\n'+
              'userId:           '+str(self.userId) +'\n'+
              'productId:        '+str(self.productId) +'\n'+
              'eventType:        '+self.eventType +'\n'+
              'offeredDiscount:  '+str(self.offeredDiscount) +'\n'+
              'purchaseId:       '+str(self.purchaseId) +'\n')