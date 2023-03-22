import time
import datetime
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour,OneShotBehaviour
from spade.message import Message


class aGuy(Agent):
        class StartMessagesBehav(OneShotBehaviour):
            async def run(self):
                value = 0
                msg = Message(to="test_agent@jabbim.pl/22")
                msg.body = str(value)
                await self.send(msg)
                print(f"A-> {value}")

        class ReceiveBehaviour(CyclicBehaviour):
                async def on_start(self):
                    self.zen = 0
                    self.expected = 1
                async def on_end(self):
                    await self.agent.stop()


                async def run(self):
                    msg = await self.receive(timeout=15)
                    if msg:
                        time.sleep(1)
                        value = int(msg.body)
                        if(value==self.expected ) or (str(msg.sender)=="test_agent@jabbim.pl/22" and (self.zen==0 or self.zen==2)) :  # or msg.sender=="test_agent@jabbim.pl/2"
                            print(f"A<- {value}")
                            msg = Message(to="test_agent@jabbim.pl/22")
                            value+=1
                            msg.body = str(value)
                            await self.send(msg)
                            print(f"A-> {value}")
                            self.expected=value+1
                            if self.zen==1 : self.zen+=1
                        else:
                            print(f"A!")
                            if(str(msg.sender)=="test_agent@jabbim.pl/33" and self.zen == 0) :
                                self.expected=value+2
                                self.zen=1
                                print(f"^A^")
                                print(f"A<- {self.expected-2}")
                                msg = Message(to="test_agent@jabbim.pl/22") 
                                msg.body = str(self.expected-1)
                                await self.send(msg)
                                print(f"A-> {self.expected-1}")   





               

        async def setup(self):
            print(f"A ^")
            s = self.StartMessagesBehav()
            b = self.ReceiveBehaviour()
            self.add_behaviour(s)
            self.add_behaviour(b)


class bguy(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):

            msg = await self.receive(timeout=15)
            if msg:
                value = int(msg.body)
                if(value==self.expected ) or (str(msg.sender)=="test_agent@jabbim.pl/11" and (self.zen==0 or self.zen==2) ):
                    value += 1
                    reply = Message(to="test_agent@jabbim.pl/11")
                    reply.body = str(value)
                    ##time.sleep(1)
                    await self.send(reply)
                    print(f"B<- {value-1} \nB-> {value}")
                    self.expected=value+1
                    if self.zen==1 : self.zen+=1
                else:
                        print(f"B!")
                        if(str(msg.sender)=="test_agent@jabbim.pl/33" and self.zen == 0) :
                                self.expected=value+2
                                self.zen=1
                                print(f"^B^")
                                print(f"B<- {self.expected-2}")
                                msg = Message(to="test_agent@jabbim.pl/11") 
                                msg.body = str(self.expected-1)
                                await self.send(msg)
                                print(f"B-> {self.expected-1}") 
                
            else:
                print("Did not received any message after 10 seconds")
                self.kill()

        async def on_start(self):
            self.zen = 0
            self.expected = 0

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("B ^")
        b = self.RecvBehav()
        self.add_behaviour(b)


class cGuy(Agent):
        class distractBehav(CyclicBehaviour):
            async def run(self):
                #time.sleep(2)
                propbability = random.randint(1, 10)
                value = random.randint(30,99 )
                if(value%2==0) :msg = Message(to="test_agent@jabbim.pl/11")
                else :msg = Message(to="test_agent@jabbim.pl/22")
                
                msg.body = str(value)
               # time.sleep(2)
                if propbability<2:
                    await self.send(msg)
                    print(f"C-> {value}")


        async def on_end(self):
            await self.agent.stop()

        # async def on_start(self):
        #     self.focus = 0

        async def setup(self):
            print(f"C ^")
            s = self.distractBehav()
            self.add_behaviour(s)
    

if __name__ == "__main__":
    A = aGuy("test_agent@jabbim.pl/11", "123")
    B = bguy("test_agent@jabbim.pl/22", "123")
    C = cGuy("test_agent@jabbim.pl/33", "123")
    B.start()
    future= A.start()
   

    future.result()
 
    C.start()

    while A.is_alive() or B.is_alive():
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            C.stop()
            A.stop()
            B.stop()
 
            break
    print("Agents finished")

# aguy = DummyAgent("sungod01@jabb.im", "cacktus")
# test_agent@jabbim.pl 123
# from spade import agent
# from spade.behaviour import OneShotBehaviour
# from spade.message import Message

# class SenderAgent(agent.Agent):
#     class SendBehaviour(OneShotBehaviour):
#         async def run(self):
#             # Send a message with a random integer between 1 and 100 to the ReceiverAgent
#             value = random.randint(1, 100)
#             msg = Message(to="receiver@localhost")
#             msg.body = str(value)
#             await self.send(msg)
#             print(f"SenderAgent sent: {value}")

#     class ReceiveBehaviour(OneShotBehaviour):
#         async def run(self):
#             # Receive a message from the ReceiverAgent
#             msg = await self.receive(timeout=10)
#             if msg:
#                 # Extract the integer from the message body
#                 value = int(msg.body)
#                 print(f"SenderAgent received: {value}")

#     async def setup(self):
#         # Add both the send and receive behaviours to the agent
#         sb = self.SendBehaviour()
#         rb = self.ReceiveBehaviour()
#         self.add_behaviour(sb)
#         self.add_behaviour(rb)

# class ReceiverAgent(agent.Agent):
#     class SendBehaviour(OneShotBehaviour):
#         async def run(self):
#             # Send a message with a random integer between 1 and 100 to the SenderAgent
#             value = random.randint(1, 100)
#             msg = Message(to="sender@localhost")
#             msg.body = str(value)
#             await self.send(msg)
#             print(f"ReceiverAgent sent: {value}")

#     class ReceiveBehaviour(OneShotBehaviour):
#         async def run(self):
#             # Receive a message from the SenderAgent
#             msg = await self.receive(timeout=10)
#             if msg:
#                 # Extract the integer from the message body
#                 value = int(msg.body)
#                 # Add 1 to the integer
#                 value += 1
#                 # Send the updated integer back to the SenderAgent
#                 reply = Message(to=msg.sender)
#                 reply.body = str(value)
#                 await self.send(reply)
#                 print(f"ReceiverAgent received: {value} and sent: {value+1}")

#     async def setup(self):
#         # Add both the send and receive behaviours to the agent
#         sb = self.SendBehaviour()
#         rb = self.ReceiveBehaviour()
#         self.add_behaviour(sb)
#         self.add_behaviour(rb)

# if __name__ == "__main__":
#     # Start both
