from socket import *  # 从 socket 模块中导入所有的公开对象
# 可以直接使用导入的对象，而不需要通过模块名 socket. 来访问它们，可以简化代码

import os  # 导入 os 模块，提供与操作系统交互的功能函数，执行对文件的管理
# 每次使用都必须用 os. 访问其对象，可以避免代码重名

import sys  # sys模块提供了许多与Python解释器和它的环境有关的函数和变量

# UDP client端
def send(udpSocket):  # 在def自定义函数send中引入一个UDP套接字udpSocket
    print("-----UDP client-----")
    dest_ip = input("请输入服务器的ip：")  # 用input等待用户在键盘输入并返回一个字符串存储在变量dest_ip里
    dest_port = int(input("请输入服务器的port："))  # 用int()将输入的字符串转化为整型
    server_address = (dest_ip, dest_port)  # 用以上两个变量创建一个server端地址的元组存储在变量server_address里
    data_name = input("请输入要发送的文件名：")  # 用变量data_name保存发送的文件名
    # with语句用于创建一个上下文管理器，它可以确保文件在使用后正确关闭，即使在读取文件过程中发生异常也是如此
    with open(data_name, 'rb') as f:  # open函数用于打开一个文件。data_name是一个变量，包含了要打开的文件的名称或路径
        # 'rb'是模式参数，表示以二进制读取模式打开文件。二进制模式允许读取任何类型的文件，包括文本文件和非文本文件（如图片、音频等）
        # as f 将打开的文件对象临时赋值给变量f，以便在with语句块中使用这个变量来引用文件
        data = f.read()  # 文件对象的方法，用于读取文件的全部内容。读取的内容作为字节串（bytes）返回
        # 将f.read()返回的字节串赋值给变量data，可以在代码中使用data变量来访问文件的内容
    print(f"向{server_address}发送数据")  # 使用print函数和格式化字符串（f-string）来输出一条消息
    # 调用udpSocket对象的sendto方法来发送数据
    sent = udpSocket.sendto(data, server_address)  # data是要发送的数据，是之前从文件中读取的字节串
    # server_address是服务器的地址和端口号，并作为一个元组
    # sendto方法返回发送的字节数，并将其存储在变量sent中
    print(f"已发送{sent}字节到{server_address}")  # 告知用户成功发送，并显示发送文件的大小与服务器地址
    udpSocket.close()  # 完成发送并关闭该套接字
# UDP server端
def recv(udpSocket):  # 在def自定义函数recv中引入一个UDP套接字udpSocket
    print("-----UDP server-----")
    port = int(input("请输入要绑定的端口号："))  # 用int()将输入的字符串转化为整型
    # 使用bind方法将udpSocket绑定到本地地址（空字符串表示本主机所有可用的网络IPv4接口）和用户指定的端口号port
    udpSocket.bind(('', port))  # 该方法引入的是一个元组( , )
    print("服务器启动，等待接收数据...")  # 告知用户启动状态
    save_path = 'recv'  # 指定当前工作目录下的一个文件夹（目录路径），用于保存接受到的文件，保存该目录路径到字符串变量里
    # 如果路径不存在，创建它
    if not os.path.exists(save_path):  # 检查save_path指定的目录是否存在
        os.makedirs(save_path)  # 如果不存在，使用os.makedirs方法创建该目录
    file_name = 'new'  # 指定保存数据文件的文件名（必要时可以添加文件后缀打开）1
    # 使用os.path.join方法将目录路径save_path和文件名file_name拼接成一个完整的文件路径，并将其存储在变量path中
    path = os.path.join(save_path, file_name)
    while True:  # 循环语句用于保持server对client数据的接收
        # 使用udpSocket的recvfrom方法接收数据
        # recvfrom方法返回一个元组，其中包含接收到的数据（字节串）和发送者的地址（元组）
        data, address = udpSocket.recvfrom(4096)  # 数据的最大接收大小设置为4096个byte
        if data:  # 检查data变量是否包含数据。如果data不为空，表示接收到了数据
            print(f"从{address}接收到数据，正在保存...")  # 打印接收到数据的来源地址
            # 将接收到的数据写入文件
            with open(path, 'ab') as f:  # 'ab' 模式表示以二进制追加模式打开path指定的文件。如果文件不存在，它将被创建
                f.write(data)  # 使用文件对象f的write方法将接收到的数据data写入文件
            print(f"数据已保存到 {path}")  # 打印数据保存的路径

def main():  # 创建一个main主函数，作为程序的入口点，用于让用户选择作为client或server
    # 创建一个UDP套接字s
    s = socket(AF_INET, SOCK_DGRAM)  # AF_INET表示用IPv4协议，SOCK_DGRAM表示用UDP协议
    while True:
        choice = input("请输入想运行的模式：（数字代表你的选择）\n0：退出程序    1：UDP client     2：UDP sever\n")
        x = int(choice)  # 用int()将字符串转化为整型
        if x == 0:  # 判断语句
            sys.exit()
        if x == 1:
            send(s)  # 调用函数send()作为客户端
        if x == 2:
            recv(s)  # 调用函数recv()作为服务端
        else:
            # 清屏
            print(os.linesep * 100)  # 打印100次换行符，适用于大多数终端
            print("-----再来一次吧-----")

# Python程序的标准入口检查
if __name__ == "__main__":  # 如果这个脚本是作为主程序运行的（而不是被导入为模块）
    main()  # 则调用main()函数





