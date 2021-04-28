import os
import time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib
code = None


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def print_info(msg, indent=0):
    global code
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                    if code is None:
                        if 'FB' in value:
                            code = value[3:8]
                        else:
                            code = value[:5]
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))

    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))


def main(email: str, password: str, pop3_server: str, port=995):
    server = poplib.POP3_SSL(pop3_server, port=port)  # 连接到POP3服务器
    server.set_debuglevel(1)  # 可以打开或关闭调试信息:
    print(server.getwelcome().decode('utf-8'))  # 可选:打印POP3服务器的欢迎文字:
    server.user(email)
    server.pass_(password)  # 身份认证
    # print('Messages: %s. Size: %s' % server.stat())   # stat()返回邮件数量和占用空间
    resp, mails, octets = server.list()  # list()返回所有邮件的编号
    # print(mails)  # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    resp, lines, octets = server.retr(index)  # lines存储了邮件的原始文本的每一行,可以获得整个邮件的原始文本
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)  # 稍后解析出邮件
    print_info(msg)
    print("确认码为：", code)  # 打印从邮件中获取的确认码
    # server.dele(index)  # 可以根据邮件索引号直接从服务器删除邮件
    server.quit()  # 关闭连接:
    return code


if __name__ == '__main__':  # 测试hotmail邮箱是否锁定
    '''
    读取文件内容格式如下：
        邮箱----密码
    xxxxx@hotmail.com----xxxx
    xxxxx@hotmail.com----xxxx
    '''
    with open(os.path.join('202104201419189025765250.txt'), 'r') as fr:
        while True:
            userinfo = fr.readline()
            if userinfo != '':
                reg_email = userinfo.split('----')[0]
                reg_password = userinfo.split('----')[1].strip('\n')
                try:
                    main(email=reg_email, password=reg_password, pop3_server="pop3.live.com")
                    with open(os.path.join('email.txt'), 'a') as fw:
                        fw.write(reg_email+ '----' + reg_password + '\n')   # 将未锁定邮箱写入新的文件中
                except (poplib.error_proto, UnicodeDecodeError):
                    print(reg_email + '获取确认码失败,帐户已锁定')
            else:
                break
