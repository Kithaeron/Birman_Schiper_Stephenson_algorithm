import copy

from abstractprocess import AbstractProcess, Message
import random
import queue

class StampMessage(Message):
    time_stamp = []
    def __init__(self, content, sender, counter, time_stamp):
        super().__init__(content, sender, counter)
        self.time_stamp = time_stamp





class EchoProcess(AbstractProcess):
    """
    Example implementation of a distributed process.
    This example sends and echo's 10 messages to another process.
    Only the algorithm() function needs to be implemented.
    The function send_message(message, to) can be used to send asynchronous messages to other processes.
    The variables first_cycle and num_echo are examples of variables custom to the EchoProcess algorithm.
    """
    # first_cycle = True
    num_msg = 14
    send_counter = 0 
    rcv_counter = 0
    clock_vec = []
    delayed_msg = None

    def __init__(self, idx: int, addresses):
        super().__init__(idx, addresses)
        self.delayed_msg = queue.Queue()
        for i in range(len(addresses)+1):
            self.clock_vec.append(0)


    def deliverable(self, msg: StampMessage) -> bool: 
        """
        检查是否接受一个message
        """
        deliver: bool = False
        other: bool = True
        # print("len(self.addresses)+1=",len(self.addresses)+1)  # 3
        for k in range(len(self.addresses)+1):
            if k!=msg.sender:
                if self.clock_vec[k]>=msg.time_stamp[k]:  # 我比发来的人更新
                    other = True # 有一个不满足就是False
                else:
                    other = False
                    break
        #print("StampMessage", msg.time_stamp)
        #print("clock_vec",self.clock_vec)
        #print("sender",msg.sender)
        if (self.clock_vec[msg.sender] == msg.time_stamp[msg.sender]-1) and True==other:
            deliver = True
        print("deliverable:",deliver)
        return deliver



    async def algorithm(self): 

        #print("self.clock=",self.clock_vec) # 开头结尾各打印一次自己的时钟

        msg1: StampMessage
        msg2: StampMessage

        if self.send_counter < self.num_msg:
            #print("first msg clock 'before +=", self.clock_vec)
            self.clock_vec[self.idx] += 1
            #print("first msg clock 'after +=", self.clock_vec)
            for to in list(self.addresses.keys()):
                '''
                广播，发送给其他所有的process
                Pi sending a message to Pj :
                Pi increments Ci[i] and sets the timestamp tm = Ci[i] for message m.
                '''
                clock = copy.deepcopy(self.clock_vec)
                msg1 = StampMessage("Hello world", self.idx, self.send_counter, clock)
                #await self._random_delay()
                #await self.send_message(msg, to)


            self.send_counter += 1  # 记录是自己第几次发送消息



        if self.send_counter < self.num_msg:
            #print("second msg clock 'before +=", self.clock_vec)

            self.clock_vec[self.idx] += 1
            for to in list(self.addresses.keys()):
                '''
                广播，发送给其他所有的process
                Pi sending a message to Pj :
                Pi increments Ci[i] and sets the timestamp tm = Ci[i] for message m.
                '''
                clock2 = copy.deepcopy(self.clock_vec)
                msg2 = StampMessage("Hello world", self.idx, self.send_counter, clock2)
                #print("second msg clock after +=", self.clock_vec)
                await self.send_message(msg2, to)
                await self.send_message(msg1, to)
                #print("msg1 clock", msg1.time_stamp)
                #print("msg2 clock", msg2.time_stamp)


            self.send_counter += 1  # 记录是自己第几次发送消息
            
        # print("self.counter=",self.counter)
            

        # If we have a new message
        if self.buffer.has_messages():           
           
            '''
            Pj receiving a message from Pi
            if  Cj[i] = tm[i] - 1  &&   for all k <= n and k != i, Cj[k] >= tm[k]
                deliver
                update Pj‘s vector clock.

            else
                delays the message’s delivery
            '''
            
            for t in range(self.buffer.size()):
                # print(t)
                print("\n my vector time is ", self.clock_vec,'\n')
                msg: StampMessage = self.buffer.get()   
                print("sender", msg.sender," buffer msg clock", msg.time_stamp)

                if(self.deliverable(msg)):
                    

                    pre_clock = self.clock_vec
                    print('\n',f'pre self.clock={pre_clock}')
                    self.clock_vec[msg.sender] += 1
                    print( f'timestamp[{msg.time_stamp}] Got message "{msg.content}" from process {msg.sender} clock after{self.clock_vec}',"\n")


                    self.rcv_counter += 1
                    
                else:
                    self.delayed_msg.put(msg) # 放到一个queue里，这里应该也可以直接self.buffer.put
                    #print("buffer size", self.buffer.size())


            if self.delayed_msg.qsize()>0:
                # print("self.delayed size ", self.delayed_msg.qsize())
                for i in range(self.delayed_msg.qsize()):
                    msg: StampMessage = self.delayed_msg.get()
                    self.buffer.put(msg)
            #print("After buffer size", self.buffer.size())


        print("self.clock=",self.clock_vec) # 开头结尾各打印一次自己的时钟
            
        # await self.send_message(echo_msg, msg.sender)
        if self.send_counter >= self.num_msg and self.rcv_counter>=self.num_msg*2 and self.delayed_msg.qsize()==0:
            print('Exiting algorithm', "self.send_counter", self.send_counter, "self.rcv-counter", self.rcv_counter)
            self.running = False
