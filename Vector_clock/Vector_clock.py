from multiprocessing import Process, Pipe

class operations:
    def __init__(self,pipe_conn,current_pid,times):
        self.pipe_conn=pipe_conn
        self.current_pid=current_pid
        self.times=times
    
    def increment(self): # function to increment the timestamp when needed
        self.times[self.current_pid]=self.times[self.current_pid]+1
        time_stamp=self.times
        print('TIME_STAMP: '+str(time_stamp)+" .CURRENT_PID: "+str(self.current_pid)+' .PID.EVENT_ID 0.' )
        return time_stamp

    def send_message(self): # function to send message
        self.times[self.current_pid]=self.times[self.current_pid]+1
        time_stamp=self.times
        self.pipe_conn.send(('Hello',time_stamp,self.current_pid))
        print('TIME_STAMP: '+str(time_stamp)+" .CURRENT_PID: "+str(self.current_pid)+' .PID.EVENT_ID 1.' )
        return time_stamp

    def receive_message(self): #function to receive message
        message,conn_time,conns_pid=self.pipe_conn.recv()
        i=0
        while(i<len(self.times)):
            self.times[i]=max(conn_time[i],self.times[i])
            i=i+1
        time_stamp=self.times
        time_stamp[self.current_pid]=time_stamp[self.current_pid]+1
        print('TIME_STAMP: '+str(time_stamp)+" .CURRENT_PID: "+str(self.current_pid)+' .PID.EVENT_ID 2.' )
        return time_stamp

class process_switch:
    def __init__(self,pipe_conn1,pipe_conn2,current_pid):
        self.pipe_conn1=pipe_conn1
        self.pipe_conn2=pipe_conn2
        self.current_pid=current_pid
    
    def first_process(self): # function for 1st process
        times=[] # vector clock time stamp for 3 process [0,0,0]
        i=0
        while(i<3): 
            times.append(0)
            i=i+1
        operation1=operations(0,self.current_pid,times)
        times=operation1.increment()
        operation2=operations(0,self.current_pid,times)
        times=operation2.increment()
        operation3=operations(self.pipe_conn1,self.current_pid,times)
        times=operation3.send_message()
        operation4=operations(self.pipe_conn1,self.current_pid,times)
        times=operation4.receive_message()
        operation5=operations(self.pipe_conn1,self.current_pid,times)
        times=operation5.send_message()
        operation6=operations(0,self.current_pid,times)
        times=operation6.increment()

    def second_process(self): #function for 2nd process
        times=[] # vector clock time stamp for 3 process [0,0,0]
        i=0
        while(i<3):
            times.append(0)
            i=i+1
        operation1=operations(self.pipe_conn1,self.current_pid,times)
        times=operation1.receive_message()
        operation2=operations(self.pipe_conn1,self.current_pid,times)
        times=operation2.send_message()
        operation3=operations(self.pipe_conn1,self.current_pid,times)
        times=operation3.receive_message()
        operation4=operations(0,self.current_pid,times)
        times=operation4.increment()
        operation5=operations(self.pipe_conn2,self.current_pid,times)
        times=operation5.send_message()
        operation6=operations(self.pipe_conn2,self.current_pid,times)
        times=operation6.receive_message()
        operation7=operations(self.pipe_conn2,self.current_pid,times)
        times=operation7.send_message()
    
    def third_process(self): #function for 3rd process
        times=[] # vector clock time stamp for 3 process [0,0,0]
        i=0
        while(i<3):
            times.append(0)
            i=i+1
        operation1=operations(self.pipe_conn1,self.current_pid,times)
        times=operation1.receive_message()
        operation2=operations(self.pipe_conn1,self.current_pid,times)
        times=operation2.send_message()
        operation3=operations(0,self.current_pid,times)
        times=operation3.increment()
        operation4=operations(self.pipe_conn1,self.current_pid,times)
        times=operation4.receive_message()

def process1(p1_p2): # 1st process
    process_1=process_switch(p1_p2,0,0)
    process_1.first_process()
def process2(p2_p1,p2_p3): #2nd process
    process_2=process_switch(p2_p1,p2_p3,1)
    process_2.second_process()
def process3(p3_p2): # 3rd process
    process_3=process_switch(p3_p2,0,2)
    process_3.third_process()



if __name__=='__main__':

    p1_p2,p2_p1=Pipe() #initalizing pipes for the 3 processes
    p2_p3,p3_p2=Pipe()

    threads=[]

    threads.append(Process(target=process1,args=(p1_p2,)))
    threads.append(Process(target=process2,args=(p2_p1,p2_p3)))
    threads.append(Process(target=process3,args=(p3_p2,)))

    i=0
    j=0
    while (i<3):
        threads[i].start() # calling multiprocessing 
        i=i+1
    while(j<3):
        threads[j].join() # ending multiprocessing
        j=j+1
