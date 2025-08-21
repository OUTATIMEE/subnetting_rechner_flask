from flask import Flask, render_template, request
import re

def net_info(ip_teile_str):
    net_b = ip_teile_str[4]
    ip_teile_int = [int(ok) for ok in ip_teile_str[0:4]]

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
        netz_id.append(ip_teile_int[index] & net_mask[index])
    for index in range(0, 4):
        broadcast.append(~(netz_id[index] ^ net_mask[index]) & 0xFF)

    first_ip = netz_id[:]
    first_ip[3] += 1
    last_ip = broadcast[:]
    last_ip[3] -= 1

    hostbits = 32 - netz_bits
    ver_ips = 2 ** hostbits - 2 if hostbits > 1 else 0
    if not ver_ips > 0: first_ip, last_ip = ("Keine Hosts vorhanden",) * 2

    def ip_anzeigen(liste):
        ip = ""
        for ind, element in enumerate(liste):
            if ind == 3:
                ip += str(element)
            else:
                ip += str(element) + "."
        return ip

    return [ip_anzeigen(ip_teile_int), ip_anzeigen(net_mask), ip_anzeigen(netz_id), ip_anzeigen(broadcast), ip_anzeigen(first_ip), ip_anzeigen(last_ip), ver_ips]


app = Flask(__name__)

@app.route("/")
def Startseite():
    return render_template("startseite.html")

@app.route("/berechne", methods=["POST"])
def berechne():
    ip = [request.form.get("first_ok"), request.form.get("second_ok"), request.form.get("third_ok"), request.form.get("fourth_ok"), request.form.get("net_mask_eingabe")]
    if all(ok and re.fullmatch(r"(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)", ok) for ok in ip[0:4]) and re.fullmatch(r"(3[0-2]|[12]?\d)", ip[4]):
        ip_cidr = f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}/{ip[4]}"
        ip_str, net_mask_str, netz_id_str, broadcast_str, first_ip_str, last_ip_str, ver_ips_str = net_info(ip)
        return render_template("startseite.html", eingabe_richtig=True, ip_cidr=ip_cidr, net_mask=net_mask_str, netz_id=netz_id_str, broadcast=broadcast_str, first_ip=first_ip_str, last_ip=last_ip_str, ver_ips=ver_ips_str)
    else:
        return render_template("startseite.html", eingabe_falsch=True)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

