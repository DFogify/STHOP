#! /usr/bin/env python3

""" The purpose of this python script is to generate random packets for the verification and 
flagging of the Malicious Traffic """
import json
import random
import socket
import struct
import dpkt
import traceback
import datetime
from scapy.all import *
import binascii
import datetime

""" Requesting the number of packets required to be created later. """

num_packets = input('How many random packets do you require?\n')

""" List of the most commonly used TLS or SSL """

tls_versions = ["TLSv1.0", "TLSv1.1", "TLSv1.2", "SSLv1.0", "SSLv2.0", "SSLv3.0"];

""" List of the most commonly used Ciphers for each version of TLS or SSL """

cipher_tlsv0 = ["NULL-MD5","NULL-SHA","EXP-RC4-MD5","RC4-MD5","RC4-SHA","EXP-RC2-CBC-MD5","IDEA-CBC-SHA","EXP-DES-CBC-SHA","DES-CBC-SHA","DES-CBC3-SHA","EXP-DHE-DSS-DES-CBC-SHA","DHE-DSS-CBC-SHA","DHE-DSS-DES-CBC3-SHA","EXP-DHE-RSA-DES-CBC-SHA","DHE-RSA-DES-CBC-SHA","DHE-RSA-DES-CBC3-SHA","EXP-ADH-RC4-MD5","ADH-RC4-MD5","EXP-ADH-DES-CBC-SHA","ADH-DES-CBC-SHA","ADH-DES-CBC3-SHA","AES128-SHA","AES256-SHA","DH-DSS-AES128-SHA","DH-DSS-AES256-SHA","DH-RSA-AES128-SHA","DH-RSA-AES256-SHA","DHE-DSS-AES128-SHA","DHE-DSS-AES256-SHA","DHE-RSA-AES128-SHA","DHE-RSA-AES256-SHA","ADH-AES128-SHA","ADH-AES256-SHA","CAMELLIA128-SHA","CAMELLIA256-SHA","DH-DSS-CAMELLIA128-SHA","DH-DSS-CAMELLIA256-SHA","DH-RSA-CAMELLIA128-SHA","DH-RSA-CAMELLIA256-SHA","DHE-DSS-CAMELLIA128-SHA","DHE-DSS-CAMELLIA256-SHA","DHE-RSA-CAMELLIA128-SHA","DHE-RSA-CAMELLIA256-SHA","ADH-CAMELLIA128-SHA","ADH-CAMELLIA256-SHA","SEED-SHA","DH-DSS-SEED-SHA","DH-RSA-SEED-SHA","DHE-DSS-SEED-SHA","DHE-RSA-SEED-SHA","ADH-SEED-SHA","GOST94-GOST89-GOST89","GOST2001-GOST89-GOST89","GOST94-NULL-GOST94","GOST2001-NULL-GOST94","EXP1024-DES-CBC-SHA","EXP1024-RC4-SHA","EXP1024-DHE-DSS-DES-CBC-SHA","EXP1024-DHE-DSS-RC4-SHA","DHE-DSS-RC4-SHA","ECDH-RSA-NULL-SHA","ECDH-RSA-RC4-SHA","ECDH-RSA-DES-CBC3-SHA","ECDH-RSA-AES128-SHA","ECDH-RSA-AES256-SHA","ECDH-ECDSA-NULL-SHA","ECDH-ECDSA-RC4-SHA","ECDH-ECDSA-DES-CBC3-SHA","ECDH-ECDSA-AES128-SHA","ECDH-ECDSA-AES256-SHA","ECDHE-RSA-NULL-SHA","ECDHE-RSA-RC4-SHA","ECDHE-RSA-DES-CBC3-SHA","ECDHE-RSA-AES128-SHA","ECDHE-RSA-AES256-SHA","ECDHE-ECDSA-NULL-SHA","ECDHE-ECDSA-RC4-SHA","ECDHE-ECDSA-DES-CBC3-SHA","ECDHE-ECDSA-AES128-SHA","ECDHE-ECDSA-AES256-SHA","AECDH-NULL-SHA","AECDH-RC4-SHA","AECDH-DES-CBC3-SHA","AECDH-AES128-SHA","AECDH-AES256-SHA"];
cipher_tlsv1 = ["NULL-SHA256","AES128-SHA256","AES256-SHA256","AES128-GCM-SHA256","AES256-GCM-SHA384","DH-RSA-AES128-SHA256","DH-RSA-AES256-SHA256","DH-RSA-AES128-GCM-SHA256","DH-RSA-AES256-GCM-SHA384","DH-DSS-AES128-SHA256","DH-DSS-AES256-SHA256","DH-DSS-AES128-GCM-SHA256","DH-DSS-AES256-GCM-SHA384","DHE-RSA-AES128-SHA256","DHE-RSA-AES256-SHA256","DHE-RSA-AES128-GCM-SHA256","DHE-RSA-AES256-GCM-SHA384","DHE-DSS-AES128-SHA256","DHE-DSS-AES256-SHA256","DHE-DSS-AES128-GCM-SHA256","DHE-DSS-AES256-GCM-SHA384","ECDH-RSA-AES128-SHA256","ECDH-RSA-AES256-SHA384","ECDH-RSA-AES128-GCM-SHA256","ECDH-RSA-AES256-GCM-SHA384","ECDH-ECDSA-AES128-SHA256","ECDH-ECDSA-AES256-SHA384","ECDH-ECDSA-AES128-GCM-SHA256","ECDH-ECDSA-AES256-GCM-SHA384","ECDHE-RSA-AES128-SHA256","ECDHE-RSA-AES256-SHA384","ECDHE-RSA-AES128-GCM-SHA256","ECDHE-RSA-AES256-GCM-SHA384","ECDHE-ECDSA-AES128-SHA256","ECDHE-ECDSA-AES256-SHA384","ECDHE-ECDSA-AES128-GCM-SHA256","ECDHE-ECDSA-AES256-GCM-SHA384","ADH-AES128-SHA256","ADH-AES256-SHA256","ADH-AES128-GCM-SHA256","ADH-AES256-GCM-SHA384","ECDHE-ECDSA-CAMELLIA128-SHA256","ECDHE-ECDSA-CAMELLIA256-SHA384","ECDH-ECDSA-CAMELLIA128-SHA256","ECDH-ECDSA-CAMELLIA256-SHA384","ECDHE-RSA-CAMELLIA128-SHA256","ECDHE-RSA-CAMELLIA256-SHA384","ECDH-RSA-CAMELLIA128-SHA256","ECDH-RSA-CAMELLIA256-SHA384"];
cipher_tlsv2 = ["NULL-SHA256","AES128-SHA256","AES256-SHA256","AES128-GCM-SHA256","AES256-GCM-SHA384","DH-RSA-AES128-SHA256","DH-RSA-AES256-SHA256","DH-RSA-AES128-GCM-SHA256","DH-RSA-AES256-GCM-SHA384","DH-DSS-AES128-SHA256","DH-DSS-AES256-SHA256","DH-DSS-AES128-GCM-SHA256","DH-DSS-AES256-GCM-SHA384","DHE-RSA-AES128-SHA256","DHE-RSA-AES256-SHA256","DHE-RSA-AES128-GCM-SHA256","DHE-RSA-AES256-GCM-SHA384","DHE-DSS-AES128-SHA256","DHE-DSS-AES256-SHA256","DHE-DSS-AES128-GCM-SHA256","DHE-DSS-AES256-GCM-SHA384","ECDH-RSA-AES128-SHA256","ECDH-RSA-AES256-SHA384","ECDH-RSA-AES128-GCM-SHA256","ECDH-RSA-AES256-GCM-SHA384","ECDH-ECDSA-AES128-SHA256","ECDH-ECDSA-AES256-SHA384","ECDH-ECDSA-AES128-GCM-SHA256","ECDH-ECDSA-AES256-GCM-SHA384","ECDHE-RSA-AES128-SHA256","ECDHE-RSA-AES256-SHA384","ECDHE-RSA-AES128-GCM-SHA256","ECDHE-RSA-AES256-GCM-SHA384","ECDHE-ECDSA-AES128-SHA256","ECDHE-ECDSA-AES256-SHA384","ECDHE-ECDSA-AES128-GCM-SHA256","ECDHE-ECDSA-AES256-GCM-SHA384","ADH-AES128-SHA256","ADH-AES256-SHA256","ADH-AES128-GCM-SHA256","ADH-AES256-GCM-SHA384","ECDHE-ECDSA-CAMELLIA128-SHA256","ECDHE-ECDSA-CAMELLIA256-SHA384","ECDH-ECDSA-CAMELLIA128-SHA256","ECDH-ECDSA-CAMELLIA256-SHA384","ECDHE-RSA-CAMELLIA128-SHA256","ECDHE-RSA-CAMELLIA256-SHA384","ECDH-RSA-CAMELLIA128-SHA256","ECDH-RSA-CAMELLIA256-SHA384"];
cipher_sslv1 = ["NONE FOUND"];
cipher_sslv2 = ["RC4-MD5","EXP-RC4-MD5","RC2-MD5","EXP-RC2-MD5","IDEA-CBC-MD5","DES-CBC-MD5","DES-CBC3-MD5"];
cipher_sslv3 = ["NULL-MD5","NULL-SHA","EXP-RC4-MD5","RC4-MD5","RC4-SHA","EXP-RC2-CBC-MD5","IDEA-CBC-SHA","EXP-DES-CBC-SHA","DES-CBC-SHA","DES-CBC3-SHA","EXP-EDH-DSS-DES-CBC-SHA","EDH-DSS-CBC-SHA","EDH-DSS-DES-CBC3-SHA","EXP-EDH-RSA-DES-CBC-SHA","EDH-RSA-DES-CBC-SHA","EDH-RSA-DES-CBC3-SHA","EXP-ADH-RC4-MD5","ADH-RC4-MD5","EXP-ADH-DES-CBC-SHA","ADH-DES-CBC-SHA","ADH-DES-CBC3-SHA","DHE-DSS-RC4-SHA"];

