FW�ǉ������e�X�g�c�[���̎g�p���@

[�a�ʊm�F���ƍ\�z���@]
���\�[�X�݊����FPython 3.6�ȏ�

�E�X�N���v�g�J�����FWindows10/IntelliJ/Python 3.7.2/Scapy 2.4.0
    1. IntelliJ: Tools/Manager Python Packages
       a. Scapy(2.4.0)���C���X�g�[��
         2019/02/06���_��2.4.1,2.4.2�ɂ͏d��o�O����B�ihttps://github.com/secdev/scapy/issues/1819�j

�E���s�� Windows10/Ptthon 3.6.8/Scapy(latest)
    1. Python��3.6.8 ���C���X�g�[��
    2. Python�ƁAPython/Scripts��Path��ʂ��B
    3. winpcap4.1.3���C���X�g�[�� (wireshark���ŃC���X�g�[���ρj
    4. https://github.com/secdev/scapy����ŐV��zip���_�E�����[�h
    5.�W�J�����f�B���N�g���ŁApython setup.py install�����s

[�ǉ��e�X�g�v��]
A. H/U - �T�[�o�Ԃ�TCP�v���g�R���ُ�f�[�^����DCM�ŏ��u
    1. TCP�Z�b�V�����^�C���A�E�g��̃T�[�o�����TCP FIN
    2. TCP�Z�b�V�����^�C���A�E�g��̃T�[�o�����TCP RST
    3. TCP�Z�b�V�����^�C���A�E�g���H/U�����TCP FIN
    4. TCP�Z�b�V�����^�C���A�E�g���H/U�����TCP RST
    5. TCP�ڑ���ԂŃT�[�o����ُ�ȃV�[�P���X�i���o�[��TCP PSH
    6. TCP�ڑ���Ԃ�H/U����ُ�ȃV�[�P���X�i���o�[��TCP PSH
    7. TCP�ؒf��Ԃł�H/U�����TCP FIN
    8. TCP�ؒf��Ԃł�H/U�����TCP RST
    9. TCP�ؒf��Ԃł̃T�[�o�����TCP SYN
   10. TCP�ؒf��Ԃł̃T�[�o�����TCP PSH
   11. TCP�ؒf��Ԃł̃T�[�o�����TCP FIN
   12. TCP�ؒf��Ԃł̃T�[�o�����TCP RST
   13. TCP�ؒf��Ԃł̃T�[�o�����TCP ACK

B.  H/U - DCM - DNS�T�[�o�Ԃ�DNS�v���g�R���ُ펞��DCM�ŏ��u
    1. H/U�����DNS���N�G�X�g�ɑ΂����b���DNS�T�[�o���牞��
       �@���F30,60,90,120,150,180,210,240,270,300�@��10�p�^�[���Ŏ��{

C. VS����̒��
�@�@1.�U�����
�@�@�@�@1.Smurf�U���iICMP echo reply ��DoS�U���j
�@�@�@�@2.SYN�t���b�h�U��
�@�@�@�@3.ICMP�t���b�h�U���iICMP echo request ��DoS�U���j
�@�@�@�@4.LAND�U���i���M���𑗐M��ɋU������SYN�p�P�b�g�𑗂�j
    2.DCM�̏o������NAT�ϊ�����Ă��Ȃ��p�P�b�g���������`�F�b�N
    3. IPv6�ł̊m�F

[�v���O��������]
�Erepeatable_tcp.py
    �w��񐔘A������TCP�t���O���P�̃z�X�g�ɑ��M����B
    Usage: # python %s source_ip source_port target_ip target_port repeat iface flags [seq]
      - source_ip��range�w�肪�\:(ex. 192.168.10.1-255)
      - flags�ɔC�ӂ�TCP�t���O���w��\�F(ex. S/F/P/U/R/A)
      - seq�ɔC�ӂ̃V�[�P���X�ԍ����w��\

   �i��j���M��IP192.168.54.1-5�͈̔́A���M���|�[�g12345�ŁA192.168.54.101:54321��TCP(PUSH)���V�[�P���X�ԍ�999�ő��M
        >python repeatable_tcp.py 192.168.56.1-5 12345 192.168.56.101 54321 3 "VirtualBox Host-Only Ethernet Adapter" P 999
        target_ip:192.168.56.101
        target_port:54321
        repeat:3
        iface:VirtualBox Host-Only Ethernet Adapter
        flags:P
        seq:999
        .....
        Sent 5 packets.
        .....
        Sent 5 packets.
        .....
        Sent 5 packets.

   �K�p��
    �ELAND�U���@(source_ip/target_ip�𓯂��ɂ���j
        >python repeatable_tcp.py 192.168.56.101 12345 192.168.56.101 54321 1 "VirtualBox Host-Only Ethernet Adapter" S

    �ESYN�t���b�h�U�� (source_ip��range�w��j
        >python repeatable_tcp.py 192.168.56.1-255 12345 192.168.56.101 54321 100 "VirtualBox Host-Only Ethernet Adapter" S

�Edns_proxy.py
    DNS�v���N�V�Ƃ��ăf�[�����N�����ADNS�₢���킹�ɑ΂��鉞�����A�w�莞�Ԍ�ɉ�������B

    Usage: # python dns_proxy.py proxy_ip dns_ip wait(sec) iface src_ip [filter_qname]
        src_ip: sniff�ΏۂƂȂ鑗�M��IP�A�h���X
        filter_qname: ���̕�������܂ރN�G���[�ɑ΂��Ă̂ݎw�莞�ԑ҂�����������B(def."" -> �N�G���[�҂��������j

    �i��jDNS�v���L�V�Ƃ��āA192.168.150.139����127.0.0.1:53�ւ̃p�P�b�g�𒆌p���A8.8.8.8��DNS�₢���킹���s���A3�b��ɉ�������B
        > python dns_proxy.py 127.0.0.1 8.8.8.8 3 "Intel(R) Ethernet Connection (5) I219-LM" 192.168.150.139
        proxy_ip:127.0.0.1
        dns_ip:8.8.8.8
        wait(sec):3
        iface:Intel(R) Ethernet Connection (5) I219-LM
        src_ip:192.168.150.139
        filter_qname:
        sniffing...udp port 53 and ip dst 127.0.0.1 and ip src 192.168.150.139
        Forwarding: www.google.com.
        waiting...3(sec)
        Responding to 192.168.150.139:DNS Ans "172.217.25.196"

    �i�K�p�͈́j
     �EB1.

�Edns_request.py
    DNS�N�G���[�𔭍s
    Usage: # python dns_request.py dns_ip dns_qname iface

    �i��jDNS�v���L�V(dns_proxy.py)�ɑ΂��āADNS�N�G���[�𔭍s�B
        C:\work\python\NetworkTool>python dns_request.py 127.0.0.1 www.google.com "Intel(R) Ethernet Connection (5) I219-LM"
        dns_ip:127.0.0.1
        dns_qname:www.google.com
        iface:Intel(R) Ethernet Connection (5) I219-LM
        DNS Ans "172.217.26.36"

�Erepeatable_icmp.py
    �w��񐔘A������ICMP�G�R�[���P�̃z�X�g�ɑ��M����B
    Usage: # python %s source_ip target_ip repeat iface [icmp_type]
       - source_ip��range�w�肪�\:(ex. 192.168.10.1-255)
       - icmp_type�͊����"echo-request"�B("echo-reply"��Smurf�U�����V�~�����[�g�j

    �i��j
            >python repeatable_icmp.py 192.168.56.1-255 192.168.56.101 5 "VirtualBox Host-Only Ethernet Adapter" "echo-reply"
            source_ip:192.168.56.1-255
            target_ip:192.168.56.101
            repeat:5
            iface:VirtualBox Host-Only Ethernet Adapter
            icmp_type:echo-reply
            ...............................................................................................................................................................................................................................................................
            Sent 255 packets.
            ...............................................................................................................................................................................................................................................................
            Sent 255 packets.
            ...............................................................................................................................................................................................................................................................
            Sent 255 packets.
            ...............................................................................................................................................................................................................................................................
            Sent 255 packets.
            ...............................................................................................................................................................................................................................................................
            Sent 255 packets.

     �K�p��
        �Esmurf�U��
            >python repeatable_icmp.py 192.168.56.1-255 192.168.56.101 5 "VirtualBox Host-Only Ethernet Adapter" "echo-reply"

        �Eicmp�t���b�h�U��
            >python repeatable_icmp.py 192.168.56.1-255 192.168.56.101 5 "VirtualBox Host-Only Ethernet Adapter"

[�ۑ�]
�E�W���o�́E�W���G���[�o�͂ɑ΂��Ẵu���b�N����������B
    -> dev/null�ւ̃��_�C���N�g�ŉ���
�ETCP/seq�̎w�蔽�f�����p�P�b�g�Ŋm�F�ł��Ă��Ȃ��B(�������j
�ETCP�t���O�ɂ���Ă�ACK������S�Ď�M�ł��Ă��Ȃ����߁A�����ł�ACK�đ�����������B
    -> �S��������M���I����ďI������悤�ɉ��C�\��
�E�C���^�[�t�F�[�X���w�肷��K�v������Bscapy�����[�e�B���O(conf.route)�ݒ�͒������B
�Escapy�ŐV��(2.4.2)�ɂ͒v���I�ȃo�O����B(https://github.com/secdev/scapy/issues/1819)