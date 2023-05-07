from opcua import Client
from time import sleep

def flag(delta):
    # List of elements in order (not computed, extracted from vizualisation output from get_valves)
    e = [1, 3, 7, 11, 2, 13, 6, 15, 8, 12, 4, 16, 9, 10, 5, 14]
    flag = ''
    for i in range(0, len(e), 2):
        flag += format(e[i], "02x") + format(e[i+1], "02x")
        flag += format(delta[e[i]-1], "02x") + format(delta[e[i+1]-1], "02x")
    return "FCSC{" + flag + "}"

def get_valves(client, objs):
    # Get list of valves nodes
    nodes = list(); names = list()
    list_child = objs.get_children()
    for child in list_child:
        name = child.get_display_name().Text
        if name[0] == 'V' or name == 'VMIX':
            nodes.append(child)
            names.append(name)
    #print(nodes)
    print(names)

    # Print values and loop over to visualize changes
    for _ in range(50):
        # Get valves status
        values = client.get_values(nodes)
        # Dummy print of valves values (x for True, one column per valve)
        s = ''
        for v in values:
            if v == True:
                s += 'x'
            else:
                s += ' '
        print(s)
        # 2s looks a correct delay value (try-error)
        sleep(2)

def get_valves_and_elements(client, objs):
    # Get list of valves nodes + element nodes
    nodes = list(); names = list()
    list_child = objs.get_children()
    for child in list_child:
        name = child.get_display_name().Text
        if name[0] == 'V' or name[0] == 'E' or name == 'VMIX':
            nodes.append(child)
            names.append(name)

    # Print values and loop over to visualize changes
    previous_elements = list();
    delta = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    begin_cycle = False; end_cycle = False
    for _ in range(100):
        # Get valves status
        values = client.get_values(nodes)
        elements = values[:16]
        valves = values[16:]
        # Dummy print of valvles values (x for True, one column per valve)
        s = ''
        for v in valves:
            if v == True:
                s += 'x'
            else:
                s += ' '
        # Print elements changes
        if previous_elements:
            for i in range(16):
                if elements[i] != previous_elements[i]:
                    delta[i] = previous_elements[i] - elements[i]
                    s = s + ' ' + names[i] + '=' + str(-delta[i])
                    # Beginning of cycle at V1 and V3
                    if valves[0] == True and valves[2] == True:
                        begin_cycle = True; end_cycle = False
                    # End of cycle after V5 & V14
                    if valves[4] == True and valves[13] == True:
                        end_cycle = True
        print(s)
        # End after one complete cycle
        if begin_cycle == True and end_cycle == True:
            # build flag
            return print(flag(delta))
        else:
            # Prepare next cycle
            previous_elements = elements
            sleep(1)


def main():
    srv_url="opc.tcp://evil-plant.france-cybersecurity-challenge.fr:4841"
    client = Client(srv_url)
    client.connect()

    root = client.get_root_node()
    objs = client.get_objects_node()

    # Get valves status, print values and loop over to visualize changes
    #get_valves(client, objs)
    get_valves_and_elements(client, objs)

    client.disconnect()


if __name__ == "__main__":
    main()
