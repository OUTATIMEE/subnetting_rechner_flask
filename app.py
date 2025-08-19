from flask import Flask, render_template, request
import re

def net_info(ip_input, net_b):
    ip = re.split(r"[./]", ip_input)
    ip_binary = [int(oc) for oc in ip[0:4]]

    bits = [128, 64, 32, 16, 8, 4, 2, 1]
    netz_bits = int(net_b)
    net_mask = [0,0,0,0]
    runs = 0
    index = 0
    bit = 0

    for numb in range(32):
        if runs < netz_bits:
            net_mask[index] += bits[bit]
            bit += 1
        else:
            net_mask[index] += 0
        runs += 1
        if runs % 8 == 0:
            index += 1
            bit = 0


    netz_id = []
    broadcast = []
    for index in range(0, 4):
        netz_id.append(ip_binary[index] & net_mask[index])
    for index in range(0, 4):
        broadcast.append(~(netz_id[index] ^ net_mask[index]) & 0xFF)

    first_ip = netz_id[:]
    first_ip[3] += 1
    last_ip = broadcast[:]
    last_ip[3] -= 1

    hostbits = 32 - netz_bits
    ver_ips = 2 ** hostbits - 2 if hostbits > 1 else 0

    def ip_anzeigen(liste):
        ip = ""
        for ind, element in enumerate(liste):
            if ind == 3:
                ip += str(element)
            else:
                ip += str(element) + "."
        return ip

    return [ip_anzeigen(ip_binary), ip_anzeigen(net_mask), ip_anzeigen(netz_id), ip_anzeigen(broadcast), ip_anzeigen(first_ip), ip_anzeigen(last_ip), ver_ips]


app = Flask(__name__)

@app.route("/")
def Startseite():
    return render_template("startseite.html")

@app.route("/berechne", methods=["POST"])
def berechne():
    ip = request.form.get("IP_eingabe")
    net_bits = request.form.get("net_mask_eingabe")
    ip_cidr = f"{ip}/{net_bits}"
    ip_binary, net_mask, netz_id, broadcast, first_ip, last_ip, ver_ips = net_info(ip, net_bits)

    return render_template("endseite.html", ip_cidr=ip_cidr, net_mask=net_mask, netz_id=netz_id, broadcast=broadcast, first_ip=first_ip, last_ip=last_ip, ver_ips=ver_ips)

@app.route("/back")
def back():
    return render_template("startseite.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

