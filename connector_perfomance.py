import time

from worktory import InventoryManager
inventory = InventoryManager('inventory.yml')

connectors_result = {}
fh = open('results.txt', 'w')

for device in inventory.filter(mode='sync'):
    connector = device.connection_manager.registry_name
    print(f'\nStart collecting {device.name} with {connector}')
    connectors_result[connector] = {
        'times': [],
        'failures': 0
    }
    for it in range(50):
        try:
            start = time.time()
            device.connect()
            output = device.parse("show version")
            print(output)
            device.disconnect()
            end = time.time()
            connectors_result[connector]['times'].append(end - start)
        except Exception as e:
            print(f"{connector} -- {e}")
            connectors_result[connector]['failures'] += 1


print('\n\n')

for connector in connectors_result:
    times = connectors_result[connector]['times']
    total_time  = sum(times)
    mean_time = total_time/len(times)
    min_time = min(times)
    max_time = max(times)
    fh.write(f"{connector};{times};{max_time};{min_time};{mean_time}\n")
    print(f"Connector: {connector}:\n"
          f"Max time: {max_time}\n"
          f"Min time: {min_time}\n"
          f"Mean time: {mean_time}\n\n")

fh.close()  