""" Section Name: Random Number of Packets (PCAP) """""""""""""""""""""""""""""""""""""""

def pcap_packets():
    data = 'I am sending test data, please check and reply';
    for i in range(0, int(num_packets)):
        ts = time.time();
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mac_src = "%02x:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)); 
        mac_dst = "%02x:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255));
        domain = str("fake"+str(i)+".com");
        ip_src = socket.inet_ntoa(struct.pack('>I',random.randint(1, 0xffffffff)));
        ip_dst = socket.inet_ntoa(struct.pack('>I',random.randint(1, 0xffffffff)));
        version = random.choice(tls_versions);
        if version == "TLSv1.0":
            cipher = random.choice(cipher_tlsv0);
            packet = Ether(src = mac_src, dst = mac_dst)/IP(src = ip_src, dst = ip_dst)/Raw(load = data);
            hexdump(packet)
            a = ("newfile"+str(i)+".pcap")
            wrpcap(a,packet)
        elif version == "TLSv1.1":
            cipher = random.choice(cipher_tlsv1);
            packet = Ether(src = mac_src, dst = mac_dst)/IP(src = ip_src, dst = ip_dst)/Raw(load = data);
            hexdump(packet)
            a = ("newfile"+str(i)+".pcap")
            wrpcap(a,packet)
        elif version == "TLSv1.2":
            cipher = random.choice(cipher_tlsv2);
            packet = Ether(src = mac_src, dst = mac_dst)/IP(src = ip_src, dst = ip_dst)/Raw(load = data);
            hexdump(packet)
            a = ("newfile"+str(i)+".pcap")
            wrpcap(a,packet)
        elif version == "SSLv1.0":
            cipher = random.choice(cipher_sslv1);
            packet = Ether(src = mac_src, dst = mac_dst)/IP(src = ip_src, dst = ip_dst)/Raw(load = data);
            hexdump(packet)
            a = ("newfile"+str(i)+".pcap")
            wrpcap(a,packet)
        elif version == "SSLv2.0":
            cipher = random.choice(cipher_sslv2);
            packet = Ether(src = mac_src, dst = mac_dst)/IP(src = ip_src, dst = ip_dst)/Raw(load = data);
            hexdump(packet)
            a = ("newfile"+str(i)+".pcap")
            wrpcap(a,packet)
        elif version == "SSLv3.0":
            cipher = random.choice(cipher_sslv3);
            packet = Ether(src = mac_src, dst = mac_dst)/IP(src = ip_src, dst = ip_dst)/Raw(load = data);
            hexdump(packet)
            a = ("newfile"+str(i)+".pcap")
            wrpcap(a,packet)



""" Main Function """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main():
    pcap_packets()

""" Running The Script """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
main()
""" Termination Point """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
