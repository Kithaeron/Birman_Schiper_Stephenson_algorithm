import queue
def deliverable(a,b) -> bool:


    """
    检查是否接受一个message
    """
    deliver: bool = False
    other: bool = True
    sender = 0
    # print("len(self.addresses)+1=",len(self.addresses)+1)  # 3
    for k in range(len(a)):
        if k != sender:
            if a[k] >= b[k]:  # 我比发来的人更新
                other = True  # 有一个不满足就是False
            else:
                other = False
                break
    print("sender", sender)
    if (a[sender] == b[sender] - 1) and True == other:
        deliver = True
    print("deliverable:", deliver)
    return deliver

if __name__ == '__main__':
    print(deliverable([0,2,0],[1,0,0]))
    msg = queue.Queue()
    msg.put(0)
    msg.put(1)
    msg.put(2)
    print("gt", msg.get())
    print("2",msg.put(0))
    print("546484", msg.get())
