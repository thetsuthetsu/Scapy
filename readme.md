# FW追加試験テストツールの使用方法
## 開発環境
* スクリプト開発環境：Windows10/PyCharm/Python 3.6.8/Scapy 2.4.0
    1. PyCharmで新規プロジェクト作成
        1. 「New environment using」で VirtualEnvを指定
        2. 「Base Interpreter」でpython3.6のパスを指定
    1. プロジェクトの「Terminal」を開く
        1. pythonコマントを実行し、version等のvirtualenv環境を確認。
    1. pipでScapy(2.4.0)をインストール
         * 2019/02/06時点で2.4.1,2.4.2には重大バグあり。[github](https://github.com/secdev/scapy/issues/1819)
         * インストール状態
         ```
         (Scapy) C:\work\Python\projects\Scapy>pip list
        Package    Version
        ---------- -------
        pip        10.0.1
        scapy      2.4.0
        setuptools 39.1.0
         ```

## 実行環境
1. git clone https://github.com/thetsuthetsu/Scapy.git
2. cd Scapy
3. virtualenvを起動
    1. Script\activate
    2. pythonバージョンが3.6.8であることを確認
        ```
        (Scapy) C:\work\Scapy>python --version
        Python 3.6.8
        ```
4. 任意のスクリプトを実行
    ```
    (Scapy) C:\work\Scapy>python repeatable_icmp.py
    Usage: # python repeatable_icmp.py source_ip target_ip repeat iface [icmp_type]
    ```
        
## 追加テスト要件
1. H/U - サーバ間のTCPプロトコル異常データ時のDCMで処置
    1. TCPセッションタイムアウト後のサーバからのTCP FIN
    2. TCPセッションタイムアウト後のサーバからのTCP RST
    3. TCPセッションタイムアウト後のH/UからのTCP FIN
    4. TCPセッションタイムアウト後のH/UからのTCP RST
    5. TCP接続状態でサーバから異常なシーケンスナンバーのTCP PSH
    6. TCP接続状態でH/Uから異常なシーケンスナンバーのTCP PSH
    7. TCP切断状態でのH/UからのTCP FIN
    8. TCP切断状態でのH/UからのTCP RST
    9. TCP切断状態でのサーバからのTCP SYN
   10. TCP切断状態でのサーバからのTCP PSH
   11. TCP切断状態でのサーバからのTCP FIN
   12. TCP切断状態でのサーバからのTCP RST
   13. TCP切断状態でのサーバからのTCP ACK

2.  H/U - DCM - DNSサーバ間のDNSプロトコル異常時のDCMで処置
    1. H/UからのDNSリクエストに対し○秒後にDNSサーバから応答
       　○：30,60,90,120,150,180,210,240,270,300　の10パターンで実施

3. VSからの提案
    1. 攻撃種別
        1. Smurf攻撃（ICMP echo reply でDoS攻撃）
        2. SYNフラッド攻撃
        3. ICMPフラッド攻撃（ICMP echo request でDoS攻撃）
        4. LAND攻撃（送信元を送信先に偽装したSYNパケットを送る）
    2. DCMの出口側でNAT変換されていないパケットが無いかチェック
    3. IPv6での確認

## プログラム説明
* repeatable_tcp.py
    ```
    指定回数連続してTCPフラグを１つのホストに送信する。
    Usage: # python %s source_ip source_port target_ip target_port repeat iface flags [seq]
      - source_ipにrange指定が可能:(ex. 192.168.10.1-255)
      - flagsに任意のTCPフラグを指定可能：(ex. S/F/P/U/R/A)
      - seqに任意のシーケンス番号を指定可能

   （例）送信元IP192.168.54.1-5の範囲、送信元ポート12345で、192.168.54.101:54321にTCP(PUSH)をシーケンス番号999で送信
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

   適用例
    ・LAND攻撃　(source_ip/target_ipを同じにする）
        >python repeatable_tcp.py 192.168.56.101 12345 192.168.56.101 54321 1 "VirtualBox Host-Only Ethernet Adapter" S

    ・SYNフラッド攻撃 (source_ipをrange指定）
        >python repeatable_tcp.py 192.168.56.1-255 12345 192.168.56.101 54321 100 "VirtualBox Host-Only Ethernet Adapter" S
    ```
    
* dns_proxy.py
    ```
    DNSプロクシとしてデーモン起動し、DNS問い合わせに対する応答を、指定時間後に応答する。

    Usage: # python dns_proxy.py proxy_ip dns_ip wait(sec) iface src_ip [filter_qname]
        src_ip: sniff対象となる送信元IPアドレス
        filter_qname: この文字列を含むクエリーに対してのみ指定時間待ちが発生する。(def."" -> クエリー待ちが発生）

    （例）DNSプロキシとして、192.168.150.139から127.0.0.1:53へのパケットを中継し、8.8.8.8にDNS問い合わせを行い、3秒後に応答する。
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

    （適用範囲）
     ・B1.
    ```
    
* dns_request.py
    ```
    DNSクエリーを発行
    Usage: # python dns_request.py dns_ip dns_qname iface

    （例）DNSプロキシ(dns_proxy.py)に対して、DNSクエリーを発行。
        C:\work\python\NetworkTool>python dns_request.py 127.0.0.1 www.google.com "Intel(R) Ethernet Connection (5) I219-LM"
        dns_ip:127.0.0.1
        dns_qname:www.google.com
        iface:Intel(R) Ethernet Connection (5) I219-LM
        DNS Ans "172.217.26.36"
    ```
    
* repeatable_icmp.py
    ```
    指定回数連続してICMPエコーを１つのホストに送信する。
    Usage: # python %s source_ip target_ip repeat iface [icmp_type]
       - source_ipにrange指定が可能:(ex. 192.168.10.1-255)
       - icmp_typeは既定で"echo-request"。("echo-reply"でSmurf攻撃をシミュレート）

    （例）
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

     適用例
        ・smurf攻撃
            >python repeatable_icmp.py 192.168.56.1-255 192.168.56.101 5 "VirtualBox Host-Only Ethernet Adapter" "echo-reply"

        ・icmpフラッド攻撃
            >python repeatable_icmp.py 192.168.56.1-255 192.168.56.101 5 "VirtualBox Host-Only Ethernet Adapter"
    ```
    
## 課題
* 標準出力・標準エラー出力に対してのブロックが発生する。-> dev/nullへのリダイレクトで解消
* TCP/seqの指定反映が実パケットで確認できていない。(調査中）
* TCPフラグによってはACK応答を全て受信できていないため、応答でのACK再送が発生する。-> 全応答を受信し終わって終了するように改修予定
* インターフェースを指定する必要がある。scapy内ルーティング(conf.route)設定は調査中。
* scapy最新版(2.4.2)には致命的なバグあり。[github](https://github.com/secdev/scapy/issues/1819)
